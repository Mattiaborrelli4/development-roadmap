"""
Custom Log Parser
Analizza log con formati custom definiti dall'utente

Educational - Log Parser Techniques:
- Pattern flessibili e customizzabili
- Config-driven parsing
- Gestione di molteplici formati
- Configurazione da YAML
"""

import re
from datetime import datetime
from typing import Dict, Optional, Any, List
import logging
import yaml

logger = logging.getLogger(__name__)


class CustomLogParser:
    """
    Parser per log con formati custom

    Supporta:
    - Formati definiti da pattern regex
    - Configurazione da file YAML
    - Molteplici formati contemporaneamente
    """

    # Formati predefiniti
    DEFAULT_FORMATS = {
        'timestamp_level_module_message': re.compile(
            r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[.,]\d{3})\s+'
            r'\[(?P<level>\w+)\]\s+'
            r'\[(?P<module>[^\]]+)\]\s+'
            r'(?P<message>.*)$'
        ),
        'level_timestamp_message': re.compile(
            r'^(?P<level>\w+)\s+'
            r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
            r'(?P<message>.*)$'
        ),
        'bracket_timestamp_level_message': re.compile(
            r'^\[(?P<timestamp>[^\]]+)\]\s+'
            r'(?P<level>\w+)\s+'
            r'(?P<message>.*)$'
        ),
        'simple_timestamp_level_message': re.compile(
            r'^(?P<timestamp>\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})\s+'
            r'(?P<level>\w+)\s+'
            r'(?P<message>.*)$'
        ),
    }

    TIMESTAMP_FORMATS = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S,%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S%z',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%d/%b/%Y:%H:%M:%S',
        '%b %d %H:%M:%S',
        '%Y %b %d %H:%M:%S',
    ]

    def __init__(self, config_path: Optional[str] = None):
        """
        Inizializza il parser custom

        Args:
            config_path: Percorso file config YAML (opzionale)
        """
        self.patterns = {}
        self.pattern_names = []

        # Carica formati predefiniti
        for name, pattern in self.DEFAULT_FORMATS.items():
            self.add_pattern(name, pattern)

        # Carica da config se specificato
        if config_path:
            self.load_config(config_path)

        logger.info(f"Custom Log Parser inizializzato con {len(self.patterns)} pattern")

    def add_pattern(self, name: str, pattern: re.Pattern):
        """
        Aggiunge un pattern di parsing

        Args:
            name: Nome del pattern
            pattern: Pattern regex compilato
        """
        self.patterns[name] = pattern
        self.pattern_names.append(name)
        logger.debug(f"Aggiunto pattern: {name}")

    def load_config(self, config_path: str):
        """
        Carica pattern da file YAML

        Args:
            config_path: Percorso file config
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            if 'formats' in config:
                for name, pattern_str in config['formats'].items():
                    try:
                        pattern = re.compile(pattern_str)
                        self.add_pattern(f"custom_{name}", pattern)
                    except re.error as e:
                        logger.error(f"Pattern non valido '{name}': {e}")

            logger.info(f"Caricati {len(config.get('formats', {}))} pattern da {config_path}")

        except IOError as e:
            logger.error(f"Errore lettura config {config_path}: {e}")
            raise

    def parse_line(self, line: str, pattern_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Parsa una riga di log

        Prova tutti i pattern fino a che uno non matcha

        Args:
            line: Riga di log
            pattern_name: Nome pattern specifico (opzionale)

        Returns:
            Dict con campi parsati o None
        """
        if not line or not line.strip():
            return None

        # Se specificato, usa solo quel pattern
        if pattern_name and pattern_name in self.patterns:
            return self._parse_with_pattern(line, self.patterns[pattern_name])

        # Altrimenti prova tutti i pattern
        for name, pattern in self.patterns.items():
            result = self._parse_with_pattern(line, pattern)
            if result:
                result['_pattern_used'] = name
                return result

        logger.debug(f"Nessun pattern match per: {line[:100]}...")
        return None

    def _parse_with_pattern(self, line: str, pattern: re.Pattern) -> Optional[Dict[str, Any]]:
        """
        Parsa con uno specifico pattern

        Args:
            line: Riga di log
            pattern: Pattern regex

        Returns:
            Dict o None
        """
        match = pattern.match(line.strip())
        if not match:
            return None

        data = match.groupdict()

        # Parsing timestamp se presente
        if 'timestamp' in data:
            data['timestamp_parsed'] = self._parse_timestamp(data['timestamp'])

        # Normalizza livello
        if 'level' in data:
            data['level'] = data['level'].upper()

        # Aggiungi raw line
        data['_raw_line'] = line.strip()

        return data

    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Prova molteplici formati per il timestamp

        Args:
            timestamp_str: Stringa timestamp

        Returns:
            datetime oggetto o None
        """
        # Cleanup stringa
        ts_clean = timestamp_str.strip()

        for fmt in self.TIMESTAMP_FORMATS:
            try:
                return datetime.strptime(ts_clean, fmt)
            except ValueError:
                continue

        logger.debug(f"Impossibile parsare timestamp: {ts_clean}")
        return None

    def parse_file(self, filepath: str, encoding: str = 'utf-8',
                   pattern_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Parsa un intero file

        Args:
            filepath: Percorso file
            encoding: Encoding file
            pattern_name: Pattern specifico (opzionale)

        Returns:
            Lista entry parsate
        """
        entries = []

        try:
            with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    parsed = self.parse_line(line, pattern_name)
                    if parsed:
                        parsed['_line_number'] = line_num
                        entries.append(parsed)

                    if line_num % 10000 == 0:
                        logger.info(f"Parsate {line_num} righe...")

        except IOError as e:
            logger.error(f"Errore lettura file {filepath}: {e}")
            raise

        logger.info(f"Parsing completato: {len(entries)} entry")
        return entries

    def detect_format(self, sample_lines: List[str]) -> str:
        """
        Rileva il formato automaticamente da sample lines

        Args:
            sample_lines: Lista righe di esempio

        Returns:
            Nome del pattern migliore
        """
        pattern_counts = {name: 0 for name in self.pattern_names}

        for line in sample_lines:
            for name, pattern in self.patterns.items():
                if pattern.match(line.strip()):
                    pattern_counts[name] += 1

        # Trova il pattern con più match
        best_pattern = max(pattern_counts.items(), key=lambda x: x[1])

        logger.info(f"Formato rilevato: {best_pattern[0]} ({best_pattern[1]} match su {len(sample_lines)})")

        return best_pattern[0]

    def is_error(self, entry: Dict[str, Any]) -> bool:
        """
        Verifica se entry è un errore

        Args:
            entry: Entry parsata

        Returns:
            True se è errore
        """
        level = entry.get('level', '').upper()
        return level in ('ERROR', 'FATAL', 'CRITICAL')

    def is_warning(self, entry: Dict[str, Any]) -> bool:
        """
        Verifica se entry è un warning

        Args:
            entry: Entry parsata

        Returns:
            True se è warning
        """
        level = entry.get('level', '').upper()
        return level in ('WARN', 'WARNING')


class ApplicationLogParser(CustomLogParser):
    """
    Parser specializzato per log di applicazioni Python

    Supporta il formato standard di logging Python
    """

    PYTHON_LOG_PATTERN = re.compile(
        r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+'
        r'(?P<level>\w+)\s+'
        r'(?P<logger>\S+)\s+'
        r'(?P<module>\S+)\s+'
        r'(?P<message>.*)$'
    )

    def __init__(self):
        super().__init__()
        self.add_pattern('python_app', self.PYTHON_LOG_PATTERN)


class JavaLogParser(CustomLogParser):
    """
    Parser per log Java (Log4j, Logback)
    """

    JAVA_LOG_PATTERN = re.compile(
        r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[.,]\d{3})\s+'
        r'\[(?P<thread>[^\]]+)\]\s+'
        r'(?P<level>\w+)\s+'
        r'(?P<logger>\S+)\s+-\s+'
        r'(?P<message>.*)$'
    )

    def __init__(self):
        super().__init__()
        self.add_pattern('java_log', self.JAVA_LOG_PATTERN)


def main():
    """Test del parser custom"""
    parser = CustomLogParser()

    # Esempi di righe
    test_lines = [
        '2024-01-15 10:30:45 [INFO] [main] Application started',
        '2024-01-15 10:30:46 [ERROR] [database] Connection failed',
        'ERROR 2024-01-15 10:30:47 Something went wrong',
        '[2024-01-15 10:30:48] WARN Memory usage high',
        '01/15/2024 10:30:49 DEBUG Processing request',
    ]

    print("Test parsing righe custom:\n")
    for line in test_lines:
        result = parser.parse_line(line)
        if result:
            print(f"✓ {line}")
            print(f"  Pattern: {result.get('_pattern_used', 'N/A')}")
            print(f"  Level: {result.get('level')}")
            print(f"  Message: {result.get('message', 'N/A')[:50]}...")
            print()
        else:
            print(f"✗ {line}")

    # Test auto-detect format
    print("\nAuto-detect formato:")
    detected = parser.detect_format(test_lines)
    print(f"Formato migliore: {detected}")


if __name__ == '__main__':
    main()
