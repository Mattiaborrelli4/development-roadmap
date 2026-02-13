"""
HTML Report Generator
Genera report in formato HTML

Educational - Reporting Techniques:
- HTML template generation
- CSS styling per report
- Table rendering
- Responsive design
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HTMLReporter:
    """
    Generatore di report in formato HTML

    Crea report HTML con:
    - Tables
    - Charts (CSS based)
    - Responsive design
    - Styling professionale
    """

    def __init__(self):
        """Inizializza il reporter HTML"""
        logger.info("HTMLReporter inizializzato")

    def generate_report(self, stats: Dict[str, Any],
                       title: str = "Log Analyzer Report") -> str:
        """
        Genera report HTML completo

        Args:
            stats: Dict con tutte le statistiche
            title: Titolo del report

        Returns:
            Stringa HTML completa
        """
        html_parts = []

        # Header
        html_parts.append(self._generate_header(title))

        # Navigation
        html_parts.append(self._generate_navigation())

        # Main content
        html_parts.append('<main class="container">')

        # Summary section
        html_parts.append(self._generate_summary_section(stats))

        # Level distribution
        html_parts.append(self._generate_level_distribution(stats.get('by_level', {}),
                                                           stats.get('total_entries', 1)))

        # HTTP Status
        html_parts.append(self._generate_http_status_section(stats.get('http_status_codes', {})))

        # Top errors
        html_parts.append(self._generate_top_errors_section(stats.get('top_errors', [])))

        # Top IPs
        html_parts.append(self._generate_top_ips_section(stats.get('top_ips', [])))

        # Top paths
        html_parts.append(self._generate_top_paths_section(stats.get('top_paths', [])))

        # Hourly stats
        html_parts.append(self._generate_hourly_section(stats.get('by_hour', {})))

        # Error rate
        html_parts.append(self._generate_error_rate_section(stats.get('error_rate', {})))

        html_parts.append('</main>')

        # Footer
        html_parts.append(self._generate_footer())

        # Chiudi HTML
        html_parts.append('</body></html>')

        return "\n".join(html_parts)

    def _generate_header(self, title: str) -> str:
        """Genera header HTML"""
        return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <header class="header">
        <h1>{title}</h1>
        <p class="subtitle">Generato il {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </header>
"""

    def _generate_navigation(self) -> str:
        """Genera navigation menu"""
        return """
    <nav class="nav">
        <a href="#summary">Riepilogo</a>
        <a href="#levels">Livelli</a>
        <a href="#status">Status Code</a>
        <a href="#errors">Errori</a>
        <a href="#ips">IP Address</a>
        <a href="#paths">Paths</a>
        <a href="#hourly">Orario</a>
    </nav>
"""

    def _generate_summary_section(self, stats: Dict[str, Any]) -> str:
        """Genera sezione riepilogo"""
        total = stats.get('total_entries', 0)
        unique_ips = stats.get('unique_ips', 0)
        time_range = stats.get('time_range', {})

        first = time_range.get('first_timestamp')
        last = time_range.get('last_timestamp')

        time_str = "N/A"
        if first and last:
            time_str = f"{first.strftime('%Y-%m-%d %H:%M')} - {last.strftime('%Y-%m-%d %H:%M')}"

        return f"""
    <section id="summary" class="section">
        <h2>Riepilogo Generale</h2>
        <div class="summary-cards">
            <div class="card">
                <h3>Totale Entries</h3>
                <p class="big-number">{total:,}</p>
            </div>
            <div class="card">
                <h3>IP Unici</h3>
                <p class="big-number">{unique_ips:,}</p>
            </div>
            <div class="card">
                <h3>Periodo</h3>
                <p>{time_str}</p>
            </div>
        </div>
    </section>
"""

    def _generate_level_distribution(self, by_level: Dict[str, int],
                                    total: int) -> str:
        """Genera sezione distribuzione livelli"""
        rows = []

        for level, count in sorted(by_level.items()):
            pct = (count / total) * 100 if total > 0 else 0
            color = self._get_level_color(level)
            rows.append(f"""
                <tr>
                    <td><span class="badge" style="background-color: {color}">{level}</span></td>
                    <td class="number">{count:,}</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {pct}%; background-color: {color}"></div>
                        </div>
                    </td>
                    <td class="number">{pct:.2f}%</td>
                </tr>
            """)

        return f"""
    <section id="levels" class="section">
        <h2>Distribuzione per Livello</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>Livello</th>
                    <th>Count</th>
                    <th>Distribuzione</th>
                    <th>Percentuale</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
"""

    def _generate_http_status_section(self, status_codes: Dict[int, int]) -> str:
        """Genera sezione HTTP status codes"""
        rows = []

        for status, count in sorted(status_codes.items()):
            color = self._get_status_color(status)
            rows.append(f"""
                <tr>
                    <td><span class="badge" style="background-color: {color}">{status}</span></td>
                    <td class="number">{count:,}</td>
                </tr>
            """)

        return f"""
    <section id="status" class="section">
        <h2>HTTP Status Codes</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>Status</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
"""

    def _generate_top_errors_section(self, top_errors: List[tuple]) -> str:
        """Genera sezione top errori"""
        if not top_errors:
            return """
    <section id="errors" class="section">
        <h2>Top Errori</h2>
        <p>Nessun errore trovato.</p>
    </section>
"""

        rows = []
        for i, (message, count) in enumerate(top_errors, 1):
            rows.append(f"""
                <tr>
                    <td>{i}</td>
                    <td class="number">{count:,}</td>
                    <td>{self._escape_html(message)}</td>
                </tr>
            """)

        return f"""
    <section id="errors" class="section">
        <h2>Top {len(top_errors)} Errori</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Count</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
"""

    def _generate_top_ips_section(self, top_ips: List[tuple]) -> str:
        """Genera sezione top IP"""
        if not top_ips:
            return """
    <section id="ips" class="section">
        <h2>Top IP Addresses</h2>
        <p>Nessun IP trovato.</p>
    </section>
"""

        rows = []
        for i, (ip, count) in enumerate(top_ips, 1):
            rows.append(f"""
                <tr>
                    <td>{i}</td>
                    <td><code>{ip}</code></td>
                    <td class="number">{count:,}</td>
                </tr>
            """)

        return f"""
    <section id="ips" class="section">
        <h2>Top {len(top_ips)} IP Addresses</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>IP Address</th>
                    <th>Requests</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
"""

    def _generate_top_paths_section(self, top_paths: List[tuple]) -> str:
        """Genera sezione top paths"""
        if not top_paths:
            return """
    <section id="paths" class="section">
        <h2>Top Paths</h2>
        <p>Nessun path trovato.</p>
    </section>
"""

        rows = []
        for i, (path, count) in enumerate(top_paths, 1):
            rows.append(f"""
                <tr>
                    <td>{i}</td>
                    <td class="number">{count:,}</td>
                    <td><code>{self._escape_html(path)}</code></td>
                </tr>
            """)

        return f"""
    <section id="paths" class="section">
        <h2>Top {len(top_paths)} Paths</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Count</th>
                    <th>Path</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
"""

    def _generate_hourly_section(self, hourly_stats: Dict[str, int]) -> str:
        """Genera sezione statistiche orarie"""
        if not hourly_stats:
            return ""

        max_count = max(hourly_stats.values())

        rows = []
        for hour, count in sorted(hourly_stats.items()):
            pct = (count / max_count) * 100 if max_count > 0 else 0
            rows.append(f"""
                <tr>
                    <td>{hour}</td>
                    <td class="number">{count:,}</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {pct}%"></div>
                        </div>
                    </td>
                </tr>
            """)

        return f"""
    <section id="hourly" class="section">
        <h2>Statistiche Orarie</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>Ora</th>
                    <th>Count</th>
                    <th>Distribuzione</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </section>
"""

    def _generate_error_rate_section(self, error_rate: Dict[str, Any]) -> str:
        """Genera sezione error rate"""
        total = error_rate.get('total', 0)
        errors = error_rate.get('errors', 0)
        rate = error_rate.get('error_rate', 0)

        color = '#e74c3c' if rate > 5 else '#f39c12' if rate > 1 else '#27ae60'

        return f"""
    <section class="section">
        <h2>Tasso di Errore</h2>
        <div class="error-rate-box" style="border-color: {color}">
            <h3 style="color: {color}">{rate:.2f}%</h3>
            <p>{errors:,} errori su {total:,} richieste totali</p>
        </div>
    </section>
"""

    def _generate_footer(self) -> str:
        """Genera footer HTML"""
        return """
    <footer class="footer">
        <p>Generato da <strong>Log Analyzer</strong> - Tool educativo per System Programming</p>
    </footer>
"""

    def _get_level_color(self, level: str) -> str:
        """Ritorna colore per livello"""
        colors = {
            'ERROR': '#e74c3c',
            'FATAL': '#c0392b',
            'CRITICAL': '#c0392b',
            'WARN': '#f39c12',
            'WARNING': '#f39c12',
            'INFO': '#3498db',
            'DEBUG': '#95a5a6',
            'TRACE': '#7f8c8d'
        }
        return colors.get(level.upper(), '#95a5a6')

    def _get_status_color(self, status: int) -> str:
        """Ritorna colore per status code"""
        if status >= 500:
            return '#e74c3c'
        elif status >= 400:
            return '#e67e22'
        elif status >= 300:
            return '#f39c12'
        elif status >= 200:
            return '#27ae60'
        else:
            return '#95a5a6'

    def _escape_html(self, text: str) -> str:
        """Escape HTML entities"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))

    def _get_css(self) -> str:
        """Ritorna CSS per il report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1rem;
            opacity: 0.9;
        }

        .nav {
            background: #fff;
            padding: 1rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav a {
            color: #667eea;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background 0.3s;
        }

        .nav a:hover {
            background: #f0f0f0;
        }

        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        .section {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #667eea;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }

        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }

        .card h3 {
            font-size: 1rem;
            margin-bottom: 0.5rem;
            opacity: 0.9;
        }

        .big-number {
            font-size: 2.5rem;
            font-weight: bold;
        }

        .table {
            width: 100%;
            border-collapse: collapse;
        }

        .table th,
        .table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        .table th {
            background: #f8f9fa;
            font-weight: 600;
        }

        .table tr:hover {
            background: #f8f9fa;
        }

        .number {
            text-align: right !important;
            font-family: 'Courier New', monospace;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.875rem;
            color: white;
            font-weight: 500;
        }

        .progress-bar {
            background: #ecf0f1;
            border-radius: 4px;
            height: 20px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: #667eea;
            transition: width 0.3s;
        }

        .error-rate-box {
            border: 3px solid;
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
        }

        .error-rate-box h3 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }

        code {
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8rem;
            }

            .nav {
                flex-wrap: wrap;
            }

            .big-number {
                font-size: 2rem;
            }
        }
        """

    def save_report(self, content: str, filepath: str):
        """
        Salva report HTML su file

        Args:
            content: Contenuto HTML
            filepath: Percorso file
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Report HTML salvato in {filepath}")
        except IOError as e:
            logger.error(f"Errore salvataggio report: {e}")
            raise


def main():
    """Test del reporter HTML"""
    reporter = HTMLReporter()

    # Dati di test
    stats = {
        'total_entries': 1500,
        'unique_ips': 45,
        'time_range': {
            'first_timestamp': datetime(2024, 1, 15, 10, 0),
            'last_timestamp': datetime(2024, 1, 15, 18, 0)
        },
        'by_level': {'INFO': 1200, 'WARN': 200, 'ERROR': 80, 'DEBUG': 20},
        'http_status_codes': {200: 1100, 404: 300, 500: 80, 304: 20},
        'top_errors': [
            ('Database connection failed', 35),
            ('File not found', 20),
        ],
        'top_ips': [
            ('192.168.1.100', 450),
            ('192.168.1.50', 320),
        ],
        'top_paths': [
            ('/index.html', 500),
            ('/api/users', 300),
        ],
        'by_hour': {
            '2024-01-15 10:00': 150,
            '2024-01-15 11:00': 200,
        },
        'error_rate': {'total': 1500, 'errors': 80, 'error_rate': 5.33}
    }

    html = reporter.generate_report(stats)
    print("HTML report generato con successo!")
    print(f"Lunghezza: {len(html)} characters")


if __name__ == '__main__':
    main()
