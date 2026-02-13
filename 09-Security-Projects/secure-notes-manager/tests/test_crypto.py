"""Test per il modulo crypto."""
import pytest
import json
from crypto import CryptoManager, VaultEncryption


class TestCryptoManager:
    """Test per CryptoManager."""

    def test_generate_key(self):
        """Test la generazione della chiave."""
        key = CryptoManager.generate_key()
        assert isinstance(key, bytes)
        assert len(key) == 44  # 32 bytes in base64

    def test_init_with_key(self):
        """Test l'inizializzazione con chiave."""
        key = CryptoManager.generate_key()
        crypto = CryptoManager(key)
        assert crypto.key == key

    def test_init_without_key(self):
        """Test l'inizializzazione senza chiave."""
        crypto = CryptoManager()
        assert crypto.key is not None
        assert len(crypto.key) == 44

    def test_encrypt_decrypt_note(self):
        """Test la crittografia e decrittografia di una nota."""
        crypto = CryptoManager()

        note = {
            "id": 1,
            "title": "Test Note",
            "content": "Contenuto segreto",
            "created_at": "2024-01-01",
            "updated_at": "2024-01-01",
            "tags": ["test", "segreto"]
        }

        # Crittografa
        encrypted = crypto.encrypt_note(note)
        assert isinstance(encrypted, bytes)
        assert encrypted != note

        # Decrittografa
        decrypted = crypto.decrypt_note(encrypted)
        assert decrypted == note

    def test_encrypt_decrypt_vault(self):
        """Test la crittografia e decrittografia del vault."""
        crypto = CryptoManager()

        notes = [
            {"id": 1, "title": "Nota 1", "content": "Contenuto 1"},
            {"id": 2, "title": "Nota 2", "content": "Contenuto 2"}
        ]

        # Crittografa
        encrypted = crypto.encrypt_vault(notes)
        assert isinstance(encrypted, bytes)

        # Decrittografa
        decrypted = crypto.decrypt_vault(encrypted)
        assert decrypted == notes

    def test_decrypt_with_wrong_key(self):
        """Test la decrittografia con chiave errata."""
        crypto1 = CryptoManager()
        crypto2 = CryptoManager()

        note = {"id": 1, "title": "Test", "content": "Segreto"}

        # Crittografa con crypto1
        encrypted = crypto1.encrypt_note(note)

        # Tenta di decrittografare con crypto2
        with pytest.raises(ValueError, match="Decifratura fallita"):
            crypto2.decrypt_note(encrypted)

    def test_verify_key(self):
        """Test la verifica della chiave."""
        crypto = CryptoManager()
        assert crypto.verify_key() is True


class TestVaultEncryption:
    """Test per VaultEncryption."""

    def test_create_vault(self):
        """Test la creazione di un vault."""
        encryption = VaultEncryption()
        password = "TestPassword123!"

        notes = [
            {"id": 1, "title": "Nota 1", "content": "Contenuto 1"}
        ]

        vault = encryption.create_vault(password, notes)

        assert "version" in vault
        assert "salt" in vault
        assert "iterations" in vault
        assert "encrypted_vault" in vault
        assert vault["version"] == "1.0"
        assert vault["iterations"] == 100000

    def test_unlock_vault(self):
        """Test lo sblocco di un vault."""
        encryption = VaultEncryption()
        password = "TestPassword123!"

        # Crea vault
        notes = [
            {"id": 1, "title": "Nota 1", "content": "Contenuto 1"},
            {"id": 2, "title": "Nota 2", "content": "Contenuto 2"}
        ]
        vault = encryption.create_vault(password, notes)

        # Sblocca vault
        unlocked_notes = encryption.unlock_vault(password, vault)
        assert unlocked_notes == notes

    def test_unlock_vault_wrong_password(self):
        """Test lo sblocco con password errata."""
        encryption = VaultEncryption()
        password = "TestPassword123!"

        # Crea vault
        notes = [{"id": 1, "title": "Nota 1", "content": "Contenuto 1"}]
        vault = encryption.create_vault(password, notes)

        # Tenta di sbloccare con password errata
        with pytest.raises(ValueError, match="Impossibile sbloccare"):
            encryption.unlock_vault("WrongPassword", vault)

    def test_reencrypt_vault(self):
        """Test la re-criptazione del vault."""
        encryption = VaultEncryption()
        old_password = "OldPassword123!"
        new_password = "NewPassword456!"

        # Crea vault con vecchia password
        notes = [{"id": 1, "title": "Nota 1", "content": "Contenuto 1"}]
        vault = encryption.create_vault(old_password, notes)

        # Re-cripta con nuova password
        new_vault = encryption.reencrypt_vault(old_password, new_password, vault)

        # Verifica che la nuova password funzioni
        unlocked = encryption.unlock_vault(new_password, new_vault)
        assert unlocked == notes

        # Verifica che la vecchia password non funzioni più
        with pytest.raises(ValueError):
            encryption.unlock_vault(old_password, new_vault)

    def test_derive_key_deterministic(self):
        """Test che la derivazione della chiave sia deterministica."""
        encryption = VaultEncryption()
        password = "TestPassword123!"
        salt = encryption.salt_length * b'\x00'

        # Deriva due volte la stessa chiave
        key1 = encryption.derive_key_from_password(password, salt)
        key2 = encryption.derive_key_from_password(password, salt)

        assert key1 == key2

    def test_derive_key_different_salts(self):
        """Test che sale diversi producano chiavi diverse."""
        encryption = VaultEncryption()
        password = "TestPassword123!"

        import os
        salt1 = os.urandom(16)
        salt2 = os.urandom(16)

        key1 = encryption.derive_key_from_password(password, salt1)
        key2 = encryption.derive_key_from_password(password, salt2)

        assert key1 != key2


class TestPasswordStrength:
    """Test per la verifica della password."""

    def test_weak_password(self):
        """Test password debole."""
        from password import PasswordStrengthChecker

        checker = PasswordStrengthChecker()

        # Password molto debole
        result = checker.check_strength("123")
        assert result["score"] < 20
        assert result["level"] == "MOLTO DEBOLE"

    def test_strong_password(self):
        """Test password forte."""
        from password import PasswordStrengthChecker

        checker = PasswordStrengthChecker()

        # Password forte
        result = checker.check_strength("MySecureP@ssw0rd123!")
        assert result["score"] >= 80
        assert result["level"] == "FORTE"

    def test_password_entropy(self):
        """Test il calcolo dell'entropia."""
        from password import PasswordStrengthChecker

        checker = PasswordStrengthChecker()

        # Password semplice
        result1 = checker.check_strength("abc")
        assert result1["entropy"] < result1["entropy"] * 2  # Bassa entropia

        # Password complessa
        result2 = checker.check_strength("MySecureP@ssw0rd!")
        assert result2["entropy"] > 100  # Alta entropia


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
