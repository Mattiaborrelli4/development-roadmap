"""Modulo di crittografia per il Secure Notes Manager."""
import json
import base64
from typing import Dict, Any, List
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os


class CryptoManager:
    """
    Gestore della crittografia usando Fernet (AES-128 in CBC mode con HMAC).

    AES (Advanced Encryption Standard) è uno standard di crittografia simmetrica:
    - AES-128 usa chiavi di 128 bit (16 bytes)
    - Utilizza Cipher Block Chaining (CBC) mode
    - Include HMAC per autenticazione
    - Fernet garantisce: confidenzialità, integrità, autenticità

    Vantaggi di Fernet:
    1. Implementazione sicura by default
    2. Include HMAC per prevenire tampering
    3. Gestisce automaticamente IV (Initialization Vector)
    4. Usa timestamp per prevenire replay attacks
    """

    def __init__(self, key: bytes = None):
        """
        Inizializza il gestore crittografico.

        Args:
            key: Chiave crittografica (se None, ne genera una nuova)
        """
        if key is None:
            # Genera una nuova chiave
            self.key = Fernet.generate_key()
        else:
            # Assicura che la chiave sia valida
            if len(key) != 44:  # 32 bytes = 44 chars in base64
                raise ValueError("Chiave non valida. Deve essere 44 caratteri base64.")
            self.key = key

        self.fernet = Fernet(self.key)

    @staticmethod
    def generate_key() -> bytes:
        """
        Genera una nuova chiave crittografica casuale.

        Returns:
            Chiave Fernet (32 bytes, URL-safe base64 encoded)
        """
        return Fernet.generate_key()

    def encrypt_note(self, note: Dict[str, Any]) -> bytes:
        """
        Crittografa una nota.

        Args:
            note: Dizionario rappresentante la nota

        Returns:
            Dati crittografati (bytes)

        Esempio:
            >>> note = {"id": 1, "title": "Segreto", "content": "Dati sensibili"}
            >>> encrypted = crypto.encrypt_note(note)
        """
        # Converti il dizionario in JSON string
        json_data = json.dumps(note, ensure_ascii=False)

        # Crittografa i dati
        encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))

        return encrypted_data

    def decrypt_note(self, encrypted_data: bytes) -> Dict[str, Any]:
        """
        Decrittografa una nota.

        Args:
            encrypted_data: Dati crittografati

        Returns:
            Dizionario rappresentante la nota

        Raises:
            InvalidToken: Se la chiave non è corretta o i dati sono corrotti

        Esempio:
            >>> note = crypto.decrypt_note(encrypted_data)
        """
        try:
            # Decrittografa i dati
            decrypted_data = self.fernet.decrypt(encrypted_data)

            # Converti da JSON a dizionario
            note = json.loads(decrypted_data.decode('utf-8'))

            return note

        except InvalidToken as e:
            raise ValueError("Decifratura fallita: Chiave non valida o dati corrotti.") from e
        except json.JSONDecodeError as e:
            raise ValueError("Decifratura fallita: Dati corrotti.") from e

    def encrypt_vault(self, notes: List[Dict[str, Any]]) -> bytes:
        """
        Crittografa l'intero vault (tutte le note).

        Args:
            notes: Lista di note da crittografare

        Returns:
            Dati crittografati (bytes)
        """
        vault_data = {
            "version": "1.0",
            "notes": notes
        }

        json_data = json.dumps(vault_data, ensure_ascii=False)
        encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))

        return encrypted_data

    def decrypt_vault(self, encrypted_data: bytes) -> List[Dict[str, Any]]:
        """
        Decrittografa l'intero vault.

        Args:
            encrypted_data: Dati crittografati

        Returns:
            Lista di note decrittografate

        Raises:
            InvalidToken: Se la chiave non è corretta
        """
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            vault_data = json.loads(decrypted_data.decode('utf-8'))

            return vault_data.get("notes", [])

        except InvalidToken as e:
            raise ValueError("Decifratura vault fallita: Chiave non valida.") from e
        except json.JSONDecodeError as e:
            raise ValueError("Decifratura vault fallita: Dati corrotti.") from e

    def verify_key(self) -> bool:
        """
        Verifica che la chiave sia valida.

        Returns:
            True se la chiave è valida
        """
        try:
            # Tenta di criptare e decriptare un dato di test
            test_data = b"test"
            encrypted = self.fernet.encrypt(test_data)
            decrypted = self.fernet.decrypt(encrypted)
            return decrypted == test_data
        except Exception:
            return False


class VaultEncryption:
    """
    Gestore completo della crittografia del vault.

    Combina PBKDF2 per la derivazione della chiave e Fernet per la crittografia.
    """

    def __init__(self):
        """Inizializza il vault encryption."""
        self.iterations = 100000  # PBKDF2 iterations
        self.salt_length = 16

    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """
        Deriva una chiave crittografica dalla password usando PBKDF2.

        Args:
            password: Password master
            salt: Salt per la derivazione

        Returns:
            Chiave Fernet (44 caratteri base64)
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bit
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key

    def create_vault(self, password: str, notes: List[Dict] = None) -> Dict[str, Any]:
        """
        Crea un nuovo vault crittografato.

        Args:
            password: Password master
            notes: Lista iniziale di note (opzionale)

        Returns:
            Dizionario con salt, hash_password, e encrypted_vault
        """
        # Genera salt
        salt = os.urandom(self.salt_length)

        # Deriva chiave dalla password
        key = self.derive_key_from_password(password, salt)

        # Crea crypto manager
        crypto = CryptoManager(key)

        # Crittografa le note
        if notes is None:
            notes = []

        encrypted_vault = crypto.encrypt_vault(notes)

        return {
            "version": "1.0",
            "salt": base64.b64encode(salt).decode('ascii'),
            "iterations": self.iterations,
            "encrypted_vault": base64.b64encode(encrypted_vault).decode('ascii')
        }

    def unlock_vault(self, password: str, vault_data: Dict[str, Any]) -> List[Dict]:
        """
        Sblocca un vault esistente.

        Args:
            password: Password master
            vault_data: Dati del vault crittografato

        Returns:
            Lista di note decrittografate

        Raises:
            ValueError: Se la password non è corretta
        """
        try:
            # Estrai salt e vault crittografato
            salt = base64.b64decode(vault_data["salt"])
            encrypted_vault = base64.b64decode(vault_data["encrypted_vault"])

            # Deriva la chiave
            key = self.derive_key_from_password(password, salt)

            # Decrittografa il vault
            crypto = CryptoManager(key)
            notes = crypto.decrypt_vault(encrypted_vault)

            return notes

        except Exception as e:
            raise ValueError(f"Impossibile sbloccare il vault: {str(e)}")

    def reencrypt_vault(self, old_password: str, new_password: str,
                       vault_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Re-cripta il vault con una nuova password.

        Args:
            old_password: Vecchia password
            new_password: Nuova password
            vault_data: Dati del vault attuale

        Returns:
            Nuovi dati del vault crittografato
        """
        # Sblocca con la vecchia password
        notes = self.unlock_vault(old_password, vault_data)

        # Crea nuovo vault con la nuova password
        new_vault = self.create_vault(new_password, notes)

        return new_vault
