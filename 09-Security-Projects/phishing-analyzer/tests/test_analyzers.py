"""
Test per gli analyzer del Phishing Analyzer
"""

import unittest
import sys
import os

# Aggiungi il path del progetto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzers.links import LinkAnalyzer
from analyzers.sender import SenderAnalyzer
from analyzers.content import ContentAnalyzer
from utils.dns_tools import DNSChecker
from utils.risk_calculator import RiskCalculator
import email
from email.message import EmailMessage
from email.policy import default


class TestLinkAnalyzer(unittest.TestCase):
    """Test per LinkAnalyzer"""

    def setUp(self):
        self.analyzer = LinkAnalyzer()

    def test_extract_links(self):
        """Test l'estrazione dei link dal testo"""
        text = "Visita https://example.com e anche http://test.org"
        links = self.analyzer.extract_links(text)
        self.assertEqual(len(links), 2)
        self.assertIn("https://example.com", links)
        self.assertIn("http://test.org", links)

    def test_analyze_safe_link(self):
        """Test l'analisi di un link sicuro"""
        result = self.analyzer.analyze_link("https://www.google.com")
        self.assertFalse(result['suspicious'])
        self.assertEqual(result['risk_score'], 0)

    def test_analyze_http_link(self):
        """Test l'analisi di un link HTTP (non sicuro)"""
        result = self.analyzer.analyze_link("http://example.com")
        self.assertTrue(result['suspicious'])
        self.assertGreater(result['risk_score'], 0)
        self.assertFalse(result['checks']['https'])

    def test_analyze_ip_url(self):
        """Test l'analisi di un URL con indirizzo IP"""
        result = self.analyzer.analyze_link("http://192.168.1.1/login")
        self.assertTrue(result['suspicious'])
        self.assertTrue(result['checks']['ip_address'])

    def test_detect_suspicious_tld(self):
        """Test il rilevamento di TLD sospetti"""
        result = self.analyzer.analyze_link("http://example.xyz")
        self.assertTrue(result['suspicious'])
        self.assertTrue(result['checks']['suspicious_tld'])

    def test_detect_misspelled_domain(self):
        """Test il rilevamento di domini con refusi"""
        result = self.analyzer.analyze_link("http://paypa1.com")
        # Dovrebbe rilevare la somiglianza con paypal.com
        self.assertTrue(result['checks']['misspelled'] or result['suspicious'])


class TestSenderAnalyzer(unittest.TestCase):
    """Test per SenderAnalyzer"""

    def setUp(self):
        self.analyzer = SenderAnalyzer()

    def test_parse_from_header(self):
        """Test il parsing dell'header From"""
        name, email = self.analyzer._parse_from_header('"Mario Rossi" <mario.rossi@example.com>')
        self.assertEqual(name, "Mario Rossi")
        self.assertEqual(email, "mario.rossi@example.com")

    def test_parse_from_header_no_name(self):
        """Test il parsing dell'header From senza nome"""
        name, email = self.analyzer._parse_from_header('mario.rossi@example.com')
        self.assertIsNone(name)
        self.assertEqual(email, "mario.rossi@example.com")

    def test_is_free_email_domain(self):
        """Test il riconoscimento di domini di email gratuita"""
        self.assertTrue(self.analyzer._is_free_email_domain('gmail.com'))
        self.assertTrue(self.analyzer._is_free_email_domain('yahoo.com'))
        self.assertFalse(self.analyzer._is_free_email_domain('microsoft.com'))

    def test_is_generic_role(self):
        """Test il riconoscimento di ruoli generici"""
        self.assertTrue(self.analyzer._is_generic_role('support@example.com'))
        self.assertTrue(self.analyzer._is_generic_role('admin@example.com'))
        self.assertFalse(self.analyzer._is_generic_role('mario.rossi@example.com'))


class TestContentAnalyzer(unittest.TestCase):
    """Test per ContentAnalyzer"""

    def setUp(self):
        self.analyzer = ContentAnalyzer()

    def test_detect_urgency(self):
        """Test il rilevamento di parole di urgenza"""
        email_msg = EmailMessage()
        email_msg.set_content("Questa email è urgente, rispondi immediatamente")

        result = self.analyzer.analyze_content(email_msg)
        self.assertTrue(result['urgency_detected'])
        self.assertGreater(len(result['urgency_keywords']), 0)

    def test_detect_credential_requests(self):
        """Test il rilevamento di richieste di credenziali"""
        email_msg = EmailMessage()
        email_msg.set_content("Per favore conferma la tua password cliccando qui")

        result = self.analyzer.analyze_content(email_msg)
        self.assertTrue(result['credential_requests'])

    def test_detect_financial_keywords(self):
        """Test il rilevamento di keyword finanziarie"""
        email_msg = EmailMessage()
        email_msg.set_content("Effettua il bonifico entro domani")

        result = self.analyzer.analyze_content(email_msg)
        self.assertTrue(result['financial_keywords'])


class TestDNSChecker(unittest.TestCase):
    """Test per DNSChecker"""

    def setUp(self):
        self.checker = DNSChecker()

    def test_check_spf_google(self):
        """Test la verifica SPF per un dominio noto"""
        result = self.checker.check_spf('google.com')
        self.assertIn(result['status'], ['pass', 'softfail', 'none'])

    def test_check_dmarc_google(self):
        """Test la verifica DMARC per un dominio noto"""
        result = self.checker.check_dmarc('google.com')
        self.assertIn(result['status'], ['found', 'none'])


class TestRiskCalculator(unittest.TestCase):
    """Test per RiskCalculator"""

    def setUp(self):
        self.calculator = RiskCalculator()

    def test_calculate_low_risk(self):
        """Test il calcolo del rischio basso"""
        analysis = {
            'spf': {'status': 'pass'},
            'dkim': {'valid': True},
            'dmarc': {'status': 'found', 'policy': 'reject'},
            'sender': {'suspicious': False},
            'links': {'has_suspicious_links': False, 'analyzed_links': []},
            'content': {'urgency_detected': False, 'credential_requests': False},
            'attachments': {'has_attachments': False}
        }

        result = self.calculator.calculate_risk_score(analysis)
        self.assertEqual(result['level'], 'MOLTO BASSO')

    def test_calculate_high_risk(self):
        """Test il calcolo del rischio alto"""
        analysis = {
            'spf': {'status': 'fail'},
            'dkim': {'valid': False},
            'dmarc': {'status': 'none'},
            'sender': {'suspicious': True, 'spoofed': True},
            'links': {'has_suspicious_links': True, 'analyzed_links': [
                {'suspicious': True, 'risk_score': 30}
            ]},
            'content': {
                'urgency_detected': True,
                'credential_requests': True,
                'urgency_score': 15,
                'pressure_score': 12,
                'credential_score': 25
            },
            'attachments': {'has_attachments': True, 'suspicious_extensions': True}
        }

        result = self.calculator.calculate_risk_score(analysis)
        self.assertIn(result['level'], ['ALTO', 'CRITICO'])


class TestIntegration(unittest.TestCase):
    """Test di integrazione"""

    def test_full_phishing_email_analysis(self):
        """Test l'analisi completa di una email di phishing simulata"""
        # Crea una email di phishing simulata
        msg = EmailMessage()
        msg['From'] = '"PayPal Security" <security@paypa1.com>'
        msg['To'] = 'victim@example.com'
        msg['Subject'] = 'URGENTE: Il tuo account verrà chiuso!'
        msg.set_content("""
        Gentile utente,

        Il tuo account PayPal verrà chiuso entro 24 ore.
        Conferma la tua password cliccando qui: http://paypa1.com/login

        Urgente!
        """)

        # Analizza header
        sender_analyzer = SenderAnalyzer()
        sender_result = sender_analyzer.analyze_sender(msg)
        self.assertTrue(sender_result['suspicious'])

        # Analizza link
        link_analyzer = LinkAnalyzer()
        links = link_analyzer.analyze_email_links(msg.get_content())
        self.assertTrue(links['has_suspicious_links'])

        # Analizza contenuto
        content_analyzer = ContentAnalyzer()
        content_result = content_analyzer.analyze_content(msg)
        self.assertTrue(content_result['urgency_detected'])
        self.assertTrue(content_result['credential_requests'])


def run_tests():
    """Esegue tutti i test"""
    # Crea il test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Aggiungi tutti i test
    suite.addTests(loader.loadTestsFromTestCase(TestLinkAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSenderAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestContentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestDNSChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Esegui i test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report finale
    print("\n" + "="*70)
    print(f"Test eseguiti: {result.testsRun}")
    print(f"Successi: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallimenti: {len(result.failures)}")
    print(f"Errori: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
