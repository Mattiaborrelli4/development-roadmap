"""
Text Report Generator
Genera report in formato testo/plain

Educational - Reporting Techniques:
- String formatting
- Template rendering
- Table formatting
- ASCII art per visualizzazioni
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TextReporter:
    """
    Generatore di report in formato testo

    Crea report leggibili da console con:
    - Table formatting
    - Statistics summary
    - Top entries
    """

    def __init__(self, width: int = 100):
        """
        Inizializza il reporter

        Args:
            width: Larghezza massima del report
        """
        self.width = width
        logger.info("TextReporter inizializzato")

    def generate_summary(self, stats: Dict[str, Any]) -> str:
        """
        Genera riepilogo statistiche

        Args:
            stats: Dict con statistiche

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("LOG ANALYZER - RIEPILOGO STATISTICHE".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        # Info generali
        lines.append("INFORMAZIONI GENERALI")
        lines.append("-" * self.width)
        lines.append(f"  Totale Entries:        {stats.get('total_entries', 0):,}")
        lines.append(f"  IP Unici:              {stats.get('unique_ips', 0):,}")
        lines.append(f"  Range Temporale:       {self._format_time_range(stats.get('time_range', {}))}")
        lines.append("")

        # Livelli
        lines.append("DISTRIBUZIONE PER LIVELLO")
        lines.append("-" * self.width)
        by_level = stats.get('by_level', {})
        for level, count in sorted(by_level.items()):
            total = stats.get('total_entries', 1)
            pct = (count / total) * 100
            bar = self._create_bar(pct)
            lines.append(f"  {level:8}  {count:8,}  {pct:6.2f}%  {bar}")
        lines.append("")

        # HTTP Status
        lines.append("STATUS CODES HTTP")
        lines.append("-" * self.width)
        status_codes = stats.get('http_status_codes', {})
        for status, count in sorted(status_codes.items()):
            lines.append(f"  {status:4}  {count:8,}")
        lines.append("")

        # HTTP Methods
        lines.append("HTTP METHODS")
        lines.append("-" * self.width)
        methods = stats.get('http_methods', {})
        for method, count in sorted(methods.items()):
            lines.append(f"  {method:8}  {count:8,}")
        lines.append("")

        # Error Rate
        lines.append("TASSO DI ERRORE")
        lines.append("-" * self.width)
        error_rate = stats.get('error_rate', {})
        lines.append(f"  Totale Richieste:      {error_rate.get('total', 0):,}")
        lines.append(f"  Errori:               {error_rate.get('errors', 0):,}")
        lines.append(f"  Error Rate:           {error_rate.get('error_rate', 0):.2f}%")
        lines.append("")

        # Avg Response Size
        lines.append("DIMENSIONE MEDIA RISPOSTA")
        lines.append("-" * self.width)
        avg_size = stats.get('avg_response_size', {})
        lines.append(f"  Media:                 {avg_size.get('avg_size', 0):,.2f} bytes")
        lines.append(f"  Totale:                {avg_size.get('total_size', 0):,} bytes")
        lines.append("")

        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def generate_top_errors(self, top_errors: List[tuple]) -> str:
        """
        Genera report top errori

        Args:
            top_errors: Lista di (message, count)

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("TOP ERROR MESSAGES".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        if not top_errors:
            lines.append("Nessun errore trovato.")
        else:
            for i, (message, count) in enumerate(top_errors, 1):
                lines.append(f"{i:2}. [{count:4}x] {message[:80]}")

        lines.append("")
        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def generate_top_ips(self, top_ips: List[tuple]) -> str:
        """
        Genera report top IP

        Args:
            top_ips: Lista di (ip, count)

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("TOP IP ADDRESSES".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        if not top_ips:
            lines.append("Nessun IP trovato.")
        else:
            max_count = top_ips[0][1] if top_ips else 1

            for i, (ip, count) in enumerate(top_ips, 1):
                pct = (count / max_count) * 100 if max_count > 0 else 0
                bar = self._create_bar(pct, width=30)
                lines.append(f"{i:2}. {ip:15} [{count:6,}] {bar}")

        lines.append("")
        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def generate_top_paths(self, top_paths: List[tuple]) -> str:
        """
        Genera report top paths

        Args:
            top_paths: Lista di (path, count)

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("TOP REQUESTED PATHS".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        if not top_paths:
            lines.append("Nessun path trovato.")
        else:
            for i, (path, count) in enumerate(top_paths, 1):
                lines.append(f"{i:2}. [{count:6,}] {path[:80]}")

        lines.append("")
        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def generate_hourly_stats(self, hourly_stats: Dict[str, int]) -> str:
        """
        Genera report statistiche orarie con visualizzazione ASCII

        Args:
            hourly_stats: Dict {hour: count}

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("STATISTICHE ORARIE".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        if not hourly_stats:
            lines.append("Nessun dato orario disponibile.")
        else:
            max_count = max(hourly_stats.values())

            # Sort by hour
            sorted_hours = sorted(hourly_stats.items())

            for hour, count in sorted_hours:
                pct = (count / max_count) * 100 if max_count > 0 else 0
                bar = self._create_bar(pct)
                lines.append(f"  {hour}  [{count:6,}]  {bar}")

        lines.append("")
        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def generate_errors_by_hour(self, errors_by_hour: Dict[str, int]) -> str:
        """
        Genera report errori per ora

        Args:
            errors_by_hour: Dict {hour: error_count}

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("ERRORI PER ORA".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        if not errors_by_hour:
            lines.append("Nessun errore registrato.")
        else:
            max_count = max(errors_by_hour.values())
            sorted_hours = sorted(errors_by_hour.items())

            for hour, count in sorted_hours:
                pct = (count / max_count) * 100 if max_count > 0 else 0
                bar = self._create_bar(pct, char='█')
                lines.append(f"  {hour}  [{count:4}]  {bar}")

        lines.append("")
        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def generate_suspicious_activity(self, suspicious: Dict[str, Any]) -> str:
        """
        Genera report attività sospette

        Args:
            suspicious: Dict con attività sospetta

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * self.width)
        lines.append("ATTIVITÀ SOSPETTA RILEVATA".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        stats = suspicious.get('stats', {})

        lines.append(f"Totale IP unici analizzati:    {stats.get('total_unique_ips', 0):,}")
        lines.append(f"IP sospetti rilevati:         {stats.get('suspicious_count', 0):,}")
        lines.append(f"IP con molti errori:          {stats.get('high_error_count', 0):,}")
        lines.append("")

        high_volume = suspicious.get('high_volume_ips', [])
        if high_volume:
            lines.append("IP con alto volume di richieste:")
            for ip in high_volume[:10]:
                lines.append(f"  - {ip}")
            lines.append("")

        high_errors = suspicious.get('high_error_ips', [])
        if high_errors:
            lines.append("IP con alto tasso di errori:")
            for ip in high_errors[:10]:
                lines.append(f"  - {ip}")
            lines.append("")

        injection = suspicious.get('potential_injection_ips', [])
        if injection:
            lines.append("IP con potenziali attacchi injection:")
            for ip in injection[:10]:
                lines.append(f"  - {ip}")
            lines.append("")

        lines.append("=" * self.width)
        lines.append("")

        return "\n".join(lines)

    def _create_bar(self, percentage: float, width: int = 40,
                    char: str = '#') -> str:
        """
        Crea una bar ASCII per percentuali

        Args:
            percentage: Percentuale (0-100)
            width: Larghezza bar
            char: Carattere da usare

        Returns:
            Stringa con la bar
        """
        filled = int((percentage / 100) * width)
        empty = width - filled
        return char * filled + '-' * empty

    def _format_time_range(self, time_range: Dict[str, Any]) -> str:
        """
        Formatta range temporale

        Args:
            time_range: Dict con first_timestamp e last_timestamp

        Returns:
            Stringa formattata
        """
        first = time_range.get('first_timestamp')
        last = time_range.get('last_timestamp')

        if first and last:
            duration = time_range.get('duration_seconds', 0)
            hours = duration // 3600
            minutes = (duration % 3600) // 60

            return f"{first.strftime('%Y-%m-%d %H:%M')} - {last.strftime('%Y-%m-%d %H:%M')} ({hours}h {minutes}m)"
        elif first:
            return f"Da {first.strftime('%Y-%m-%d %H:%M')}"
        else:
            return "N/A"

    def save_report(self, content: str, filepath: str):
        """
        Salva report su file

        Args:
            content: Contenuto del report
            filepath: Percorso file
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Report salvato in {filepath}")
        except IOError as e:
            logger.error(f"Errore salvataggio report: {e}")
            raise


def main():
    """Test del reporter"""
    reporter = TextReporter()

    # Dati di test
    stats = {
        'total_entries': 1500,
        'unique_ips': 45,
        'time_range': {
            'first_timestamp': datetime(2024, 1, 15, 10, 0),
            'last_timestamp': datetime(2024, 1, 15, 18, 0),
            'duration_seconds': 28800
        },
        'by_level': {'INFO': 1200, 'WARN': 200, 'ERROR': 80, 'DEBUG': 20},
        'http_status_codes': {200: 1100, 404: 300, 500: 80, 304: 20},
        'http_methods': {'GET': 1000, 'POST': 400, 'PUT': 80, 'DELETE': 20},
        'error_rate': {'total': 1500, 'errors': 80, 'error_rate': 5.33},
        'avg_response_size': {'avg_size': 15432.5, 'total_size': 23148750}
    }

    top_errors = [
        ('Database connection failed', 35),
        ('File not found: /missing.html', 20),
        ('Timeout waiting for response', 15),
    ]

    top_ips = [
        ('192.168.1.100', 450),
        ('192.168.1.50', 320),
        ('10.0.0.1', 180),
    ]

    print("Generazione report:\n")
    print(reporter.generate_summary(stats))
    print(reporter.generate_top_errors(top_errors))
    print(reporter.generate_top_ips(top_ips))


if __name__ == '__main__':
    main()
