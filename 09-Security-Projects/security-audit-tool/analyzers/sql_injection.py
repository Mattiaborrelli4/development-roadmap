"""
SQL Injection Analyzer
Analizzatore per vulnerabilità di SQL Injection
"""

import re
from typing import Dict, List, Optional
from parsers.ast_parser import ASTParser


class SQLInjectionAnalyzer:
    """Analizzatore per pattern di SQL Injection."""

    def __init__(self, config: Dict):
        """
        Inizializza l'analizzatore.

        Args:
            config: Configurazione dei pattern da cercare
        """
        self.config = config
        self.patterns = config.get('patterns', [])
        self.severity = config.get('severity', 'HIGH')
        self.cwe = config.get('cwe', 'CWE-89')
        self.description = config.get('description', 'SQL Injection vulnerability')
        self.ast_parser = ASTParser()

    def analyze(self, files: List[Dict]) -> List[Dict]:
        """
        Analizza i file per cercare vulnerabilità SQL Injection.

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

        # Analisi AST per Python
        if extension in {'.py', '.pyw'}:
            findings.extend(self._analyze_python_ast(file_info))

        # Analisi per JavaScript
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

                # Verifica se è una query sicura (parametrizzata)
                if self._is_safe_query(file_info, line_number, line_content):
                    continue

                finding = {
                    'type': 'sql_injection',
                    'severity': self.severity,
                    'cwe': self.cwe,
                    'title': 'Potential SQL Injection',
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
            # Pattern regex invalido, ignora
            pass

        return findings

    def _analyze_python_ast(self, file_info: Dict) -> List[Dict]:
        """Analizza codice Python tramite AST."""
        findings = []

        ast_info = self.ast_parser.parse(file_info)
        if not ast_info:
            return findings

        # Cerca operazioni su stringhe
        for string_op in ast_info.get('strings', []):
            line = string_op.get('line')
            context = string_op.get('context', '')

            # Verifica se contiene execute/query
            if any(keyword in context.lower() for keyword in ['execute', 'query', 'select', 'insert', 'update', 'delete']):
                if not self._is_safe_query(file_info, line, context):
                    finding = {
                        'type': 'sql_injection',
                        'severity': self.severity,
                        'cwe': self.cwe,
                        'title': 'Potential SQL Injection (String Operation)',
                        'description': f'{self.description} - {string_op.get("type")} detected',
                        'file': file_info.get('path'),
                        'line': line,
                        'code': context.strip(),
                        'pattern_matched': f'{string_op.get("type")}_operation',
                        'recommendation': self._get_recommendation(),
                        'references': self.config.get('references', [])
                    }
                    findings.append(finding)

        return findings

    def _analyze_javascript(self, file_info: Dict) -> List[Dict]:
        """Analizza codice JavaScript."""
        findings = []
        content = file_info.get('content', '')

        # Pattern JavaScript specifici
        js_patterns = [
            # Template literals con query
            (r'(?:query|execute)\(`[^`]*\$\{[^}]+\}[^`]*`', 'template_literal_query'),
            # Concatenazione stringhe con query
            (r'(?:query|execute)\s*\(\s*["\'][^"\']*["\']\s*\+', 'concatenated_query'),
            # db.query con concatenazione
            (r'db\.(?:query|execute)\([^)]*\+[^)]*\)', 'db_query_concat'),
        ]

        for pattern, pattern_name in js_patterns:
            try:
                regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)

                for match in regex.finditer(content):
                    line_number = content[:match.start()].count('\n') + 1
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ''

                    finding = {
                        'type': 'sql_injection',
                        'severity': self.severity,
                        'cwe': self.cwe,
                        'title': 'Potential SQL Injection (JavaScript)',
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

    def _is_safe_query(self, file_info: Dict, line_number: int, line_content: str) -> bool:
        """Verifica se una query sembra sicura."""
        # Placeholder sicuri
        safe_indicators = [
            '%s', '%d',  # Python
            '?',        # JDBC
            '$1', '$2',  # PostgreSQL
            ':1', ':2',  # PostgreSQL
            '@p',        # ADO.NET
            'param',
            'bind',
            'escape',
            'quote'
        ]

        line_lower = line_content.lower()

        # Verifica placeholder
        for indicator in safe_indicators:
            if indicator in line_lower:
                return True

        # Verifica tupla/lista come secondo argomento
        if any(x in line_content for x in [', (', ', [', ',\n(', ',\n[']):
            return True

        return False

    def _get_recommendation(self) -> str:
        """Restituisce raccomandazioni per fix."""
        return (
            "Usa query parametrizzate invece di concatenare stringhe:\n"
            "  Python: cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))\n"
            "  JavaScript: db.query('SELECT * FROM users WHERE id=?', [userId])\n"
            "  PHP: $stmt = $pdo->prepare('SELECT * FROM users WHERE id=:id');\n"
            "Non concatenare mai input utente direttamente nella query SQL."
        )
