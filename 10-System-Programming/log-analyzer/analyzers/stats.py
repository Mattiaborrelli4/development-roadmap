"""
Statistics Generator Module
Genera statistiche dai log entries

Educational - Statistics Techniques:
- collections.Counter per counting
- defaultdict per aggregazione
- Time-based grouping
- Data aggregation patterns
"""

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class LogStatistics:
    """
    Generatore di statistiche per log entries

    Calcola:
    - Count per livello
    - Count per ora/giorno
    - Top errori
    - Statistiche HTTP
    - IP address analytics
    """

    def __init__(self, entries: List[Dict[str, Any]]):
        """
        Inizializza con entries

        Args:
            entries: Lista di log entries
        """
        self.entries = entries
        logger.info(f"LogStatistics inizializzato con {len(entries)} entries")

    def count_by_level(self) -> Dict[str, int]:
        """
        Conta entries per livello

        Returns:
            Dict {level: count}
        """
        counter = Counter()

        for entry in self.entries:
            level = entry.get('level', 'UNKNOWN').upper()
            counter[level] += 1

        result = dict(counter)
        logger.info(f"Count by level: {result}")
        return result

    def count_by_hour(self) -> Dict[str, int]:
        """
        Conta entries per ora

        Returns:
            Dict {hour: count}
        """
        counter = Counter()

        for entry in self.entries:
            timestamp = entry.get('timestamp_parsed')
            if timestamp:
                hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                counter[hour_key] += 1

        result = dict(counter)
        logger.info(f"Count by hour: {len(result)} ore diverse")
        return result

    def count_by_day(self) -> Dict[str, int]:
        """
        Conta entries per giorno

        Returns:
            Dict {day: count}
        """
        counter = Counter()

        for entry in self.entries:
            timestamp = entry.get('timestamp_parsed')
            if timestamp:
                day_key = timestamp.strftime('%Y-%m-%d')
                counter[day_key] += 1

        result = dict(counter)
        logger.info(f"Count by day: {len(result)} giorni diversi")
        return result

    def count_errors_by_hour(self) -> Dict[str, int]:
        """
        Conta errori per ora

        Returns:
            Dict {hour: error_count}
        """
        counter = Counter()

        for entry in self.entries:
            level = entry.get('level', '').upper()
            if level in ('ERROR', 'CRITICAL', 'FATAL'):
                timestamp = entry.get('timestamp_parsed')
                if timestamp:
                    hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                    counter[hour_key] += 1

        result = dict(counter)
        logger.info(f"Errors by hour: {len(result)} ore con errori")
        return result

    def top_errors(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Trova i top N error messages

        Args:
            n: Numero di top errori

        Returns:
            Lista di (message, count) tuples
        """
        counter = Counter()

        for entry in self.entries:
            level = entry.get('level', '').upper()
            if level in ('ERROR', 'CRITICAL', 'FATAL'):
                message = entry.get('message', '')
                if message:
                    # Tronca messaggi lunghi
                    if len(message) > 100:
                        message = message[:100] + '...'
                    counter[message] += 1

        top = counter.most_common(n)
        logger.info(f"Top {n} errors: {len(top)} trovati")
        return top

    def top_ips(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Trova i top N IP addresses

        Args:
            n: Numero di top IP

        Returns:
            Lista di (ip, count) tuples
        """
        counter = Counter()

        for entry in self.entries:
            ip = entry.get('ip')
            if ip:
                counter[ip] += 1

        top = counter.most_common(n)
        logger.info(f"Top {n} IPs: {len(top)} trovati")
        return top

    def http_status_codes(self) -> Dict[int, int]:
        """
        Conta occorrenze per status code HTTP

        Returns:
            Dict {status_code: count}
        """
        counter = Counter()

        for entry in self.entries:
            status = entry.get('status')
            if status is not None:
                counter[status] += 1

        result = dict(counter)
        logger.info(f"HTTP status codes: {result}")
        return result

    def http_methods(self) -> Dict[str, int]:
        """
        Conta occorrenze per HTTP method

        Returns:
            Dict {method: count}
        """
        counter = Counter()

        for entry in self.entries:
            method = entry.get('method')
            if method:
                counter[method.upper()] += 1

        result = dict(counter)
        logger.info(f"HTTP methods: {result}")
        return result

    def top_paths(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Trova i top N paths richiesti

        Args:
            n: Numero di top paths

        Returns:
            Lista di (path, count) tuples
        """
        counter = Counter()

        for entry in self.entries:
            path = entry.get('path')
            if path:
                counter[path] += 1

        top = counter.most_common(n)
        logger.info(f"Top {n} paths: {len(top)} trovati")
        return top

    def error_rate(self) -> Dict[str, float]:
        """
        Calcola il tasso di errore

        Returns:
            Dict con error_rate (percentuale)
        """
        if not self.entries:
            return {'error_rate': 0.0}

        total = len(self.entries)
        errors = 0

        for entry in self.entries:
            level = entry.get('level', '').upper()
            if level in ('ERROR', 'CRITICAL', 'FATAL'):
                errors += 1
            else:
                # Anche per HTTP status codes
                status = entry.get('status')
                if status and status >= 400:
                    errors += 1

        rate = (errors / total) * 100 if total > 0 else 0

        result = {
            'total': total,
            'errors': errors,
            'error_rate': round(rate, 2)
        }
        logger.info(f"Error rate: {rate:.2f}%")
        return result

    def time_range(self) -> Dict[str, datetime]:
        """
        Trova range temporale dei log

        Returns:
            Dict con first_timestamp e last_timestamp
        """
        timestamps = []

        for entry in self.entries:
            timestamp = entry.get('timestamp_parsed')
            if timestamp:
                timestamps.append(timestamp)

        if not timestamps:
            return {'first_timestamp': None, 'last_timestamp': None}

        result = {
            'first_timestamp': min(timestamps),
            'last_timestamp': max(timestamps)
        }

        if result['last_timestamp'] and result['first_timestamp']:
            duration = result['last_timestamp'] - result['first_timestamp']
            result['duration_seconds'] = duration.total_seconds()

        logger.info(f"Time range: {result['first_timestamp']} - {result['last_timestamp']}")
        return result

    def unique_ips(self) -> int:
        """
        Conta IP addresses unici

        Returns:
            Numero di IP unici
        """
        ips = set()

        for entry in self.entries:
            ip = entry.get('ip')
            if ip:
                ips.add(ip)

        count = len(ips)
        logger.info(f"Unique IPs: {count}")
        return count

    def average_response_size(self) -> Dict[str, float]:
        """
        Calcola size medio delle risposte

        Returns:
            Dict con avg_size
        """
        sizes = []

        for entry in self.entries:
            size = entry.get('size')
            if size is not None and isinstance(size, (int, float)):
                sizes.append(size)

        if not sizes:
            return {'avg_size': 0, 'total_size': 0, 'count': 0}

        avg = sum(sizes) / len(sizes)

        result = {
            'avg_size': round(avg, 2),
            'total_size': sum(sizes),
            'count': len(sizes)
        }
        logger.info(f"Average response size: {avg:.2f} bytes")
        return result

    def generate_summary(self) -> Dict[str, Any]:
        """
        Genera riepilogo completo di tutte le statistiche

        Returns:
            Dict con tutte le statistiche
        """
        logger.info("Generazione riepilogo statistiche...")

        summary = {
            'total_entries': len(self.entries),
            'by_level': self.count_by_level(),
            'by_hour': self.count_by_hour(),
            'by_day': self.count_by_day(),
            'errors_by_hour': self.count_errors_by_hour(),
            'top_errors': self.top_errors(10),
            'top_ips': self.top_ips(10),
            'top_paths': self.top_paths(10),
            'http_status_codes': self.http_status_codes(),
            'http_methods': self.http_methods(),
            'error_rate': self.error_rate(),
            'time_range': self.time_range(),
            'unique_ips': self.unique_ips(),
            'avg_response_size': self.average_response_size(),
        }

        logger.info("Riepilogo statistiche completato")
        return summary


def main():
    """Test del generatore statistiche"""
    # Dati di test
    test_entries = [
        {
            'level': 'INFO',
            'timestamp_parsed': datetime(2024, 1, 15, 10, 30, 0),
            'ip': '192.168.1.1',
            'status': 200,
            'path': '/index.html',
            'method': 'GET',
            'size': 1234,
            'message': 'Request successful'
        },
        {
            'level': 'ERROR',
            'timestamp_parsed': datetime(2024, 1, 15, 10, 30, 0),
            'ip': '192.168.1.2',
            'status': 500,
            'path': '/api/users',
            'method': 'GET',
            'size': 567,
            'message': 'Database connection failed'
        },
        {
            'level': 'ERROR',
            'timestamp_parsed': datetime(2024, 1, 15, 10, 30, 0),
            'ip': '192.168.1.2',
            'status': 500,
            'path': '/api/users',
            'method': 'GET',
            'size': 567,
            'message': 'Database connection failed'
        },
        {
            'level': 'WARN',
            'timestamp_parsed': datetime(2024, 1, 15, 11, 0, 0),
            'ip': '192.168.1.1',
            'status': 404,
            'path': '/missing',
            'method': 'GET',
            'size': 234,
            'message': 'File not found'
        },
    ]

    stats = LogStatistics(test_entries)

    print("Statistiche Log:\n")

    print("1. Count by level:")
    print(f"   {stats.count_by_level()}")

    print("\n2. Count by hour:")
    print(f"   {stats.count_by_hour()}")

    print("\n3. Top errors:")
    for msg, count in stats.top_errors(5):
        print(f"   {count}x: {msg}")

    print("\n4. Top IPs:")
    for ip, count in stats.top_ips(5):
        print(f"   {count}x: {ip}")

    print("\n5. HTTP Status codes:")
    print(f"   {stats.http_status_codes()}")

    print("\n6. Error rate:")
    print(f"   {stats.error_rate()}")

    print("\n7. Summary completo:")
    summary = stats.generate_summary()
    print(f"   Total entries: {summary['total_entries']}")
    print(f"   Unique IPs: {summary['unique_ips']}")
    print(f"   Avg response size: {summary['avg_response_size']['avg_size']} bytes")


if __name__ == '__main__':
    main()
