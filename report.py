"""Generate an offline HTML defect report from a JSON file."""
import argparse
import html
import json
from pathlib import Path

VERSION = '0.1.0'


def render(data):
    if not isinstance(data, dict) or not isinstance(data.get('title'), str):
        raise ValueError('title must be a string')
    defects = data.get('defects')
    if not isinstance(defects, list):
        raise ValueError('defects must be a list')
    cards = []
    for item in defects:
        if not isinstance(item, dict):
            raise ValueError('Each defect must be an object')
        for field in ('id', 'title', 'severity', 'expected', 'actual'):
            if not isinstance(item.get(field), str):
                raise ValueError('Missing or invalid defect field')
        steps = item.get('steps')
        if not isinstance(steps, list) or not all(isinstance(s, str) for s in steps):
            raise ValueError('steps must be a list of strings')
        e = lambda name: html.escape(item[name], quote=True)
        step_html = ''.join('<li>' + html.escape(s) + '</li>' for s in steps)
        cards.append('<article><h2>' + e('id') + ': ' + e('title') + '</h2>'
                     '<p>Severity: ' + e('severity') + '</p><ol>' + step_html + '</ol>'
                     '<h3>Expected</h3><p>' + e('expected') + '</p>'
                     '<h3>Actual</h3><p>' + e('actual') + '</p></article>')
    title = html.escape(data['title'], quote=True)
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
            '<title>' + title + '</title><style>'
            'body{font:16px system-ui;background:#f1f4f8;color:#182338;max-width:900px;margin:40px auto;padding:20px}'
            'article{background:white;border:1px solid #ccd6e3;border-radius:12px;padding:24px;margin:20px 0}'
            'p,li{white-space:pre-wrap;overflow-wrap:anywhere}h1{font-size:32px}h3{font-size:16px}'
            '@media print{body{margin:0;background:white}article{break-inside:avoid}}'
            '</style><h1>' + title + '</h1><p>Defects: ' + str(len(defects)) + '</p>'
            + ''.join(cards) + '</html>')


def main(argv=None):
    p = argparse.ArgumentParser(description='Vilod Test Report - JSON to local HTML')
    p.add_argument('--version', action='version', version=VERSION)
    p.add_argument('input'); p.add_argument('output')
    a = p.parse_args(argv)
    try:
        document = render(json.loads(Path(a.input).read_text(encoding='utf-8-sig')))
        with Path(a.output).open('x', encoding='utf-8') as f:
            f.write(document)
    except (ValueError, OSError):
        p.exit(2, 'Cannot generate report. Check schema, input and output availability.\n')
    print('Report created. Review content before sharing.')


if __name__ == '__main__': main()
