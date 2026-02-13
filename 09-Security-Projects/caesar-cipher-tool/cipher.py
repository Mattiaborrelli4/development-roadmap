"""
Core Caesar Cipher implementation
Algoritmo di cifratura e decifratura Caesar
"""


class CaesarCipher:
    """
    Implementazione del cifrario di Caesar con supporto alfabeti multipli
    """

    def __init__(self, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        """
        Inizializza il cifrario con un alfabeto specifico

        Args:
            alphabet: Stringa contenente l'alfabeto da utilizzare
        """
        self.alphabet = alphabet
        self.alphabet_length = len(alphabet)
        self.alphabet_set = set(alphabet)

        # Crea mapping per ricerca veloce
        self.char_to_idx = {char: idx for idx, char in enumerate(alphabet)}

    def encrypt(self, text: str, key: int) -> str:
        """
        Cripta un testo usando il cifrario di Caesar

        Formula: C = (P + K) mod N
        Dove:
            C = carattere cifrato
            P = carattere in chiaro (plaintext)
            K = chiave (key)
            N = lunghezza dell'alfabeto

        Args:
            text: Testo da criptare
            key: Chiave di cifratura (shift)

        Returns:
            Testo criptato
        """
        result = []
        key = key % self.alphabet_length  # Normalizza la chiave

        for char in text:
            if char in self.alphabet_set:
                # Trova indice carattere
                idx = self.char_to_idx[char]
                # Applica shift con modulo
                new_idx = (idx + key) % self.alphabet_length
                # Aggiungi carattere cifrato
                result.append(self.alphabet[new_idx])
            else:
                # Mantieni spazi, punteggiatura, ecc.
                result.append(char)

        return "".join(result)

    def decrypt(self, text: str, key: int) -> str:
        """
        Decripta un testo cifrato con Caesar

        Formula: P = (C - K) mod N
        Dove:
            P = carattere in chiaro (plaintext)
            C = carattere cifrato
            K = chiave (key)
            N = lunghezza dell'alfabeto

        Args:
            text: Testo da decriptare
            key: Chiave usata per la cifratura

        Returns:
            Testo decriptato
        """
        result = []
        key = key % self.alphabet_length  # Normalizza la chiave

        for char in text:
            if char in self.alphabet_set:
                # Trova indice carattere cifrato
                idx = self.char_to_idx[char]
                # Inverti shift con modulo
                new_idx = (idx - key) % self.alphabet_length
                # Aggiungi carattere in chiaro
                result.append(self.alphabet[new_idx])
            else:
                # Mantieni spazi, punteggiatura, ecc.
                result.append(char)

        return "".join(result)

    def brute_force(self, text: str) -> list:
        """
        Prova tutte le chiavi possibili (brute force)

        Per un alfabeto di N lettere, esistono N-1 chiavi significative
        (la chiave 0 e la chiave N sono equivalenti)

        Args:
            text: Testo cifrato

        Returns:
            Lista di tuple (key, decrypted_text) per ogni chiave possibile
        """
        results = []
        for key in range(1, self.alphabet_length):
            decrypted = self.decrypt(text, key)
            results.append((key, decrypted))

        return results

    def encrypt_with_visual(self, text: str, key: int) -> tuple:
        """
        Cripta testo con rappresentazione visiva del processo

        Args:
            text: Testo da criptare
            key: Chiave di cifratura

        Returns:
            Tuple (encrypted_text, visual_steps)
        """
        key = key % self.alphabet_length
        visual_steps = []

        for i, char in enumerate(text):
            if char in self.alphabet_set:
                idx = self.char_to_idx[char]
                new_idx = (idx + key) % self.alphabet_length
                new_char = self.alphabet[new_idx]

                step = {
                    "position": i + 1,
                    "original": char,
                    "original_idx": idx,
                    "key": key,
                    "operation": f"{idx} + {key} = {idx + key}",
                    "modulo": f"{idx + key} mod {self.alphabet_length} = {new_idx}",
                    "result": new_char,
                }
                visual_steps.append(step)
            else:
                step = {
                    "position": i + 1,
                    "original": char,
                    "original_idx": "N/A",
                    "key": "N/A",
                    "operation": "Non cifrato",
                    "modulo": "Mantenuto",
                    "result": char,
                }
                visual_steps.append(step)

        encrypted = self.encrypt(text, key)
        return encrypted, visual_steps


def caesar_cipher(text: str, key: int, encrypt: bool = True, alphabet: str = None) -> str:
    """
    Funzione helper per cifratura/decifratura rapida

    Args:
        text: Testo da processare
        key: Chiave di cifratura
        encrypt: True per criptare, False per decriptare
        alphabet: Alfabeto da usare (default: inglese)

    Returns:
        Testo processato
    """
    if alphabet is None:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    cipher = CaesarCipher(alphabet)

    if encrypt:
        return cipher.encrypt(text, key)
    else:
        return cipher.decrypt(text, key)
