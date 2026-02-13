"""
Dependencies Analyzer
Analizzatore per dipendenze vulnerabili o outdated
"""

import re
import json
from pathlib import Path
from typing import Dict, List


class DependenciesAnalyzer:
    """Analizzatore per dipendenze insicure."""

    def __init__(self, config: Dict = None):
        """
        Inizializza l'analizzatore.

        Args:
            config: Configurazione (opzionale)
        """
        self.config = config or {}
        self.severity = 'MEDIUM'
        self.cwe = 'CWE-1104'

    def analyze(self, target_path: Path) -> List[Dict]:
        """
        Analizza le dipendenze del progetto.

        Args:
            target_path: Percorso del progetto

        Returns:
            Lista di vulnerabilità trovate
        """
        findings = []
        target = Path(target_path)

        # Cerca file di dipendenze comuni
        dependency_files = [
            'requirements.txt',
            'package.json',
            'package-lock.json',
            'yarn.lock',
            'Pipfile',
            'poetry.lock',
            'Gemfile',
            'Gemfile.lock',
            'composer.json',
            'composer.lock',
            'go.mod',
            'go.sum',
            'Cargo.toml',
            'Cargo.lock'
        ]

        for dep_file in dependency_files:
            filepath = target / dep_file
            if filepath.exists():
                findings.extend(self._analyze_dependency_file(filepath))

        # Cerca versioni pinned pericolose
        findings.extend(self._check_pinned_versions(target))

        return findings

    def _analyze_dependency_file(self, filepath: Path) -> List[Dict]:
        """Analizza un file di dipendenze."""
        findings = []
        filename = filepath.name

        try:
            if filename == 'requirements.txt':
                findings.extend(self._analyze_requirements_txt(filepath))
            elif filename == 'package.json':
                findings.extend(self._analyze_package_json(filepath))
            elif filename == 'Pipfile':
                findings.extend(self._analyze_pipfile(filepath))
            elif filename == 'composer.json':
                findings.extend(self._analyze_composer_json(filepath))

        except Exception:
            pass

        return findings

    def _analyze_requirements_txt(self, filepath: Path) -> List[Dict]:
        """Analizza requirements.txt Python."""
        findings = []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Ignora commenti e righe vuote
            if not line or line.startswith('#'):
                continue

            # Parse requirement
            package_info = self._parse_requirement_line(line)

            # Controlla problemi
            issues = []

            # Versione non specificata
            if '==' not in line and '>=' not in line and '<=' not in line:
                issues.append("No version specified - could install any version")

            # Versione molto vecchia
            for version in ['==0.', '==1.0.', '==1.1.', '==1.2.']:
                if version in line:
                    issues.append(f"Very old version pinned: {version}")

            # Pacchetti noti problematici
            vulnerable_packages = {
                'urllib3': 'Consider upgrading urllib3',
                'requests': 'Ensure requests>=2.20.0',
                'pyyaml': 'Ensure pyyaml>=5.1',
                'flask': 'Ensure flask>=1.0 for security fixes',
                'django': 'Ensure django>=2.2.13 for LTS',
                'pillow': 'Pillow had several CVEs, ensure latest version',
            }

            for pkg, message in vulnerable_packages.items():
                if line.lower().startswith(pkg):
                    issues.append(message)

            if issues:
                finding = {
                    'type': 'insecure_dependency',
                    'severity': 'MEDIUM',
                    'cwe': self.cwe,
                    'title': 'Potentially Insecure Python Dependency',
                    'description': f'Issue with package: {package_info["name"]}',
                    'file': str(filepath),
                    'line': line_num,
                    'code': line,
                    'issues': issues,
                    'recommendation': 'Pin specific versions and keep dependencies updated. Run: pip install --upgrade package_name',
                    'references': [
                        'https://pyup.io/',
                        'https://pypi.org/'
                    ]
                }
                findings.append(finding)

        return findings

    def _analyze_package_json(self, filepath: Path) -> List[Dict]:
        """Analizza package.json Node.js."""
        findings = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                package_json = json.load(f)

            # Analizza dependencies
            all_deps = {}
            all_deps.update(package_json.get('dependencies', {}))
            all_deps.update(package_json.get('devDependencies', {}))

            for package, version in all_deps.items():
                issues = []

                # Range di versione ampio
                if version in ['*', 'latest', 'x.x.x', '>=']:
                    issues.append(f"Version range too broad: {version}")

                # Pacchetti noti problematici
                vulnerable_packages = {
                    'lodash': 'Ensure lodash>=4.17.15',
                    'express': 'Ensure express>=4.16.0',
                    'axios': 'Keep axios updated',
                    'react': 'Keep React updated',
                    'vue': 'Keep Vue updated',
                    'angular': 'Keep Angular updated',
                }

                for pkg, message in vulnerable_packages.items():
                    if package.lower().startswith(pkg):
                        issues.append(message)

                if issues:
                    finding = {
                        'type': 'insecure_dependency',
                        'severity': 'MEDIUM',
                        'cwe': self.cwe,
                        'title': 'Potentially Insecure Node.js Dependency',
                        'description': f'Issue with package: {package}',
                        'file': str(filepath),
                        'line': None,
                        'code': f'"{package}": "{version}"',
                        'issues': issues,
                        'recommendation': 'Use npm audit to check for vulnerabilities. Pin specific versions with package-lock.json',
                        'references': [
                            'https://www.npmjs.com/advisories',
                            'https://npmjs.com/'
                        ]
                    }
                    findings.append(finding)

        except json.JSONDecodeError:
            pass

        return findings

    def _analyze_pipfile(self, filepath: Path) -> List[Dict]:
        """Analizza Pipfile Python."""
        findings = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Controlla se usa versioni non specificate
            if 'version = "*"' in content:
                finding = {
                    'type': 'insecure_dependency',
                    'severity': 'LOW',
                    'cwe': self.cwe,
                    'title': 'Unpinned Python Dependencies',
                    'description': 'Pipfile uses unpinned versions',
                    'file': str(filepath),
                    'line': None,
                    'code': 'version = "*"',
                    'issues': ['Unpinned versions may install insecure updates'],
                    'recommendation': 'Pin specific versions in Pipfile',
                    'references': ['https://pipenv.pypa.io/']
                }
                findings.append(finding)

        except Exception:
            pass

        return findings

    def _analyze_composer_json(self, filepath: Path) -> List[Dict]:
        """Analizza composer.json PHP."""
        findings = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                composer_json = json.load(f)

            all_deps = {}
            all_deps.update(composer_json.get('require', {}))
            all_deps.update(composer_json.get('require-dev', {}))

            for package, version in all_deps.items():
                if package == 'php':
                    # Check PHP version
                    if version.startswith('5.'):
                        finding = {
                            'type': 'insecure_dependency',
                            'severity': 'HIGH',
                            'cwe': self.cwe,
                            'title': 'Outdated PHP Version',
                            'description': 'PHP 5.x is EOL and unsupported',
                            'file': str(filepath),
                            'line': None,
                            'code': f'"php": "{version}"',
                            'issues': ['PHP 5.x reached End of Life. Upgrade to PHP 8.x'],
                            'recommendation': 'Upgrade to PHP 8.0 or later',
                            'references': ['https://www.php.net/supported-versions.php']
                        }
                        findings.append(finding)

        except Exception:
            pass

        return findings

    def _parse_requirement_line(self, line: str) -> Dict:
        """Parse una riga di requirements.txt."""
        # Rimuovi commenti
        line = line.split('#')[0].strip()

        # Estrai nome e versione
        if '==' in line:
            name, version = line.split('==', 1)
            name = name.strip()
            version = version.strip()
        elif '>=' in line:
            name, version = line.split('>=', 1)
            name = name.strip()
            version = '>=' + version.strip()
        elif '<=' in line:
            name, version = line.split('<=', 1)
            name = name.strip()
            version = '<=' + version.strip()
        elif '>=' in line:
            name, version = line.split('>=', 1)
            name = name.strip()
            version = '>=' + version.strip()
        else:
            name = line.split('[')[0].split(';')[0].strip()
            version = 'any'

        return {'name': name, 'version': version}

    def _check_pinned_versions(self, target_path: Path) -> List[Dict]:
        """Controlla versioni pinned problematiche."""
        findings = []

        # Pattern per versioni problematiche
        problematic_patterns = [
            (r'django\s*==\s*1\.\d+\.\d+', 'Django 1.x is EOL. Upgrade to Django 3.x+'),
            (r'flask\s*==\s*0\.\d+\.\d+', 'Flask 0.x is old. Upgrade to Flask 1.x+'),
            (r'requests\s*==\s*2\.\d+\.\d+', 'Old requests version. Upgrade to 2.20+'),
            (r'urllib3\s*==\s*1\.\d+\.\d+', 'Old urllib3 version. Check for updates'),
        ]

        for pattern_file, pattern in [
            ('requirements.txt', problematic_patterns[0]),
            ('requirements.txt', problematic_patterns[1]),
        ]:
            filepath = target_path / pattern_file
            if not filepath.exists():
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                for pattern_re, message in problematic_patterns:
                    matches = re.finditer(pattern_re, content, re.MULTILINE | re.IGNORECASE)
                    for match in matches:
                        line_number = content[:match.start()].count('\n') + 1
                        finding = {
                            'type': 'outdated_dependency',
                            'severity': 'MEDIUM',
                            'cwe': self.cwe,
                            'title': 'Outdated Package Version',
                            'description': message,
                            'file': str(filepath),
                            'line': line_number,
                            'code': match.group(0),
                            'recommendation': 'Upgrade to the latest stable version',
                            'references': []
                        }
                        findings.append(finding)

            except Exception:
                pass

        return findings
