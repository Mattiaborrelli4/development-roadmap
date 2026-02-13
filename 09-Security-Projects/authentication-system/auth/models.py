"""
Modelli del database per il sistema di autenticazione
Include: User, AuditLog, PasswordResetToken, TwoFactorAuth
"""

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()


class User(db.Model):
    """Modello Utente con funzionalità di sicurezza avanzate"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Informazioni profilo
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    # Stato account
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Sicurezza
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    password_changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relazioni
    two_factor_auth = db.relationship('TwoFactorAuth', backref='user', uselist=False, cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', cascade='all, delete-orphan')
    password_reset_tokens = db.relationship('PasswordResetToken', backref='user', cascade='all, delete-orphan')
    refresh_tokens = db.relationship('RefreshToken', backref='user', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Imposta la password usando bcrypt"""
        self.password_hash = generate_password_hash(password)
        self.password_changed_at = datetime.utcnow()

    def check_password(self, password: str) -> bool:
        """Verifica la password"""
        return check_password_hash(self.password_hash, password)

    def is_locked(self) -> bool:
        """Verifica se l'account è bloccato"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def record_failed_login(self):
        """Registra un tentativo di login fallito"""
        self.failed_login_attempts += 1
        # Blocca l'account dopo 5 tentativi
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)

    def reset_failed_login(self):
        """Resetta i tentativi di login falliti dopo un login riuscito"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Converte l'utente in dizionario (senza dati sensibili)"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }


class TwoFactorAuth(db.Model):
    """Modello per l'autenticazione a due fattori (TOTP)"""

    __tablename__ = 'two_factor_auth'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Segreto TOTP (crittografato nel database)
    secret_key = db.Column(db.String(255), nullable=False)
    is_enabled = db.Column(db.Boolean, default=False, nullable=False)

    # Backup codes (crittografati)
    backup_codes = db.Column(db.Text)  # JSON string

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    enabled_at = db.Column(db.DateTime)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'is_enabled': self.is_enabled,
            'created_at': self.created_at.isoformat()
        }


class AuditLog(db.Model):
    """Log di audit per tracciare le azioni degli utenti"""

    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Dettagli dell'azione
    action = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

    # Metadati aggiuntivi (JSON)
    metadata = db.Column(db.Text)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'description': self.description,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat()
        }


class PasswordResetToken(db.Model):
    """Token per il reset della password"""

    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Token sicuro generato casualmente
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # Scadenza (1 ora)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

    # IP address di richiesta
    ip_address = db.Column(db.String(45))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def generate_token(cls, user_id: int) -> 'PasswordResetToken':
        """Genera un token sicuro per il reset della password"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        reset_token = cls(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.session.add(reset_token)
        db.session.commit()

        return reset_token

    def is_valid(self) -> bool:
        """Verifica se il token è valido (non usato e non scaduto)"""
        if self.used:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True


class RefreshToken(db.Model):
    """Token di refresh per il rinnovo dei JWT"""

    __tablename__ = 'refresh_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Token univoco
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # Revocazione
    is_revoked = db.Column(db.Boolean, default=False, nullable=False)
    revoked_at = db.Column(db.DateTime)

    # Informazioni dispositivo
    device_info = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))

    # Timestamps
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def is_valid(self) -> bool:
        """Verifica se il token è valido"""
        if self.is_revoked:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True

    def revoke(self):
        """Revoca il token"""
        self.is_revoked = True
        self.revoked_at = datetime.utcnow()
        db.session.commit()
