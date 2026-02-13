"""
Code Reader Module
Modulo per la lettura e gestione dei file di codice sorgente.

Supporta: Python, JavaScript, TypeScript, PHP, Java, C#, Go
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Set
import hashlib


class CodeFile:
    """Rappresenta un file di codice sorgente."""

    def __init__(self, filepath: Path, content: str = None):
        self.filepath = filepath
        self.content = content
        self.extension = filepath.suffix.lower()
        self.filename = filepath.name
        self.line_count = 0
        self.hash = None

        if content:
            self.line_count = len(content.split('\n'))
            self.hash = hashlib.md5(content.encode()).hexdigest()

    def read(self) -> str:
        """Legge il contenuto del file."""
        if self.content is None:
            try:
                with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    self.content = f.read()
                self.line_count = len(self.content.split('\n'))
                self.hash = hashlib.md5(self.content.encode()).hexdigest()
            except Exception as e:
                self.content = ""
        return self.content

    def get_lines(self, start: int = 1, end: int = None) -> List[str]:
        """Restituisce righe specifiche del file."""
        if not self.content:
            self.read()

        lines = self.content.split('\n')
        if end:
            return lines[start-1:end]
        return lines[start-1:]

    def to_dict(self) -> Dict:
        """Converte il file in dizionario."""
        if self.content is None:
            self.read()

        return {
            'path': str(self.filepath),
            'filename': self.filename,
            'extension': self.extension,
            'line_count': self.line_count,
            'hash': self.hash,
            'content': self.content,
            'relative_path': str(self.filepath)
        }


class CodeReader:
    """Classe principale per leggere e gestire file di codice."""

    # Estensioni supportate per categoria
    SUPPORTED_EXTENSIONS = {
        'python': {'.py', '.pyw'},
        'javascript': {'.js', '.jsx', '.mjs'},
        'typescript': {'.ts', '.tsx'},
        'php': {'.php', '.phtml'},
        'java': {'.java'},
        'csharp': {'.cs'},
        'go': {'.go'},
        'ruby': {'.rb'},
        'html': {'.html', '.htm'},
        'css': {'.css', '.scss', '.sass', '.less'}
    }

    # Directory e file da ignorare
    IGNORED_DIRS = {
        '__pycache__', '.git', '.svn', '.hg', '.idea', '.vscode',
        'node_modules', 'vendor', 'bower_components', 'dist', 'build',
        'venv', 'env', '.venv', 'site-packages', 'target', 'bin', 'obj'
    }

    IGNORED_FILES = {
        '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dylib', '*.dll',
        '*.exe', '*.bin', '*.class', '*.jar', '*.war',
        '*.min.js', '*.min.css', '*.bundle.js',
        '.DS_Store', 'Thumbs.db'
    }

    def __init__(self, target_path: Path):
        """
        Inizializza il CodeReader.

        Args:
            target_path: Percorso del file o directory da analizzare
        """
        self.target_path = Path(target_path).resolve()
        self.files: List[CodeFile] = []

    def is_supported_extension(self, filepath: Path) -> bool:
        """Verifica se l'estensione del file è supportata."""
        ext = filepath.suffix.lower()

        # Controlla se è nelle estensioni supportate
        for lang_extensions in self.SUPPORTED_EXTENSIONS.values():
            if ext in lang_extensions:
                return True

        return False

    def should_ignore_directory(self, dirname: str) -> bool:
        """Verifica se una directory dovrebbe essere ignorata."""
        return dirname in self.IGNORED_DIRS

    def should_ignore_file(self, filename: str) -> bool:
        """Verifica se un file dovrebbe essere ignorato."""
        # Controlla pattern
        for pattern in self.IGNORED_FILES:
            if filename.endswith(pattern.replace('*', '')):
                return True

        # File che iniziano con punto (nascosti)
        if filename.startswith('.') and filename not in {'.gitignore', '.env.example'}:
            return True

        return False

    def scan_files(self, max_size_mb: int = 10) -> List[Dict]:
        """
        Scansiona i file di codice nel percorso target.

        Args:
            max_size_mb: Dimensione massima file in MB

        Returns:
            Lista di dizionari con informazioni sui file
        """
        self.files = []
        max_size_bytes = max_size_mb * 1024 * 1024

        if self.target_path.is_file():
            # Single file
            if self.is_supported_extension(self.target_path):
                code_file = CodeFile(self.target_path)
                code_file.read()
                self.files.append(code_file)
        else:
            # Directory - attraversa ricorsivamente
            for root, dirs, files in os.walk(self.target_path):
                # Filtra directories
                dirs[:] = [d for d in dirs if not self.should_ignore_directory(d)]

                for filename in files:
                    if self.should_ignore_file(filename):
                        continue

                    filepath = Path(root) / filename

                    # Verifica estensione
                    if not self.is_supported_extension(filepath):
                        continue

                    # Verifica dimensione
                    try:
                        if filepath.stat().st_size > max_size_bytes:
                            continue
                    except OSError:
                        continue

                    # Crea CodeFile
                    code_file = CodeFile(filepath)
                    code_file.read()
                    self.files.append(code_file)

        # Converti in dizionari
        return [f.to_dict() for f in self.files]

    def get_files_by_language(self, language: str) -> List[Dict]:
        """
        Restituisce i file filtrati per linguaggio.

        Args:
            language: Nome del linguaggio (python, javascript, etc.)

        Returns:
            Lista di file del linguaggio specificato
        """
        extensions = self.SUPPORTED_EXTENSIONS.get(language.lower(), set())
        return [f for f in self.files if f.extension in extensions]

    def get_file_statistics(self) -> Dict:
        """Restituisce statistiche sui file analizzati."""
        stats = {
            'total_files': len(self.files),
            'total_lines': sum(f.line_count for f in self.files),
            'by_language': {},
            'by_extension': {}
        }

        for file in self.files:
            # Per estensione
            ext = file.extension
            stats['by_extension'][ext] = stats['by_extension'].get(ext, 0) + 1

            # Per linguaggio
            for lang, extensions in self.SUPPORTED_EXTENSIONS.items():
                if ext in extensions:
                    stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
                    break

        return stats

    def search_content(self, pattern: str, language: str = None) -> List[Dict]:
        """
        Cerca un pattern nel contenuto dei file.

        Args:
            pattern: Pattern da cercare
            language: Filtra per linguaggio (opzionale)

        Returns:
            Lista di match trovati
        """
        import re

        results = []
        files_to_search = self.files

        if language:
            files_to_search = self.get_files_by_language(language)

        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)

        for code_file in files_to_search:
            content = code_file.content
            if not content:
                continue

            for match in regex.finditer(content):
                line_number = content[:match.start()].count('\n') + 1
                lines = content.split('\n')
                line_content = lines[line_number - 1].strip() if line_number <= len(lines) else ''

                results.append({
                    'file': code_file.to_dict(),
                    'line_number': line_number,
                    'match': match.group(0),
                    'line_content': line_content,
                    'start': match.start(),
                    'end': match.end()
                })

        return results
