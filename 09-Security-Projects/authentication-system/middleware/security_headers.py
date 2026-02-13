"""
Security Headers Middleware
Implementa HTTP headers per la sicurezza
"""

from flask import Flask, after_this_request


# ============================================================================
# SECURITY HEADERS
# ============================================================================

def init_security_headers(app: Flask):
    """
    Inizializza i security headers per l'applicazione Flask.

    HEADERS IMPLEMENTATI:
    1. X-Content-Type-Options: nosniff
    2. X-Frame-Options: DENY
    3. X-XSS-Protection: 1; mode=block
    4. Strict-Transport-Security: max-age=31536000; includeSubDomains
    5. Content-Security-Policy: default-src 'self'
    6. Permissions-Policy: controlla le feature del browser
    7. Referrer-Policy: strict-origin-when-cross-origin

    Args:
        app: Flask application
    """

    @app.after_request
    def set_security_headers(response):
        """
        Aggiunge security headers a tutte le risposte.

        SPiegazione dei singoli header:

        1. X-Content-Type-Options: nosniff
           - Previene MIME-type sniffing
           - Il browser non "indovina" il tipo di contenuto

        2. X-Frame-Options: DENY
           - Previene clickjacking
           - Impedisce di essere incluso in iframe

        3. X-XSS-Protection: 1; mode=block
           - Attiva filtro XSS del browser
           - Nota: CSP è più efficace

        4. Strict-Transport-Security (HSTS)
           - Forza HTTPS per 1 anno
           - Include subdomini
           - Previene downgrade attacks

        5. Content-Security-Policy (CSP)
           - Controlla quali risorse possono essere caricate
           - Previene XSS, clickjacking, etc.
           - Permette solo risorse dallo stesso dominio

        6. Permissions-Policy (precedentemente Feature-Policy)
           - Controlla feature browser (geolocation, camera, etc.)
           - Disabilita feature non necessarie

        7. Referrer-Policy
           - Controlla informazioni Referrer inviate
           - Protegge privacy dell'utente
        """

        # X-Content-Type-Options: previene MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # X-Frame-Options: previene clickjacking
        response.headers['X-Frame-Options'] = 'DENY'

        # X-XSS-Protection: filtro XSS browser
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Strict-Transport-Security: forza HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Content-Security-Policy: controlla risorse caricate
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "object-src 'none'; "
        )

        # Permissions-Policy: controlla feature browser
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'magnetometer=(), '
            'gyroscope=(), '
            'fullscreen=(self), '
            'payment=(), '
            'usb=(), '
            'vr=(), '
            'interest-cohort=()'  # Disabilita FLoC
        )

        # Referrer-Policy: controlla referrer
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Cache-Control per pagine sensibili
        if app.config.get('SECURE_CACHE', True):
            # Non cachare pagine con dati sensibili
            if '/auth/' in str(response.headers.get('Location', '')):
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'

        # X-Powered-By: rimuovi informazioni server
        response.headers.pop('X-Powered-By', None)
        response.headers.pop('Server', None)

        return response

    return app


# ============================================================================
# CSP BUILDER UTILITY
# ============================================================================

class CSPBuilder:
    """
    Builder per Content Security Policy personalizzate.

    CSP è una delle difese più efficaci contro XSS.
    Permette di controllare esattamente quali risorse
    possono essere caricate dalla tua applicazione.

    USAGE:
        csp = CSPBuilder()
        csp.add_default_src("'self'")
        csp.add_script_src("'self'", "https://cdn.example.com")
        csp.add_style_src("'self'", "'unsafe-inline'")
        header = csp.build()
    """

    def __init__(self):
        self.directives = {}

    def add_default_src(self, *sources):
        """Default source per tutti i tipi di contenuto"""
        self.directives['default-src'] = sources

    def add_script_src(self, *sources):
        """Sorgenti per JavaScript"""
        self.directives['script-src'] = sources

    def add_style_src(self, *sources):
        """Sorgenti per CSS"""
        self.directives['style-src'] = sources

    def add_img_src(self, *sources):
        """Sorgenti per immagini"""
        self.directives['img-src'] = sources

    def add_font_src(self, *sources):
        """Sorgenti per font"""
        self.directives['font-src'] = sources

    def add_connect_src(self, *sources):
        """Sorgenti per AJAX/WebSocket"""
        self.directives['connect-src'] = sources

    def add_frame_src(self, *sources):
        """Sorgenti per frame/iframe"""
        self.directives['frame-src'] = sources

    def add_frame_ancestors(self, *sources):
        """Chi può includerci in iframe"""
        self.directives['frame-ancestors'] = sources

    def add_form_action(self, *sources):
        """Dove i form possono inviare dati"""
        self.directives['form-action'] = sources

    def add_object_src(self, *sources):
        """Sorgenti per plugin (Flash, etc.)"""
        self.directives['object-src'] = sources

    def add_base_uri(self, *sources):
        """Base URI per relative URLs"""
        self.directives['base-uri'] = sources

    def add_report_uri(self, uri):
        """URI per report violazioni CSP"""
        self.directives['report-uri'] = uri

    def add_report_to(self, endpoint):
        """Report-To endpoint"""
        self.directives['report-to'] = endpoint

    def add_upgrade_insecure_requests(self):
        """Forza upgrade HTTP -> HTTPS"""
        self.directives['upgrade-insecure-requests'] = []

    def add_block_all_mixed_content(self):
        """Blocca contenuti misti HTTP/HTTPS"""
        self.directives['block-all-mixed-content'] = []

    def build(self) -> str:
        """
        Costruisce la stringa CSP.

        Returns:
            Stringa CSP completa
        """
        parts = []
        for directive, sources in self.directives.items():
            if sources:
                parts.append(f"{directive} {' '.join(sources)}")
            else:
                parts.append(directive)

        return '; '.join(parts)


# ============================================================================
# CSP REPORTING
# ============================================================================

def init_csp_reporting(app: Flask, report_endpoint: str = '/api/csp-report'):
    """
    Inizializza il reporting delle violazioni CSP.

    Utile per monitorare e risolvere problemi CSP
    senza bloccare completamente l'applicazione.

    Può essere usato in modalità report-only:

    Content-Security-Policy-Report-Only: ...

    Args:
        app: Flask application
        report_endpoint: Endpoint per ricevere report
    """

    @app.route(report_endpoint, methods=['POST'])
    def csp_report():
        """Endpoint per ricevere report violazioni CSP"""
        import json
        from flask import request, current_app

        # Logga la violazione
        report = request.get_json()
        current_app.logger.warning(f'CSP Violation: {json.dumps(report)}')

        # In produzione, salva in database o invia a servizio monitoring
        # Esempio: Sentry, Datadog, etc.

        return '', 204  # No content

    return app


# ============================================================================
# CORS CONFIGURATION
# ============================================================================

def init_cors(app: Flask, allowed_origins: list = None):
    """
    Configura CORS (Cross-Origin Resource Sharing).

    CORS permette di controllare quali domini possono fare
    richieste alla tua API da browser.

    BEST PRACTICES:
    - Non usare '*' in produzione
    - Specificare domini specifici
    - Usare credentials solo se necessario

    Args:
        app: Flask application
        allowed_origins: Lista di origini permesse
    """

    if allowed_origins is None:
        allowed_origins = ['http://localhost:3000']

    @app.after_request
    def set_cors_headers(response):
        """
        Imposta header CORS.

        CORS HEADERS:
        - Access-Control-Allow-Origin: chi può fare richieste
        - Access-Control-Allow-Methods: metodi permessi
        - Access-Control-Allow-Headers: header permessi
        - Access-Control-Allow-Credentials: permette cookies
        - Access-Control-Max-Age: dura preflight cache
        """
        origin = request.headers.get('Origin')

        # Verifica se l'origine è permessa
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin

        # Metodi permessi
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'

        # Header permessi
        response.headers['Access-Control-Allow-Headers'] = (
            'Content-Type, Authorization, X-CSRF-Token, X-Requested-With'
        )

        # Credentials (cookies, auth headers)
        response.headers['Access-Control-Allow-Credentials'] = 'true'

        # Preflight cache (1 ora)
        response.headers['Access-Control-Max-Age'] = '3600'

        # Expose headers (header che il browser può leggere)
        response.headers['Access-Control-Expose-Headers'] = 'X-Total-Count, X-Page-Count'

        return response

    # Gestisci preflight OPTIONS
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            return response

    return app


# ============================================================================
# RATE LIMITING HEADERS
# ============================================================================

def add_rate_limit_headers(response, limit: int, remaining: int, reset: int):
    """
    Aggiunge header per rate limiting.

    HEADERS:
    - X-RateLimit-Limit: limite massimo
    - X-RateLimit-Remaining: richieste rimaste
    - X-RateLimit-Reset: UNIX timestamp reset

    Utile per i client per implementare backoff.

    Args:
        response: Flask response
        limit: Limite massimo
        remaining: Richieste rimanenti
        reset: Timestamp reset

    Returns:
        Response con headers
    """
    response.headers['X-RateLimit-Limit'] = str(limit)
    response.headers['X-RateLimit-Remaining'] = str(remaining)
    response.headers['X-RateLimit-Reset'] = str(reset)

    # Retry-After se rate limited
    if remaining == 0:
        retry_after = max(0, reset - int(time.time()))
        response.headers['Retry-After'] = str(retry_after)

    return response
