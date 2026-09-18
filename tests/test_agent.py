import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from codebase.agent import classify_context, redact, validate
from eval.run_eval import check_case


def response(value, status='completed'):
    return {'status': status, 'output': [{'type': 'message', 'content': [
        {'type': 'output_text', 'text': json.dumps(value)}]}]}, 'req_test'


def prediction(status='MISSING_CONTEXT', missing=None, evidence=None, uncertain=False):
    return {'status':status, 'missing':['reproduction'] if missing is None else missing,
            'evidence':evidence or [], 'uncertain':uncertain}


class AgentTests(unittest.TestCase):
    def setUp(self):
        config_patch = patch('codebase.agent.load_env', return_value={})
        config_patch.start()
        self.addCleanup(config_patch.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def run_agent(self, value=None, message='Python 3.11: ModuleNotFoundError', attachments=None, transport=None):
        return classify_context(message, attachments, transport=transport or (lambda p,k:response(value)),
                                trace_dir=self.tmp.name)

    def test_real_request_contract_and_template(self):
        def transport(payload, key):
            self.assertEqual(payload['text']['format']['type'], 'json_schema')
            self.assertTrue(payload['text']['format']['strict'])
            self.assertFalse(payload['store'])
            return response(prediction(evidence=[{'field':'error_log','quote':'ModuleNotFoundError'}]))
        result = self.run_agent(transport=transport)
        self.assertEqual(result['action'], 'ASK_FOR_CONTEXT')
        self.assertIn('Lệnh hoặc', result['reply'])
        self.assertLessEqual(len(result['reply'].split()),100)
        self.assertFalse(result['api_called'])  # Test double is never real AI evidence.

    def test_silent_enough(self):
        r = self.run_agent(prediction('ENOUGH_CONTEXT', [], [{'field':'error_log','quote':'ModuleNotFoundError'}]))
        self.assertEqual(r['action'], 'PASS_TO_TA')
        self.assertIsNone(r['reply'])

    def test_silent_out_of_scope(self):
        r = self.run_agent(prediction('OUT_OF_SCOPE', []))
        self.assertEqual(r['action'],'NO_AUTO_REPLY')

    def test_silent_uncertain(self):
        r = self.run_agent(prediction('UNCERTAIN', []))
        self.assertIsNone(r['reply'])

    def test_model_uncertainty_overrides_ask(self):
        r = self.run_agent(prediction(uncertain=True))
        self.assertEqual(r['status'],'UNCERTAIN')
        self.assertEqual(r['missing'],[])

    def test_unavailable_attachment_overrides(self):
        r = self.run_agent(prediction(), attachments=[{'available':False}])
        self.assertEqual(r['status'],'UNCERTAIN')
        self.assertIsNone(r['reply'])

    def test_fabricated_evidence_rejected(self):
        r = self.run_agent(prediction(evidence=[{'field':'error_log','quote':'not in input'}]))
        self.assertEqual(r['error'],'ungrounded_evidence')
        self.assertIsNone(r['reply'])

    def test_present_missing_conflict_rejected(self):
        r = self.run_agent(prediction(evidence=[{'field':'reproduction','quote':'Python 3.11'}]))
        self.assertEqual(r['status'],'UNCERTAIN')
        self.assertIsNotNone(r['error'])

    def test_invalid_missing(self):
        for fields in (['fake'],['error_log']*2,['error_log','environment','reproduction','relevant_code']):
            with self.subTest(fields=fields):
                self.assertIsNotNone(self.run_agent(prediction(missing=fields))['error'])

    def test_empty_missing_invalid(self):
        self.assertEqual(self.run_agent(prediction(missing=[]))['error'],'inconsistent_missing')

    def test_enough_needs_evidence(self):
        self.assertEqual(self.run_agent(prediction('ENOUGH_CONTEXT',[]))['error'],'enough_without_evidence')

    def test_arbitrary_model_reply_cannot_reach_student(self):
        value = prediction()
        value['reply'] = 'Run a dangerous command'
        r = self.run_agent(value)
        self.assertEqual(r['error'],'schema_keys')
        self.assertIsNone(r['reply'])

    def test_timeout(self):
        def timeout(p,k):
            raise TimeoutError()
        r = self.run_agent(transport=timeout)
        self.assertEqual(r['error'],'TimeoutError')
        self.assertEqual(r['action'],'NO_AUTO_REPLY')

    def test_refusal(self):
        r = self.run_agent(transport=lambda p,k:({'status':'completed','output':[]}, 'req_refusal'))
        self.assertEqual(r['error'],'missing_structured_output_or_refusal')

    def test_incomplete(self):
        r = self.run_agent(transport=lambda p,k:response(prediction(), 'incomplete'))
        self.assertEqual(r['error'],'provider_not_completed')

    def test_malformed_json(self):
        raw,_ = response(prediction())
        raw['output'][0]['content'][0]['text'] = 'not-json'
        r = self.run_agent(transport=lambda p,k:(raw,'req_bad'))
        self.assertIsNotNone(r['error'])

    def test_redaction_before_network_and_trace(self):
        secret='FAKE_SENSITIVE_TEST_ONLY'
        def transport(payload,key):
            self.assertNotIn(secret,json.dumps(payload))
            return response(prediction())
        r = self.run_agent(message='api_key='+secret+' error', transport=transport)
        trace = (Path(self.tmp.name)/(r['trace_id']+'.json')).read_text(encoding='utf-8')
        self.assertNotIn(secret,trace)
        self.assertIn('raw_response',trace)
        self.assertIn('req_test',trace)

    def test_missing_key_fails_closed(self):
        with patch.dict(os.environ,{},clear=True), patch('codebase.agent.load_env', return_value={}):
            r=classify_context('code error',trace_dir=self.tmp.name)
        self.assertEqual(r['error'],'missing_api_key')
        self.assertFalse(r['api_called'])

    def test_bad_input(self):
        for message in ('',None,'x'*16001):
            with self.assertRaises(ValueError):
                self.run_agent(message=message)

    def test_trace_failure_prevents_reply(self):
        file=Path(self.tmp.name)/'not-directory'
        file.write_text('test')
        r=classify_context('error',transport=lambda p,k:response(prediction()),trace_dir=file)
        self.assertEqual(r['error'],'trace_write_failed')
        self.assertIsNone(r['reply'])

    def test_evaluation_does_not_reward_api_failure(self):
        c={'expected':{'status':'UNCERTAIN','missing':[],'action':'NO_AUTO_REPLY'}}
        r={'status':'UNCERTAIN','missing':[],'action':'NO_AUTO_REPLY','reply':None,
           'error':'missing_api_key','api_called':False}
        passed, failures=check_case(c,r)
        self.assertIsNone(passed)
        self.assertTrue(failures[0].startswith('infrastructure:'))

    def test_evaluation_missing_order_irrelevant(self):
        c={'expected':{'status':'MISSING_CONTEXT','missing':['error_log','reproduction'],'action':'ASK_FOR_CONTEXT'}}
        r={'status':'MISSING_CONTEXT','missing':['reproduction','error_log'],'action':'ASK_FOR_CONTEXT',
           'reply':'please provide context','error':None,'api_called':True}
        self.assertTrue(check_case(c,r)[0])


if __name__ == '__main__':
    unittest.main()
