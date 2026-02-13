"""
CSRF Protection - Cross-Site Request Forgery Protection
Implementa token CSRF per proteggere le richieste POST/PUT/DELETE
"""

import secrets
from flask import session, request
from functools import wraps


# ============================================================================
# CSRF TOKEN GENERATION
# ============================================================================

def generate_csrf_token() -> str:
    """
    Genera un token CSRF sicuro.

    COS'È CSRF:
    - Attack che forza l'utente a eseguire azioni non volute
    - Esempio: utente loggato visita sito malevolo che fa POST
    - Il token previene che altri siti facciano richieste

    IMPLEMENTAZIONE:
    - Token unico per sessione
    - Verificato su richieste state-changing (POST/PUT/DELETE)
    - Inviato come header o in form

    Returns:
        Token CSRF sicuro
    """
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


def validate_csrf_token(token: str) -> bool:
    """
    Valida un token CSRF.

    COME FUNZIONA:
    1. Server genera token e lo salva in session
    2. Client invia token con richiesta
    3. Server verifica che token corrisponda a session

    Args:
        token: Token da validare

    Returns:
        True se valido
    """
    return 'csrf_token' in session and secrets.compare_digest(
        session['csrf_token'],
        token
    )


# ============================================================================
# CSRF DECORATOR
# ============================================================================

def csrf_protect(f):
    """
    Decorator per proteggere le route da CSRF.

    USAGE:
        @app.route('/api/transfer', methods=['POST'])
        @csrf_protect
        def transfer():
            ...

    Il token deve essere inviato come:
    - Header: X-CSRF-Token
    - Form field: csrf_token

    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Solo per richieste state-changing
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            # Ottieni token dall'header
            token = request.headers.get('X-CSRF-Token')

            # Se non nell'header, cerca nel form
            if not token:
                token = request.form.get('csrf_token')

            # Se non nel form, cerca nel JSON
            if not token and request.is_json:
                token = request.get_json().get('csrf_token')

            if not token:
                return {
                    'error': 'Token CSRF mancante',
                    'message': 'CSRF token required'
                }, 403

            if not validate_csrf_token(token):
                return {
                    'error': 'Token CSRF non valido',
                    'message': 'Invalid CSRF token'
                }, 403

        return f(*args, **kwargs)

    return decorated_function


# ============================================================================
# TEMPLATE HELPER
# ============================================================================

def csrf_token_field() -> str:
    """
    Genera un hidden field per form HTML.

    USAGE IN TEMPLATE:
        <form method="POST">
            {{ csrf_token_field() }}
            <!-- other fields -->
        </form>

    Returns:
        HTML input hidden con token
    """
    token = generate_csrf_token()
    return f'<input type="hidden" name="csrf_token" value="{token}">'


# ============================================================================
# AJAX/AXIOS CONFIG
# ============================================================================

def get_csrf_token_meta() -> str:
    """
    Genera meta tag per CSRF (per JavaScript).

    USAGE:
        <head>
            {{ get_csrf_token_meta() }}
        </head>

    In JavaScript:
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    Returns:
        HTML meta tag
    """
    token = generate_csrf_token()
    return f'<meta name="csrf-token" content="{token}">'


# ============================================================================
# DOUBLE SUBMIT COOKIE PATTERN (alternativa)
# ============================================================================

class DoubleSubmitCSRF:
    """
    Implementazione Double Submit Cookie pattern.

    ALTERNATIVA ALLA SESSION:
    - Utile per API stateless
    - Token inviato sia come cookie che header
    - Server verifica che corrispondano

    FLOW:
    1. Client riceve token via cookie
    2. Client legge cookie e lo invia come header
    3. Server verifica cookie == header
    """

    def __init__(self):
        self.cookie_name = 'csrf_token'

    def generate_token(self) -> str:
        """Genera e restituisce token"""
        return secrets.token_hex(32)

    def set_cookie(self, response):
        """Imposta il cookie nella risposta"""
        token = self.generate_token()
        response.set_cookie(
            self.cookie_name,
            token,
            httponly=True,
            secure=True,  # Solo HTTPS
            samesite='Strict'  # Protezione CSRF
        )
        return token

    def validate_request(self, request) -> bool:
        """
        Valida che il token cookie corrisponda all'header.

        Args:
            request: Flask request object

        Returns:
            True se valido
        """
        cookie_token = request.cookies.get(self.cookie_name)
        header_token = request.headers.get('X-CSRF-Token')

        if not cookie_token or not header_token:
            return False

        return secrets.compare_digest(cookie_token, header_token)


double_submit_csrf = DoubleSubmitCSRF()


# ============================================================================
# FLASK-WTF STYLE (se usi Flask-WTF)
# ============================================================================

def init_csrf_protect(app):
    """
    Inizializza CSRF protection per Flask app.

    Da chiamare nella configurazione dell'app.

    Args:
        app: Flask application
    """
    app.jinja_env.globals['csrf_token'] = generate_csrf_token
    app.jinja_env.globals['csrf_token_field'] = csrf_token_field
    app.jinja_env.globals['csrf_token_meta'] = get_csrf_token_meta

    # Aggiungi before_request per validare automaticamente
    @app.before_request
    def csrf_protect_before():
        # Escludi metodi sicuri
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return

        # Escludi API routes se usano JWT
        if request.path.startswith('/api/'):
            # Le API usano JWT, non CSRF
            return

        # Valida token per le altre route
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')

            if not token or not validate_csrf_token(token):
                return {'error': 'Invalid CSRF token'}, 403
