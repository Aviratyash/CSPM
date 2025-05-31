import os
import json

def generate_html_report(report_path="reports/inventory.json", output_path="reports/report.html"):
    with open(report_path, "r") as f:
        data = json.load(f)

    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CSPM Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; background-color: #f8f9fa; }
        h1 { color: #333; }
        h2 { color: #007bff; margin-top: 2em; }
        table { width: 100%; border-collapse: collapse; margin-top: 1em; }
        th, td { border: 1px solid #ccc; padding: 0.6em; text-align: left; vertical-align: top; }
        th { background-color: #e9ecef; }
        tr:nth-child(even) { background-color: #f1f3f5; }
        code { background-color: #eee; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Cloud Security Posture Management (CSPM) Report</h1>
"""

    for section, items in data["Misconfigurations"].items():
        html += f"<h2>{section.replace('_', ' ')}</h2>"
        if not items:
            html += "<p><strong>No issues found 🎉</strong></p>"
            continue
        html += "<table><tr>"
        if isinstance(items[0], dict):
            for key in items[0]:
                html += f"<th>{key}</th>"
            html += "</tr>"
            for item in items:
                html += "<tr>"
                for value in item.values():
                    html += f"<td><pre>{json.dumps(value, indent=2)}</pre></td>"
                html += "</tr>"
        else:
            for item in items:
                html += f"<tr><td>{item}</td></tr>"
        html += "</table>"

    html += """
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


    print(f"✅ HTML report saved to: {output_path}")
