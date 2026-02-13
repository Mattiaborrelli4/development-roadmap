"""
Log Filter Module
Filtra log entries per vari criteri

Educational - Filtering Techniques:
- List comprehension per performance
- Lambda functions
- Generator expressions per memory efficiency
- Predicate composition
"""

from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)


class LogFilter:
    """
    Filtro per log entries

    Supporta filtraggio per:
    - Livello (ERROR, WARN, INFO, DEBUG)
    - Intervallo temporale
    - IP address
    - Status code
    - Custom predicate functions
    """

    # Livelli di log ordinati per severità
    LOG_LEVELS = {
        'DEBUG': 0,
        'INFO': 1,
        'WARN': 2,
        'WARNING': 2,
        'ERROR': 3,
        'CRITICAL': 4,
        'FATAL': 4
    }

    def __init__(self):
        """Inizializza il filtro"""
        self.filters: List[Callable[[Dict[str, Any]], bool]] = []
        logger.info("LogFilter inizializzato")

    def by_level(self, level: str) -> 'LogFilter':
        """
        Filtra per livello di log

        Args:
            level: Livello (DEBUG, INFO, WARN, ERROR)

        Returns:
            Self per method chaining
        """
        level_upper = level.upper()

        def level_filter(entry: Dict[str, Any]) -> bool:
            entry_level = entry.get('level', '').upper()
            return entry_level == level_upper

        self.filters.append(level_filter)
        logger.debug(f"Aggiunto filtro livello: {level}")
        return self

    def by_min_level(self, min_level: str) -> 'LogFilter':
        """
        Filtra per livello minimo (es. ERROR include ERROR, CRITICAL, FATAL)

        Args:
            min_level: Livello minimo

        Returns:
            Self per method chaining
        """
        min_severity = self.LOG_LEVELS.get(min_level.upper(), 0)

        def min_level_filter(entry: Dict[str, Any]) -> bool:
            entry_level = entry.get('level', '').upper()
            entry_severity = self.LOG_LEVELS.get(entry_level, 0)
            return entry_severity >= min_severity

        self.filters.append(min_level_filter)
        logger.debug(f"Aggiunto filtro livello minimo: {min_level}")
        return self

    def by_time_range(self, start: datetime, end: datetime) -> 'LogFilter':
        """
        Filtra per intervallo temporale

        Args:
            start: Data/ora inizio
            end: Data/ora fine

        Returns:
            Self per method chaining
        """
        def time_filter(entry: Dict[str, Any]) -> bool:
            timestamp = entry.get('timestamp_parsed')
            if not timestamp:
                return False
            return start <= timestamp <= end

        self.filters.append(time_filter)
        logger.debug(f"Aggiunto filtro tempo: {start} - {end}")
        return self

    def by_ip(self, ip_address: str) -> 'LogFilter':
        """
        Filtra per IP address

        Args:
            ip_address: IP da filtrare

        Returns:
            Self per method chaining
        """
        def ip_filter(entry: Dict[str, Any]) -> bool:
            return entry.get('ip') == ip_address

        self.filters.append(ip_filter)
        logger.debug(f"Aggiunto filtro IP: {ip_address}")
        return self

    def by_ip_pattern(self, pattern: str) -> 'LogFilter':
        """
        Filtra per pattern IP (es. "192.168." per subnet)

        Args:
            pattern: Pattern IP

        Returns:
            Self per method chaining
        """
        def ip_pattern_filter(entry: Dict[str, Any]) -> bool:
            ip = entry.get('ip', '')
            return ip.startswith(pattern)

        self.filters.append(ip_pattern_filter)
        logger.debug(f"Aggiunto filtro pattern IP: {pattern}")
        return self

    def by_status_code(self, status: int) -> 'LogFilter':
        """
        Filtra per status code HTTP

        Args:
            status: Status code

        Returns:
            Self per method chaining
        """
        def status_filter(entry: Dict[str, Any]) -> bool:
            return entry.get('status') == status

        self.filters.append(status_filter)
        logger.debug(f"Aggiunto filtro status: {status}")
        return self

    def by_status_range(self, min_status: int, max_status: int) -> 'LogFilter':
        """
        Filtra per range di status code

        Args:
            min_status: Status minimo
            max_status: Status massimo

        Returns:
            Self per method chaining
        """
        def status_range_filter(entry: Dict[str, Any]) -> bool:
            status = entry.get('status', 0)
            return min_status <= status <= max_status

        self.filters.append(status_range_filter)
        logger.debug(f"Aggiunto filtro range status: {min_status}-{max_status}")
        return self

    def by_path(self, path_pattern: str) -> 'LogFilter':
        """
        Filtra per path URL

        Args:
            path_pattern: Pattern path (supporta * wildcard)

        Returns:
            Self per method chaining
        """
        import fnmatch

        def path_filter(entry: Dict[str, Any]) -> bool:
            path = entry.get('path', '')
            return fnmatch.fnmatch(path, path_pattern)

        self.filters.append(path_filter)
        logger.debug(f"Aggiunto filtro path: {path_pattern}")
        return self

    def by_method(self, method: str) -> 'LogFilter':
        """
        Filtra per HTTP method

        Args:
            method: Method (GET, POST, etc.)

        Returns:
            Self per method chaining
        """
        method_upper = method.upper()

        def method_filter(entry: Dict[str, Any]) -> bool:
            return entry.get('method', '').upper() == method_upper

        self.filters.append(method_filter)
        logger.debug(f"Aggiunto filtro method: {method}")
        return self

    def by_message_contains(self, text: str, case_sensitive: bool = False) -> 'LogFilter':
        """
        Filtra per testo nel messaggio

        Args:
            text: Testo da cercare
            case_sensitive: Se True, case sensitive

        Returns:
            Self per method chaining
        """
        if case_sensitive:
            def message_filter(entry: Dict[str, Any]) -> bool:
                return text in entry.get('message', '')
        else:
            text_lower = text.lower()
            def message_filter(entry: Dict[str, Any]) -> bool:
                return text_lower in entry.get('message', '').lower()

        self.filters.append(message_filter)
        logger.debug(f"Aggiunto filtro message contains: {text}")
        return self

    def by_custom(self, predicate: Callable[[Dict[str, Any]], bool]) -> 'LogFilter':
        """
        Aggiunge filtro custom

        Args:
            predicate: Funzione che ritorna True se entry passa il filtro

        Returns:
            Self per method chaining
        """
        self.filters.append(predicate)
        logger.debug("Aggiunto filtro custom")
        return self

    def apply(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Applica tutti i filtri

        Args:
            entries: Lista di entries

        Returns:
            Lista filtrata
        """
        if not self.filters:
            return entries

        # Usa generator per memory efficiency
        result = entries
        for filter_func in self.filters:
            result = [entry for entry in result if filter_func(entry)]

        logger.info(f"Filtraggio: {len(entries)} -> {len(result)} entries")
        return result

    def apply_iter(self, entries: List[Dict[str, Any]]):
        """
        Applica filtri con generator (per grandi dataset)

        Args:
            entries: Lista di entries

        Yields:
            Entries filtrate una alla volta
        """
        if not self.filters:
            yield from entries
            return

        result = entries
        for filter_func in self.filters:
            result = (entry for entry in result if filter_func(entry))

        yield from result

    def reset(self) -> 'LogFilter':
        """
        Resetta tutti i filtri

        Returns:
            Self
        """
        self.filters.clear()
        logger.debug("Filtri resettati")
        return self


class LogFilterBuilder:
    """
    Builder per creare filtri complessi
    """

    @staticmethod
    def errors_only() -> LogFilter:
        """Crea filtro per soli errori"""
        return LogFilter().by_min_level('ERROR')

    @staticmethod
    def client_errors() -> LogFilter:
        """Crea filtro per errori client (4xx)"""
        return LogFilter().by_status_range(400, 499)

    @staticmethod
    def server_errors() -> LogFilter:
        """Crea filtro per errori server (5xx)"""
        return LogFilter().by_status_range(500, 599)

    @staticmethod
    def failed_requests() -> LogFilter:
        """Crea filtro per richieste fallite (4xx e 5xx)"""
        return LogFilter().by_status_range(400, 599)

    @staticmethod
    def last_hours(hours: int) -> LogFilter:
        """Crea filtro per ultime N ore"""
        from datetime import timedelta
        start = datetime.now() - timedelta(hours=hours)
        end = datetime.now()
        return LogFilter().by_time_range(start, end)

    @staticmethod
    def specific_ip(ip: str) -> LogFilter:
        """Crea filtro per IP specifico"""
        return LogFilter().by_ip(ip)


def main():
    """Test del filtro"""
    # Dati di test
    test_entries = [
        {
            'level': 'INFO',
            'timestamp_parsed': datetime(2024, 1, 15, 10, 30, 0),
            'ip': '192.168.1.1',
            'status': 200,
            'path': '/index.html',
            'message': 'Request successful'
        },
        {
            'level': 'ERROR',
            'timestamp_parsed': datetime(2024, 1, 15, 10, 31, 0),
            'ip': '192.168.1.2',
            'status': 500,
            'path': '/api/users',
            'message': 'Database connection failed'
        },
        {
            'level': 'WARN',
            'timestamp_parsed': datetime(2024, 1, 15, 10, 32, 0),
            'ip': '192.168.1.1',
            'status': 404,
            'path': '/missing',
            'message': 'File not found'
        },
    ]

    print("Test filtri:\n")

    # Test 1: Solo errori
    print("1. Solo ERROR:")
    errors = LogFilterBuilder.errors_only().apply(test_entries)
    for e in errors:
        print(f"   {e['level']}: {e['message']}")

    # Test 2: Solo IP 192.168.1.1
    print("\n2. Solo IP 192.168.1.1:")
    ip_filtered = LogFilterBuilder.specific_ip('192.168.1.1').apply(test_entries)
    for e in ip_filtered:
        print(f"   {e['ip']}: {e['message']}")

    # Test 3: Errori client (4xx)
    print("\n3. Errori client (4xx):")
    client_errors = LogFilterBuilder.client_errors().apply(test_entries)
    for e in client_errors:
        print(f"   Status {e['status']}: {e['path']}")

    # Test 4: Combinazione multipla
    print("\n4. ERROR + IP 192.168.1.2:")
    combined = (LogFilter()
                .by_min_level('ERROR')
                .by_ip('192.168.1.2')
                .apply(test_entries))
    for e in combined:
        print(f"   {e['level']}: {e['message']}")


if __name__ == '__main__':
    main()
