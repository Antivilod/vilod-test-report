import unittest
import json
import tempfile
from pathlib import Path
import report


class ReportTests(unittest.TestCase):
    def test_script_and_html_escaped(self):
        s = '<script>alert(1)</script>'
        data = {'title': s, 'defects': [{'id': '1', 'title': s, 'severity': 'Low',
                'steps': [s], 'expected': s, 'actual': s}]}
        out = report.render(data)
        self.assertNotIn('<script>', out)
        self.assertIn('&lt;script&gt;', out)

    def test_invalid_schema(self):
        for data in ({}, [], {'title':'x','defects':[{}]}):
            with self.assertRaises(ValueError): report.render(data)

    def test_empty_report(self):
        self.assertIn('Defects: 0', report.render({'title':'Empty','defects':[]}))

    def test_environment_escaped(self):
        out = report.render({'title':'Demo','defects':[], 'environment':{'<b>':'<img src=x>'}})
        self.assertIn('&lt;b&gt;', out)
        self.assertIn('&lt;img src=x&gt;', out)
        self.assertNotIn('<img', out)

    def test_status_counts_and_default(self):
        defect = {'id':'1','title':'Demo','severity':'Low','steps':[], 'expected':'x','actual':'y'}
        out = report.render({'title':'Demo','defects':[defect, dict(defect, status='fixed')]})
        self.assertIn('open: 1', out)
        self.assertIn('fixed: 1', out)

    def test_invalid_optional_fields(self):
        defect = {'id':'1','title':'Demo','severity':'Low','steps':[], 'expected':'x','actual':'y'}
        for status in ('<script>', [], None):
            with self.assertRaises(ValueError):
                report.render({'title':'Demo','defects':[dict(defect, status=status)]})
        with self.assertRaises(ValueError):
            report.render({'title':'Demo','defects':[], 'environment':{'x':42}})

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory)/'in.json', Path(directory)/'out.html'
            source.write_text(json.dumps({'title':'Demo','defects':[]}), encoding='utf-8')
            target.write_text('preserve', encoding='utf-8')
            with self.assertRaises(SystemExit) as error:
                report.main([str(source), str(target)])
            self.assertEqual(error.exception.code, 2)
            self.assertEqual(target.read_text(), 'preserve')

    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"title":"a","title":"b"}', object_pairs_hook=report.unique_object)
