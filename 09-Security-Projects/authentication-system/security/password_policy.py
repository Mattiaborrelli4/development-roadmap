"""
Password Policy e Validazione
Definisce i requisiti delle password e la validazione
"""

import re
from typing import Tuple, List


# ============================================================================
# PASSWORD POLICY
# ============================================================================

class PasswordPolicy:
    """
    Policy per le password.

    REQUISITI SICUREZZA:
    - Lunghezza minima 12 caratteri (NIST consiglia 8+)
    - Complessità: maiuscole, minuscole, numeri, speciali
    - Niente informazioni personali
    - Niente password comuni
    - Storia password (non ripetere ultime N)
    - Scadenza periodica (opzionale, dibattuto)

    NIST GUIDELINES 2023:
    - Minimo 8 caratteri (consigliati 12+)
    - Permettere tutti i caratteri Unicode
    - Non forzare rotazione periodica
    - Controllare contro password comuni
    """

    def __init__(
        self,
        min_length: int = 12,
        max_length: int = 128,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digits: bool = True,
        require_special: bool = True,
        special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?",
        check_common_passwords: bool = True
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special = require_special
        self.special_chars = special_chars
        self.check_common_passwords = check_common_passwords

        # Password comuni (semplificato)
        self.common_passwords = {
            'password', 'password123', '12345678', 'qwerty',
            'abc123', 'monkey', 'master', 'dragon', 'letmein',
            'login', 'password1', 'admin', 'welcome', 'football'
        }

    def validate(self, password: str, user_info: dict = None) -> Tuple[bool, List[str]]:
        """
        Valida una password contro la policy.

        Args:
            password: Password da validare
            user_info: Info utente (email, nome) per controlli aggiuntivi

        Returns:
            Tuple (is_valid, list_of_errors)
        """
        errors = []

        # Lunghezza
        if len(password) < self.min_length:
            errors.append(f"La password deve avere almeno {self.min_length} caratteri")

        if len(password) > self.max_length:
            errors.append(f"La password non può superare {self.max_length} caratteri")

        # Complessità
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("La password deve contenere almeno una maiuscola")

        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("La password deve contenere almeno una minuscola")

        if self.require_digits and not re.search(r'\d', password):
            errors.append("La password deve contenere almeno un numero")

        if self.require_special and not re.search(f'[{re.escape(self.special_chars)}]', password):
            errors.append(f"La password deve contenere almeno un carattere speciale ({self.special_chars})")

        # Password comuni
        if self.check_common_passwords and password.lower() in self.common_passwords:
            errors.append("Questa password è troppo comune. Scegline una più sicura.")

        # Controlli con info utente
        if user_info:
            # Verifica che la password non contenga l'email
            email = user_info.get('email', '')
            if email and email.split('@')[0].lower() in password.lower():
                errors.append("La password non può contenere il tuo username/email")

            # Verifica che non contenga il nome
            first_name = user_info.get('first_name', '')
            if first_name and first_name.lower() in password.lower():
                errors.append("La password non può contenere il tuo nome")

            last_name = user_info.get('last_name', '')
            if last_name and last_name.lower() in password.lower():
                errors.append("La password non può contenere il tuo cognome")

        return len(errors) == 0, errors

    def calculate_strength(self, password: str) -> dict:
        """
        Calcola la forza della password.

        Usa un algoritmo semplificato basato su:
        - Entropia
        - Lunghezza
        - Varietà di caratteri

        Args:
            password: Password da analizzare

        Returns:
            Dict con strength score e livello
        """
        score = 0
        feedback = []

        # Lunghezza
        length_score = min(len(password) * 4, 40)
        score += length_score

        # Varietà caratteri
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 15

        # Bonus per caratteri ripetuti (penalità)
        repeated = len(password) - len(set(password))
        if repeated > 0:
            score -= repeated * 2

        # Normalizza score 0-100
        score = max(0, min(100, score))

        # Determina livello
        if score < 30:
            level = "MOLTO DEBOLE"
            feedback.append("La password è molto facile da indovinare")
        elif score < 50:
            level = "DEBOLE"
            feedback.append("La password potrebbe essere indovinata")
        elif score < 70:
            level = "MEDIA"
            feedback.append("La password è accettabile ma può essere migliorata")
        elif score < 90:
            level = "FORTE"
            feedback.append("Buona password")
        else:
            level = "MOLTO FORTE"
            feedback.append("Eccellente password")

        return {
            'score': score,
            'level': level,
            'feedback': feedback
        }


# Istanza globale della policy
password_policy = PasswordPolicy()


# ============================================================================
# FUNZIONI DI VALIDAZIONE
# ============================================================================

def validate_password_input(password: str, user_info: dict = None) -> Tuple[bool, List[str]]:
    """
    Valida una password usando la policy globale.

    Args:
        password: Password da validare
        user_info: Info utente per controlli aggiuntivi

    Returns:
        Tuple (is_valid, errors)
    """
    return password_policy.validate(password, user_info)


def get_password_strength(password: str) -> dict:
    """
    Calcola la forza della password.

    Args:
        password: Password da analizzare

    Returns:
        Dict con strength info
    """
    return password_policy.calculate_strength(password)


def generate_password_suggestion(min_length: int = 16) -> str:
    """
    Genera una password sicura casuale.

    Usa secrets module per sicurezza crittografica.

    Args:
        min_length: Lunghezza minima

    Returns:
        Password generata
    """
    import secrets
    import string

    alphabet = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*()_+-=[]{}|;:,.<>?"
    )

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(min_length))

        # Verifica che soddisfi i requisiti
        is_valid, _ = password_policy.validate(password)
        if is_valid:
            return password


# ============================================================================
# PASSWORD HISTORY (per implementazione con database)
# ============================================================================

class PasswordHistory:
    """
    Gestisce la storia delle password per evitare riutilizzi.

    NIST consiglia di NON forzare la rotazione periodica,
    MA se implementata, mantenere storia di 5-13 password.
    """

    def __init__(self, max_history: int = 10):
        self.max_history = max_history

    def check_reuse(self, current_password_hash: str, history: List[str]) -> bool:
        """
        Verifica se la password è stata usata recentemente.

        Args:
            current_password_hash: Hash della nuova password
            history: Lista di hash precedenti

        Returns:
            True se la password può essere usata (non in storia)
        """
        return current_password_hash not in history

    def add_to_history(self, password_hash: str, history: List[str]) -> List[str]:
        """
        Aggiunge una password alla storia.

        Args:
            password_hash: Hash della password
            history: Storia corrente

        Returns:
            Nuova storia
        """
        new_history = [password_hash] + history
        return new_history[:self.max_history]


password_history = PasswordHistory()


# ============================================================================
# PASSPHRASE SUPPORT (alternativa alle password complesse)
# ============================================================================

def generate_passphrase(word_count: int = 5) -> str:
    """
    Genera una passphrase sicura usando parole casuali.

    VANTAGGI PASSPHRASE:
    - Più facili da ricordare
    - Spesso più sicure di password complesse corte
    - Raccomandate da NIST
    - Esempio: "correct-horse-battery-staple"

    Args:
        word_count: Numero di parole

    Returns:
        Passphrase generata
    """
    import secrets

    # Lista di parole comuni (semplificata)
    word_list = [
        "correct", "horse", "battery", "staple", "apple", "banana",
        "camera", "delta", "eagle", "forest", "guitar", "house",
        "island", "jungle", "kangaroo", "lemon", "mountain", "night",
        "orange", "planet", "quiet", "river", "star", "tree", "umbrella",
        "video", "water", "yellow", "zebra", "brave", "cloud", "dance"
    ]

    words = [secrets.choice(word_list) for _ in range(word_count)]
    return '-'.join(words)


def validate_passphrase(passphrase: str, min_words: int = 4) -> Tuple[bool, List[str]]:
    """
    Valida una passphrase.

    Args:
        passphrase: Passphrase da validare
        min_words: Numero minimo di parole

    Returns:
        Tuple (is_valid, errors)
    """
    errors = []
    words = passphrase.split('-')

    if len(words) < min_words:
        errors.append(f"La passphrase deve contenere almeno {min_words} parole")

    for word in words:
        if len(word) < 4:
            errors.append("Ogni parola deve avere almeno 4 caratteri")

    return len(errors) == 0, errors
