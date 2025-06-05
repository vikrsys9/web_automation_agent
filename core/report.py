import logging
import os

def generate_html_report(results, report_path):
    html = [
        '<html><head><title>Automation Test Report</title><style>',
        'body { font-family: Arial; }',
        'table { border-collapse: collapse; width: 100%; }',
        'th, td { border: 1px solid #ddd; padding: 8px; }',
        'th { background-color: #f2f2f2; }',
        '.pass { color: green; font-weight: bold; }',
        '.fail { color: red; font-weight: bold; }',
        '</style></head><body>'
        '<h1>Automation Test Report</h1>'
        '<table>'
        '<tr><th>Test Goal</th><th>Status</th><th>Screenshots</th></tr>'
    ]
    for result in results:
        goal = result['goal']
        status = '<span class="pass">PASS</span>' if result['success'] else '<span class="fail">FAIL</span>'
        screenshots = ''
        for shot in result.get('screenshots', []):
            screenshots += f'<a href="{shot}" target="_blank">Screenshot</a><br>'
        html.append(f'<tr><td>{goal}</td><td>{status}</td><td>{screenshots}</td></tr>')
    html.append('</table></body></html>')
    # Ensure the parent directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))
    logging.info(f"HTML report generated at {report_path}") 