"""
Web Vulnerability Scanner - Report Generator
Generates detailed security reports in HTML and PDF formats
"""

from typing import List, Dict, Any
from datetime import datetime
import os
from jinja2 import Template


class ReportGenerator:
    """Generates security scan reports"""

    def __init__(self):
        self.findings = []
        self.scan_info = {}

    def generate_report(self, findings: List[Dict[str, Any]],
                       scan_info: Dict[str, Any],
                       output_file: str = 'report.html',
                       format: str = 'html'):
        """
        Generate a security report

        Args:
            findings: List of vulnerability findings
            scan_info: Scan information (target, duration, etc.)
            output_file: Output file path
            format: Report format (html or pdf)
        """
        self.findings = findings
        self.scan_info = scan_info

        # Sort findings by severity
        sorted_findings = self._sort_by_severity(findings)

        # Generate statistics
        stats = self._generate_statistics(findings)

        if format == 'html':
            self._generate_html_report(sorted_findings, stats, output_file)
        elif format == 'pdf':
            self._generate_pdf_report(sorted_findings, stats, output_file)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _sort_by_severity(self, findings: List[Dict[str, Any]]) -> Dict[str, List]:
        """Sort findings by severity"""
        severity_order = ['Critical', 'High', 'Medium', 'Low', 'Info']

        sorted_findings = {
            'Critical': [],
            'High': [],
            'Medium': [],
            'Low': [],
            'Info': []
        }

        for finding in findings:
            severity = finding.get('severity', 'Info')
            if severity in sorted_findings:
                sorted_findings[severity].append(finding)

        return sorted_findings

    def _generate_statistics(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics from findings"""
        stats = {
            'total': len(findings),
            'by_severity': {},
            'by_type': {},
            'by_url': {}
        }

        for finding in findings:
            # Count by severity
            severity = finding.get('severity', 'Info')
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1

            # Count by vulnerability type
            vuln_type = finding.get('vulnerability', 'Unknown')
            stats['by_type'][vuln_type] = stats['by_type'].get(vuln_type, 0) + 1

            # Count by URL
            url = finding.get('url', '')
            if url:
                stats['by_url'][url] = stats['by_url'].get(url, 0) + 1

        return stats

    def _generate_html_report(self, findings: Dict[str, List],
                             stats: Dict[str, Any], output_file: str):
        """Generate HTML report"""
        template = self._get_html_template()

        html_content = template.render(
            scan_info=self.scan_info,
            findings=findings,
            stats=stats,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[+] Report saved to: {output_file}")

    def _generate_pdf_report(self, findings: Dict[str, List],
                            stats: Dict[str, Any], output_file: str):
        """Generate PDF report"""
        try:
            import weasyprint

            # Generate HTML first
            html_file = output_file.replace('.pdf', '_temp.html')
            self._generate_html_report(findings, stats, html_file)

            # Convert to PDF
            weasyprint.HTML(filename=html_file).write_pdf(output_file)

            # Remove temporary HTML file
            if os.path.exists(html_file):
                os.remove(html_file)

            print(f"[+] PDF report saved to: {output_file}")

        except ImportError:
            print("[!] PDF generation requires weasyprint. Install with: pip install weasyprint")
            print("[!] Falling back to HTML format...")
            self._generate_html_report(findings, stats, output_file.replace('.pdf', '.html'))

    def _get_html_template(self) -> Template:
        """Get HTML template for report"""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Scan Report - {{ scan_info.get('target', 'Unknown') }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f4f4f4;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        h2 {
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }

        h3 {
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .header-info {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        .header-info p {
            margin: 5px 0;
        }

        .header-info strong {
            display: inline-block;
            width: 150px;
            color: #2c3e50;
        }

        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .summary-card h3 {
            color: white;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .summary-card .count {
            font-size: 36px;
            font-weight: bold;
        }

        .finding {
            background: #f8f9fa;
            border-left: 4px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }

        .finding.critical {
            border-left-color: #e74c3c;
            background: #fdedec;
        }

        .finding.high {
            border-left-color: #e67e22;
            background: #fef5e9;
        }

        .finding.medium {
            border-left-color: #f39c12;
            background: #fef9e7;
        }

        .finding.low {
            border-left-color: #3498db;
            background: #ebf5fb;
        }

        .finding.info {
            border-left-color: #95a5a6;
            background: #f4f4f4;
        }

        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .finding-title {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }

        .severity-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }

        .severity-badge.critical { background: #e74c3c; }
        .severity-badge.high { background: #e67e22; }
        .severity-badge.medium { background: #f39c12; }
        .severity-badge.low { background: #3498db; }
        .severity-badge.info { background: #95a5a6; }

        .finding-detail {
            margin: 10px 0;
        }

        .finding-detail strong {
            color: #2c3e50;
            display: inline-block;
            width: 120px;
        }

        .code-block {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }

        .recommendation {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin-top: 15px;
            border-radius: 5px;
        }

        .recommendation strong {
            color: #155724;
            display: block;
            margin-bottom: 5px;
        }

        .disclaimer {
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 20px;
            margin-top: 40px;
            border-radius: 8px;
        }

        .disclaimer h3 {
            color: #856404;
            margin-top: 0;
        }

        .disclaimer p {
            color: #856404;
            margin: 10px 0;
        }

        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background: #34495e;
            color: white;
            font-weight: bold;
        }

        tr:hover {
            background: #f5f5f5;
        }

        @media print {
            body {
                padding: 0;
                background: white;
            }
            .container {
                box-shadow: none;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Security Scan Report</h1>

        <div class="header-info">
            <p><strong>Target:</strong> {{ scan_info.get('target', 'Unknown') }}</p>
            <p><strong>Scan Date:</strong> {{ timestamp }}</p>
            <p><strong>Duration:</strong> {{ scan_info.get('duration', 'N/A') }}</p>
            <p><strong>Pages Scanned:</strong> {{ scan_info.get('pages_scanned', 0) }}</p>
            <p><strong>Forms Tested:</strong> {{ scan_info.get('forms_tested', 0) }}</p>
        </div>

        <h2>📊 Summary</h2>
        <div class="summary">
            <div class="summary-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h3>Total Findings</h3>
                <div class="count">{{ stats.total }}</div>
            </div>
            <div class="summary-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h3>Critical</h3>
                <div class="count">{{ stats.by_severity.get('Critical', 0) }}</div>
            </div>
            <div class="summary-card" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
                <h3>High</h3>
                <div class="count">{{ stats.by_severity.get('High', 0) }}</div>
            </div>
            <div class="summary-card" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
                <h3>Medium</h3>
                <div class="count">{{ stats.by_severity.get('Medium', 0) }}</div>
            </div>
        </div>

        {% for severity in ['Critical', 'High', 'Medium', 'Low', 'Info'] %}
            {% if findings[severity] %}
                <h2>{{ severity }} Severity Findings</h2>

                {% for finding in findings[severity] %}
                    <div class="finding {{ severity.lower() }}">
                        <div class="finding-header">
                            <div class="finding-title">{{ finding.get('vulnerability', 'Unknown') }}</div>
                            <span class="severity-badge {{ severity.lower() }}">{{ severity }}</span>
                        </div>

                        <div class="finding-detail">
                            <strong>URL:</strong>
                            <code>{{ finding.get('url', 'N/A') }}</code>
                        </div>

                        {% if finding.get('parameter') %}
                        <div class="finding-detail">
                            <strong>Parameter:</strong>
                            <code>{{ finding.get('parameter') }}</code>
                        </div>
                        {% endif %}

                        <div class="finding-detail">
                            <strong>Description:</strong>
                            <p>{{ finding.get('description', 'No description available') }}</p>
                        </div>

                        {% if finding.get('payload') %}
                        <div class="finding-detail">
                            <strong>Payload:</strong>
                            <div class="code-block">{{ finding.get('payload') }}</div>
                        </div>
                        {% endif %}

                        {% if finding.get('evidence') %}
                        <div class="finding-detail">
                            <strong>Evidence:</strong>
                            <div class="code-block">{{ finding.get('evidence')[:500] }}{% if finding.get('evidence')|length > 500 %}...{% endif %}</div>
                        </div>
                        {% endif %}

                        <div class="recommendation">
                            <strong>💡 Recommendation:</strong>
                            <p>{{ finding.get('recommendation', 'No recommendation available') }}</p>
                        </div>
                    </div>
                {% endfor %}
            {% endif %}
        {% endfor %}

        <div class="disclaimer">
            <h3>⚠️ LEGAL DISCLAIMER</h3>
            <p>This report was generated for EDUCATIONAL and DEFENSIVE purposes only.</p>
            <p>Scan was performed on a target that the operator has EXPLICIT PERMISSION to test.</p>
            <p>Unauthorized security testing is illegal. Only scan systems you own or have written permission to test.</p>
            <p>The findings in this report should be used to improve security posture.</p>
        </div>

        <div class="footer">
            <p>Generated by Web Vulnerability Scanner | Educational Security Tool</p>
            <p>This tool should only be used for legitimate security testing with proper authorization.</p>
            <p>Generated on {{ timestamp }}</p>
        </div>
    </div>
</body>
</html>
        """

        return Template(template_str)

    def generate_json_report(self, findings: List[Dict[str, Any]],
                            scan_info: Dict[str, Any],
                            output_file: str):
        """Generate JSON report"""
        import json

        report = {
            'scan_info': scan_info,
            'timestamp': datetime.now().isoformat(),
            'statistics': self._generate_statistics(findings),
            'findings': findings
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"[+] JSON report saved to: {output_file}")
