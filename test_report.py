import unittest
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
