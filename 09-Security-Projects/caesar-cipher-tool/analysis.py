"""
Strumenti di analisi per Caesar Cipher
Include analisi delle frequenze e brute force
"""

from collections import Counter
from typing import List, Tuple, Dict
import math


class FrequencyAnalyzer:
    """
    Analizzatore di frequenze per crittanalisi del cifrario di Caesar
    """

    # Frequenze delle lettere in italiano (in percentuale)
    ITALIAN_FREQUENCIES = {
        "A": 11.74,
        "B": 0.92,
        "C": 4.50,
        "D": 3.73,
        "E": 11.79,
        "F": 1.00,
        "G": 1.54,
        "H": 0.93,
        "I": 11.28,
        "L": 6.51,
        "M": 2.51,
        "N": 6.88,
        "O": 9.20,
        "P": 3.05,
        "Q": 0.51,
        "R": 6.37,
        "S": 4.98,
        "T": 5.62,
        "U": 3.01,
        "V": 2.10,
        "Z": 1.10,
    }

    # Frequenze delle lettere in inglese (in percentuale)
    ENGLISH_FREQUENCIES = {
        "A": 8.167,
        "B": 1.492,
        "C": 2.782,
        "D": 4.253,
        "E": 12.702,
        "F": 2.228,
        "G": 2.015,
        "H": 6.094,
        "I": 6.966,
        "J": 0.153,
        "K": 0.772,
        "L": 4.025,
        "M": 2.406,
        "N": 6.749,
        "O": 7.507,
        "P": 1.929,
        "Q": 0.095,
        "R": 5.987,
        "S": 6.327,
        "T": 9.056,
        "U": 2.758,
        "V": 0.978,
        "W": 2.360,
        "X": 0.150,
        "Y": 1.974,
        "Z": 0.074,
    }

    def __init__(self, language: str = "english"):
        """
        Inizializza l'analizzatore

        Args:
            language: 'english' o 'italian' per frequenze di riferimento
        """
        self.language = language
        if language == "italian":
            self.reference_freq = self.ITALIAN_FREQUENCIES
        else:
            self.reference_freq = self.ENGLISH_FREQUENCIES

    def count_frequency(self, text: str, alphabet: str) -> Dict[str, int]:
        """
        Conta la frequenza di ogni lettera nel testo

        Args:
            text: Testo da analizzare
            alphabet: Alfabeto da considerare

        Returns:
            Dizionario {lettera: conteggio}
        """
        # Converti in maiuscolo e filtra solo lettere dell'alfabeto
        filtered_text = [char.upper() for char in text if char.upper() in alphabet]

        # Conta frequenze
        counter = Counter(filtered_text)

        # Assicurati che tutte le lettere dell'alfabeto siano presenti
        for char in alphabet:
            if char not in counter:
                counter[char] = 0

        return dict(sorted(counter.items()))

    def calculate_percentage(self, frequency: Dict[str, int]) -> Dict[str, float]:
        """
        Converte conteggi in percentuali

        Args:
            frequency: Dizionario {lettera: conteggio}

        Returns:
            Dizionario {lettera: percentuale}
        """
        total = sum(frequency.values())
        if total == 0:
            return {char: 0.0 for char in frequency}

        return {char: (count / total) * 100 for char, count in frequency.items()}

    def chi_squared_test(self, observed_freq: Dict[str, float]) -> float:
        """
        Test del chi-quadrato per confrontare frequenze osservate con attese

        Formula: χ² = Σ((O - E)² / E)
        Dove:
            O = frequenza osservata
            E = frequenza attesa

        Più basso è il valore, più probabile è che il testo sia nella lingua corretta

        Args:
            observed_freq: Frequenze osservate nel testo

        Returns:
            Valore del chi-quadrato
        """
        chi_squared = 0.0

        for char in observed_freq:
            observed = observed_freq[char]
            expected = self.reference_freq.get(char, 0)

            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected

        return chi_squared

    def find_best_key(self, cipher_text: str, alphabet: str, decrypt_func) -> Tuple[int, float, str]:
        """
        Trova la chiave più probabile usando l'analisi delle frequenze

        Args:
            cipher_text: Testo cifrato
            alphabet: Alfabeto usato
            decrypt_func: Funzione di decifratura

        Returns:
            Tuple (best_key, chi_squared, decrypted_text)
        """
        best_key = 0
        best_score = float("inf")
        best_decrypted = ""

        for key in range(1, len(alphabet)):
            # Decripta con questa chiave
            decrypted = decrypt_func(cipher_text, key)

            # Calcola frequenze
            freq = self.count_frequency(decrypted, alphabet)
            percent_freq = self.calculate_percentage(freq)

            # Calcola chi-quadrato
            score = self.chi_squared_test(percent_freq)

            # Mantieni il miglior risultato
            if score < best_score:
                best_score = score
                best_key = key
                best_decrypted = decrypted

        return best_key, best_score, best_decrypted

    def get_frequency_report(
        self, text: str, alphabet: str, title: str = "Analisi Frequenze"
    ) -> str:
        """
        Genera un report dettagliato delle frequenze

        Args:
            text: Testo da analizzare
            alphabet: Alfabeto da usare
            title: Titolo del report

        Returns:
            Report formattato come stringa
        """
        freq = self.count_frequency(text, alphabet)
        percent = self.calculate_percentage(freq)

        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"{title:^60}")
        lines.append(f"{'='*60}\n")

        # Intestazione tabella
        lines.append(f"{'Lettera':<10} {'Conteggio':<12} {'Percentuale':<12} {'Atteso':<12}")
        lines.append("-" * 60)

        # Righe dati
        for char in alphabet:
            observed = percent[char]
            expected = self.reference_freq.get(char, 0)
            count = freq[char]

            lines.append(f"{char:<10} {count:<12} {observed:<12.2f}% {expected:<12.2f}%")

        lines.append("-" * 60)
        lines.append(f"\nLingua di riferimento: {self.language.upper()}")
        lines.append(f"Totale caratteri analizzati: {sum(freq.values())}")

        return "\n".join(lines)


def index_of_coincidence(text: str, alphabet: str) -> float:
    """
    Calcola l'indice di coincidenza di un testo

    Formula: IC = Σ(f_i * (f_i - 1)) / (N * (N - 1))
    Dove:
        f_i = frequenza della i-esima lettera
        N = totale delle lettere

    Valori tipici:
        - Italiano: ~0.0738
        - Inglese: ~0.0667
        - Testo casuale: ~0.0385

    Args:
        text: Testo da analizzare
        alphabet: Alfabeto considerato

    Returns:
        Indice di coincidenza
    """
    # Filtra solo lettere dell'alfabeto
    filtered = [char.upper() for char in text if char.upper() in alphabet]
    n = len(filtered)

    if n < 2:
        return 0.0

    # Conta frequenze
    freq = Counter(filtered)

    # Calcola IC
    numerator = sum(f * (f - 1) for f in freq.values())
    denominator = n * (n - 1)

    return numerator / denominator if denominator > 0 else 0.0


def entropy(text: str, alphabet: str) -> float:
    """
    Calcola l'entropia di Shannon di un testo

    Formula: H = -Σ(p_i * log2(p_i))
    Dove:
        p_i = probabilità della i-esima lettera

    Più alto è l'entropia, più "casuale" appare il testo

    Args:
        text: Testo da analizzare
        alphabet: Alfabeto considerato

    Returns:
        Entropia in bit
    """
    # Filtra e conta
    filtered = [char.upper() for char in text if char.upper() in alphabet]
    total = len(filtered)

    if total == 0:
        return 0.0

    freq = Counter(filtered)
    ent = 0.0

    for count in freq.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)

    return ent
