"""Gestione password e derivazione chiavi."""
import bcrypt
import secrets
import string
import re
from typing import Dict, Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


class PasswordStrengthChecker:
    """Verificatore della robustezza delle password."""

    def __init__(self):
        """Inizializza il verificatore."""
        self.min_length = 8
        self.recommended_length = 12

    def check_strength(self, password: str) -> Dict:
        """
        Verifica la robustezza della password.

        Args:
            password: La password da verificare

        Returns:
            Dizionario con score (0-100), feedback e livello
        """
        score = 0
        feedback = []

        # Controllo lunghezza
        length = len(password)
        if length >= self.recommended_length:
            score += 30
        elif length >= self.min_length:
            score += 15
            feedback.append("Password corta. Usa almeno 12 caratteri.")
        else:
            feedback.append(f"Password troppo corta! Minimo {self.min_length} caratteri.")

        # Controllo maiuscole
        if re.search(r'[A-Z]', password):
            score += 15
        else:
            feedback.append("Aggiungi lettere maiuscole.")

        # Controllo minuscole
        if re.search(r'[a-z]', password):
            score += 15
        else:
            feedback.append("Aggiungi lettere minuscole.")

        # Controllo numeri
        if re.search(r'[0-9]', password):
            score += 15
        else:
            feedback.append("Aggiungi numeri.")

        # Controllo caratteri speciali
        if re.search(r'[^A-Za-z0-9]', password):
            score += 15
        else:
            feedback.append("Aggiungi caratteri speciali (!@#$%^&*).")

        # Bonus per password molto lunghe
        if length >= 16:
            score += 10

        # Calcolo entropia approssimativa
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[^A-Za-z0-9]', password):
            charset_size += 32

        entropy = length * (charset_size.bit_length() - 1) if charset_size > 0 else 0

        # Determina il livello
        if score >= 80:
            level = "FORTE"
        elif score >= 60:
            level = "BUONA"
        elif score >= 40:
            level = "MEDIA"
        elif score >= 20:
            level = "DEBOLE"
        else:
            level = "MOLTO DEBOLE"

        return {
            "score": min(score, 100),
            "level": level,
            "feedback": feedback,
            "entropy": entropy,
            "length": length
        }


class KeyDerivation:
    """Gestione della derivazione delle chiavi con PBKDF2."""

    # PBKDF2 è più sicuro di bcrypt per la derivazione di chiavi crittografiche
    # perché produce un output di lunghezza fissa adatto a Fernet

    def __init__(self, iterations: int = 100000):
        """
        Inizializza la derivazione delle chiavi.

        Args:
            iterations: Numero di iterazioni PBKDF2 (default: 100000)
        """
        self.iterations = iterations
        self.salt_length = 16  # 128 bit

    def generate_salt(self) -> bytes:
        """
        Genera un salt casuale.

        Returns:
            Salt casuale di 16 bytes
        """
        return secrets.token_bytes(self.salt_length)

    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Deriva una chiave crittografica dalla password usando PBKDF2-HMAC-SHA256.

        PBKDF2 (Password-Based Key Derivation Function 2) è importante perché:
        1. Rende gli attacchi brute force molto più lenti
        2. Aggiunge un salt unico per prevenire rainbow table attacks
        3. Utilizza molte iterazioni per rallentare attacchi offline

        Args:
            password: La password master
            salt: Il salt da utilizzare

        Returns:
            Chiave derivata di 32 bytes (URL-safe base64 encoded)
        """
        if len(salt) != self.salt_length:
            raise ValueError(f"Salt deve essere {self.salt_length} bytes")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bit per AES-256
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )

        key = kdf.derive(password.encode('utf-8'))
        # Converti in formato URL-safe base64 per Fernet
        return base64.urlsafe_b64encode(key)

    def hash_password(self, password: str) -> Tuple[bytes, bytes]:
        """
        Hash della password usando bcrypt per la verifica.

        Usa bcrypt perché è specificamente progettato per le password:
        - Adattivo (il fattore di lavoro può essere aumentato)
        - Include salt automaticamente
        - Resiste ad attacchi GPU/ASIC

        Args:
            password: La password da hashare

        Returns:
            Tuple di (salt, hashed_password)
        """
        # Genera un nuovo salt
        salt = self.generate_salt()

        # Usa bcrypt per l'hash
        # Nota: bcrypt ha un limite di 72 caratteri, quindi usiamo solo i primi 72
        password_bytes = password.encode('utf-8')[:72]
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))

        return salt, hashed

    def verify_password(self, password: str, hashed: bytes) -> bool:
        """
        Verifica che la password corrisponda all'hash.

        Args:
            password: La password da verificare
            hashed: L'hash bcrypt memorizzato

        Returns:
            True se la password è corretta
        """
        password_bytes = password.encode('utf-8')[:72]
        return bcrypt.checkpw(password_bytes, hashed)


def generate_secure_password(length: int = 16) -> str:
    """
    Genera una password sicura casuale.

    Args:
        length: Lunghezza della password (default: 16)

    Returns:
        Password sicura casuale
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
