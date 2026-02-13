"""
Apache Log Parser
Analizza log in formato Apache Common Log Format (CLF) e Combined Log Format

 Educational - Log Parser Techniques:
 - Regex compilation per performance
 - Named capture groups per estrazione dati
 - Gestione errori nel parsing
"""

import re
from datetime import datetime
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class ApacheLogParser:
    """
    Parser per log Apache (Common e Combined Log Format)

    Formati supportati:
    - Common Log Format (CLF)
    - Combined Log Format

    Esempio CLF:
    127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326

    Esempio Combined:
    127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326 "http://example.com" "Mozilla/5.0"
    """

    # Pattern regex per Common Log Format
    CLF_PATTERN = re.compile(
        r'^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
        r'(?P<identity>\S+)\s+'
        r'(?P<userid>\S+)\s+'
        r'\[(?P<timestamp>[^\]]+)\]\s+'
        r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+'
        r'(?P<status>\d+)\s+'
        r'(?P<size>\d+)$'
    )

    # Pattern regex per Combined Log Format
    COMBINED_PATTERN = re.compile(
        r'^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
        r'(?P<identity>\S+)\s+'
        r'(?P<userid>\S+)\s+'
        r'\[(?P<timestamp>[^\]]+)\]\s+'
        r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+'
        r'(?P<status>\d+)\s+'
        r'(?P<size>\d+)\s+'
        r'"(?P<referer>[^"]*)"\s+'
        r'"(?P<user_agent>[^"]*)"$'
    )

    def __init__(self, use_combined: bool = True):
        """
        Inizializza il parser Apache

        Args:
            use_combined: Se True usa Combined Log Format, altrimenti Common Log Format
        """
        self.use_combined = use_combined
        self.pattern = self.COMBINED_PATTERN if use_combined else self.CLF_PATTERN
        logger.info(f"Apache Log Parser inizializzato con formato {'Combined' if use_combined else 'CLF'}")

    def parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parsa una riga di log Apache

        Args:
            line: Riga di log da parsare

        Returns:
            Dict con i campi parsati o None se la riga non matcha il pattern
        """
        if not line or not line.strip():
            return None

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

        # Aggiungi campo livello basato sullo status code
        data['level'] = self._get_log_level(data['status'])

        # Aggiungi campo messaggio per compatibilità
        data['message'] = f"{data['method']} {data['path']} - {data['status']}"

        # Campi opzionali per Combined format
        if self.use_combined:
            if not data.get('referer'):
                data['referer'] = '-'
            if not data.get('user_agent'):
                data['user_agent'] = '-'
        else:
            data['referer'] = '-'
            data['user_agent'] = '-'

        return data

    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Parsa il timestamp Apache

        Format: 10/Oct/2023:13:55:36 +0000

        Args:
            timestamp_str: Stringa timestamp

        Returns:
            datetime oggetto o None
        """
        try:
            # Rimuovi timezone per semplicità
            ts_clean = timestamp_str.split()[0]
            return datetime.strptime(ts_clean, '%d/%b/%Y:%H:%M:%S')
        except (ValueError, IndexError) as e:
            logger.warning(f"Errore parsing timestamp {timestamp_str}: {e}")
            return None

    def _get_log_level(self, status_code: int) -> str:
        """
        Determina il livello di log basato sullo status HTTP

        Args:
            status_code: Codice status HTTP

        Returns:
            Stringa livello (ERROR, WARN, INFO)
        """
        if status_code >= 500:
            return 'ERROR'
        elif status_code >= 400:
            return 'WARN'
        else:
            return 'INFO'

    def parse_file(self, filepath: str, encoding: str = 'utf-8') -> list:
        """
        Parsa un intero file di log

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

                    # Log progress ogni 10000 righe
                    if line_num % 10000 == 0:
                        logger.info(f"Parsate {line_num} righe...")

        except IOError as e:
            logger.error(f"Errore lettura file {filepath}: {e}")
            raise

        logger.info(f"Parsing completato: {len(entries)} entry parsate")
        return entries

    def is_error(self, entry: Dict[str, Any]) -> bool:
        """
        Verifica se l'entry è un errore

        Args:
            entry: Entry parsata

        Returns:
            True se è un errore (4xx o 5xx)
        """
        return entry.get('status', 0) >= 400

    def get_error_category(self, entry: Dict[str, Any]) -> str:
        """
        Categorizza l'errore

        Args:
            entry: Entry parsata

        Returns:
            Categoria errore
        """
        status = entry.get('status', 0)

        if status >= 500:
            return 'Server Error'
        elif status >= 400:
            return 'Client Error'
        elif status >= 300:
            return 'Redirect'
        else:
            return 'Success'


def main():
    """Test del parser Apache"""
    parser = ApacheLogParser(use_combined=True)

    # Esempio di riga Combined
    test_line = '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326 "http://example.com" "Mozilla/5.0"'

    result = parser.parse_line(test_line)
    if result:
        print("Parsing riuscito:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("Parsing fallito")


if __name__ == '__main__':
    main()
