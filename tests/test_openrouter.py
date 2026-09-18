import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from codebase.agent import classify_context, get_config, load_env, OPENROUTER_MODEL, call_openrouter


def tool_response(value):
    return {'id':'gen-test-only','choices':[{'finish_reason':'tool_calls', 'message': {
        'tool_calls':[{'type':'function','function':{'name':'classify_context',
                                                  'arguments':json.dumps(value)}}]}}]}, None


class OpenRouterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        config_patch = patch('codebase.agent.load_env', return_value={
            'LLM_PROVIDER':'openrouter','OPENROUTER_API_KEY':'test-only'})
        config_patch.start()
        self.addCleanup(config_patch.stop)

    def classify(self, raw):
        return classify_context('Code em lỗi rồi', transport=lambda p,k:raw, trace_dir=self.tmp.name)

    def test_tool_contract_and_trace(self):
        value={'status':'MISSING_CONTEXT','missing':['error_log','reproduction'], 'evidence':[], 'uncertain':False}
        def transport(payload,key):
            self.assertEqual(payload['model'],OPENROUTER_MODEL)
            self.assertEqual(payload['tool_choice']['function']['name'],'classify_context')
            self.assertTrue(payload['provider']['require_parameters'])
            self.assertNotIn('response_format',payload)
            self.assertNotIn('input',payload)
            return tool_response(value)
        result=classify_context('Code em lỗi rồi',transport=transport,trace_dir=self.tmp.name)
        self.assertIsNone(result['error'])
        self.assertEqual(result['action'],'ASK_FOR_CONTEXT')
        trace=json.loads((Path(self.tmp.name)/(result['trace_id']+'.json')).read_text(encoding='utf-8'))
        self.assertEqual(trace['raw_response']['id'],'gen-test-only')
        self.assertEqual(trace['provider_response_id'],'gen-test-only')

    def test_text_only_answer_rejected(self):
        r=self.classify(({'choices':[{'finish_reason':'stop','message':{'content':'Try pip install'}}]},None))
        self.assertEqual(r['error'],'missing_structured_output_or_refusal')
        self.assertIsNone(r['reply'])

    def test_wrong_tool_rejected(self):
        raw,identifier=tool_response({})
        raw['choices'][0]['message']['tool_calls'][0]['function']['name']='execute_code'
        self.assertEqual(self.classify((raw,identifier))['error'],'unexpected_tool_call')

    def test_truncated_output_rejected(self):
        raw,identifier=tool_response({})
        raw['choices'][0]['finish_reason']='length'
        self.assertEqual(self.classify((raw,identifier))['error'],'provider_not_completed')

    def test_error_response_rejected(self):
        self.assertEqual(self.classify(({'error':{'message':'rate limit'}},None))['error'],'provider_error_response')

    def test_openai_key_not_used_for_openrouter(self):
        with patch('codebase.agent.load_env',return_value={'LLM_PROVIDER':'openrouter','OPENAI_API_KEY':'other-key'}):
            self.assertEqual(get_config()['api_key'],'')

    def test_http_destination(self):
        with patch('codebase.agent.call_http',return_value=({},None)) as http:
            call_openrouter({'model':OPENROUTER_MODEL},'test-only')
            self.assertEqual(http.call_args.args[0],'https://openrouter.ai/api/v1/chat/completions')

    def test_env_edit_reload(self):
        # Imported function still refers to the original implementation, despite module mock.
        root=Path(self.tmp.name)
        with patch('codebase.agent.ROOT',root), patch.dict('os.environ',{},clear=True):
            (root/'.env').write_text('OPENROUTER_MODEL=first',encoding='utf-8')
            self.assertEqual(load_env()['OPENROUTER_MODEL'],'first')
            (root/'.env').write_text('OPENROUTER_MODEL=second',encoding='utf-8')
            self.assertEqual(load_env()['OPENROUTER_MODEL'],'second')
