"""
Rotte API per l'autenticazione
"""

from flask import Blueprint, request, jsonify, g
from functools import wraps
import re

from .models import db, User
from .services import AuthService
from .utils import verify_token, sanitize_input
from ..security.rate_limit import rate_limit
from ..security.password_policy import validate_password_input

# Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()


# ============================================================================
# DECORATORI
# ============================================================================

def require_auth(f):
    """Decorator per richiedere autenticazione"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Ottieni token dall'header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Token mancante'}), 401

        # Estrai token (format: Bearer <token>)
        match = re.match(r'Bearer\s+(.+)', auth_header)
        if not match:
            return jsonify({'error': 'Formato token non valido'}), 401

        token = match.group(1)

        # Verifica token
        try:
            payload = verify_token(token)
            if not payload:
                return jsonify({'error': 'Token non valido'}), 401

            # Salva user_id in g per usarlo nelle route
            g.user_id = payload.get('user_id')
            g.user = User.query.get(g.user_id)

            if not g.user or not g.user.is_active:
                return jsonify({'error': 'Utente non trovato o inattivo'}), 401

        except Exception as e:
            return jsonify({'error': f'Token non valido: {str(e)}'}), 401

        return f(*args, **kwargs)

    return decorated_function


# ============================================================================
# ROTTE PUBBLICHE
# ============================================================================

@auth_bp.route('/register', methods=['POST'])
@rate_limit('register', limit=5, period=3600)  # 5 registrazioni/ora
def register():
    """
    Registra un nuovo utente.

    Request Body:
        {
            "email": "user@example.com",
            "password": "SecurePass123!",
            "first_name": "Mario",
            "last_name": "Rossi"
        }

    Response:
        {
            "success": true,
            "user": {...}
        }
    """
    try:
        data = request.get_json()

        # Sanitizza input
        email = sanitize_input(data.get('email', ''), 255).lower()
        password = data.get('password', '')
        first_name = sanitize_input(data.get('first_name', ''), 100)
        last_name = sanitize_input(data.get('last_name', ''), 100)

        # Validazione base
        if not email or not password:
            return jsonify({
                'success': False,
                'errors': ['Email e password sono richiesti']
            }), 400

        # Registra utente
        success, user, errors = auth_service.register_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if not success:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        return jsonify({
            'success': True,
            'message': 'Registrazione completata con successo',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/login', methods=['POST'])
@rate_limit('login', limit=10, period=300)  # 10 tentativi/5 minuti
def login():
    """
    Autentica un utente.

    Request Body:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Response:
        {
            "success": true,
            "access_token": "...",
            "refresh_token": "...",
            "user": {...},
            "requires_2fa": true/false
        }
    """
    try:
        data = request.get_json()

        # Sanitizza input
        email = sanitize_input(data.get('email', ''), 255).lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({
                'success': False,
                'errors': ['Email e password sono richiesti']
            }), 400

        # Autentica utente
        success, user, access_token, errors = auth_service.authenticate_user(
            email=email,
            password=password,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )

        if not success:
            return jsonify({
                'success': False,
                'errors': errors
            }), 401

        # Verifica se richiede 2FA
        requires_2fa = user.two_factor_auth and user.two_factor_auth.is_enabled

        response_data = {
            'success': True,
            'user': user.to_dict(),
            'requires_2fa': requires_2fa
        }

        # Include token solo se 2FA non è abilitato
        if not requires_2fa:
            from .utils import create_refresh_token
            refresh_token, _ = create_refresh_token(user.id)
            response_data['access_token'] = access_token
            response_data['refresh_token'] = refresh_token

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/verify-2fa', methods=['POST'])
@rate_limit('2fa', limit=20, period=300)  # 20 tentativi/5 minuti
def verify_2fa():
    """
    Verifica il codice 2FA durante il login.

    Request Body:
        {
            "email": "user@example.com",
            "totp_code": "123456"
        }

    Response:
        {
            "success": true,
            "access_token": "...",
            "refresh_token": "..."
        }
    """
    try:
        data = request.get_json()

        email = sanitize_input(data.get('email', ''), 255).lower()
        totp_code = sanitize_input(data.get('totp_code', ''), 6)

        if not email or not totp_code:
            return jsonify({
                'success': False,
                'errors': ['Email e codice 2FA sono richiesti']
            }), 400

        # Ottieni utente
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'success': False,
                'errors': ['Utente non trovato']
            }), 404

        # Verifica 2FA
        success, result = auth_service.verify_2fa(user, totp_code)

        if not success:
            return jsonify({
                'success': False,
                'errors': [result]
            }), 401

        # Genera refresh token
        from .utils import create_refresh_token
        access_token = result
        refresh_token, _ = create_refresh_token(user.id)

        return jsonify({
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Rinnova un access token usando il refresh token.

    Request Body:
        {
            "refresh_token": "..."
        }

    Response:
        {
            "success": true,
            "access_token": "..."
        }
    """
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token', '')

        if not refresh_token:
            return jsonify({
                'success': False,
                'errors': ['Refresh token richiesto']
            }), 400

        # Rinnova token
        success, access_token, errors = auth_service.refresh_access_token(refresh_token)

        if not success:
            return jsonify({
                'success': False,
                'errors': errors
            }), 401

        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/forgot-password', methods=['POST'])
@rate_limit('password_reset', limit=3, period=3600)  # 3 richieste/ora
def forgot_password():
    """
    Richiede il reset della password.

    Request Body:
        {
            "email": "user@example.com"
        }

    Response:
        {
            "success": true,
            "message": "..."
        }
    """
    try:
        data = request.get_json()
        email = sanitize_input(data.get('email', ''), 255).lower()

        if not email:
            return jsonify({
                'success': False,
                'errors': ['Email richiesta']
            }), 400

        # Richiedi reset
        success, message = auth_service.request_password_reset(
            email=email,
            ip_address=request.remote_addr
        )

        return jsonify({
            'success': success,
            'message': message
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Resetta la password usando il token ricevuto via email.

    Request Body:
        {
            "token": "...",
            "new_password": "NewSecurePass123!"
        }

    Response:
        {
            "success": true,
            "message": "Password resettata con successo"
        }
    """
    try:
        data = request.get_json()
        token = data.get('token', '')
        new_password = data.get('new_password', '')

        if not token or not new_password:
            return jsonify({
                'success': False,
                'errors': ['Token e nuova password sono richiesti']
            }), 400

        # Reset password
        success, errors = auth_service.reset_password(token, new_password)

        if not success:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        return jsonify({
            'success': True,
            'message': 'Password resettata con successo'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


# ============================================================================
# ROTTE PROTETTE (richiedono autenticazione)
# ============================================================================

@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """
    Ottieni informazioni sull'utente corrente.

    Response:
        {
            "success": true,
            "user": {...}
        }
    """
    return jsonify({
        'success': True,
        'user': g.user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    Logout dell'utente.
    In un'implementazione con database, revoca il refresh token.

    Response:
        {
            "success": true,
            "message": "Logout effettuato"
        }
    """
    # In un'implementazione completa, qui revocheresti il refresh token
    auth_service.log_action(
        g.user_id,
        'LOGOUT',
        'Logout effettuato',
        ip_address=request.remote_addr
    )

    return jsonify({
        'success': True,
        'message': 'Logout effettuato con successo'
    }), 200


@auth_bp.route('/enable-2fa', methods=['POST'])
@require_auth
def enable_2fa():
    """
    Inizializza l'abilitazione del 2FA.

    Response:
        {
            "success": true,
            "secret": "...",
            "qr_code_uri": "..."
        }
    """
    try:
        # Abilita 2FA
        success, secret, qr_uri = auth_service.enable_2fa(g.user)

        if not success:
            return jsonify({
                'success': False,
                'errors': [secret]
            }), 400

        return jsonify({
            'success': True,
            'secret': secret,
            'qr_code_uri': qr_uri,
            'message': 'Scansiona il QR code con Google Authenticator'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/confirm-2fa', methods=['POST'])
@require_auth
def confirm_2fa():
    """
    Conferma l'abilitazione del 2FA inserendo il codice.

    Request Body:
        {
            "totp_code": "123456"
        }

    Response:
        {
            "success": true,
            "backup_codes": ["...", "..."]
        }
    """
    try:
        data = request.get_json()
        totp_code = sanitize_input(data.get('totp_code', ''), 6)

        if not totp_code:
            return jsonify({
                'success': False,
                'errors': ['Codice TOTP richiesto']
            }), 400

        # Conferma 2FA
        success, backup_codes, errors = auth_service.confirm_2fa(g.user, totp_code)

        if not success:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        return jsonify({
            'success': True,
            'backup_codes': backup_codes,
            'message': '2FA abilitato. Salva i codici di backup in un luogo sicuro!'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/disable-2fa', methods=['POST'])
@require_auth
def disable_2fa():
    """
    Disabilita il 2FA.

    Request Body:
        {
            "totp_code": "123456"
        }

    Response:
        {
            "success": true,
            "message": "2FA disabilitato"
        }
    """
    try:
        data = request.get_json()
        totp_code = sanitize_input(data.get('totp_code', ''), 6)

        if not totp_code:
            return jsonify({
                'success': False,
                'errors': ['Codice TOTP richiesto']
            }), 400

        # Disabilita 2FA
        success, errors = auth_service.disable_2fa(g.user, totp_code)

        if not success:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        return jsonify({
            'success': True,
            'message': '2FA disabilitato con successo'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/audit-logs', methods=['GET'])
@require_auth
def get_audit_logs():
    """
    Ottieni i log di audit dell'utente corrente.

    Query params:
        - limit: numero di log (default 100)

    Response:
        {
            "success": true,
            "logs": [...]
        }
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        limit = min(limit, 1000)  # Max 1000

        logs = auth_service.get_user_audit_logs(g.user_id, limit)

        return jsonify({
            'success': True,
            'logs': logs
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """
    Cambia la password dell'utente corrente.

    Request Body:
        {
            "current_password": "...",
            "new_password": "NewSecurePass123!"
        }

    Response:
        {
            "success": true,
            "message": "Password cambiata"
        }
    """
    try:
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'errors': ['Password attuale e nuova sono richieste']
            }), 400

        # Verifica password attuale
        if not g.user.check_password(current_password):
            return jsonify({
                'success': False,
                'errors': ['Password attuale non corretta']
            }), 400

        # Cambia password
        g.user.set_password(new_password)
        db.session.commit()

        auth_service.log_action(
            g.user_id,
            'PASSWORD_CHANGED',
            'Password cambiata dall\'utente',
            ip_address=request.remote_addr
        )

        return jsonify({
            'success': True,
            'message': 'Password cambiata con successo'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Errore del server: {str(e)}']
        }), 500
