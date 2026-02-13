"""
HTML Reporter Module
Genera report HTML interattivi
"""

from typing import List, Dict
from pathlib import Path
from datetime import datetime
from jinja2 import Template


class HTMLReporter:
    """Generatore di report HTML."""

    def __init__(self):
        pass

    def generate(self, findings: List[Dict], output_path: str, target_path: Path) -> None:
        """
        Genera il report HTML.

        Args:
            findings: Lista di vulnerabilità trovate
            output_path: Percorso del file HTML da generare
            target_path: Percorso analizzato
        """
        # Prepara i dati
        report_data = self._prepare_report_data(findings, target_path)

        # Genera HTML
        html_content = self._render_html(report_data)

        # Salva file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _prepare_report_data(self, findings: List[Dict], target_path: Path) -> Dict:
        """Prepara i dati per il template."""
        # Ordina per severità
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        findings.sort(key=lambda x: severity_order.get(x.get('severity', 'LOW'), 4))

        # Raggruppa per severità
        grouped = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }

        for finding in findings:
            severity = finding.get('severity', 'LOW')
            if severity in grouped:
                grouped[severity].append(finding)

        # Statistiche
        stats = {
            'total': len(findings),
            'by_severity': {
                'CRITICAL': len(grouped['CRITICAL']),
                'HIGH': len(grouped['HIGH']),
                'MEDIUM': len(grouped['MEDIUM']),
                'LOW': len(grouped['LOW'])
            },
            'by_type': {}
        }

        for finding in findings:
            ftype = finding.get('type', 'unknown')
            stats['by_type'][ftype] = stats['by_type'].get(ftype, 0) + 1

        return {
            'findings': findings,
            'grouped': grouped,
            'stats': stats,
            'target_path': str(target_path),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.now().strftime('%d/%m/%Y')
        }

    def _render_html(self, data: Dict) -> str:
        """Renderizza il template HTML."""
        template_str = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Audit Report - {{ data.date }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .disclaimer-banner {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            margin: 0;
            border-bottom: 1px solid #ffc107;
        }

        .disclaimer-banner strong {
            color: #856404;
        }

        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }

        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }

        .summary-card h3 {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .summary-card .number {
            font-size: 2.5em;
            font-weight: bold;
        }

        .summary-card.critical .number { color: #dc3545; }
        .summary-card.high .number { color: #fd7e14; }
        .summary-card.medium .number { color: #ffc107; }
        .summary-card.low .number { color: #0dcaf0; }
        .summary-card.total .number { color: #6f42c1; }

        .content {
            padding: 30px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .severity-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            color: white;
        }

        .severity-critical { background: #dc3545; }
        .severity-high { background: #fd7e14; }
        .severity-medium { background: #ffc107; color: #000; }
        .severity-low { background: #0dcaf0; }

        .finding {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .finding:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .finding-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }

        .finding-meta {
            display: flex;
            gap: 15px;
            font-size: 0.9em;
            color: #666;
            flex-wrap: wrap;
        }

        .finding-meta span {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            margin: 15px 0;
        }

        .recommendation {
            background: #e7f3ff;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }

        .recommendation strong {
            color: #1976d2;
        }

        .description {
            color: #555;
            margin: 10px 0;
        }

        .references {
            margin-top: 15px;
        }

        .references a {
            color: #667eea;
            text-decoration: none;
            display: block;
            margin: 5px 0;
        }

        .references a:hover {
            text-decoration: underline;
        }

        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #28a745;
        }

        .empty-state .icon {
            font-size: 4em;
            margin-bottom: 20px;
        }

        @media (max-width: 768px) {
            .header h1 { font-size: 1.8em; }
            .summary { grid-template-columns: 1fr; }
            .finding-header { flex-direction: column; }
        }

        .chart-container {
            margin: 20px 0;
        }

        .bar-chart {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .bar-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .bar-label {
            min-width: 150px;
            font-size: 0.9em;
        }

        .bar {
            flex: 1;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-size: 0.85em;
            font-weight: bold;
            transition: width 0.5s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Security Audit Report</h1>
            <div class="subtitle">Generated: {{ data.timestamp }}</div>
            <div class="subtitle">Target: {{ data.target_path }}</div>
        </div>

        <div class="disclaimer-banner">
            <strong>⚠️ DISCLAIMER:</strong>
            Questo report è generato da uno strumento educativo/defensivo.
            I risultati sono indicativi e richiedono verifica umana.
            Utilizzare solo su codice di propria proprietà o con esplicito permesso.
        </div>

        {% if data.stats.total > 0 %}
        <div class="summary">
            <div class="summary-card total">
                <h3>Totale Vulnerabilità</h3>
                <div class="number">{{ data.stats.total }}</div>
            </div>
            <div class="summary-card critical">
                <h3>Critical</h3>
                <div class="number">{{ data.stats.by_severity.CRITICAL }}</div>
            </div>
            <div class="summary-card high">
                <h3>High</h3>
                <div class="number">{{ data.stats.by_severity.HIGH }}</div>
            </div>
            <div class="summary-card medium">
                <h3>Medium</h3>
                <div class="number">{{ data.stats.by_severity.MEDIUM }}</div>
            </div>
            <div class="summary-card low">
                <h3>Low</h3>
                <div class="number">{{ data.stats.by_severity.LOW }}</div>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <h2 class="section-title">📊 Vulnerabilità per Tipo</h2>
                <div class="bar-chart">
                    {% set max_count = data.stats.by_type.values() | max | default(1) %}
                    {% for type, count in data.stats.by_type.items() %}
                    <div class="bar-item">
                        <div class="bar-label">{{ type.replace('_', ' ').title() }}</div>
                        <div class="bar">
                            <div class="bar-fill" style="width: {{ (count / max_count * 100) | int }}%">{{ count }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            {% for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'] %}
                {% if data.grouped[severity] %}
                <div class="section">
                    <h2 class="section-title">
                        {{ severity }}
                        <span class="severity-badge severity-{{ severity.lower() }}">{{ data.grouped[severity]|length }}</span>
                    </h2>

                    {% for finding in data.grouped[severity] %}
                    <div class="finding">
                        <div class="finding-header">
                            <div class="finding-title">{{ finding.title }}</div>
                            <span class="severity-badge severity-{{ finding.severity.lower() }}">
                                {{ finding.severity }}
                            </span>
                        </div>

                        <div class="finding-meta">
                            <span>📁 {{ finding.file.split('/')[-1] }}</span>
                            <span>📍 Linea {{ finding.line }}</span>
                            <span>🔍 {{ finding.cwe }}</span>
                        </div>

                        <p class="description">{{ finding.description }}</p>

                        {% if finding.code %}
                        <div class="code-block">{{ finding.code }}</div>
                        {% endif %}

                        {% if finding.recommendation %}
                        <div class="recommendation">
                            <strong>💡 Raccomandazione:</strong><br>
                            {{ finding.recommendation | replace('\n', '<br>') | safe }}
                        </div>
                        {% endif %}

                        {% if finding.references %}
                        <div class="references">
                            <strong>📚 Riferimenti:</strong>
                            {% for ref in finding.references %}
                            <a href="{{ ref }}" target="_blank">{{ ref }}</a>
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state">
            <div class="icon">✅</div>
            <h2>Nessuna Vulnerabilità Trovata</h2>
            <p>Non sono state rilevate vulnerabilità nel codice analizzato.</p>
            <p><small>Nota: Questo non garantisce che il codice sia completamente sicuro.</small></p>
        </div>
        {% endif %}

        <div class="footer">
            <p>Generato da Security Audit Tool v1.0.0 | Strumento Educativo/Difensivo</p>
            <p>
                ⚠️ Questo report è indicativo. Una revisione umana professionale è sempre raccomandata.
            </p>
        </div>
    </div>
</body>
</html>
        """

        template = Template(template_str)
        return template.render(data=data)
