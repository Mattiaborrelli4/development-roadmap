"""
Credentials Analyzer
Analizzatore per credenziali hardcoded e segreti esposti
"""

import re
from typing import Dict, List


class CredentialsAnalyzer:
    """Analizzatore per credenziali hardcoded."""

    def __init__(self, config: Dict):
        """
        Inizializza l'analizzatore.

        Args:
            config: Configurazione dei pattern da cercare
        """
        self.config = config
        self.patterns = config.get('patterns', [])
        self.severity = config.get('severity', 'CRITICAL')
        self.cwe = config.get('cwe', 'CWE-798')
        self.description = config.get('description', 'Hardcoded credentials')

    def analyze(self, files: List[Dict]) -> List[Dict]:
        """
        Analizza i file per cercare credenziali hardcoded.

        Args:
            files: Lista di file da analizzare

        Returns:
            Lista di credenziali trovate
        """
        findings = []

        for file_info in files:
            findings.extend(self._analyze_file(file_info))

        return findings

    def _analyze_file(self, file_info: Dict) -> List[Dict]:
        """Analizza un singolo file."""
        findings = []
        content = file_info.get('content', '')

        if not content:
            return findings

        # Ottieni pattern
        for pattern_config in self.patterns:
            language = pattern_config.get('language', 'all')
            patterns = pattern_config.get('patterns', [])

            for pattern in patterns:
                findings.extend(self._check_pattern(content, pattern, file_info))

        return findings

    def _check_pattern(self, content: str, pattern: str, file_info: Dict) -> List[Dict]:
        """Verifica un pattern regex nel contenuto."""
        findings = []

        try:
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

            for match in regex.finditer(content):
                line_number = content[:match.start()].count('\n') + 1
                lines = content.split('\n')
                line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                # Filtra falsi positivi comuni
                if self._is_false_positive(line_content, match.group(0)):
                    continue

                finding = {
                    'type': 'hardcoded_credentials',
                    'severity': self.severity,
                    'cwe': self.cwe,
                    'title': 'Hardcoded Credential Detected',
                    'description': self.description,
                    'file': file_info.get('path'),
                    'line': line_number,
                    'code': self._sanitize_code_output(line_content.strip()),
                    'pattern_matched': pattern,
                    'recommendation': self._get_recommendation(),
                    'references': self.config.get('references', [])
                }
                findings.append(finding)

        except re.error:
            pass

        return findings

    def _is_false_positive(self, line_content: str, match: str) -> bool:
        """
        Filtra falsi positivi comuni.
        """
        # Indicatori di uso sicuro di variabili d'ambiente
        safe_patterns = [
            r'os\.environ\.get',
            r'os\.getenv',
            r'os\.env\[',
            r'environ\.get',
            r'process\.env\.',
            r'\.env\.',
            r'config\.',
            r'Config\.get',
            r'getenv\(',
            r'KEY_HERE',
            r'YOUR_',
            r'<INSERT',
            r'xxx',
            r'example\.',
            r'test_',
            r'dummy_',
            r'placeholder',
            r'\.env\.example',
            r'config\.example',
        ]

        line_lower = line_content.lower()

        for safe_pattern in safe_patterns:
            if re.search(safe_pattern, line_lower):
                return True

        # Stringhe troppo corte (probabilmente non vere password)
        match_stripped = match.strip('\'"')
        if len(match_stripped) < 4:
            return True

        # Valori ovvi di esempio
        example_values = [
            'password', 'pass', 'secret', 'key', 'token',
            '123', 'test', 'demo', 'example', 'sample',
            'changeme', 'changeit', 'admin', 'user',
            'asdf', 'qwerty', 'password123'
        ]

        if match_stripped.lower() in example_values:
            return True

        return False

    def _sanitize_code_output(self, code: str) -> str:
        """
        Sanitizza l'output del codice per non esporre credenziali nel report.
        """
        # Maschera valori che sembrano credenziali
        patterns_to_mask = [
            (r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', r'\1 = "*****"'),
            (r'(api_key|apikey|api-key)\s*=\s*["\'][^"\']+["\']', r'\1 = "*****"'),
            (r'(secret|secret_key)\s*=\s*["\'][^"\']+["\']', r'\1 = "*****"'),
            (r'(token|access_token)\s*=\s*["\'][^"\']+["\']', r'\1 = "*****"'),
        ]

        sanitized = code
        for pattern, replacement in patterns_to_mask:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    def _get_recommendation(self) -> str:
        """Restituisce raccomandazioni per fix."""
        return (
            "Non hardcoded mai credenziali nel codice:\n"
            "  - Usa variabili d'ambiente (os.environ in Python, process.env in Node.js)\n"
            "  - Usa file di configurazione NON committati (.env)\n"
            "  - Usa secret management service (AWS Secrets Manager, HashiCorp Vault)\n"
            "  - Usa config Injection o CI/CD secrets\n"
            "Aggiungi .env a .gitignore per evitare commit accidentali."
        )
