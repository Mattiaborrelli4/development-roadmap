"""
Cryptography Analyzer
Analizzatore per crittografia debole o insicura
"""

import re
from typing import Dict, List


class CryptoAnalyzer:
    """Analizzatore per crittografia insicura."""

    def __init__(self, config: Dict):
        """
        Inizializza l'analizzatore.

        Args:
            config: Configurazione dei pattern da cercare
        """
        self.config = config
        self.patterns = config.get('patterns', [])
        self.severity = config.get('severity', 'MEDIUM')
        self.cwe = config.get('cwe', 'CWE-327')
        self.description = config.get('description', 'Weak cryptography')

    def analyze(self, files: List[Dict]) -> List[Dict]:
        """
        Analizza i file per cercare crittografia debole.

        Args:
            files: Lista di file da analizzare

        Returns:
            Lista di vulnerabilità trovate
        """
        findings = []

        for file_info in files:
            findings.extend(self._analyze_file(file_info))

        return findings

    def _analyze_file(self, file_info: Dict) -> List[Dict]:
        """Analizza un singolo file."""
        findings = []
        content = file_info.get('content', '')
        extension = file_info.get('extension', '')

        if not content:
            return findings

        # Identifica il linguaggio
        language = self._detect_language(extension)

        # Ottieni pattern per questo linguaggio
        lang_patterns = self._get_patterns_for_language(language)

        # Analizza con regex
        for pattern_config in lang_patterns:
            for pattern in pattern_config.get('patterns', []):
                findings.extend(self._check_pattern(content, pattern, file_info))

        # Analisi specifica per linguaggio
        if extension in {'.py', '.pyw'}:
            findings.extend(self._analyze_python(file_info))

        if extension in {'.js', '.jsx', '.ts', '.tsx'}:
            findings.extend(self._analyze_javascript(file_info))

        return findings

    def _detect_language(self, extension: str) -> str:
        """Rileva il linguaggio dall'estensione."""
        lang_map = {
            '.py': 'python', '.pyw': 'python',
            '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'javascript', '.tsx': 'javascript',
            '.php': 'php', '.phtml': 'php'
        }
        return lang_map.get(extension.lower(), 'unknown')

    def _get_patterns_for_language(self, language: str) -> List[Dict]:
        """Ottieni i pattern per un linguaggio specifico."""
        for pattern_config in self.patterns:
            if pattern_config.get('language') in [language, 'all']:
                return [pattern_config]
        return []

    def _check_pattern(self, content: str, pattern: str, file_info: Dict) -> List[Dict]:
        """Verifica un pattern regex nel contenuto."""
        findings = []

        try:
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

            for match in regex.finditer(content):
                line_number = content[:match.start()].count('\n') + 1
                lines = content.split('\n')
                line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                finding = {
                    'type': 'weak_cryptography',
                    'severity': self.severity,
                    'cwe': self.cwe,
                    'title': 'Weak Cryptography Detected',
                    'description': self.description,
                    'file': file_info.get('path'),
                    'line': line_number,
                    'code': line_content.strip(),
                    'pattern_matched': pattern,
                    'recommendation': self._get_recommendation(),
                    'references': self.config.get('references', [])
                }
                findings.append(finding)

        except re.error:
            pass

        return findings

    def _analyze_python(self, file_info: Dict) -> List[Dict]:
        """Analizza codice Python per crittografia debole."""
        findings = []
        content = file_info.get('content', '')

        # Pattern Python specifici
        py_patterns = [
            # Import di algoritmi deboli
            (r'from\s+Crypto\.Cipher\s+import\s+DES', 'DES import'),
            (r'from\s+Crypto\.Cipher\s+import\s+ARC4', 'RC4 import'),
            (r'from\s+Crypto\.Cipher\s+import\s+(?:DES|ARC4|Blowfish)', 'weak cipher import'),
            # hashlib con algoritmi deboli
            (r'hashlib\.md5\(', 'MD5 hash'),
            (r'hashlib\.sha1\(', 'SHA1 hash'),
            # Import diretti
            (r'import\s+md5', 'md5 module import'),
            (r'import\s+sha', 'sha module import'),
            # Keys troppo corte
            (r'key\s*=\s*["\'][^"\']{1,16}["\']', 'short encryption key'),
        ]

        for pattern, pattern_name in py_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    finding = {
                        'type': 'weak_cryptography',
                        'severity': self.severity,
                        'cwe': self.cwe,
                        'title': 'Weak Cryptography (Python)',
                        'description': f'{self.description} - {pattern_name}',
                        'file': file_info.get('path'),
                        'line': line_number,
                        'code': line_content.strip(),
                        'pattern_matched': pattern_name,
                        'recommendation': self._get_recommendation(),
                        'references': self.config.get('references', [])
                    }
                    findings.append(finding)

            except re.error:
                pass

        return findings

    def _analyze_javascript(self, file_info: Dict) -> List[Dict]:
        """Analizza codice JavaScript per crittografia debole."""
        findings = []
        content = file_info.get('content', '')

        # Pattern JavaScript specifici
        js_patterns = [
            # MD5 con crypto
            (r"crypto\.createHash\(['\"]md5['\"]", 'MD5 hash'),
            (r"crypto\.createHash\(['\"]sha1['\"]", 'SHA1 hash'),
            # Math.random() per sicurezza
            (r"Math\.random\(\)", 'insecure random'),
        ]

        for pattern, pattern_name in js_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    # Verifica se Math.random è usato per scopi di sicurezza
                    if 'random' in pattern_name:
                        if not self._is_security_context(line_content):
                            continue

                    finding = {
                        'type': 'weak_cryptography',
                        'severity': 'LOW',
                        'cwe': 'CWE-330',
                        'title': 'Weak Cryptography (JavaScript)',
                        'description': f'{self.description} - {pattern_name}',
                        'file': file_info.get('path'),
                        'line': line_number,
                        'code': line_content.strip(),
                        'pattern_matched': pattern_name,
                        'recommendation': self._get_recommendation(),
                        'references': self.config.get('references', [])
                    }
                    findings.append(finding)

            except re.error:
                pass

        return findings

    def _is_security_context(self, line_content: str) -> bool:
        """Verifica se l'uso di Math.random è in un contesto di sicurezza."""
        security_keywords = [
            'token', 'password', 'key', 'secret', 'session', 'nonce',
            'salt', 'iv', 'cipher', 'crypt', 'randombytes', 'uuid',
            'otp', 'auth', 'csrf'
        ]

        line_lower = line_content.lower()

        for keyword in security_keywords:
            if keyword in line_lower:
                return True

        return False

    def _get_recommendation(self) -> str:
        """Restituisce raccomandazioni per fix."""
        return (
            "Usa algoritmi crittografici sicuri:\n"
            "  Hash: SHA-256, SHA-384, SHA-512 (non MD5, SHA1)\n"
            "  Encryption: AES-256-GCM (non DES, RC4, Blowfish)\n"
            "  Random: secrets.token_bytes() in Python, crypto.randomBytes() in Node.js\n"
            "  Non usare MAI Math.random() per scopi di sicurezza\n"
            "Consulta: NIST Cryptographic Standards"
        )
