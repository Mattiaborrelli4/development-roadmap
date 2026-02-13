"""
Unit tests per gli analizzatori di sicurezza.
"""

import unittest
import sys
from pathlib import Path

# Aggiungi il path del progetto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from analyzers.sql_injection import SQLInjectionAnalyzer
from analyzers.xss_detector import XSSAnalyzer
from analyzers.credentials import CredentialsAnalyzer
from analyzers.crypto import CryptoAnalyzer
from analyzers.validation import ValidationAnalyzer


class TestSQLInjectionAnalyzer(unittest.TestCase):
    """Test per SQL Injection Analyzer."""

    def setUp(self):
        """Configura i test."""
        self.config = {
            'severity': 'CRITICAL',
            'cwe': 'CWE-89',
            'description': 'SQL Injection',
            'patterns': [
                {
                    'language': 'python',
                    'patterns': [r'\.execute\(f?"[^"]*\{[^}]+\}[^"]*"\)']
                }
            ]
        }
        self.analyzer = SQLInjectionAnalyzer(self.config)

    def test_detect_f_string_sql(self):
        """Test rilevamento f-string SQL."""
        file_info = {
            'path': 'test.py',
            'extension': '.py',
            'content': 'cursor.execute(f"SELECT * FROM users WHERE id={user_id}")'
        }

        findings = self.analyzer._check_pattern(
            file_info['content'],
            r'\.execute\(f?"[^"]*\{[^}]+\}[^"]*"\)',
            file_info
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['type'], 'sql_injection')

    def test_safe_query_not_detected(self):
        """Test che query sicure non siano rilevate."""
        file_info = {
            'path': 'test.py',
            'extension': '.py',
            'content': 'cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))'
        }

        findings = self.analyzer._check_pattern(
            file_info['content'],
            r'\.execute\(f?"[^"]*\{[^}]+\}[^"]*"\)',
            file_info
        )

        self.assertEqual(len(findings), 0)


class TestXSSAnalyzer(unittest.TestCase):
    """Test per XSS Analyzer."""

    def setUp(self):
        """Configura i test."""
        self.config = {
            'severity': 'HIGH',
            'cwe': 'CWE-79',
            'description': 'XSS',
            'patterns': [
                {
                    'language': 'javascript',
                    'patterns': [r'innerHTML\s*=']
                }
            ]
        }
        self.analyzer = XSSAnalyzer(self.config)

    def test_detect_innerHTML(self):
        """Test rilevamento innerHTML."""
        file_info = {
            'path': 'test.js',
            'extension': '.js',
            'content': 'element.innerHTML = user_input;'
        }

        findings = self.analyzer._check_pattern(
            file_info['content'],
            r'innerHTML\s*=',
            file_info
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['type'], 'xss')


class TestCredentialsAnalyzer(unittest.TestCase):
    """Test per Credentials Analyzer."""

    def setUp(self):
        """Configura i test."""
        self.config = {
            'severity': 'CRITICAL',
            'cwe': 'CWE-798',
            'description': 'Hardcoded credentials',
            'patterns': [
                {
                    'language': 'all',
                    'patterns': [r'password\s*=\s*["\'][^"\']{4,}["\']']
                }
            ]
        }
        self.analyzer = CredentialsAnalyzer(self.config)

    def test_detect_hardcoded_password(self):
        """Test rilevamento password hardcoded."""
        file_info = {
            'path': 'test.py',
            'extension': '.py',
            'content': 'password = "mysupersecretpassword123"'
        }

        findings = self.analyzer._check_pattern(
            file_info['content'],
            r'password\s*=\s*["\'][^"\']{4,}["\']',
            file_info
        )

        # Dovrebbe essere filtrato come falso positivo
        self.assertEqual(len(findings), 0)

    def test_env_var_not_detected(self):
        """Test che variabili ambiente non siano rilevate."""
        file_info = {
            'path': 'test.py',
            'extension': '.py',
            'content': 'password = os.environ.get("DB_PASSWORD")'
        }

        findings = self.analyzer._check_pattern(
            file_info['content'],
            r'password\s*=\s*["\'][^"\']{4,}["\']',
            file_info
        )

        self.assertEqual(len(findings), 0)


class TestCryptoAnalyzer(unittest.TestCase):
    """Test per Crypto Analyzer."""

    def setUp(self):
        """Configura i test."""
        self.config = {
            'severity': 'MEDIUM',
            'cwe': 'CWE-327',
            'description': 'Weak crypto',
            'patterns': [
                {
                    'language': 'python',
                    'patterns': [r'hashlib\.md5\(']
                }
            ]
        }
        self.analyzer = CryptoAnalyzer(self.config)

    def test_detect_md5(self):
        """Test rilevamento MD5."""
        file_info = {
            'path': 'test.py',
            'extension': '.py',
            'content': 'hashlib.md5(data).hexdigest()'
        }

        findings = self.analyzer._check_pattern(
            file_info['content'],
            r'hashlib\.md5\(',
            file_info
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['type'], 'weak_cryptography')


class TestValidationAnalyzer(unittest.TestCase):
    """Test per Validation Analyzer."""

    def setUp(self):
        """Configura i test."""
        self.config = {
            'severity': 'MEDIUM',
            'cwe': 'CWE-20',
            'description': 'Missing validation',
            'patterns': []
        }
        self.analyzer = ValidationAnalyzer(self.config)

    def test_has_validation(self):
        """Test rilevamento validazione."""
        self.assertTrue(self.analyzer._has_validation('input.validate()'))
        self.assertTrue(self.analyzer._has_validation('input.strip()'))
        self.assertFalse(self.analyzer._has_validation('input'))


def run_tests():
    """Esegue tutti i test."""
    # Crea test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Aggiungi test
    suite.addTests(loader.loadTestsFromTestCase(TestSQLInjectionAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestXSSAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCredentialsAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationAnalyzer))

    # Esegui
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
