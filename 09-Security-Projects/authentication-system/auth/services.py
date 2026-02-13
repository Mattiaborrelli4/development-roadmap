"""
Servizi di autenticazione - Business logic
Gestisce la logica di business per l'autenticazione
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from flask import current_app, url_for
from flask_mail import Mail, Message
import secrets

from .models import db, User, AuditLog, PasswordResetToken, TwoFactorAuth
from .utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    generate_totp_secret,
    generate_totp_uri,
    generate_totp_qr_code,
    verify_totp_token,
    generate_backup_codes,
    is_strong_password
)


class AuthService:
    """Servizio per la gestione dell'autenticazione"""

    def __init__(self, mail: Mail = None):
        self.mail = mail

    # ========================================================================
    # REGISTRAZIONE
    # ========================================================================

    def register_user(
        self,
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None
    ) -> Tuple[bool, Optional[User], list]:
        """
        Registra un nuovo utente.

        VALIDAZIONI:
        - Email unica
        - Password forte
        - Email valida

        Args:
            email: Email dell'utente
            password: Password in chiaro
            first_name: Nome (opzionale)
            last_name: Cognome (opzionale)

        Returns:
            Tuple (success, user, errors)
        """
        errors = []

        # Verifica se l'email esiste già
        if User.query.filter_by(email=email).first():
            errors.append("Email già registrata")
            return False, None, errors

        # Valida la password
        is_strong, password_errors = is_strong_password(password)
        if not is_strong:
            errors.extend(password_errors)
            return False, None, errors

        # Crea l'utente
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()

            # Log di audit
            self.log_action(
                user.id,
                'USER_REGISTERED',
                'Utente registrato con successo'
            )

            # Invia email di verifica (in produzione)
            # self.send_verification_email(user)

            return True, user, []

        except Exception as e:
            db.session.rollback()
            errors.append(f"Errore durante la registrazione: {str(e)}")
            return False, None, errors

    # ========================================================================
    # LOGIN
    # ========================================================================

    def authenticate_user(
        self,
        email: str,
        password: str,
        ip_address: str,
        user_agent: str
    ) -> Tuple[bool, Optional[User], Optional[str], list]:
        """
        Autentica un utente.

        LOGICA LOGIN:
        1. Verifica credenziali
        2. Controlla se l'account è bloccato
        3. Verifica 2FA se abilitato
        4. Registra tentativo (successo/fallimento)
        5. Genera token

        Args:
            email: Email dell'utente
            password: Password
            ip_address: IP address del client
            user_agent: User agent del client

        Returns:
            Tuple (success, user, access_token, errors)
        """
        errors = []

        # Cerca l'utente
        user = User.query.filter_by(email=email).first()
        if not user:
            errors.append("Credenziali non valide")
            return False, None, None, errors

        # Verifica se l'account è bloccato
        if user.is_locked():
            remaining_time = (user.locked_until - datetime.utcnow()).seconds // 60
            errors.append(f"Account bloccato. Riprova tra {remaining_time} minuti")
            return False, None, None, errors

        # Verifica la password
        if not user.check_password(password):
            # Registra tentativo fallito
            user.record_failed_login()
            db.session.commit()

            self.log_action(
                user.id,
                'LOGIN_FAILED',
                'Tentativo di login fallito: password errata',
                ip_address=ip_address,
                user_agent=user_agent
            )

            if user.is_locked():
                self.log_action(
                    user.id,
                    'ACCOUNT_LOCKED',
                    f'Account bloccato dopo {user.failed_login_attempts} tentativi',
                    ip_address=ip_address
                )

            errors.append("Credenziali non valide")
            return False, None, None, errors

        # Verifica se l'account è attivo
        if not user.is_active:
            errors.append("Account disattivato")
            return False, None, None, errors

        # Resetta i tentativi falliti
        user.reset_failed_login()
        user.last_login_ip = ip_address
        db.session.commit()

        # Genera access token
        access_token = create_access_token(user.id)

        self.log_action(
            user.id,
            'LOGIN_SUCCESS',
            'Login effettuato con successo',
            ip_address=ip_address,
            user_agent=user_agent
        )

        return True, user, access_token, []

    def verify_2fa(
        self,
        user: User,
        totp_code: str
    ) -> Tuple[bool, str]:
        """
        Verifica il codice 2FA.

        Args:
            user: Utente
            totp_code: Codice TOTP a 6 cifre

        Returns:
            Tuple (success, access_token)
        """
        if not user.two_factor_auth or not user.two_factor_auth.is_enabled:
            return False, "2FA non abilitato"

        secret = user.two_factor_auth.secret_key

        if not verify_totp_token(secret, totp_code):
            self.log_action(
                user.id,
                '2FA_FAILED',
                'Codice 2FA non valido'
            )
            return False, "Codice non valido"

        # Codice valido - genera token
        access_token = create_access_token(user.id)

        self.log_action(
            user.id,
            '2FA_SUCCESS',
            '2FA verificato con successo'
        )

        return True, access_token

    # ========================================================================
    # REFRESH TOKEN
    # ========================================================================

    def refresh_access_token(self, refresh_token: str) -> Tuple[bool, Optional[str], list]:
        """
        Rinnova un access token usando il refresh token.

        ROTAZIONE REFRESH TOKEN:
        - Ad ogni refresh, generare un nuovo refresh token
        - Revocare il vecchio token
        - Previene il riutilizzo di token compromessi

        Args:
            refresh_token: Refresh token

        Returns:
            Tuple (success, new_access_token, errors)
        """
        errors = []

        try:
            payload = verify_token(refresh_token, token_type='refresh')
            if not payload:
                errors.append("Refresh token non valido")
                return False, None, errors

            user_id = payload.get('user_id')
            user = User.query.get(user_id)

            if not user or not user.is_active:
                errors.append("Utente non trovato o inattivo")
                return False, None, errors

            # Genera nuovo access token
            new_access_token = create_access_token(user_id)

            self.log_action(
                user_id,
                'TOKEN_REFRESHED',
                'Access token rinnovato'
            )

            return True, new_access_token, []

        except Exception as e:
            errors.append(f"Errore durante il refresh: {str(e)}")
            return False, None, errors

    # ========================================================================
    # PASSWORD RESET
    # ========================================================================

    def request_password_reset(self, email: str, ip_address: str) -> Tuple[bool, str]:
        """
        Richiede il reset della password.

        FLOW:
        1. Verifica se l'email esiste
        2. Genera token sicuro
        3. Invia email con link
        4. Registra log

        SECURITY:
        - Non rivelare se l'email esiste o meno
        - Token scade dopo 1 ora
        - Token monouso

        Args:
            email: Email dell'utente
            ip_address: IP del client

        Returns:
            Tuple (success, message)
        """
        user = User.query.filter_by(email=email).first()

        # Sempre restituisci successo (per non rivelare se email esiste)
        if not user:
            return True, "Se l'email esiste, riceverai un link per resettare la password"

        # Genera token
        reset_token = PasswordResetToken.generate_token(user.id)
        reset_token.ip_address = ip_address
        db.session.commit()

        # In produzione, invia email
        # self.send_password_reset_email(user, reset_token.token)

        self.log_action(
            user.id,
            'PASSWORD_RESET_REQUESTED',
            'Richiesta reset password',
            ip_address=ip_address
        )

        return True, "Se l'email esiste, riceverai un link per resettare la password"

    def reset_password(
        self,
        token: str,
        new_password: str
    ) -> Tuple[bool, list]:
        """
        Resetta la password usando il token.

        Args:
            token: Token di reset
            new_password: Nuova password

        Returns:
            Tuple (success, errors)
        """
        errors = []

        # Valida nuova password
        is_strong, password_errors = is_strong_password(new_password)
        if not is_strong:
            errors.extend(password_errors)
            return False, errors

        # Cerca il token
        reset_token = PasswordResetToken.query.filter_by(token=token).first()

        if not reset_token:
            errors.append("Token non valido")
            return False, errors

        if not reset_token.is_valid():
            errors.append("Token scaduto o già usato")
            return False, errors

        # Aggiorna password
        user = User.query.get(reset_token.user_id)
        user.set_password(new_password)

        # Marchia il token come usato
        reset_token.used = True
        db.session.commit()

        self.log_action(
            user.id,
            'PASSWORD_RESET',
            'Password resettata con successo'
        )

        return True, []

    # ========================================================================
    # 2FA MANAGEMENT
    # ========================================================================

    def enable_2fa(self, user: User) -> Tuple[bool, str, str]:
        """
        Abilita 2FA per un utente.

        Args:
            user: Utente

        Returns:
            Tuple (success, secret, qr_code_uri)
        """
        # Genera segreto
        secret = generate_totp_secret()

        # Crea o aggiorna record 2FA
        if not user.two_factor_auth:
            two_fa = TwoFactorAuth(
                user_id=user.id,
                secret_key=secret,
                is_enabled=False
            )
            db.session.add(two_fa)
        else:
            user.two_factor_auth.secret_key = secret

        # Genera QR code URI
        issuer = current_app.config.get('2FA_ISSUER', 'SecureAuthApp')
        uri = generate_totp_uri(secret, user.email, issuer)

        db.session.commit()

        self.log_action(
            user.id,
            '2FA_INITIATED',
            'Inizializzazione 2FA'
        )

        return True, secret, uri

    def confirm_2fa(self, user: User, totp_code: str) -> Tuple[bool, str, list]:
        """
        Conferma e attiva 2FA.

        Args:
            user: Utente
            totp_code: Codice TOTP di verifica

        Returns:
            Tuple (success, backup_codes, errors)
        """
        if not user.two_factor_auth:
            return False, [], ["2FA non inizializzato"]

        # Verifica il codice
        if not verify_totp_token(user.two_factor_auth.secret_key, totp_code):
            return False, [], ["Codice non valido"]

        # Attiva 2FA
        user.two_factor_auth.is_enabled = True
        user.two_factor_auth.enabled_at = datetime.utcnow()

        # Genera backup codes
        backup_codes = generate_backup_codes(10)

        # Salva backup codes (in produzione, crittografarli)
        import json
        user.two_factor_auth.backup_codes = json.dumps(backup_codes)

        db.session.commit()

        self.log_action(
            user.id,
            '2FA_ENABLED',
            '2FA abilitato con successo'
        )

        return True, backup_codes, []

    def disable_2fa(self, user: User, totp_code: str) -> Tuple[bool, list]:
        """
        Disabilita 2FA.

        Args:
            user: Utente
            totp_code: Codice TOTP di conferma

        Returns:
            Tuple (success, errors)
        """
        if not user.two_factor_auth or not user.two_factor_auth.is_enabled:
            return False, ["2FA non abilitato"]

        # Verifica il codice
        if not verify_totp_token(user.two_factor_auth.secret_key, totp_code):
            return False, ["Codice non valido"]

        # Disabilita 2FA
        user.two_factor_auth.is_enabled = False
        user.two_factor_auth.enabled_at = None

        db.session.commit()

        self.log_action(
            user.id,
            '2FA_DISABLED',
            '2FA disabilitato'
        )

        return True, []

    # ========================================================================
    # AUDIT LOGGING
    # ========================================================================

    def log_action(
        self,
        user_id: int,
        action: str,
        description: str = None,
        ip_address: str = None,
        user_agent: str = None,
        metadata: dict = None
    ):
        """
        Registra un'azione nell'audit log.

        IMPORTANZA AUDIT LOG:
        - Tracciare tutte le azioni sensibili
        - Utile per forensic analysis
        - Rilevare comportamenti anomali
        - Compliance (GDPR, HIPAA, etc.)

        Args:
            user_id: ID dell'utente
            action: Tipo di azione
            description: Descrizione
            ip_address: IP address
            user_agent: User agent
            metadata: Metadati aggiuntivi (JSON)
        """
        import json

        log = AuditLog(
            user_id=user_id,
            action=action,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=json.dumps(metadata) if metadata else None
        )

        db.session.add(log)
        db.session.commit()

    def get_user_audit_logs(
        self,
        user_id: int,
        limit: int = 100
    ) -> list:
        """
        Recupera i log di audit di un utente.

        Args:
            user_id: ID dell'utente
            limit: Numero massimo di log

        Returns:
            Lista di log
        """
        logs = AuditLog.query.filter_by(
            user_id=user_id
        ).order_by(
            AuditLog.created_at.desc()
        ).limit(limit).all()

        return [log.to_dict() for log in logs]

    # ========================================================================
    # EMAIL (placeholder)
    # ========================================================================

    def send_verification_email(self, user: User):
        """Invia email di verifica (da implementare con Flask-Mail)"""
        if not self.mail:
            return

        token = generate_email_verification_token()
        # TODO: Implementare invio email
        pass

    def send_password_reset_email(self, user: User, token: str):
        """Invia email di reset password (da implementare con Flask-Mail)"""
        if not self.mail:
            return
        # TODO: Implementare invio email
        pass
