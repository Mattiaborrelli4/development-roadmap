"""
Configurazione alfabeti per Caesar Cipher
Supporta alfabeti multipli per scopi educativi
"""

# Alfabeto inglese standard
ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Alfabeto italiano (con 21 lettere standard)
ITALIAN_ALPHABET = "ABCDEFGHIILMNOPQRSTVZ"  # J, K, W, X, Y non sono in italiano standard

# Alfabeto italiano completo con lettere straniere (per testi moderni)
ITALIAN_EXTENDED_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Alfabeto minuscolo
ENGLISH_LOWER = "abcdefghijklmnopqrstuvwxyz"
ITALIAN_LOWER = "abcdefghilmnopqrstvz"

# Alfabeti custom per esperimenti educativi
ALPHABETS = {
    "english": ENGLISH_ALPHABET,
    "italian": ITALIAN_ALPHABET,
    "italian_extended": ITALIAN_EXTENDED_ALPHABET,
    "english_lower": ENGLISH_LOWER,
    "italian_lower": ITALIAN_LOWER,
}

DEFAULT_ALPHABET = "english"


def get_alphabet(name: str = None) -> str:
    """
    Ottieni un alfabeto per nome

    Args:
        name: Nome dell'alfabeto ('english', 'italian', etc.)

    Returns:
        Stringa dell'alfabeto richiesto
    """
    if name is None:
        name = DEFAULT_ALPHABET

    return ALPHABETS.get(name.lower(), ENGLISH_ALPHABET)


def list_alphabets() -> dict:
    """Restituisci la lista degli alfabeti disponibili con descrizioni"""
    return {
        "english": "Alfabeto inglese standard (A-Z, 26 lettere)",
        "italian": "Alfabeto italiano classico (21 lettere, senza J,K,W,X,Y)",
        "italian_extended": "Alfabeto italiano esteso con lettere straniere (26 lettere)",
        "english_lower": "Alfabeto inglese minuscolo (a-z)",
        "italian_lower": "Alfabeto italiano minuscolo (21 lettere)",
    }


def validate_key(key: int, alphabet: str) -> bool:
    """
    Valida una chiave per l'alfabeto specificato

    Args:
        key: Chiave di cifratura
        alphabet: Alfabeto da usare

    Returns:
        True se la chiave è valida
    """
    if not isinstance(key, int):
        return False
    if len(alphabet) == 0:
        return False
    # La chiave può essere qualsiasi intero (verrà ridotta con modulo)
    return True
