#!/usr/bin/env python3
"""
Log Analyzer - Main Entry Point
CLI tool per analizzare file di log

Educational - System Programming Concepts:
- File I/O (open, read, seek)
- Command-line argument parsing
- Real-time file monitoring (tail -f style)
- Signal handling per graceful shutdown
"""

import argparse
import sys
import logging
import time
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

# Import moduli locali
from parsers import ApacheLogParser, NginxLogParser, CustomLogParser
from analyzers import LogFilter, LogFilterBuilder, LogStatistics, DataExtractor
from reporters import TextReporter, HTMLReporter

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LogAnalyzer:
    """
    Main application class per Log Analyzer
    """

    def __init__(self):
        """Inizializza l'analizzatore"""
        self.parser = None
        self.entries = []

    def detect_format(self, filepath: str) -> str:
        """
        Rileva automaticamente il formato del log

        Args:
            filepath: Percorso file log

        Returns:
            Stringa formato ('apache', 'nginx', 'custom')
        """
        logger.info("Rilevamento formato log...")

        # Leggi prime righe
        sample_lines = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i >= 10:  # Prima 10 righe
                        break
                    sample_lines.append(line.strip())
        except IOError as e:
            logger.error(f"Errore lettura file: {e}")
            return 'custom'

        # Prova Apache
        apache_parser = ApacheLogParser()
        apache_matches = sum(1 for line in sample_lines if apache_parser.parse_line(line))

        # Prova Nginx
        nginx_parser = NginxLogParser()
        nginx_matches = sum(1 for line in sample_lines if nginx_parser.parse_line(line))

        # Decide basato su match
        if apache_matches > len(sample_lines) * 0.7:
            logger.info(f"Formato rilevato: Apache ({apache_matches}/{len(sample_lines)} match)")
            return 'apache'
        elif nginx_matches > len(sample_lines) * 0.7:
            logger.info(f"Formato rilevato: Nginx ({nginx_matches}/{len(sample_lines)} match)")
            return 'nginx'
        else:
            logger.info("Formato rilevato: Custom (no match chiaro)")
            return 'custom'

    def load_file(self, filepath: str, log_format: Optional[str] = None) -> bool:
        """
        Carica e parsa il file di log

        Args:
            filepath: Percorso file
            log_format: Format ('apache', 'nginx', 'custom') o None per auto-detect

        Returns:
            True se successo, False altrimenti
        """
        if not Path(filepath).exists():
            logger.error(f"File non trovato: {filepath}")
            return False

        # Rileva o usa formato specificato
        if log_format is None:
            log_format = self.detect_format(filepath)

        # Crea parser appropriato
        if log_format == 'apache':
            self.parser = ApacheLogParser()
        elif log_format == 'nginx':
            self.parser = NginxLogParser()
        elif log_format == 'custom':
            self.parser = CustomLogParser()
        else:
            logger.error(f"Formato non supportato: {log_format}")
            return False

        # Parsa file
        logger.info(f"Parsing file {filepath}...")
        try:
            self.entries = self.parser.parse_file(filepath)
            logger.info(f"Caricate {len(self.entries)} entries")
            return True
        except Exception as e:
            logger.error(f"Errore parsing: {e}")
            return False

    def analyze(self, args):
        """Comando analyze"""
        if not self.load_file(args.log_file, args.format):
            return 1

        logger.info("Analisi in corso...")

        # Filtra entries se richiesto
        entries = self.entries
        if args.level:
            log_filter = LogFilter().by_min_level(args.level)
            entries = log_filter.apply(entries)
            logger.info(f"Filtrato per livello >= {args.level}: {len(entries)} entries")

        if args.start_time or args.end_time:
            from datetime import datetime
            start = datetime.fromisoformat(args.start_time) if args.start_time else datetime.min
            end = datetime.fromisoformat(args.end_time) if args.end_time else datetime.max
            log_filter = LogFilter().by_time_range(start, end)
            entries = log_filter.apply(entries)
            logger.info(f"Filtrato per tempo: {len(entries)} entries")

        # Genera statistiche
        stats = LogStatistics(entries)

        # Genera report
        if args.output and args.output.endswith('.html'):
            reporter = HTMLReporter()
            summary = stats.generate_summary()
            html = reporter.generate_report(summary)
            reporter.save_report(html, args.output)
            logger.info(f"Report HTML salvato in {args.output}")
        else:
            reporter = TextReporter()

            # Stampa summary
            print(reporter.generate_summary(stats.generate_summary()))
            print(reporter.generate_top_errors(stats.top_errors(args.top)))
            print(reporter.generate_top_ips(stats.top_ips(args.top)))
            print(reporter.generate_top_paths(stats.top_paths(args.top)))

            if args.errors_by_hour:
                print(reporter.generate_errors_by_hour(stats.count_errors_by_hour()))

        return 0

    def tail(self, args):
        """Comando tail - follow log file in real-time"""
        filepath = args.log_file

        if not Path(filepath).exists():
            logger.error(f"File non trovato: {filepath}")
            return 1

        # Rileva formato
        log_format = args.format or self.detect_format(filepath)

        # Crea parser
        if log_format == 'apache':
            parser = ApacheLogParser()
        elif log_format == 'nginx':
            parser = NginxLogParser()
        else:
            parser = CustomLogParser()

        logger.info(f"Following {filepath} (Ctrl+C to stop)...")
        print(f"\n=== Log Tail Mode ===")
        print(f"File: {filepath}")
        print(f"Format: {log_format}")
        print(f"Filter: {args.level or 'ALL'}")
        print(f"{'=' * 60}\n")

        # Inizializza filtro
        log_filter = None
        if args.level:
            log_filter = LogFilter().by_min_level(args.level)

        try:
            # Posiziona alla fine del file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # Seek to end
                f.seek(0, 2)
                file_size = f.tell()

                # Track inode per detect log rotation
                last_inode = os.fstat(f.fileno()).st_ino

                line_count = 0

                while True:
                    line = f.readline()

                    if line:
                        # Parsa riga
                        parsed = parser.parse_line(line)
                        if parsed:
                            # Applica filtro
                            if log_filter:
                                if not log_filter.filters[0](parsed):  # type: ignore
                                    continue

                            # Stampa
                            timestamp = parsed.get('timestamp_parsed')
                            ts_str = timestamp.strftime('%H:%M:%S') if timestamp else '??'
                            level = parsed.get('level', '???')
                            message = parsed.get('message', line.strip())[:100]

                            color = self._get_level_color(level)
                            print(f"{ts_str} [{color}{level}{Fore.RESET}] {message}")
                            line_count += 1

                    else:
                        # Check for log rotation
                        try:
                            current_inode = os.fstat(f.fileno()).st_ino
                            if current_inode != last_inode:
                                logger.info("Log rotation detected, reopening...")
                                f.close()
                                f = open(filepath, 'r', encoding='utf-8', errors='ignore')
                                f.seek(0, 2)
                                last_inode = os.fstat(f.fileno()).st_ino
                        except:
                            pass

                        time.sleep(0.1)

        except KeyboardInterrupt:
            print(f"\n\nStopped. Processed {line_count} new lines.")
            return 0

    def stats(self, args):
        """Comando stats"""
        if not self.load_file(args.log_file, args.format):
            return 1

        stats = LogStatistics(self.entries)
        reporter = TextReporter()

        if args.by == 'hour':
            print(reporter.generate_hourly_stats(stats.count_by_hour()))
        elif args.by == 'day':
            daily = stats.count_by_day()
            print("\n=== Statistiche per Giorno ===\n")
            for day, count in sorted(daily.items()):
                print(f"  {day}: {count:,}")
        elif args.by == 'level':
            by_level = stats.count_by_level()
            print("\n=== Statistiche per Livello ===\n")
            for level, count in sorted(by_level.items()):
                print(f"  {level}: {count:,}")
        else:
            # Full summary
            print(reporter.generate_summary(stats.generate_summary()))

        return 0

    def extract_ips(self, args):
        """Comando extract-ips"""
        if not self.load_file(args.log_file, args.format):
            return 1

        extractor = DataExtractor()
        ips = extractor.extract_ips(self.entries, unique=True)

        print(f"\n=== IP Addresses Trovati: {len(ips)} ===\n")

        if args.top:
            # Count occurrences
            from collections import Counter
            ip_counter = Counter()

            for entry in self.entries:
                ip = entry.get('ip')
                if ip:
                    ip_counter[ip] += 1

            print(f"Top {args.top} IP per richieste:\n")
            for ip, count in ip_counter.most_common(args.top):
                print(f"  {ip:15} {count:6,} richieste")
        else:
            for ip in sorted(ips):
                print(f"  {ip}")

        return 0

    def _get_level_color(self, level: str) -> str:
        """Ritorna codice colore ANSI per livello"""
        from colorama import Fore

        level = level.upper()
        if level in ('ERROR', 'FATAL', 'CRITICAL'):
            return Fore.RED
        elif level in ('WARN', 'WARNING'):
            return Fore.YELLOW
        elif level == 'INFO':
            return Fore.GREEN
        else:
            return Fore.CYAN


def main():
    """Entry point principale"""
    # Import colorama per Windows colors
    try:
        from colorama import init, Fore, Style
        init()
    except ImportError:
        # Crea dummy Fore/Style se colorama non installato
        class DummyColors:
            RESET = ''
            RED = ''
            GREEN = ''
            YELLOW = ''
            CYAN = ''
        Fore = DummyColors()
        Style = type('Style', (), {'RESET_ALL': ''})()

    parser = argparse.ArgumentParser(
        prog='log-analyzer',
        description='Log Analyzer - Tool educativo per System Programming',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s analyze access.log --level ERROR
  %(prog)s analyze access.log --output report.html
  %(prog)s tail access.log
  %(prog)s stats access.log --by hour
  %(prog)s extract-ips access.log --top 10
        """
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Output verbose')

    subparsers = parser.add_subparsers(dest='command', help='Comandi disponibili')

    # Comando analyze
    analyze_parser = subparsers.add_parser('analyze', help='Analizza file di log')
    analyze_parser.add_argument('log_file', help='File di log da analizzare')
    analyze_parser.add_argument('--format', choices=['apache', 'nginx', 'custom'],
                              help='Formato log (default: auto-detect)')
    analyze_parser.add_argument('--level', choices=['DEBUG', 'INFO', 'WARN', 'ERROR'],
                              help='Filtra per livello minimo')
    analyze_parser.add_argument('--start-time', help='Data/ora inizio (ISO format)')
    analyze_parser.add_argument('--end-time', help='Data/ora fine (ISO format)')
    analyze_parser.add_argument('--output', '-o', help='File output (es. report.html)')
    analyze_parser.add_argument('--top', type=int, default=10,
                              help='Numero top results (default: 10)')
    analyze_parser.add_argument('--errors-by-hour', action='store_true',
                              help='Mostra errori per ora')

    # Comando tail
    tail_parser = subparsers.add_parser('tail', help='Follow log file in real-time')
    tail_parser.add_argument('log_file', help='File di log da seguire')
    tail_parser.add_argument('--format', choices=['apache', 'nginx', 'custom'],
                           help='Formato log (default: auto-detect)')
    tail_parser.add_argument('--level', choices=['DEBUG', 'INFO', 'WARN', 'ERROR'],
                           help='Filtra per livello minimo')

    # Comando stats
    stats_parser = subparsers.add_parser('stats', help='Genera statistiche')
    stats_parser.add_argument('log_file', help='File di log')
    stats_parser.add_argument('--format', choices=['apache', 'nginx', 'custom'],
                             help='Formato log (default: auto-detect)')
    stats_parser.add_argument('--by', choices=['hour', 'day', 'level', 'full'],
                            default='full', help='Raggruppa per (default: full)')

    # Comando extract-ips
    ips_parser = subparsers.add_parser('extract-ips', help='Estrae IP addresses')
    ips_parser.add_argument('log_file', help='File di log')
    ips_parser.add_argument('--format', choices=['apache', 'nginx', 'custom'],
                           help='Formato log (default: auto-detect)')
    ips_parser.add_argument('--top', type=int, help='Mostra top N IP per richieste')

    # Parse args
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Crea analyzer ed esegui comando
    analyzer = LogAnalyzer()

    try:
        if args.command == 'analyze':
            return analyzer.analyze(args)
        elif args.command == 'tail':
            return analyzer.tail(args)
        elif args.command == 'stats':
            return analyzer.stats(args)
        elif args.command == 'extract-ips':
            return analyzer.extract_ips(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        logger.error(f"Errore: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
