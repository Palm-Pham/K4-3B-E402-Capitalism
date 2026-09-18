import itertools
import json
import tempfile
import unittest
from unittest.mock import patch
from codebase.agent import classify_context, render_reply, FIELDS, ProviderError


class ContextRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        config = patch('codebase.agent.load_env', return_value={'LLM_PROVIDER':'openrouter'})
        config.start()
        self.addCleanup(config.stop)

    def test_missing_context_renders_fill_in_template(self):
        reply = render_reply({'action':'ASK_FOR_CONTEXT', 'missing':['error_log','reproduction','environment']})
        self.assertTrue(reply.startswith('Thiếu ngữ cảnh.'))
        self.assertIn('theo mẫu dưới đây', reply)
        self.assertEqual(reply.count('[Điền thông tin tại đây]'), 3)

    def test_all_three_field_templates_within_word_limit(self):
        for fields in itertools.combinations(FIELDS,3):
            reply=render_reply({'action':'ASK_FOR_CONTEXT','missing':list(fields)})
            self.assertLessEqual(len(reply.split()),100,fields)

    def test_exact_reported_conflict_still_rejected(self):
        # Recorded model response: the same field is present AND missing.
        value={'status':'MISSING_CONTEXT', 'missing':['problem_description','error_log','reproduction'],
               'evidence':[{'field':'problem_description','quote':'biến môi trường của tôi bị lỗi'}],
               'uncertain':False}
        def transport(payload,key):
            return {'choices':[{'finish_reason':'tool_calls','message':{'tool_calls':[
                {'type':'function','function':{'name':'classify_context','arguments':json.dumps(value)}}]}}]},None
        r=classify_context('biến môi trường của tôi bị lỗi',transport=transport,trace_dir=self.tmp.name)
        self.assertEqual(r['error'],'ungrounded_evidence')
        self.assertIsNone(r['reply'])
        self.assertIn('vừa đủ vừa thiếu',r['error_message'])

    def test_tool_incompatibility_explained_not_classified_as_missing(self):
        def transport(payload,key):
            raise ProviderError('provider_http_404',json.dumps({'error':{'message':'No endpoints found that support tool use.'}}))
        r=classify_context('biến môi trường bị lỗi',transport=transport,trace_dir=self.tmp.name)
        self.assertEqual(r['status'],'UNCERTAIN')
        self.assertIsNone(r['reply'])
        self.assertIn('OPENROUTER_MODEL',r['error_message'])
        self.assertIn('tool calling',r['error_message'])
