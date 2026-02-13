"""Secure Notes Manager - CLI principale."""
import os
import sys
import getpass
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from crypto import VaultEncryption
from storage import VaultStorage
from password import PasswordStrengthChecker, generate_secure_password
from models.note import Note


console = Console()


class SecureNotesManager:
    """Gestore principale delle note sicure."""

    def __init__(self, vault_path: str = "vault.enc"):
        """
        Inizializza il gestore.

        Args:
            vault_path: Percorso del vault
        """
        self.vault_path = vault_path
        self.storage = VaultStorage(vault_path)
        self.encryption = VaultEncryption()
        self.password_checker = PasswordStrengthChecker()
        self.unlocked_notes = []
        self.master_password = None

    def init_vault(self, password: str) -> bool:
        """
        Inizializza un nuovo vault.

        Args:
            password: Password master

        Returns:
            True se l'inizializzazione ha successo
        """
        if self.storage.vault_exists():
            console.print("[red]Errore: Il vault esiste già![/red]")
            return False

        # Verifica la robustezza della password
        strength = self.password_checker.check_strength(password)
        if strength["score"] < 40:
            console.print(f"[red]Password troppo debole ({strength['level']}).[/red]")
            console.print("[yellow]Suggerimenti:[/yellow]")
            for feedback in strength["feedback"]:
                console.print(f"  • {feedback}")

            if not Confirm.ask("Vuoi procedere comunque?", default=False):
                return False

        # Crea il vault
        try:
            vault_data = self.encryption.create_vault(password)
            self.storage.save_vault(vault_data)
            self.master_password = password
            self._reload_notes()

            console.print("[green]✓ Vault inizializzato con successo![/green]")
            console.print(f"[cyan]Vault salvato in: {self.vault_path}[/cyan]")
            return True

        except Exception as e:
            console.print(f"[red]Errore durante l'inizializzazione: {str(e)}[/red]")
            return False

    def unlock_vault(self, password: str) -> bool:
        """
        Sblocca il vault.

        Args:
            password: Password master

        Returns:
            True se lo sblocco ha successo
        """
        try:
            vault_data = self.storage.load_vault()
            self.unlocked_notes = self.encryption.unlock_vault(password, vault_data)
            self.master_password = password
            console.print("[green]✓ Vault sbloccato![/green]")
            return True

        except ValueError as e:
            console.print(f"[red]Password non valida o vault corrotto.[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def add_note(self, title: str, content: str, tags: Optional[list] = None) -> bool:
        """
        Aggiunge una nuova nota.

        Args:
            title: Titolo della nota
            content: Contenuto della nota
            tags: Tag opzionali

        Returns:
            True se l'aggiunta ha successo
        """
        if not self._is_unlocked():
            return False

        try:
            # Genera nuovo ID
            note_ids = [note.get("id", 0) for note in self.unlocked_notes]
            new_id = max(note_ids) + 1 if note_ids else 1

            # Crea la nota
            note = Note(
                id=new_id,
                title=title,
                content=content,
                created_at=Note.__dict__.__get__("__data_fields__", {}).get("created_at", ""),
                updated_at=Note.__dict__.__get__("__data_fields__", {}).get("updated_at", ""),
                tags=tags or []
            )

            # Aggiungi timestamp
            from datetime import datetime
            now = datetime.now().isoformat()
            note.created_at = now
            note.updated_at = now

            # Aggiungi alla lista
            self.unlocked_notes.append(note.to_dict())

            # Salva il vault
            self._save_vault()

            console.print(f"[green]✓ Nota aggiunta con ID: {new_id}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def list_notes(self) -> None:
        """Lista tutte le note."""
        if not self._is_unlocked():
            return

        if not self.unlocked_notes:
            console.print("[yellow]Nessuna nota presente.[/yellow]")
            return

        # Crea tabella
        table = Table(title="📝 Note Sicure")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Titolo", style="green")
        table.add_column("Creato", style="blue")
        table.add_column("Tags", style="magenta")

        for note in self.unlocked_notes:
            tags_str = ", ".join(note.get("tags", []))
            table.add_row(
                str(note["id"]),
                note["title"],
                note["created_at"][:10],
                tags_str
            )

        console.print(table)
        console.print(f"\n[cyan]Totale: {len(self.unlocked_notes)} note[/cyan]")

    def view_note(self, note_id: int) -> None:
        """
        Visualizza una nota.

        Args:
            note_id: ID della nota
        """
        if not self._is_unlocked():
            return

        note = self._find_note(note_id)
        if not note:
            console.print(f"[red]Nota con ID {note_id} non trovata.[/red]")
            return

        # Mostra la nota in un panel
        tags_str = ", ".join(note.get("tags", []))
        content = f"""[bold cyan]ID:[/bold cyan] {note['id']}
[bold cyan]Titolo:[/bold cyan] {note['title']}
[bold cyan]Creato:[/bold cyan] {note['created_at']}
[bold cyan]Modificato:[/bold cyan] {note['updated_at']}
[bold cyan]Tags:[/bold cyan] {tags_str if tags_str else 'Nessuno'}

[bold yellow]Contenuto:[/bold yellow]
{note['content']}"""

        console.print(Panel(content, title=f"📄 Nota #{note_id}", border_style="green"))

    def edit_note(self, note_id: int, new_content: str) -> bool:
        """
        Modifica una nota.

        Args:
            note_id: ID della nota
            new_content: Nuovo contenuto

        Returns:
            True se la modifica ha successo
        """
        if not self._is_unlocked():
            return False

        note = self._find_note(note_id)
        if not note:
            console.print(f"[red]Nota con ID {note_id} non trovata.[/red]")
            return False

        try:
            # Aggiorna contenuto e timestamp
            from datetime import datetime
            note["content"] = new_content
            note["updated_at"] = datetime.now().isoformat()

            # Salva il vault
            self._save_vault()

            console.print(f"[green]✓ Nota {note_id} aggiornata![/green]")
            return True

        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def delete_note(self, note_id: int) -> bool:
        """
        Elimina una nota.

        Args:
            note_id: ID della nota

        Returns:
            True se l'eliminazione ha successo
        """
        if not self._is_unlocked():
            return False

        note = self._find_note(note_id)
        if not note:
            console.print(f"[red]Nota con ID {note_id} non trovata.[/red]")
            return False

        # Conferma
        if not Confirm.ask(f"Sei sicuro di voler eliminare la nota '{note['title']}'?"):
            return False

        try:
            self.unlocked_notes.remove(note)
            self._save_vault()

            console.print(f"[green]✓ Nota {note_id} eliminata![/green]")
            return True

        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def search_notes(self, query: str) -> None:
        """
        Cerca note.

        Args:
            query: Stringa di ricerca
        """
        if not self._is_unlocked():
            return

        query = query.lower()
        results = []

        for note in self.unlocked_notes:
            if (query in note["title"].lower() or
                query in note["content"].lower() or
                any(query in tag.lower() for tag in note.get("tags", []))):
                results.append(note)

        if not results:
            console.print(f"[yellow]Nessun risultato per '{query}'[/yellow]")
            return

        # Mostra risultati
        table = Table(title=f"🔍 Risultati per '{query}'")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Titolo", style="green")
        table.add_column("Anteprima", style="yellow")

        for note in results:
            preview = note["content"][:50] + "..." if len(note["content"]) > 50 else note["content"]
            table.add_row(str(note["id"]), note["title"], preview)

        console.print(table)
        console.print(f"\n[cyan]Trovate: {len(results)} note[/cyan]")

    def export_backup(self, export_path: str) -> bool:
        """
        Esporta un backup del vault.

        Args:
            export_path: Percorso del backup

        Returns:
            True se l'esportazione ha successo
        """
        try:
            vault_data = self.storage.load_vault()
            self.storage.export_backup(export_path, vault_data)
            return True

        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def import_backup(self, backup_path: str) -> bool:
        """
        Importa un backup del vault.

        Args:
            backup_path: Percorso del backup

        Returns:
            True se l'importazione ha successo
        """
        try:
            vault_data = self.storage.import_backup(backup_path)
            self.storage.save_vault(vault_data)
            console.print(f"[green]✓ Backup importato![/green]")
            console.print("[yellow]Usa 'unlock' per accedere alle note.[/yellow]")
            return True

        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def change_password(self, new_password: str) -> bool:
        """
        Cambia la password master.

        Args:
            new_password: Nuova password

        Returns:
            True se il cambio ha successo
        """
        if not self._is_unlocked():
            return False

        # Verifica robustezza nuova password
        strength = self.password_checker.check_strength(new_password)
        if strength["score"] < 40:
            console.print(f"[red]Password troppo debole ({strength['level']}).[/red]")
            return False

        try:
            vault_data = self.storage.load_vault()
            new_vault = self.encryption.reencrypt_vault(
                self.master_password, new_password, vault_data
            )
            self.storage.save_vault(new_vault)
            self.master_password = new_password

            console.print("[green]✓ Password cambiata con successo![/green]")
            return True

        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")
            return False

    def _find_note(self, note_id: int) -> Optional[dict]:
        """
        Trova una nota per ID.

        Args:
            note_id: ID della nota

        Returns:
            La nota o None
        """
        for note in self.unlocked_notes:
            if note["id"] == note_id:
                return note
        return None

    def _is_unlocked(self) -> bool:
        """Verifica se il vault è sbloccato."""
        if self.master_password is None:
            console.print("[red]Vault non sbloccato. Usa prima 'unlock'[/red]")
            return False
        return True

    def _save_vault(self) -> None:
        """Salva il vault crittografato."""
        vault_data = self.encryption.create_vault(
            self.master_password, self.unlocked_notes
        )
        self.storage.save_vault(vault_data)

    def _reload_notes(self) -> None:
        """Ricarica le note dal vault."""
        if self.master_password:
            vault_data = self.storage.load_vault()
            self.unlocked_notes = self.encryption.unlock_vault(
                self.master_password, vault_data
            )


# CLI
@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Secure Notes Manager - Gestore di note crittografate con AES-256."""
    pass


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
def init(vault):
    """Inizializza un nuovo vault."""
    manager = SecureNotesManager(vault)

    # Richiedi password
    password = Prompt.ask("Password master", password=True)
    confirm = Prompt.ask("Conferma password", password=True)

    if password != confirm:
        console.print("[red]Le password non corrispondono![/red]")
        sys.exit(1)

    # Inizializza
    if manager.init_vault(password):
        console.print("\n[green]Vault creato con successo![/green]")
        console.print("[cyan]Usa 'unlock' per accedere alle note.[/cyan]")


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
def unlock(vault):
    """Sblocca il vault."""
    manager = SecureNotesManager(vault)

    password = Prompt.ask("Password master", password=True)

    if manager.unlock_vault(password):
        # Avvia shell interattiva
        _interactive_shell(manager)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('title')
@click.argument('content')
@click.option('--tags', help='Tag separati da virgola')
def add(vault, title, content, tags):
    """Aggiungi una nuova nota."""
    manager = SecureNotesManager(vault)

    # Sblocca il vault
    password = Prompt.ask("Password master", password=True)
    if not manager.unlock_vault(password):
        sys.exit(1)

    # Parse tags
    tag_list = tags.split(',') if tags else None

    # Aggiungi nota
    manager.add_note(title, content, tag_list)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
def list(vault):
    """Lista tutte le note."""
    manager = SecureNotesManager(vault)

    # Sblocca il vault
    password = Prompt.ask("Password master", password=True)
    if not manager.unlock_vault(password):
        sys.exit(1)

    manager.list_notes()


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('note_id', type=int)
def view(vault, note_id):
    """Visualizza una nota."""
    manager = SecureNotesManager(vault)

    # Sblocca il vault
    password = Prompt.ask("Password master", password=True)
    if not manager.unlock_vault(password):
        sys.exit(1)

    manager.view_note(note_id)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('note_id', type=int)
@click.argument('new_content')
def edit(vault, note_id, new_content):
    """Modifica una nota."""
    manager = SecureNotesManager(vault)

    # Sblocca il vault
    password = Prompt.ask("Password master", password=True)
    if not manager.unlock_vault(password):
        sys.exit(1)

    manager.edit_note(note_id, new_content)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('note_id', type=int)
def delete(vault, note_id):
    """Elimina una nota."""
    manager = SecureNotesManager(vault)

    # Sblocca il vault
    password = Prompt.ask("Password master", password=True)
    if not manager.unlock_vault(password):
        sys.exit(1)

    manager.delete_note(note_id)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('query')
def search(vault, query):
    """Cerca note."""
    manager = SecureNotesManager(vault)

    # Sblocca il vault
    password = Prompt.ask("Password master", password=True)
    if not manager.unlock_vault(password):
        sys.exit(1)

    manager.search_notes(query)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('backup_path')
def export(vault, backup_path):
    """Esporta un backup del vault."""
    manager = SecureNotesManager(vault)
    manager.export_backup(backup_path)


@cli.command()
@click.option('--vault', default='vault.enc', help='Percorso del vault')
@click.argument('backup_path')
def import_backup(vault, backup_path):
    """Importa un backup del vault."""
    manager = SecureNotesManager(vault)
    manager.import_backup(backup_path)


@cli.command()
def generate():
    """Genera una password sicura."""
    length = Prompt.ask("Lunghezza", default=16)
    try:
        length = int(length)
    except ValueError:
        length = 16

    password = generate_secure_password(length)
    console.print(f"\n[green]Password generata:[/green]")
    console.print(Panel(password, title="🔐 Password Sicura", border_style="green"))


def _interactive_shell(manager: SecureNotesManager):
    """Shell interattiva per il vault."""
    console.print("\n[green]✓ Vault sbloccato![/green]")
    console.print("[cyan]Comandi disponibili:[/cyan]")
    console.print("  [yellow]list[/yellow] - Lista note")
    console.print("  [yellow]view <id>[/yellow] - Visualizza nota")
    console.print("  [yellow]add[/yellow] - Aggiungi nota")
    console.print("  [yellow]edit <id>[/yellow] - Modifica nota")
    console.print("  [yellow]delete <id>[/yellow] - Elimina nota")
    console.print("  [yellow]search <query>[/yellow] - Cerca note")
    console.print("  [yellow]quit[/yellow] - Esci\n")

    while True:
        try:
            cmd = Prompt.ask("[bold cyan]secure-notes[/bold cyan]").strip().lower()

            if not cmd:
                continue

            if cmd == "quit" or cmd == "exit":
                console.print("[yellow]Arrivederci![/yellow]")
                break

            elif cmd == "list":
                manager.list_notes()

            elif cmd.startswith("view "):
                try:
                    note_id = int(cmd.split()[1])
                    manager.view_note(note_id)
                except (ValueError, IndexError):
                    console.print("[red]Uso: view <id>[/red]")

            elif cmd == "add":
                title = Prompt.ask("Titolo")
                content = Prompt.ask("Contenuto")
                tags_input = Prompt.ask("Tags (opzionale, separati da virgola)", default="")
                tags = tags_input.split(',') if tags_input else None
                manager.add_note(title, content, tags)

            elif cmd.startswith("edit "):
                try:
                    note_id = int(cmd.split()[1])
                    new_content = Prompt.ask("Nuovo contenuto")
                    manager.edit_note(note_id, new_content)
                except (ValueError, IndexError):
                    console.print("[red]Uso: edit <id>[/red]")

            elif cmd.startswith("delete "):
                try:
                    note_id = int(cmd.split()[1])
                    manager.delete_note(note_id)
                except (ValueError, IndexError):
                    console.print("[red]Uso: delete <id>[/red]")

            elif cmd.startswith("search "):
                query = cmd[7:]
                manager.search_notes(query)

            else:
                console.print(f"[red]Comando non riconosciuto: {cmd}[/red]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Arrivederci![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Errore: {str(e)}[/red]")


if __name__ == "__main__":
    cli()
