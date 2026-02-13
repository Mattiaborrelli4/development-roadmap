"""
Demo Script - Secure Notes Manager
Mostra le funzionalità principali senza interazione utente.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from crypto import VaultEncryption, CryptoManager
from password import PasswordStrengthChecker, generate_secure_password
from models.note import Note
from storage import VaultStorage
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def demo_password_strength():
    """Demo: Verifica robustezza password."""
    console.print("\n[bold cyan]=== 1. Verifica Robustezza Password ===[/bold cyan]\n")

    checker = PasswordStrengthChecker()

    passwords = [
        "123",                           # Molto debole
        "password",                      # Debole
        "Password123",                   # Media
        "MySecurePass2024!",            # Buona
        "Tr0ub4dor&Pr3d1cam3nt#99",     # Forte
    ]

    table = Table()
    table.add_column("Password", style="yellow")
    table.add_column("Livello", style="cyan")
    table.add_column("Score", style="green")
    table.add_column("Entropia", style="magenta")

    for pwd in passwords:
        result = checker.check_strength(pwd)
        level_color = "red" if result["level"] in ["MOLTO DEBOLE", "DEBOLE"] else "green"

        table.add_row(
            pwd,
            f"[{level_color}]{result['level']}[/{level_color}]",
            str(result['score']),
            str(result['entropy'])
        )

    console.print(table)


def demo_generate_password():
    """Demo: Generazione password sicura."""
    console.print("\n[bold cyan]=== 2. Generazione Password Sicura ===[/bold cyan]\n")

    for length in [12, 16, 24]:
        password = generate_secure_password(length)
        console.print(f"Length {length:2d}: [green]{password}[/green]")


def demo_encryption():
    """Demo: Crittografia e decrittografia."""
    console.print("\n[bold cyan]=== 3. Crittografia AES con Fernet ===[/bold cyan]\n")

    # Crea crypto manager
    crypto = CryptoManager()

    # Nota di esempio
    note = {
        "id": 1,
        "title": "Password WIFI",
        "content": "SSID: Casa_Nobile - Key: xY7#kL9@mP2",
        "created_at": "2024-02-12",
        "tags": ["wifi", "casa"]
    }

    console.print("[yellow]Nota originale:[/yellow]")
    console.print(f"  {note}\n")

    # Crittografa
    encrypted = crypto.encrypt_note(note)
    console.print(f"[green]✓ Crittografata ({len(encrypted)} bytes)[/green]")
    console.print(f"  Preview: {encrypted[:50]}...\n")

    # Decrittografa
    decrypted = crypto.decrypt_note(encrypted)
    console.print(f"[green]✓ Decrittografata[/green]")
    console.print(f"  {decrypted}\n")

    # Verifica
    if decrypted == note:
        console.print("[green]✅ SUCCESSO: Crittografia/Decrittografia funzionante![/green]\n")
    else:
        console.print("[red]❌ ERRORE: Dati non corrispondono![/red]\n")


def demo_vault_operations():
    """Demo: Operazioni sul vault."""
    console.print("\n[bold cyan]=== 4. Operazioni Vault ===[/bold cyan]\n")

    encryption = VaultEncryption()
    password = "MySecureMasterPassword2024!"

    # Note di esempio
    notes = [
        {
            "id": 1,
            "title": "Password Gmail",
            "content": "email: user@gmail.com, pass: Gm@ilP@ss2024",
            "created_at": "2024-01-15",
            "updated_at": "2024-01-15",
            "tags": ["email", "google"]
        },
        {
            "id": 2,
            "title": "Carta di Credito",
            "content": "Visa **** **** **** 1234, CVV: 123, Exp: 12/25",
            "created_at": "2024-02-01",
            "updated_at": "2024-02-01",
            "tags": ["finanza", "carta"]
        },
        {
            "id": 3,
            "title": "Note Progetto Zeus",
            "content": "Deadline: 15/02/2024, Budget: €50,000",
            "created_at": "2024-02-10",
            "updated_at": "2024-02-10",
            "tags": ["lavoro", "progetto"]
        }
    ]

    # Crea vault
    console.print(f"[yellow]Creazione vault con {len(notes)} note...[/yellow]")
    vault = encryption.create_vault(password, notes)
    console.print("[green]✓ Vault creato[/green]")
    console.print(f"  Salt: {vault['salt'][:30]}...")
    console.print(f"  Iterations: {vault['iterations']}\n")

    # Sblocca vault
    console.print("[yellow]Sblocco vault...[/yellow]")
    unlocked_notes = encryption.unlock_vault(password, vault)
    console.print(f"[green]✓ Vault sbloccato: {len(unlocked_notes)} note recuperate[/green]\n")

    # Mostra note
    table = Table()
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Titolo", style="green")
    table.add_column("Tags", style="magenta")

    for note in unlocked_notes:
        tags = ", ".join(note.get("tags", []))
        table.add_row(str(note["id"]), note["title"], tags)

    console.print(table)
    console.print()

    # Test password errata
    console.print("[yellow]Test con password errata...[/yellow]")
    try:
        encryption.unlock_vault("WrongPassword123!", vault)
        console.print("[red]❌ ERRORE: Dovrebbe fallire![/red]")
    except ValueError as e:
        console.print("[green]✅ SUCCESSO: Password errata rifiutata[/green]\n")


def demo_key_derivation():
    """Demo: Derivazione chiave PBKDF2."""
    console.print("\n[bold cyan]=== 5. Derivazione Chiave PBKDF2 ===[/bold cyan]\n")

    encryption = VaultEncryption()

    password = "MyPassword123!"
    import os
    salt1 = os.urandom(16)
    salt2 = os.urandom(16)

    console.print("[yellow]Password:[/yellow] MyPassword123!")
    console.print(f"[yellow]Salt 1:[/yellow] {salt1.hex()}")
    console.print(f"[yellow]Salt 2:[/yellow] {salt2.hex()}\n")

    # Deriva chiavi
    key1 = encryption.derive_key_from_password(password, salt1)
    key2 = encryption.derive_key_from_password(password, salt2)

    console.print(f"[green]Chiave 1:[/green] {key1.decode()}")
    console.print(f"[green]Chiave 2:[/green] {key2.decode()}\n")

    # Verifica che sale diversi producano chiavi diverse
    if key1 != key2:
        console.print("[green]✅ SUCCESSO: Sale diversi = Chiavi diverse[/green]")
    else:
        console.print("[red]❌ ERRORE: Le chiavi dovrebbero essere diverse![/red]")

    # Verifica determinismo
    key1_again = encryption.derive_key_from_password(password, salt1)
    if key1 == key1_again:
        console.print("[green]✅ SUCCESSO: Stesso salt = Stessa chiave (deterministico)[/green]")
    else:
        console.print("[red]❌ ERRORE: La derivazione dovrebbe essere deterministica![/red]")


def main():
    """Esegui tutte le demo."""
    console.print(Panel.fit(
        "[bold cyan]🔐 SECURE NOTES MANAGER - DEMO[/bold cyan]\n\n"
        "Dimostrazione delle funzionalità di sicurezza",
        border_style="cyan"
    ))

    demo_password_strength()
    demo_generate_password()
    demo_encryption()
    demo_vault_operations()
    demo_key_derivation()

    console.print("\n[bold green]=== Demo Completata ===[/bold green]")
    console.print("\n[yellow]Prova l'applicazione vera:[/yellow]")
    console.print("  1. python main.py init")
    console.print("  2. python main.py unlock\n")


if __name__ == "__main__":
    main()
