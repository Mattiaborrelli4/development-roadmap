"""
XSS Detector
Analizzatore per vulnerabilità Cross-Site Scripting (XSS)
"""

import re
from typing import Dict, List


class XSSAnalyzer:
    """Analizzatore per pattern XSS."""

    def __init__(self, config: Dict):
        """
        Inizializza l'analizzatore.

        Args:
            config: Configurazione dei pattern da cercare
        """
        self.config = config
        self.patterns = config.get('patterns', [])
        self.severity = config.get('severity', 'HIGH')
        self.cwe = config.get('cwe', 'CWE-79')
        self.description = config.get('description', 'Cross-Site Scripting vulnerability')

    def analyze(self, files: List[Dict]) -> List[Dict]:
        """
        Analizza i file per cercare vulnerabilità XSS.

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

        if extension in {'.html', '.htm'}:
            findings.extend(self._analyze_html(file_info))

        return findings

    def _detect_language(self, extension: str) -> str:
        """Rileva il linguaggio dall'estensione."""
        lang_map = {
            '.py': 'python', '.pyw': 'python',
            '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'javascript', '.tsx': 'javascript',
            '.html': 'html', '.htm': 'html',
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

                # Verifica se è sanificato
                if self._is_sanitized(line_content):
                    continue

                finding = {
                    'type': 'xss',
                    'severity': self.severity,
                    'cwe': self.cwe,
                    'title': 'Potential XSS Vulnerability',
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
        """Analizza codice Python per XSS."""
        findings = []
        content = file_info.get('content', '')

        # Pattern Python specifici
        py_patterns = [
            # HttpResponse con input non sanitizzato
            (r'HttpResponse\([^)]*request\.(?:GET|POST|META)[^)]*\)', 'http_response_input'),
            # f-string con HTML e input utente
            (r'(?:return|HttpResponse)\s*\(\s*f["\'][^"\']*<[^>]*>\{[^}]*request\.(?:GET|POST)[^}]*\}', 'fstring_html_userinput'),
            # render con input diretto
            (r'render\(.*context=\{[^}]*request\.(?:GET|POST)[^}]*\}', 'render_direct_input'),
        ]

        for pattern, pattern_name in py_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    if not self._is_sanitized(line_content):
                        finding = {
                            'type': 'xss',
                            'severity': self.severity,
                            'cwe': self.cwe,
                            'title': 'Potential XSS (Python)',
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
        """Analizza codice JavaScript per XSS."""
        findings = []
        content = file_info.get('content', '')

        # Pattern JavaScript pericolosi
        js_patterns = [
            (r'innerHTML\s*=\s*[^;]+', 'innerHTML_assignment'),
            (r'document\.write\(', 'document_write_call'),
            (r'\.html\([^)]*\)', 'jquery_html'),
            (r'\.append\([^)]*<[^>]+>', 'jquery_append_html'),
            (r'eval\(', 'eval_call'),
            (r'dangerouslySetInnerHTML', 'react_dangerous_innerHTML'),
            (r'insertAdjacentHTML', 'insert_adjacent_html'),
        ]

        for pattern, pattern_name in js_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    finding = {
                        'type': 'xss',
                        'severity': self.severity,
                        'cwe': self.cwe,
                        'title': 'Potential XSS (JavaScript)',
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

    def _analyze_html(self, file_info: Dict) -> List[Dict]:
        """Analizza file HTML per XSS."""
        findings = []
        content = file_info.get('content', '')

        # Pattern HTML pericolosi
        html_patterns = [
            # Script inline con variabili
            (r'<script[^>]*>\s*(?:var|let|const)\s+\w+\s*=\s*[^;]+\s*;', 'script_inline_var'),
            # Event handlers inline
            (r'on\w+\s*=\s*["\'][^"\']*document\.location[^"\']*["\']', 'inline_event_handler'),
            # Expression non quote
            (r'<[^>]+expression\s*\(', 'css_expression'),
        ]

        for pattern, pattern_name in html_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    finding = {
                        'type': 'xss',
                        'severity': 'MEDIUM',
                        'cwe': self.cwe,
                        'title': 'Potential XSS (HTML)',
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

    def _is_sanitized(self, line_content: str) -> bool:
        """Verifica se l'output sembra sanitizzato."""
        safe_indicators = [
            'escape',
            'sanitize',
            'clean',
            'filter',
            'encode',
            'strip',
            'htmlspecialchars',
            'escapejs',
            'textContent',  # JavaScript
            '.innerText',   # JavaScript
            '|escape',      # Django/Jinja
            '|safe',        # NOTA: questo indica che NON è sanitizzato!
        ]

        line_lower = line_content.lower()

        # Controlla indicatori di sanitizzazione
        for indicator in safe_indicators:
            if indicator in line_lower and '|safe' not in line_lower:
                return True

        return False

    def _get_recommendation(self) -> str:
        """Restituisce raccomandazioni per fix."""
        return (
            "Sanifica sempre l'input dell'utente prima di output HTML:\n"
            "  Python: html.escape(user_input)\n"
            "  JavaScript: element.textContent = user_input (non innerHTML)\n"
            "  Templates: {{ user_input|escape }}\n"
            "  PHP: htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8')\n"
            "Usa sempre Content Security Policy (CSP) come difesa aggiuntiva."
        )
