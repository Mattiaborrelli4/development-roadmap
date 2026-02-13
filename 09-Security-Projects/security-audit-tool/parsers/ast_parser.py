"""
AST Parser Module
Modulo per il parsing di codice sorgente tramite Abstract Syntax Tree.

Supporta: Python (ast), JavaScript (esprima-like logic)
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import json


class ASTNode:
    """Rappresenta un nodo nell'AST."""

    def __init__(self, node_type: str, line_number: int, **kwargs):
        self.node_type = node_type
        self.line_number = line_number
        self.attributes = kwargs
        self.children = []

    def add_child(self, child: 'ASTNode'):
        """Aggiunge un nodo figlio."""
        self.children.append(child)

    def to_dict(self) -> Dict:
        """Converte il nodo in dizionario."""
        return {
            'type': self.node_type,
            'line': self.line_number,
            'attributes': self.attributes,
            'children': [c.to_dict() for c in self.children]
        }


class PythonASTParser:
    """Parser AST per codice Python."""

    def __init__(self):
        self.tree = None
        self.source_lines = []

    def parse(self, source_code: str, filepath: str = None) -> Optional[ASTNode]:
        """
        Parse codice Python e restituisce l'AST.

        Args:
            source_code: Codice sorgente Python
            filepath: Percorso del file (opzionale)

        Returns:
            Nodo AST radice o None se errore
        """
        self.source_lines = source_code.split('\n')

        try:
            self.tree = ast.parse(source_code, filename=filepath or '<string>')
            return self._build_ast_tree(self.tree)
        except SyntaxError as e:
            # File con sintassi errata, ritorna None
            return None
        except Exception:
            return None

    def _build_ast_tree(self, node: ast.AST) -> ASTNode:
        """Costruisce l'albero AST ricorsivamente."""
        node_type = node.__class__.__name__
        line_number = getattr(node, 'lineno', 0)

        # Estrai attributi rilevanti
        attributes = {}
        if isinstance(node, ast.Name):
            attributes['name'] = node.id
        elif isinstance(node, ast.Constant):
            attributes['value'] = node.value
        elif isinstance(node, ast.Str):  # Python < 3.8
            attributes['value'] = node.s
        elif isinstance(node, ast.Num):  # Python < 3.8
            attributes['value'] = node.n
        elif isinstance(node, ast.Call):
            attributes['func'] = self._get_function_name(node.func)
        elif isinstance(node, ast.Attribute):
            attributes['attr'] = node.attr
        elif isinstance(node, ast.Import):
            attributes['modules'] = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            attributes['module'] = node.module
            attributes['names'] = [alias.name for alias in node.names]

        ast_node = ASTNode(node_type, line_number, **attributes)

        # Aggiungi nodi figlio
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        ast_node.add_child(self._build_ast_tree(item))
            elif isinstance(value, ast.AST):
                ast_node.add_child(self._build_ast_tree(value))

        return ast_node

    def _get_function_name(self, func: ast.expr) -> str:
        """Estrae il nome della funzione da un nodo Call."""
        if isinstance(func, ast.Name):
            return func.id
        elif isinstance(func, ast.Attribute):
            return f"{self._get_function_name(func.value)}.{func.attr}"
        return "<unknown>"

    def find_function_calls(self, function_names: List[str]) -> List[Dict]:
        """
        Trova chiamate a funzioni specifiche.

        Args:
            function_names: Lista di nomi di funzioni da cercare

        Returns:
            Lista di dizionari con info sulle chiamate trovate
        """
        calls = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node.func)

                if func_name in function_names:
                    calls.append({
                        'function': func_name,
                        'line': node.lineno,
                        'column': node.col_offset,
                        'context': self._get_line_context(node.lineno)
                    })

        return calls

    def find_string_operations(self) -> List[Dict]:
        """Trova operazioni su stringhe potenzialmente vulnerabili."""
        operations = []

        for node in ast.walk(self.tree):
            # Formatted strings (f-strings)
            if isinstance(node, ast.JoinedStr):
                operations.append({
                    'type': 'f-string',
                    'line': node.lineno,
                    'context': self._get_line_context(node.lineno),
                    'risk': 'potential'
                })

            # String concatenation with +
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                if isinstance(node.left, (ast.Str, ast.Constant)) or \
                   isinstance(node.right, (ast.Str, ast.Constant)):
                    operations.append({
                        'type': 'concatenation',
                        'line': node.lineno,
                        'context': self._get_line_context(node.lineno)
                    })

            # .format() calls
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node.func)
                if func_name.endswith('.format'):
                    operations.append({
                        'type': 'format',
                        'line': node.lineno,
                        'context': self._get_line_context(node.lineno)
                    })

        return operations

    def find_imports(self) -> List[Dict]:
        """Trova tutti gli import nel file."""
        imports = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                imports.append({
                    'type': 'from_import',
                    'module': node.module,
                    'names': [alias.name for alias in node.names],
                    'line': node.lineno
                })

        return imports

    def find_variable_assignments(self, var_names: List[str]) -> List[Dict]:
        """
        Trova assegnamenti a variabili specifiche.

        Args:
            var_names: Lista di nomi di variabili

        Returns:
            Lista di assegnamenti trovati
        """
        assignments = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in var_names:
                        assignments.append({
                            'variable': target.id,
                            'line': node.lineno,
                            'context': self._get_line_context(node.lineno)
                        })

        return assignments

    def _get_line_context(self, line_number: int, context_lines: int = 2) -> Dict:
        """Ottiene il contesto delle righe intorno a una linea."""
        start = max(0, line_number - context_lines - 1)
        end = min(len(self.source_lines), line_number + context_lines)

        return {
            'line_before': self.source_lines[start:line_number-1] if line_number > 1 else [],
            'line_of': self.source_lines[line_number-1] if line_number <= len(self.source_lines) else '',
            'line_after': self.source_lines[line_number:end]
        }


class JavaScriptASTParser:
    """
    Parser AST semplificato per JavaScript.
    NOTA: Implementazione semplificata basata su regex.
    Per un parsing completo, usare librerie come esprima/pyjsparser.
    """

    def __init__(self):
        self.source_code = ""
        self.source_lines = []

    def parse(self, source_code: str, filepath: str = None) -> Dict:
        """
        Parse codice JavaScript (implementazione semplificata).

        Args:
            source_code: Codice sorgente JavaScript
            filepath: Percorso del file (opzionale)

        Returns:
            Dizionario con info estratte
        """
        self.source_code = source_code
        self.source_lines = source_code.split('\n')

        return {
            'functions': self._find_functions(),
            'calls': self._find_function_calls(),
            'imports': self._find_imports(),
            'variables': self._find_variable_assignments()
        }

    def _find_functions(self) -> List[Dict]:
        """Trova definizioni di funzioni."""
        functions = []
        # Pattern per function declarations e arrow functions
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*(?:async\s+)?function\s*\(',
            r'(\w+)\s*\([^)]*\)\s*{'  # Method shorthand
        ]

        for line_num, line in enumerate(self.source_lines, 1):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    functions.append({
                        'name': match.group(1),
                        'line': line_num,
                        'context': line.strip()
                    })

        return functions

    def _find_function_calls(self) -> List[Dict]:
        """Trova chiamate a funzioni."""
        calls = []

        for line_num, line in enumerate(self.source_lines, 1):
            # Pattern per chiamate funzione
            matches = re.finditer(r'(\w+(?:\.\w+)*)\s*\(', line)
            for match in matches:
                calls.append({
                    'function': match.group(1),
                    'line': line_num,
                    'context': line.strip()
                })

        return calls

    def _find_imports(self) -> List[Dict]:
        """Trova import e require."""
        imports = []

        for line_num, line in enumerate(self.source_lines, 1):
            # require()
            require_match = re.search(r'(?:const|let|var)\s+(\w+)\s*=\s*require\(["\']([^"\']+)["\']\)', line)
            if require_match:
                imports.append({
                    'type': 'require',
                    'module': require_match.group(2),
                    'variable': require_match.group(1),
                    'line': line_num
                })

            # import
            import_match = re.search(r'import\s+(?:(\w+)\s+from\s+)?["\']([^"\']+)["\']', line)
            if import_match:
                imports.append({
                    'type': 'import',
                    'module': import_match.group(2),
                    'default_import': import_match.group(1),
                    'line': line_num
                })

        return imports

    def _find_variable_assignments(self) -> List[Dict]:
        """Trova assegnamenti di variabili."""
        assignments = []

        for line_num, line in enumerate(self.source_lines, 1):
            # const, let, var
            matches = re.finditer(r'(?:const|let|var)\s+(\w+)\s*=', line)
            for match in matches:
                assignments.append({
                    'variable': match.group(1),
                    'line': line_num,
                    'context': line.strip()
                })

        return assignments


class ASTParser:
    """Parser AST universale che delega al parser specifico del linguaggio."""

    def __init__(self):
        self.python_parser = PythonASTParser()
        self.js_parser = JavaScriptASTParser()

    def parse(self, file_info: Dict) -> Optional[Dict]:
        """
        Parse un file e restituisce informazioni AST.

        Args:
            file_info: Dizionario con info sul file

        Returns:
            Informazioni AST o None se errore
        """
        content = file_info.get('content', '')
        extension = file_info.get('extension', '')

        if not content:
            return None

        try:
            if extension in {'.py', '.pyw'}:
                # Python
                ast_node = self.python_parser.parse(content, file_info.get('path'))
                if ast_node:
                    return {
                        'type': 'python',
                        'ast': ast_node.to_dict(),
                        'imports': self.python_parser.find_imports(),
                        'calls': self.python_parser.find_function_calls(['execute', 'query', 'format']),
                        'strings': self.python_parser.find_string_operations()
                    }

            elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
                # JavaScript/TypeScript
                return self.js_parser.parse(content, file_info.get('path'))

            return None
        except Exception:
            return None

    def is_safe_sql_query(self, file_info: Dict, line_number: int) -> bool:
        """
        Verifica se una query SQL è sicura (parametrizzata).

        Args:
            file_info: Info sul file
            line_number: Numero di riga

        Returns:
            True se sembra sicura
        """
        content = file_info.get('content', '')
        if not content:
            return False

        lines = content.split('\n')
        if line_number > len(lines):
            return False

        line = lines[line_number - 1]

        # Segnali di query parametrizzata
        safe_indicators = [
            '%s', '%d',  # Python placeholders
            '?',        # JDBC/SQLite style
            ':1', ':2',  # PostgreSQL
            '$1', '$2',  # PostgreSQL/MySQL
            '@p1', '@p2'  # ADO.NET
        ]

        # Verifica presenza di placeholder
        for indicator in safe_indicators:
            if indicator in line:
                return True

        # Verifica uso di tuple/lista come secondo parametro
        if ', (' in line or ', [' in line:
            return True

        return False
