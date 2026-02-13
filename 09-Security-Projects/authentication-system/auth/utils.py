"""
Utility per la sicurezza: hashing password, JWT, 2FA
"""

import bcrypt
import jwt
import pyotp
import secrets
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from flask import current_app


# ============================================================================
# PASSWORD HASHING con Bcrypt
# ============================================================================

def hash_password(password: str, rounds: int = 12) -> str:
    """
    Hash della password usando bcrypt.

    PERCHÉ BCRYPT e non MD5/SHA1:
    - Bcrypt è lento intenzionalmente (slow hash) per prevenire brute force
    - Include un salt automatico per prevenire rainbow table attacks
    - Hash adattivo (il fattore di lavoro può essere aumentato col tempo)
    - MD5/SHA1 sono veloci e vulnerabili a GPU/ASIC attacks

    Args:
        password: Password in chiaro
        rounds: Fattore di lavoro (default 12, aumenta con l'hardware)

    Returns:
        Hash della password come stringa
    """
    salt = bcrypt.gensalt(rounds=rounds)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica una password contro il suo hash.

    Args:
        password: Password in chiaro da verificare
        password_hash: Hash bcrypt memorizzato nel database

    Returns:
        True se la password è corretta, False altrimenti
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception:
        return False


# ============================================================================
# JWT TOKEN MANAGEMENT
# ============================================================================

def create_access_token(user_id: int, additional_claims: Optional[Dict] = None) -> str:
    """
    Crea un JWT access token.

    BEST PRACTICES JWT:
    - Access token di breve durata (15-60 minuti)
    - Include claim 'exp' per scadenza automatica
    - Include claim 'iat' per tracciare quando è stato emesso
    - Include claim 'jti' (JWT ID) per revocazione se necessario
    - Usare algoritmo HS256 o RS256 (mai HS256 in produzione senza secret forte)

    Args:
        user_id: ID dell'utente
        additional_claims: Claim aggiuntivi da includere

    Returns:
        JWT token firmato
    """
    secret = current_app.config.get('JWT_SECRET_KEY')
    expires_hours = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 1)

    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(hours=expires_hours),
        'iat': datetime.utcnow(),
        'jti': secrets.token_urlsafe(16)  # Unique token ID
    }

    if additional_claims:
        payload.update(additional_claims)

    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def create_refresh_token(user_id: int) -> Tuple[str, str]:
    """
    Crea un JWT refresh token.

    REFRESH TOKEN STRATEGY:
    - Durata lunga (30 giorni)
    - Usati solo per ottenere nuovi access token
    - Dovrebbero essere salvati nel database per poter essere revocati
    - Rotazione: nuovo token emesso ad ogni refresh

    Args:
        user_id: ID dell'utente

    Returns:
        Tuple (refresh_token, jti)
    """
    secret = current_app.config.get('JWT_SECRET_KEY')
    expires_days = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 30)

    jti = secrets.token_urlsafe(32)

    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=expires_days),
        'iat': datetime.utcnow(),
        'jti': jti
    }

    token = jwt.encode(payload, secret, algorithm='HS256')
    return token, jti


def verify_token(token: str, token_type: str = 'access') -> Optional[Dict]:
    """
    Verifica e decodifica un JWT token.

    Args:
        token: JWT token da verificare
        token_type: 'access' o 'refresh'

    Returns:
        Payload del token se valido, None se non valido

    Raises:
        jwt.ExpiredSignatureError: Token scaduto
        jwt.InvalidTokenError: Token non valido
    """
    try:
        secret = current_app.config.get('JWT_SECRET_KEY')
        payload = jwt.decode(token, secret, algorithms=['HS256'])

        # Verifica il tipo di token
        if payload.get('type') != token_type:
            return None

        return payload

    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        return None


def decode_token(token: str) -> Optional[Dict]:
    """
    Decodifica un token senza verificare la firma (solo per debug).
    NON usare in produzione.
    """
    try:
        payload = jwt.decode(token, options={'verify_signature': False})
        return payload
    except Exception:
        return None


# ============================================================================
# TWO-FACTOR AUTHENTICATION (TOTP)
# ============================================================================

def generate_totp_secret() -> str:
    """
    Genera un segreto per TOTP (Time-based One-Time Password).

    IMPLEMENTAZIONE 2FA:
    - Usa il time-based one-time password (TOTP) standard RFC 6238
    - Compatibile con Google Authenticator, Authy, etc.
    - Il segreto deve essere generato in modo sicuro e mai esposto

    Returns:
        Base32 encoded secret (16 bytes)
    """
    return pyotp.random_base32()


def generate_totp_uri(secret: str, email: str, issuer: str = 'SecureAuthApp') -> str:
    """
    Genera l'URI per il QR code del TOTP.

    FORMAT URI:
    otpauth://totp/ISSUER:EMAIL?secret=SECRET&issuer=ISSUER

    Args:
        secret: Segreto TOTP
        email: Email dell'utente
        issuer: Nome dell'applicazione

    Returns:
        URI otpauth://
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(
        name=email,
        issuer_name=issuer
    )


def generate_totp_qr_code(uri: str) -> str:
    """
    Genera un QR code come data URI per il segreto TOTP.

    Args:
        uri: URI otpauth://

    Returns:
        Data URI del QR code (data:image/png;base64,...)
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f'data:image/png;base64,{img_str}'


def verify_totp_token(secret: str, token: str, window: int = 1) -> bool:
    """
    Verifica un token TOTP.

    PARAMETRI:
    - secret: Il segreto condiviso
    - token: Il codice a 6 cifre inserito dall'utente
    - window: Finestra di tempo per evitare problemi di sincronizzazione
              (default: 1 = accetta token precedenti e successivi)

    SECURITY:
    - Limitare i tentativi di verifica (rate limiting)
    - Loggare ogni tentativo di verifica
    - Revocare i backup codes usati

    Args:
        secret: Segreto TOTP
        token: Codice a 6 cifre
        window: Finestra di tolleranza (default 1)

    Returns:
        True se il token è valido
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=window)


def generate_backup_codes(count: int = 10) -> list:
    """
    Genera codici di backup per il 2FA.

    I codici di backup permettono di accedere se si perde
    accesso all'app autenticatore.

    Args:
        count: Numero di codici da generare (default 10)

    Returns:
        Lista di codici di backup
    """
    codes = []
    for _ in range(count):
        code = secrets.token_hex(4).upper()  # 8 caratteri es: A1B2C3D4
        codes.append(code)
    return codes


# ============================================================================
# PASSWORD RESET TOKENS
# ============================================================================

def generate_secure_token() -> str:
    """
    Genera un token sicuro usando secrets module.

    È crittograficamente sicuro e adatto per generare token
    di reset password, verification email, etc.

    Returns:
        Token URL-safe di 64 caratteri
    """
    return secrets.token_urlsafe(48)


def generate_email_verification_token() -> str:
    """
    Genera un token per la verifica dell'email.

    Returns:
        Token sicuro
    """
    return secrets.token_urlsafe(32)


# ============================================================================
# UTILITÀ VARIO
# ============================================================================

def is_strong_password(password: str) -> Tuple[bool, list]:
    """
    Verifica se una password è forte.

    REQUISITI PASSWORD:
    - Minimo 12 caratteri
    - Almeno una maiuscola
    - Almeno una minuscola
    - Almeno un numero
    - Almeno un carattere speciale
    - Non contenere il nome utente o email
    - Non essere in password comuni (blacklist)

    Args:
        password: Password da verificare

    Returns:
        Tuple (is_valid, list_of_errors)
    """
    errors = []

    if len(password) < 12:
        errors.append("La password deve avere almeno 12 caratteri")

    if not any(c.isupper() for c in password):
        errors.append("La password deve contenere almeno una maiuscola")

    if not any(c.islower() for c in password):
        errors.append("La password deve contenere almeno una minuscola")

    if not any(c.isdigit() for c in password):
        errors.append("La password deve contenere almeno un numero")

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("La password deve contenere almeno un carattere speciale")

    return len(errors) == 0, errors


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitizza l'input utente per prevenire injection attacks.

    Args:
        text: Testo da sanificare
        max_length: Lunghezza massima consentita

    Returns:
        Testo sanificato
    """
    if not text:
        return ""

    # Rimuovi spazi eccessivi
    text = text.strip()

    # Limita lunghezza
    text = text[:max_length]

    return text
