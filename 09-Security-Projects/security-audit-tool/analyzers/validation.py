"""
Input Validation Analyzer
Analizzatore per mancanza di validazione dell'input
"""

import re
from typing import Dict, List


class ValidationAnalyzer:
    """Analizzatore per validazione input."""

    def __init__(self, config: Dict):
        """
        Inizizlizza l'analizzatore.

        Args:
            config: Configurazione dei pattern da cercare
        """
        self.config = config
        self.patterns = config.get('patterns', [])
        self.severity = config.get('severity', 'MEDIUM')
        self.cwe = config.get('cwe', 'CWE-20')
        self.description = config.get('description', 'Missing input validation')

    def analyze(self, files: List[Dict]) -> List[Dict]:
        """
        Analizza i file per cercare mancanza di validazione.

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

                # Verifica se c'è validazione
                if self._has_validation(line_content):
                    continue

                finding = {
                    'type': 'missing_validation',
                    'severity': self.severity,
                    'cwe': self.cwe,
                    'title': 'Missing Input Validation',
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
        """Analizza codice Python per mancanza di validazione."""
        findings = []
        content = file_info.get('content', '')

        # Pattern per input utente non validato
        py_patterns = [
            # request.GET/POST senza validazione
            (r'request\.(?:GET|POST|FILES)\[[^\]]+\](?!\s*\.(?:validate|sanitize|clean|escape|strip))', 'unvalidated_request'),
            # Flask request.form senza validazione
            (r'flask\.request\.form\[', 'unvalidated_form'),
            # input() senza validazione (Python 3)
            (r'input\([^\)]*\)(?!\s*\.(?:strip|validate))', 'unvalidated_input'),
        ]

        for pattern, pattern_name in py_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    if not self._has_validation(line_content):
                        finding = {
                            'type': 'missing_validation',
                            'severity': 'MEDIUM',
                            'cwe': self.cwe,
                            'title': 'Missing Input Validation (Python)',
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
        """Analizza codice JavaScript per mancanza di validazione."""
        findings = []
        content = file_info.get('content')

        # Pattern JavaScript per input non validato
        js_patterns = [
            # req.query, req.body, req.params senza validazione
            (r'req\.(?:query|body|params)\.\w+(?!\s*\.(?:validate|sanitize|trim|escape))', 'unvalidated_request'),
            # document value senza validazione
            (r'document\.getElementById\([^\)]+\)\.value(?!\s*\.(?:validate|trim))', 'unvalidated_input'),
            # jQuery val() senza validazione
            (r'\$\([^\)]+\)\.val\(\)(?!\s*\.(?:validate|trim))', 'unvalidated_jquery'),
        ]

        for pattern, pattern_name in js_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    if not self._has_validation(line_content):
                        finding = {
                            'type': 'missing_validation',
                            'severity': 'MEDIUM',
                            'cwe': self.cwe,
                            'title': 'Missing Input Validation (JavaScript)',
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

    def _has_validation(self, line_content: str) -> bool:
        """Verifica se la riga mostra validazione."""
        validation_indicators = [
            '.validate(',
            '.sanitize(',
            '.clean(',
            '.escape(',
            '.strip()',
            '.trim()',
            'validator.',
            'check(',
            'is_valid',
            'ensure',
            'verify',
            'assert',
            'int(',  # Type conversion
            'float(',
            'str(',
            '|int',  # Django template filter
            '|float',
            '|length',
            '|safe',  # NOTA: safe significa NON sanitizzato
        ]

        line_lower = line_content.lower()

        for indicator in validation_indicators:
            if indicator in line_lower and '|safe' not in line_lower:
                return True

        return False

    def _get_recommendation(self) -> str:
        """Restituisce raccomandazioni per fix."""
        return (
            "Valida sempre l'input dell'utente:\n"
            "  - Verifica tipo (int, str, email, URL)\n"
            "  - Verifica lunghezza (min, max)\n"
            "  - Verifica formato (regex per email, telefono, etc.)\n"
            "  - Sanifica/escape i dati prima dell'uso\n"
            "  - Usa whitelist invece di blacklist\n"
            "Esempio Python: user_id = int(request.GET.get('id', 0))\n"
            "Esempio JavaScript: const email = validator.isEmail(req.body.email)"
        )
