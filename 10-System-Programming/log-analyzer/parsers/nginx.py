"""
Nginx Log Parser
Analizza log in formato Nginx

Educational - Log Parser Techniques:
- Parsing di formati web server custom
- Gestione di campi opzionali
- Estrazione user agent
"""

import re
from datetime import datetime
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class NginxLogParser:
    """
    Parser per log Nginx

    Formato tipico Nginx:
    192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"

    Supporta anche formati custom Nginx
    """

    # Pattern per default Nginx format
    DEFAULT_PATTERN = re.compile(
        r'^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
        r'(?P<identity>\S+)\s+'
        r'(?P<userid>\S+)\s+'
        r'\[(?P<timestamp>[^\]]+)\]\s+'
        r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+'
        r'(?P<status>\d+)\s+'
        r'(?P<size>\d+)\s+'
        r'"(?P<referer>[^"]*)"\s+'
        r'"(?P<user_agent>[^"]*)"'
        r'(?:\s+"(?P<x_forwarded_for>[^"]*)")?'  # Opzionale
        r'(?:\s+(?P<request_time>\d+\.\d+))?'  # Opzionale
        r'$'
    )

    # Pattern per JSON logs (Nginx può loggare in JSON)
    JSON_IMPORT_ERROR = None

    try:
        import json
        JSON_AVAILABLE = True
    except ImportError:
        JSON_AVAILABLE = False
        JSON_IMPORT_ERROR = "json module not available"

    def __init__(self, pattern: Optional[str] = None):
        """
        Inizializza il parser Nginx

        Args:
            pattern: Pattern regex custom (opzionale)
        """
        if pattern:
            self.pattern = re.compile(pattern)
        else:
            self.pattern = self.DEFAULT_PATTERN

        logger.info("Nginx Log Parser inizializzato")

    def parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parsa una riga di log Nginx

        Args:
            line: Riga di log da parsare

        Returns:
            Dict con i campi parsati o None se la riga non matcha
        """
        if not line or not line.strip():
            return None

        # Prova prima JSON se disponibile
        if self.JSON_AVAILABLE and line.strip().startswith('{'):
            return self._parse_json_line(line)

        # Altrimenti regex
        match = self.pattern.match(line.strip())
        if not match:
            logger.debug(f"Impossibile parsare la riga: {line[:100]}...")
            return None

        data = match.groupdict()

        # Parsing del timestamp
        data['timestamp_parsed'] = self._parse_timestamp(data['timestamp'])

        # Conversione tipi
        data['status'] = int(data['status'])
        data['size'] = int(data['size'])

        # Campi opzionali
        if data.get('request_time'):
            data['request_time'] = float(data['request_time'])
        else:
            data['request_time'] = None

        # Livello di log
        data['level'] = self._get_log_level(data['status'])

        # Messaggio
        data['message'] = f"{data['method']} {data['path']} - {data['status']}"

        # Valori di default
        if not data.get('referer'):
            data['referer'] = '-'
        if not data.get('user_agent'):
            data['user_agent'] = '-'
        if not data.get('x_forwarded_for'):
            data['x_forwarded_for'] = None

        return data

    def _parse_json_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parsa una riga di log in formato JSON

        Args:
            line: Riga JSON

        Returns:
            Dict o None
        """
        try:
            import json
            data = json.loads(line)

            # Normalizza campi
            if 'time' in data and 'timestamp_parsed' not in data:
                data['timestamp_parsed'] = self._parse_iso_timestamp(data['time'])

            if 'status' in data:
                data['level'] = self._get_log_level(data['status'])

            return data

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Errore parsing JSON: {e}")
            return None

    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Parsa timestamp Nginx (stesso formato Apache)

        Args:
            timestamp_str: Stringa timestamp

        Returns:
            datetime oggetto o None
        """
        try:
            # Rimuovi timezone
            ts_clean = timestamp_str.split()[0]
            return datetime.strptime(ts_clean, '%d/%b/%Y:%H:%M:%S')
        except (ValueError, IndexError) as e:
            logger.warning(f"Errore parsing timestamp {timestamp_str}: {e}")
            return None

    def _parse_iso_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Parsa timestamp in formato ISO (per JSON logs)

        Args:
            timestamp_str: Stringa timestamp ISO

        Returns:
            datetime oggetto o None
        """
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except ValueError as e:
            logger.warning(f"Errore parsing ISO timestamp {timestamp_str}: {e}")
            return None

    def _get_log_level(self, status_code: int) -> str:
        """
        Determina il livello di log dallo status HTTP

        Args:
            status_code: Codice status HTTP

        Returns:
            Stringa livello
        """
        if status_code >= 500:
            return 'ERROR'
        elif status_code >= 400:
            return 'WARN'
        else:
            return 'INFO'

    def parse_file(self, filepath: str, encoding: str = 'utf-8') -> list:
        """
        Parsa un intero file di log Nginx

        Args:
            filepath: Percorso del file
            encoding: Encoding del file

        Returns:
            Lista di entry parsate
        """
        entries = []

        try:
            with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    parsed = self.parse_line(line)
                    if parsed:
                        parsed['_line_number'] = line_num
                        parsed['_raw_line'] = line.strip()
                        entries.append(parsed)

                    if line_num % 10000 == 0:
                        logger.info(f"Parsate {line_num} righe...")

        except IOError as e:
            logger.error(f"Errore lettura file {filepath}: {e}")
            raise

        logger.info(f"Parsing completato: {len(entries)} entry")
        return entries

    def get_user_agent_info(self, entry: Dict[str, Any]) -> Dict[str, str]:
        """
        Estrae informazioni dallo User Agent

        Args:
            entry: Entry parsata

        Returns:
            Dict con browser, OS, device
        """
        ua = entry.get('user_agent', '')

        info = {
            'browser': 'Unknown',
            'os': 'Unknown',
            'device': 'Unknown'
        }

        ua_lower = ua.lower()

        # Browser detection (semplice)
        if 'chrome' in ua_lower:
            info['browser'] = 'Chrome'
        elif 'firefox' in ua_lower:
            info['browser'] = 'Firefox'
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            info['browser'] = 'Safari'
        elif 'edge' in ua_lower:
            info['browser'] = 'Edge'
        elif 'bot' in ua_lower or 'spider' in ua_lower:
            info['browser'] = 'Bot/Crawler'

        # OS detection (semplice)
        if 'windows' in ua_lower:
            info['os'] = 'Windows'
        elif 'mac os x' in ua_lower or 'macos' in ua_lower:
            info['os'] = 'macOS'
        elif 'linux' in ua_lower:
            info['os'] = 'Linux'
        elif 'android' in ua_lower:
            info['os'] = 'Android'
        elif 'iphone' in ua_lower or 'ipad' in ua_lower:
            info['os'] = 'iOS'

        # Device detection (semplice)
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            info['device'] = 'Mobile'
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            info['device'] = 'Tablet'
        else:
            info['device'] = 'Desktop'

        return info


def main():
    """Test del parser Nginx"""
    parser = NginxLogParser()

    # Esempio riga Nginx
    test_lines = [
        '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"',
        '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "POST /api/login HTTP/1.1" 401 567 "-" "Mozilla/5.0"'
    ]

    for line in test_lines:
        result = parser.parse_line(line)
        if result:
            print(f"\nParsing riuscito per: {line[:80]}...")
            for key, value in result.items():
                if not key.startswith('_'):
                    print(f"  {key}: {value}")

            # Test user agent parsing
            ua_info = parser.get_user_agent_info(result)
            print(f"  User Agent Info: {ua_info}")
        else:
            print(f"\nParsing fallito per: {line}")


if __name__ == '__main__':
    main()
