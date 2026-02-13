"""
Unit test per Caesar Cipher
Test per la cifratura, decifratura e analisi
"""

import unittest
from pathlib import Path
import sys
import os

# Aggiungi la directory parent al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cipher import CaesarCipher, caesar_cipher
from analysis import FrequencyAnalyzer, index_of_coincidence, entropy
from config import get_alphabet, ALPHABETS


class TestCaesarCipher(unittest.TestCase):
    """Test per la classe CaesarCipher"""

    def setUp(self):
        """Setup prima di ogni test"""
        self.cipher = CaesarCipher("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_encrypt_basic(self):
        """Test cifratura base"""
        result = self.cipher.encrypt("HELLO", 3)
        self.assertEqual(result, "KHOOR")

    def test_encrypt_wraparound(self):
        """Test wraparound (Z → C con key 3)"""
        result = self.cipher.encrypt("XYZ", 3)
        self.assertEqual(result, "ABC")

    def test_encrypt_punctuation(self):
        """Test che punteggiatura e spazi siano mantenuti"""
        result = self.cipher.encrypt("HELLO, WORLD!", 3)
        self.assertEqual(result, "KHOOR, ZRUOG!")

    def test_decrypt_basic(self):
        """Test decifratura base"""
        result = self.cipher.decrypt("KHOOR", 3)
        self.assertEqual(result, "HELLO")

    def test_decrypt_wraparound(self):
        """Test decifratura con wraparound"""
        result = self.cipher.decrypt("ABC", 3)
        self.assertEqual(result, "XYZ")

    def test_encrypt_decrypt_roundtrip(self):
        """Test che encrypt + decrypt torni al testo originale"""
        original = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        encrypted = self.cipher.encrypt(original, 13)
        decrypted = self.cipher.decrypt(encrypted, 13)
        self.assertEqual(original, decrypted)

    def test_key_zero(self):
        """Test chiave 0 (nessuna modifica)"""
        original = "TEST"
        result = self.cipher.encrypt(original, 0)
        self.assertEqual(result, original)

    def test_large_key(self):
        """Test chiave grande (deve essere ridotta con modulo)"""
        # Key 29 è equivalente a key 3 (29 mod 26 = 3)
        result1 = self.cipher.encrypt("HELLO", 29)
        result2 = self.cipher.encrypt("HELLO", 3)
        self.assertEqual(result1, result2)

    def test_brute_force(self):
        """Test brute force"""
        cipher_text = "KHOOR"
        results = self.cipher.brute_force(cipher_text)

        # Deve ritornare 25 risultati (tutte le chiavi tranne 0)
        self.assertEqual(len(results), 25)

        # La chiave 3 deve dare "HELLO"
        self.assertIn((3, "HELLO"), results)

    def test_encrypt_with_visual(self):
        """Test rappresentazione visiva"""
        encrypted, steps = self.cipher.encrypt_with_visual("AB", 1)

        self.assertEqual(encrypted, "BC")
        self.assertEqual(len(steps), 2)


class TestFrequencyAnalysis(unittest.TestCase):
    """Test per l'analisi delle frequenze"""

    def setUp(self):
        """Setup prima di ogni test"""
        self.analyzer = FrequencyAnalyzer(language="english")
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def test_count_frequency(self):
        """Test conteggio frequenze"""
        text = "AABBB"
        freq = self.analyzer.count_frequency(text, self.alphabet)

        self.assertEqual(freq["A"], 2)
        self.assertEqual(freq["B"], 3)

    def test_calculate_percentage(self):
        """Test calcolo percentuali"""
        freq = {"A": 2, "B": 2, "C": 1}
        percent = self.analyzer.calculate_percentage(freq)

        self.assertEqual(percent["A"], 40.0)
        self.assertEqual(percent["B"], 40.0)
        self.assertEqual(percent["C"], 20.0)

    def test_chi_squared_test(self):
        """Test del chi-quadrato"""
        # Test con testo in inglese reale
        english_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        freq = self.analyzer.count_frequency(english_text, self.alphabet)
        percent = self.analyzer.calculate_percentage(freq)

        score = self.analyzer.chi_squared_test(percent)

        # Il chi-quadrato deve essere un numero positivo
        self.assertGreater(score, 0)

    def test_frequency_report(self):
        """Test generazione report frequenze"""
        text = "HELLO WORLD"
        report = self.analyzer.get_frequency_report(text, self.alphabet)

        self.assertIn("Analisi Frequenze", report)
        self.assertIn("L", report)


class TestEntropy(unittest.TestCase):
    """Test per funzioni di analisi"""

    def test_index_of_coincidence(self):
        """Test indice di coincidenza"""
        # Testo più lungo in inglese per risultato più accurato
        english_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 3
        ic = index_of_coincidence(english_text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # IC per testo in inglese dovrebbe essere ~0.06-0.07
        # Testiamo che sia maggiore di zero (testo non completamente casuale)
        self.assertGreater(ic, 0.02)
        self.assertLess(ic, 0.10)

    def test_entropy(self):
        """Test calcolo entropia"""
        # Testo con caratteri uniformi (bassa entropia)
        uniform_text = "AAAA"
        ent = entropy(uniform_text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Entropia dovrebbe essere 0 per testo uniforme
        self.assertAlmostEqual(ent, 0.0, places=5)

        # Testo vari (alta entropia)
        varied_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ent_varied = entropy(varied_text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Entropia dovrebbe essere maggiore per testo vari
        self.assertGreater(ent_varied, ent)


class TestConfig(unittest.TestCase):
    """Test per il modulo config"""

    def test_get_alphabet_default(self):
        """Test ottieni alfabeto default"""
        alphabet = get_alphabet()
        self.assertEqual(alphabet, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_get_alphabet_english(self):
        """Test ottieni alfabeto inglese"""
        alphabet = get_alphabet("english")
        self.assertEqual(alphabet, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_get_alphabet_italian(self):
        """Test ottieni alfabeto italiano"""
        alphabet = get_alphabet("italian")
        self.assertIn("A", alphabet)
        self.assertNotIn("J", alphabet)  # J non è nell'alfabeto italiano standard


class TestCaesarCipherHelper(unittest.TestCase):
    """Test per la funzione helper caesar_cipher"""

    def test_encrypt_helper(self):
        """Test funzione helper per encrypt"""
        result = caesar_cipher("HELLO", 3, encrypt=True)
        self.assertEqual(result, "KHOOR")

    def test_decrypt_helper(self):
        """Test funzione helper per decrypt"""
        result = caesar_cipher("KHOOR", 3, encrypt=False)
        self.assertEqual(result, "HELLO")

    def test_custom_alphabet(self):
        """Test con alfabeto custom"""
        custom_alpha = "ABC"
        result = caesar_cipher("ABC", 1, encrypt=True, alphabet=custom_alpha)
        self.assertEqual(result, "BCA")


def run_tests():
    """Esegui tutti i test"""
    # Crea test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Aggiungi tutti i test
    suite.addTests(loader.loadTestsFromTestCase(TestCaesarCipher))
    suite.addTests(loader.loadTestsFromTestCase(TestFrequencyAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestEntropy))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestCaesarCipherHelper))

    # Esegui test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Ritorna 0 se successo, 1 se fallimento
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
