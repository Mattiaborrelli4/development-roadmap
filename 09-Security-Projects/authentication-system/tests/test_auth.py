"""
Test per il sistema di autenticazione
Esegue test su registration, login, 2FA, password reset
"""

import pytest
import json
from app import create_app, db
from auth.models import User, TwoFactorAuth
from auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


@pytest.fixture
def app():
    """Fixture per l'app Flask"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Fixture per il test client"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Fixture per un utente di test"""
    with app.app_context():
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            is_active=True,
            is_verified=True
        )
        user.set_password('TestPassword123!')
        db.session.add(user)
        db.session.commit()
        return user


# ============================================================================
# TEST PASSWORD HASHING
# ============================================================================

class TestPasswordHashing:
    """Test per hashing password con bcrypt"""

    def test_hash_password(self):
        """Verifica che l'hashing funzioni"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 50  # Bcrypt hash lungo

    def test_verify_password_correct(self):
        """Verifica password corretta"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Verifica password errata"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_hash_is_unique(self):
        """Verifica che password uguali generino hash diversi (salt)"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Stessa password, hash diversi (grazie al salt)
        assert hash1 != hash2
        # Ma entrambi validi
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


# ============================================================================
# TEST JWT TOKENS
# ============================================================================

class TestJWTTokens:
    """Test per JWT tokens"""

    def test_create_token(self, app):
        """Verifica creazione token"""
        with app.app_context():
            token = create_access_token(1)

            assert token is not None
            assert isinstance(token, str)

    def test_verify_token_valid(self, app):
        """Verifica token valido"""
        with app.app_context():
            token = create_access_token(1)
            payload = verify_token(token)

            assert payload is not None
            assert payload['user_id'] == 1
            assert payload['type'] == 'access'

    def test_verify_token_invalid(self, app):
        """Verifica token non valido"""
        with app.app_context():
            payload = verify_token('invalid_token')

            assert payload is None

    def test_token_has_expiration(self, app):
        """Verifica che il token abbia scadenza"""
        with app.app_context():
            from datetime import datetime, timedelta

            token = create_access_token(1)
            payload = verify_token(token)

            assert 'exp' in payload
            assert 'iat' in payload

            # Verifica che scadenza sia nel futuro
            exp_time = datetime.fromtimestamp(payload['exp'])
            assert exp_time > datetime.now()


# ============================================================================
# TEST REGISTRAZIONE
# ============================================================================

class TestRegistration:
    """Test per la registrazione"""

    def test_register_success(self, client):
        """Test registrazione con successo"""
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'first_name': 'New',
            'last_name': 'User'
        })

        data = json.loads(response.data)

        assert response.status_code == 201
        assert data['success'] is True
        assert 'user' in data

    def test_register_missing_fields(self, client):
        """Test registrazione con campi mancanti"""
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com'
        })

        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['success'] is False
        assert 'errors' in data

    def test_register_weak_password(self, client):
        """Test registrazione con password debole"""
        response = client.post('/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'weak'  # Password troppo debole
        })

        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_duplicate_email(self, client, test_user):
        """Test registrazione con email duplicata"""
        response = client.post('/auth/register', json={
            'email': 'test@example.com',  # Già esistente
            'password': 'SecurePassword123!'
        })

        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['success'] is False
        assert 'già registrata' in data['errors'][0].lower()


# ============================================================================
# TEST LOGIN
# ============================================================================

class TestLogin:
    """Test per il login"""

    def test_login_success(self, client, test_user):
        """Test login con successo"""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        })

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert 'access_token' in data
        assert 'refresh_token' in data

    def test_login_wrong_password(self, client, test_user):
        """Test login con password errata"""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword123!'
        })

        data = json.loads(response.data)

        assert response.status_code == 401
        assert data['success'] is False

    def test_login_nonexistent_user(self, client):
        """Test login con utente inesistente"""
        response = client.post('/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'AnyPassword123!'
        })

        data = json.loads(response.data)

        assert response.status_code == 401
        assert data['success'] is False


# ============================================================================
# TEST PROTEZIONE ROTTE
# ============================================================================

class TestProtectedRoutes:
    """Test per le route protette"""

    def test_get_me_without_token(self, client):
        """Test accesso a route protetta senza token"""
        response = client.get('/auth/me')

        assert response.status_code == 401

    def test_get_me_with_valid_token(self, client, app, test_user):
        """Test accesso a route protetta con token valido"""
        with app.app_context():
            token = create_access_token(test_user.id)

        response = client.get('/auth/me', headers={
            'Authorization': f'Bearer {token}'
        })

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert data['user']['email'] == 'test@example.com'

    def test_get_me_with_invalid_token(self, client):
        """Test accesso a route protetta con token non valido"""
        response = client.get('/auth/me', headers={
            'Authorization': 'Bearer invalid_token'
        })

        assert response.status_code == 401


# ============================================================================
# TEST PASSWORD RESET
# ============================================================================

class TestPasswordReset:
    """Test per il reset della password"""

    def test_forgot_password(self, client, test_user):
        """Test richiesta reset password"""
        response = client.post('/auth/forgot-password', json={
            'email': 'test@example.com'
        })

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True

    def test_forgot_password_nonexistent_user(self, client):
        """Test richiesta reset per utente inesistente"""
        response = client.post('/auth/forgot-password', json={
            'email': 'nonexistent@example.com'
        })

        data = json.loads(response.data)

        # Dovrebbe restituire successo per non rivelare se email esiste
        assert response.status_code == 200


# ============================================================================
# TEST RATE LIMITING
# ============================================================================

class TestRateLimiting:
    """Test per il rate limiting"""

    def test_login_rate_limit(self, client, test_user):
        """Test rate limiting su login"""
        # Fai 6 tentativi di login (limite: 5)
        for i in range(6):
            response = client.post('/auth/login', json={
                'email': 'test@example.com',
                'password': 'WrongPassword123!'
            })

        # L'ultimo dovrebbe essere rate limited
        assert response.status_code == 429


# ============================================================================
# TEST 2FA
# ============================================================================

class TestTwoFactorAuth:
    """Test per l'autenticazione a due fattori"""

    def test_enable_2fa(self, client, app, test_user):
        """Test abilitazione 2FA"""
        with app.app_context():
            token = create_access_token(test_user.id)

        response = client.post('/auth/enable-2fa', headers={
            'Authorization': f'Bearer {token}'
        })

        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert 'secret' in data
        assert 'qr_code_uri' in data


# ============================================================================
# FIXTURE AIUTANTI
# ============================================================================

@pytest.fixture
def auth_token(client, app, test_user):
    """Fixture che genera un token di autenticazione"""
    with app.app_context():
        return create_access_token(test_user.id)


@pytest.fixture
def auth_headers(auth_token):
    """Fixture che genera header di autenticazione"""
    return {'Authorization': f'Bearer {auth_token}'}
