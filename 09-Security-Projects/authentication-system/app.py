"""
Secure Authentication System - Flask Application
Sistema di autenticazione production-ready con Flask
"""

import os
from datetime import timedelta
from flask import Flask, render_template, jsonify
from flask_mail import Mail
from flask_migrate import Migrate
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Importa moduli
from auth.models import db, User
from auth.routes import auth_bp
from auth.services import AuthService
from middleware.security_headers import init_security_headers

# Inizializza estensioni
mail = Mail()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Factory pattern per creare l'app Flask.

    Args:
        config_name: Ambiente ('development', 'production', 'testing')

    Returns:
        Flask application configurata
    """
    app = Flask(__name__)

    # Configurazione
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///auth.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 ora
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 giorni

    # Email Configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_FROM', 'noreply@secureauth.com')

    # Security Configuration
    app.config['BCRYPT_LOG_ROUNDS'] = int(os.getenv('BCRYPT_LOG_ROUNDS', 12))
    app.config['RATE_LIMIT_ENABLED'] = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    app.config['MAX_LOGIN_ATTEMPTS'] = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    app.config['LOCKOUT_DURATION'] = int(os.getenv('LOCKOUT_DURATION', 300))  # 5 minuti

    # 2FA Configuration
    app.config['2FA_ISSUER'] = os.getenv('2FA_ISSUER', 'SecureAuthApp')

    # Production specific settings
    if config_name == 'production':
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Inizializza estensioni
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Inizializza security headers
    init_security_headers(app)

    # Registra blueprint
    app.register_blueprint(auth_bp)

    # Rotte principali
    @app.route('/')
    def index():
        """Homepage"""
        return render_template('login.html')

    @app.route('/health')
    def health_check():
        """Health check endpoint per load balancers"""
        return jsonify({
            'status': 'healthy',
            'service': 'secure-auth-system'
        }), 200

    @app.route('/api/info')
    def api_info():
        """Info API"""
        return jsonify({
            'name': 'Secure Authentication System',
            'version': '1.0.0',
            'endpoints': {
                'register': 'POST /auth/register',
                'login': 'POST /auth/login',
                'logout': 'POST /auth/logout',
                'refresh': 'POST /auth/refresh',
                'forgot_password': 'POST /auth/forgot-password',
                'reset_password': 'POST /auth/reset-password',
                'verify_2fa': 'POST /auth/verify-2fa',
                'enable_2fa': 'POST /auth/enable-2fa (auth required)',
                'disable_2fa': 'POST /auth/disable-2fa (auth required)'
            }
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Non trovato'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Errore interno del server'}), 500

    @app.errorhandler(429)
    def rate_limited(error):
        return jsonify({
            'error': 'Troppe richieste',
            'message': 'Hai superato il limite di richieste. Riprova tra poco.'
        }), 429

    # Crea tabelle database
    with app.app_context():
        db.create_all()

        # Crea utente admin se non esiste (solo per sviluppo)
        if os.getenv('CREATE_ADMIN_USER', 'False').lower() == 'true':
            create_admin_user()

    return app


def create_admin_user():
    """
    Crea un utente admin per lo sviluppo.

    ATTENZIONE: Usare solo in sviluppo!
    """
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'Admin123!@#')

    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_verified=True,
            is_admin=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Admin user creato: {admin_email} / {admin_password}")


# ============================================================================
# CORS CONFIGURATION (per sviluppo)
# ============================================================================

def init_cors(app):
    """Inizializza CORS per l'app"""
    from flask import after_this_request

    @app.after_request
    def add_cors_headers(response):
        # Permetti richieste da qualsiasi origine (solo sviluppo!)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response


# ============================================================================
# SHELL CONTEXT
# ============================================================================

@app.shell_context_processor
def make_shell_context():
    """
    Rende disponibili gli oggetti nell'shell interattiva.

    Usage: flask shell
    """
    return {
        'db': db,
        'User': User,
        'AuthService': AuthService
    }


# ============================================================================
# CLI COMMANDS
# ============================================================================

@app.cli.command()
def init_db():
    """Inizializza il database"""
    db.create_all()
    print('✓ Database inizializzato')


@app.cli.command()
def create_admin():
    """Crea un utente admin"""
    from getpass import getpass

    email = input('Email admin: ')
    password = getpass('Password: ')
    confirm = getpass('Conferma password: ')

    if password != confirm:
        print('❌ Le password non corrispondono')
        return

    if User.query.filter_by(email=email).first():
        print('❌ Utente già esistente')
        return

    admin = User(
        email=email,
        is_active=True,
        is_verified=True,
        is_admin=True
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    print(f'✓ Admin creato: {email}')


@app.cli.command()
def list_users():
    """Lista tutti gli utenti"""
    users = User.query.all()
    for user in users:
        status = '✓' if user.is_active else '✗'
        print(f'{status} {user.email} - Admin: {user.is_admin}')


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))

    # In development, usa HTTPS con certificato auto-firmato
    if os.getenv('FLASK_ENV') == 'development':
        # Per HTTPS in sviluppo, installare pyopenssl:
        # pip install pyopenssl
        try:
            import ssl
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain('cert.pem', 'key.pem')
            app.run(ssl_context=context, debug=True)
        except Exception:
            print("⚠ HTTPS non disponibile, usando HTTP")
            print("⚠ Per HTTPS in sviluppo: pip install pyopenssl")
            app.run(debug=True)
    else:
        # Production
        app.run()
