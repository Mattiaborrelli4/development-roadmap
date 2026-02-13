"""
Data Extractor Module
Estrae informazioni specifiche dai log entries

Educational - Extraction Techniques:
- Regex per pattern matching
- IP extraction e validation
- Data cleaning e normalizzazione
- Set operations per deduplicazione
"""

import re
from typing import List, Dict, Any, Set
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class DataExtractor:
    """
    Estrattore di dati da log entries

    Estrae:
    - IP addresses (IPv4 e IPv6)
    - Error patterns
    - URLs
    - User agents
    - Email addresses
    - Custom patterns
    """

    # Pattern regex comuni
    IPV4_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

    IPV6_PATTERN = re.compile(
        r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|'
        r'\b(?:[0-9a-fA-F]{1,4}:){1,7}:|[0-9a-fA-F]{1,4}:'
        r'\b(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}\b'
    )

    URL_PATTERN = re.compile(
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*'
    )

    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )

    USER_AGENT_PATTERN = re.compile(
        r'"([^"]*)"$'  # Generico per quoted strings alla fine
    )

    def __init__(self):
        """Inizializza l'estrattore"""
        logger.info("DataExtractor inizializzato")

    def extract_ips(self, entries: List[Dict[str, Any]], unique: bool = True) -> List[str]:
        """
        Estrae tutti gli IP addresses

        Args:
            entries: Lista di entries
            unique: Se True, restituisce solo IP unici

        Returns:
            Lista di IP addresses
        """
        ips = []

        # Prima cerca nel campo 'ip'
        for entry in entries:
            ip = entry.get('ip')
            if ip:
                ips.append(ip)

            # Cerca anche nel message/raw line
            message = entry.get('message', '')
            if message:
                found_ips = self.IPV4_PATTERN.findall(message)
                ips.extend(found_ips)

        if unique:
            ips = list(set(ips))

        logger.info(f"Estratti {len(ips)} IP addresses (unique={unique})")
        return ips

    def extract_ips_from_text(self, text: str) -> List[str]:
        """
        Estrae IP da una stringa di testo

        Args:
            text: Testo da analizzare

        Returns:
            Lista di IP trovati
        """
        ipv4s = self.IPV4_PATTERN.findall(text)
        ipv6s = self.IPV6_PATTERN.findall(text)

        all_ips = ipv4s + ipv6s
        unique_ips = list(set(all_ips))

        logger.debug(f"Trovati {len(unique_ips)} IP nel testo")
        return unique_ips

    def extract_error_patterns(self, entries: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Estrae error pattern comuni

        Args:
            entries: Lista di entries

        Returns:
            Dict {category: [messages]}
        """
        # Pattern comuni per categoria
        error_categories = {
            'database': [
                r'database connection failed',
                r'deadlock',
                r'timeout exceeded',
                r'sql error',
                r'constraint'
            ],
            'network': [
                r'connection refused',
                r'connection timeout',
                r'network unreachable',
                r'dns.*failed',
                r'socket error'
            ],
            'security': [
                r'unauthorized',
                r'authentication failed',
                r'permission denied',
                r'invalid token',
                r'brute force',
                r'injection'
            ],
            'file': [
                r'file not found',
                r'no such file',
                r'permission denied',
                r'disk full',
                r'i/o error'
            ]
        }

        results = {category: [] for category in error_categories}

        for entry in entries:
            level = entry.get('level', '').upper()
            if level not in ('ERROR', 'CRITICAL', 'FATAL'):
                continue

            message = entry.get('message', '')
            if not message:
                continue

            message_lower = message.lower()

            for category, patterns in error_categories.items():
                for pattern in patterns:
                    if re.search(pattern, message_lower):
                        results[category].append(message[:200])  # Tronca
                        break

        # Log counts
        for category, messages in results.items():
            logger.info(f"Error pattern '{category}': {len(messages)} occorrenze")

        return results

    def extract_urls(self, entries: List[Dict[str, Any]]) -> List[str]:
        """
        Estrae URLs dai log

        Args:
            entries: Lista di entries

        Returns:
            Lista di URLs
        """
        urls = []

        for entry in entries:
            # Cerca nel referer
            referer = entry.get('referer', '')
            if referer and referer != '-':
                urls.append(referer)

            # Cerca nel message
            message = entry.get('message', '')
            if message:
                found_urls = self.URL_PATTERN.findall(message)
                urls.extend(found_urls)

        # Deduplica
        unique_urls = list(set(urls))

        logger.info(f"Estratti {len(unique_urls)} URLs")
        return unique_urls

    def extract_user_agents(self, entries: List[Dict[str, Any]]) -> Counter:
        """
        Estrae e conta user agents

        Args:
            entries: Lista di entries

        Returns:
            Counter di user agents
        """
        counter = Counter()

        for entry in entries:
            ua = entry.get('user_agent')
            if ua and ua != '-':
                counter[ua] += 1

        logger.info(f"Estratti {len(counter)} user agents unici")
        return counter

    def extract_paths(self, entries: List[Dict[str, Any]]) -> List[str]:
        """
        Estrae paths dalle richieste HTTP

        Args:
            entries: Lista di entries

        Returns:
            Lista di paths
        """
        paths = []

        for entry in entries:
            path = entry.get('path')
            if path:
                paths.append(path)

        unique_paths = list(set(paths))

        logger.info(f"Estratti {len(unique_paths)} paths unici")
        return unique_paths

    def extract_status_codes(self, entries: List[Dict[str, Any]]) -> List[int]:
        """
        Estrae status codes HTTP

        Args:
            entries: Lista di entries

        Returns:
            Lista di status codes
        """
        status_codes = []

        for entry in entries:
            status = entry.get('status')
            if status is not None:
                status_codes.append(status)

        logger.info(f"Estratti {len(status_codes)} status codes")
        return status_codes

    def extract_by_field(self, entries: List[Dict[str, Any]], field: str,
                        unique: bool = True) -> List[Any]:
        """
        Estrae valori di un campo specifico

        Args:
            entries: Lista di entries
            field: Nome del campo
            unique: Se True, restituisce valori unici

        Returns:
            Lista di valori
        """
        values = []

        for entry in entries:
            value = entry.get(field)
            if value is not None:
                values.append(value)

        if unique:
            values = list(set(values))

        logger.info(f"Estratti {len(values)} valori unici per campo '{field}'")
        return values

    def extract_custom_pattern(self, entries: List[Dict[str, Any]],
                               pattern: str, field: str = 'message') -> List[str]:
        """
        Estrae usando pattern regex custom

        Args:
            entries: Lista di entries
            pattern: Pattern regex
            field: Campo dove cercare

        Returns:
            Lista di matches
        """
        compiled_pattern = re.compile(pattern)
        matches = []

        for entry in entries:
            text = entry.get(field, '')
            if text:
                found = compiled_pattern.findall(text)
                matches.extend(found)

        unique_matches = list(set(matches))

        logger.info(f"Estratti {len(unique_matches)} matches per pattern custom")
        return unique_matches

    def find_suspicious_activity(self, entries: List[Dict[str, Any]],
                                 ip_threshold: int = 100) -> Dict[str, Any]:
        """
        Identifica attività sospette

        Args:
            entries: Lista di entries
            ip_threshold: Soglia richieste per IP

        Returns:
            Dict con attività sospetta
        """
        # Conta richieste per IP
        ip_counter = Counter()
        error_counter = Counter()

        for entry in entries:
            ip = entry.get('ip')
            if ip:
                ip_counter[ip] += 1

            level = entry.get('level', '').upper()
            if level in ('ERROR', 'CRITICAL', 'FATAL'):
                if ip:
                    error_counter[ip] += 1

        # IP con richieste ecessive
        suspicious_ips = [ip for ip, count in ip_counter.items()
                         if count > ip_threshold]

        # IP con molti errori
        high_error_ips = [ip for ip, count in error_counter.items()
                         if count > 10]

        # IP che fanno tentativi di injection (controlla patterns)
        injection_attempts = []
        for entry in entries:
            message = entry.get('message', '')
            if any(p in message.lower() for p in ['sql injection', 'xss', '../']):
                ip = entry.get('ip')
                if ip and ip not in injection_attempts:
                    injection_attempts.append(ip)

        result = {
            'high_volume_ips': suspicious_ips,
            'high_error_ips': high_error_ips,
            'potential_injection_ips': injection_attempts,
            'stats': {
                'total_unique_ips': len(ip_counter),
                'suspicious_count': len(suspicious_ips),
                'high_error_count': len(high_error_ips)
            }
        }

        logger.info(f"Trovati {len(suspicious_ips)} IP sospetti")
        return result


def main():
    """Test dell'estrattore"""
    # Dati di test
    test_entries = [
        {
            'level': 'INFO',
            'message': 'Request from 192.168.1.1 successful',
            'ip': '192.168.1.1',
            'referer': 'http://example.com',
            'user_agent': 'Mozilla/5.0'
        },
        {
            'level': 'ERROR',
            'message': 'Database connection failed for 192.168.1.2',
            'ip': '192.168.1.2'
        },
        {
            'level': 'ERROR',
            'message': 'SQL injection attempt from 10.0.0.1',
            'ip': '10.0.0.1'
        },
    ]

    extractor = DataExtractor()

    print("Test Estrazione Dati:\n")

    print("1. IP addresses:")
    ips = extractor.extract_ips(test_entries)
    for ip in ips:
        print(f"   {ip}")

    print("\n2. IP dal testo:")
    text_ips = extractor.extract_ips_from_text("Contact 192.168.1.1 or 10.0.0.1 for support")
    print(f"   {text_ips}")

    print("\n3. Error patterns:")
    errors = extractor.extract_error_patterns(test_entries)
    for category, messages in errors.items():
        if messages:
            print(f"   {category}: {len(messages)} occorrenze")

    print("\n4. User agents:")
    uas = extractor.extract_user_agents(test_entries)
    for ua, count in uas.most_common():
        print(f"   {count}x: {ua}")

    print("\n5. Attività sospetta:")
    suspicious = extractor.find_suspicious_activity(test_entries, ip_threshold=2)
    print(f"   IP alto volume: {suspicious['high_volume_ips']}")
    print(f"   IP injection: {suspicious['potential_injection_ips']}")


if __name__ == '__main__':
    main()
