"""
Operazioni sui file per Caesar Cipher
Gestisce lettura e scrittura di file cifrati
"""

from pathlib import Path
from typing import Optional


class CaesarFileHandler:
    """
    Gestore per operazioni di file con cifratura Caesar
    """

    def __init__(self, cipher_instance):
        """
        Inizializza il gestore file

        Args:
            cipher_instance: Istanza di CaesarCipher da usare
        """
        self.cipher = cipher_instance

    def encrypt_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        key: int = 3,
        encoding: str = "utf-8",
    ) -> str:
        """
        Cripta un file

        Args:
            input_path: Percorso del file di input
            output_path: Percorso del file di output (opzionale)
            key: Chiave di cifratura
            encoding: Codifica del file (default: utf-8)

        Returns:
            Percorso del file criptato

        Raises:
            FileNotFoundError: Se il file di input non esiste
        """
        input_path_obj = Path(input_path)

        if not input_path_obj.exists():
            raise FileNotFoundError(f"File non trovato: {input_path}")

        # Genera nome output se non specificato
        if output_path is None:
            output_path = input_path_obj.parent / f"{input_path_obj.stem}_encrypted{input_path_obj.suffix}"

        # Leggi file
        with open(input_path, "r", encoding=encoding) as f:
            content = f.read()

        # Cripta contenuto
        encrypted_content = self.cipher.encrypt(content, key)

        # Scrivi file criptato
        output_path_obj = Path(output_path)
        with open(output_path, "w", encoding=encoding) as f:
            f.write(encrypted_content)

        return str(output_path_obj)

    def decrypt_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        key: int = 3,
        encoding: str = "utf-8",
    ) -> str:
        """
        Decripta un file

        Args:
            input_path: Percorso del file cifrato
            output_path: Percorso del file di output (opzionale)
            key: Chiave di decifratura
            encoding: Codifica del file (default: utf-8)

        Returns:
            Percorso del file decriptato

        Raises:
            FileNotFoundError: Se il file di input non esiste
        """
        input_path_obj = Path(input_path)

        if not input_path_obj.exists():
            raise FileNotFoundError(f"File non trovato: {input_path}")

        # Genera nome output se non specificato
        if output_path is None:
            output_path = input_path_obj.parent / f"{input_path_obj.stem}_decrypted{input_path_obj.suffix}"

        # Leggi file
        with open(input_path, "r", encoding=encoding) as f:
            content = f.read()

        # Decripta contenuto
        decrypted_content = self.cipher.decrypt(content, key)

        # Scrivi file decriptato
        output_path_obj = Path(output_path)
        with open(output_path, "w", encoding=encoding) as f:
            f.write(decrypted_content)

        return str(output_path_obj)

    def brute_force_file(
        self,
        input_path: str,
        output_dir: Optional[str] = None,
        encoding: str = "utf-8",
    ) -> list:
        """
        Prova tutte le chiavi su un file cifrato

        Args:
            input_path: Percorso del file cifrato
            output_dir: Directory per i file di output (opzionale)
            encoding: Codifica del file (default: utf-8)

        Returns:
            Lista di tuple (key, output_path)
        """
        input_path_obj = Path(input_path)

        if not input_path_obj.exists():
            raise FileNotFoundError(f"File non trovato: {input_path}")

        # Crea directory output se necessario
        if output_dir is None:
            output_dir = input_path_obj.parent / "brute_force_results"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Leggi file
        with open(input_path, "r", encoding=encoding) as f:
            content = f.read()

        # Prova tutte le chiavi
        results = []
        brute_force = self.cipher.brute_force(content)

        for key, decrypted_content in brute_force:
            output_filename = f"key_{key:02d}_{input_path_obj.stem}{input_path_obj.suffix}"
            output_path = output_dir / output_filename

            with open(output_path, "w", encoding=encoding) as f:
                f.write(decrypted_content)

            results.append((key, str(output_path)))

        return results

    def get_file_info(self, file_path: str, encoding: str = "utf-8") -> dict:
        """
        Ottieni informazioni su un file

        Args:
            file_path: Percorso del file
            encoding: Codifica del file (default: utf-8)

        Returns:
            Dizionario con informazioni sul file
        """
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            raise FileNotFoundError(f"File non trovato: {file_path}")

        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()

        return {
            "path": str(file_path_obj.absolute()),
            "name": file_path_obj.name,
            "size_bytes": file_path_obj.stat().st_size,
            "size_chars": len(content),
            "size_lines": len(content.splitlines()),
            "extension": file_path_obj.suffix,
        }

    def create_sample_file(self, output_path: str, content: str, encoding: str = "utf-8") -> str:
        """
        Crea un file di esempio per test

        Args:
            output_path: Percorso del file da creare
            content: Contenuto del file
            encoding: Codifica del file (default: utf-8)

        Returns:
            Percorso del file creato
        """
        output_path_obj = Path(output_path)

        # Crea directory se necessario
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Scrivi file
        with open(output_path, "w", encoding=encoding) as f:
            f.write(content)

        return str(output_path_obj)
