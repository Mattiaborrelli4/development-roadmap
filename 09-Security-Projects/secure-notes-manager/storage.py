"""Gestione dello storage crittografato."""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class VaultStorage:
    """Gestore dello storage del vault crittografato."""

    def __init__(self, vault_path: str = "vault.enc"):
        """
        Inizializza lo storage del vault.

        Args:
            vault_path: Percorso del file vault
        """
        self.vault_path = Path(vault_path)
        self.backup_dir = self.vault_path.parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def vault_exists(self) -> bool:
        """
        Verifica se il vault esiste.

        Returns:
            True se il vault esiste
        """
        return self.vault_path.exists()

    def save_vault(self, vault_data: Dict[str, any]) -> None:
        """
        Salva il vault crittografato su disco.

        Args:
            vault_data: Dati del vault da salvare
        """
        # Crea backup automatico prima di sovrascrivere
        if self.vault_exists():
            self._create_auto_backup()

        # Salva il vault
        with open(self.vault_path, 'w', encoding='utf-8') as f:
            json.dump(vault_data, f, indent=2, ensure_ascii=False)

    def load_vault(self) -> Dict[str, any]:
        """
        Carica il vault crittografato dal disco.

        Returns:
            Dati del vault

        Raises:
            FileNotFoundError: Se il vault non esiste
            ValueError: Se il file è corrotto
        """
        if not self.vault_exists():
            raise FileNotFoundError("Vault non trovato. Usa 'init' per crearne uno.")

        try:
            with open(self.vault_path, 'r', encoding='utf-8') as f:
                vault_data = json.load(f)
            return vault_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Vault corrotto: {str(e)}")

    def export_backup(self, export_path: str, vault_data: Dict[str, any]) -> None:
        """
        Esporta il vault su un file di backup.

        Args:
            export_path: Percorso del file di backup
            vault_data: Dati del vault da esportare
        """
        export_path = Path(export_path)

        # Assicurati che la directory esista
        export_path.parent.mkdir(parents=True, exist_ok=True)

        # Salva il backup
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(vault_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Backup esportato in: {export_path}")

    def import_backup(self, backup_path: str) -> Dict[str, any]:
        """
        Importa un vault da un file di backup.

        Args:
            backup_path: Percorso del file di backup

        Returns:
            Dati del vault importato

        Raises:
            FileNotFoundError: Se il backup non esiste
            ValueError: Se il file è corrotto
        """
        backup_path = Path(backup_path)

        if not backup_path.exists():
            raise FileNotFoundError(f"Backup non trovato: {backup_path}")

        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                vault_data = json.load(f)
            return vault_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Backup corrotto: {str(e)}")

    def _create_auto_backup(self) -> None:
        """Crea un backup automatico del vault attuale."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"auto_backup_{timestamp}.enc"
        backup_path = self.backup_dir / backup_name

        # Copia il vault attuale
        import shutil
        shutil.copy2(self.vault_path, backup_path)

        # Mantieni solo gli ultimi 10 backup automatici
        self._cleanup_old_backups(keep=10)

    def _cleanup_old_backups(self, keep: int = 10) -> None:
        """
        Rimuove i backup automatici più vecchi.

        Args:
            keep: Numero di backup da mantenere
        """
        backups = sorted(self.backup_dir.glob("auto_backup_*.enc"), reverse=True)

        for old_backup in backups[keep:]:
            old_backup.unlink()

    def list_backups(self) -> List[Dict[str, str]]:
        """
        Lista tutti i backup disponibili.

        Returns:
            Lista di dizionari con info sui backup
        """
        backups = []

        # Backup automatici
        for backup_path in sorted(self.backup_dir.glob("auto_backup_*.enc"), reverse=True):
            stat = backup_path.stat()
            backups.append({
                "path": str(backup_path),
                "type": "auto",
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })

        # Backup manuali
        vault_dir = self.vault_path.parent
        for backup_path in sorted(vault_dir.glob("backup_*.enc"), reverse=True):
            stat = backup_path.stat()
            backups.append({
                "path": str(backup_path),
                "type": "manual",
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })

        return backups

    def restore_from_backup(self, backup_path: str) -> None:
        """
        Ripristina il vault da un backup.

        Args:
            backup_path: Percorso del backup da ripristinare

        Raises:
            FileNotFoundError: Se il backup non esiste
        """
        backup_path = Path(backup_path)

        if not backup_path.exists():
            raise FileNotFoundError(f"Backup non trovato: {backup_path}")

        # Crea backup del vault attuale prima di ripristinare
        if self.vault_exists():
            self._create_auto_backup()

        # Copia il backup
        import shutil
        shutil.copy2(backup_path, self.vault_path)

        print(f"✓ Vault ripristinato da: {backup_path}")

    def get_vault_info(self) -> Dict[str, any]:
        """
        Ottiene informazioni sul vault.

        Returns:
            Dizionario con info sul vault
        """
        if not self.vault_exists():
            return {"exists": False}

        stat = self.vault_path.stat()
        return {
            "exists": True,
            "path": str(self.vault_path),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "backups_count": len(list(self.backup_dir.glob("*.enc")))
        }

    def delete_vault(self) -> None:
        """
        Elimina il vault (pericoloso!).

        Procede solo dopo conferma.
        """
        if self.vault_exists():
            # Crea ultimo backup
            self._create_auto_backup()

            # Elimina il vault
            self.vault_path.unlink()
            print(f"✓ Vault eliminato. Backup mantenuto in: {self.backup_dir}")
        else:
            print("Vault non esiste.")


class NoteIndex:
    """
    Indice delle note in memoria (non crittografato).

    Mantiene solo metadati per la ricerca rapida.
    """

    def __init__(self):
        """Inizializza l'indice."""
        self.index: Dict[int, Dict[str, any]] = {}

    def build_index(self, notes: List[Dict]) -> None:
        """
        Costruisce l'indice dalle note.

        Args:
            notes: Lista di note
        """
        self.index = {}

        for note in notes:
            self.index[note["id"]] = {
                "title": note["title"],
                "created": note["created_at"],
                "updated": note["updated_at"],
                "tags": note.get("tags", [])
            }

    def search(self, query: str) -> List[int]:
        """
        Cerca note per titolo o contenuto.

        Args:
            query: Stringa di ricerca

        Returns:
            Lista di ID delle note trovate
        """
        query = query.lower()
        results = []

        for note_id, metadata in self.index.items():
            if query in metadata["title"].lower():
                results.append(note_id)

        return results

    def get_by_tags(self, tags: List[str]) -> List[int]:
        """
        Ottieni note per tag.

        Args:
            tags: Lista di tag da cercare

        Returns:
            Lista di ID delle note
        """
        results = []

        for note_id, metadata in self.index.items():
            note_tags = metadata.get("tags", [])
            if any(tag in note_tags for tag in tags):
                results.append(note_id)

        return results

    def get_next_id(self) -> int:
        """
        Genera il prossimo ID per una nuova nota.

        Returns:
            Nuovo ID
        """
        if not self.index:
            return 1

        return max(self.index.keys()) + 1
