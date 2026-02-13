"""
Caesar Cipher Tool - CLI Interface
Interfaccia a riga di comando per il cifrario di Caesar
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from cipher import CaesarCipher, caesar_cipher
from analysis import FrequencyAnalyzer, index_of_coincidence, entropy
from file_ops import CaesarFileHandler
from config import get_alphabet, list_alphabets, ALPHABETS

console = Console()


def print_banner():
    """Stampa il banner del programma"""
    banner = """
    ================================================================
    |                                                               |
    |        [CAESAR CIPHER TOOL]                                   |
    |        Strumento Educativo di Crittografia                     |
    |                                                               |
    |        ATTENZIONE: SOLO PER SCOPI EDUCATIVI                  |
    |        NON usare per sicurezza reale!                         |
    |                                                               |
    ================================================================
    """
    console.print(banner, style="bold cyan")


def print_warning():
    """Stampa avviso educativo"""
    warning = Panel(
        """
        [bold red]ATTENZIONE - IMPORTANTE[/bold red]

        Questo è uno [bold yellow]strumento educativo[/bold yellow] per apprendere la crittografia classica.

        Il cifrario di Caesar [bold red]NON e sicuro[/bold red] per uso moderno:
        * Puo essere craccato in pochi secondi con brute force
        * Esistono solo 25 chiavi possibili (per alfabeto inglese)
        * Vulnerabile ad analisi delle frequenze

        [bold green]Alternative moderne sicure:[/bold green]
        * AES (Advanced Encryption Standard)
        * RSA (Rivest-Shamir-Adleman)
        * ChaCha20, Twofish, ecc.

        Usa questo tool solo per [cyan]apprendimento[/cyan] e [cyan]esperimenti[/cyan]!
        """,
        title="[bold yellow]Avviso Educativo[/bold yellow]",
        border_style="red",
    )
    console.print(warning)


def encrypt_command(args):
    """Gestisce il comando encrypt"""
    cipher = CaesarCipher(get_alphabet(args.alphabet))

    # Cripta il testo
    encrypted = cipher.encrypt(args.text, args.key)

    # Mostra risultato
    result_panel = Panel(
        f"""
        [bold]Testo originale:[/bold]
        {args.text}

        [bold]Chiave:[/bold] {args.key}

        [bold]Testo cifrato:[/bold]
        [cyan]{encrypted}[/cyan]
        """,
        title="[green]Cifratura Completata[/green]",
        border_style="green",
    )
    console.print(result_panel)

    # Mostra processo visivo se richiesto
    if args.visual:
        console.print("\n[bold]Rappresentazione Visiva del Processo:[/bold]\n")
        _, visual_steps = cipher.encrypt_with_visual(args.text, args.key)

        table = Table(title="Processo di Cifratura", box=box.ROUNDED)
        table.add_column("Pos", style="dim")
        table.add_column("Originale")
        table.add_column("Indice")
        table.add_column("Operazione")
        table.add_column("Modulo")
        table.add_column("Risultato", style="cyan")

        for step in visual_steps:
            table.add_row(
                str(step["position"]),
                step["original"],
                str(step["original_idx"]),
                step["operation"],
                step["modulo"],
                step["result"],
            )

        console.print(table)

    # Salva su file se richiesto
    if args.output:
        handler = CaesarFileHandler(cipher)
        handler.create_sample_file(args.output, encrypted)
        console.print(f"\n[green][OK][/green] Salvato in: {args.output}")

    return encrypted


def decrypt_command(args):
    """Gestisce il comando decrypt"""
    cipher = CaesarCipher(get_alphabet(args.alphabet))

    # Decripta il testo
    decrypted = cipher.decrypt(args.text, args.key)

    # Mostra risultato
    result_panel = Panel(
        f"""
        [bold]Testo cifrato:[/bold]
        {args.text}

        [bold]Chiave:[/bold] {args.key}

        [bold]Testo decifrato:[/bold]
        [green]{decrypted}[/green]
        """,
        title="[green]Decifratura Completata[/green]",
        border_style="green",
    )
    console.print(result_panel)

    # Salva su file se richiesto
    if args.output:
        handler = CaesarFileHandler(cipher)
        handler.create_sample_file(args.output, decrypted)
        console.print(f"\n[green][OK][/green] Salvato in: {args.output}")

    return decrypted


def brute_force_command(args):
    """Gestisce il comando brute-force"""
    cipher = CaesarCipher(get_alphabet(args.alphabet))

    console.print(f"\n[bold]Brute Force del testo:[/bold] {args.text}")
    console.print(f"[dim]Alfabeto: {args.alphabet}[/dim]\n")

    # Esegui brute force
    results = cipher.brute_force(args.text)

    # Mostra risultati in tabella
    table = Table(title="Risultati Brute Force", box=box.ROUNDED)
    table.add_column("Chiave", style="cyan")
    table.add_column("Testo Decifrato")

    for key, decrypted in results:
        table.add_row(str(key), decrypted)

    console.print(table)

    # Salva risultati su file se richiesto
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Brute Force Results for: {args.text}\n")
            f.write("=" * 60 + "\n\n")
            for key, decrypted in results:
                f.write(f"Key {key}: {decrypted}\n")

        console.print(f"\n[green][OK][/green] Risultati salvati in: {args.output}")

    return results


def analyze_command(args):
    """Gestisce il comando analyze"""
    # Leggi contenuto (da file o testo)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
        console.print(f"\n[bold]Analisi del file:[/bold] {args.file}")
    else:
        text = args.text
        console.print(f"\n[bold]Analisi del testo:[/bold] {text[:50]}...")

    alphabet = get_alphabet(args.alphabet)
    analyzer = FrequencyAnalyzer(language=args.alphabet)

    # Report frequenze
    freq_report = analyzer.get_frequency_report(text, alphabet)
    console.print(freq_report)

    # Calcola metriche aggiuntive
    ic = index_of_coincidence(text, alphabet)
    ent = entropy(text, alphabet)

    console.print(f"\n[bold]📈 Metriche Aggiuntive:[/bold]")
    console.print(f"  Indice di Coincidenza: {ic:.4f}")
    console.print(f"  Entropia: {ent:.4f} bit")

    if args.alphabet == "english":
        console.print("  [dim](IC atteso per inglese: ~0.0667)[/dim]")
    else:
        console.print("  [dim](IC atteso per italiano: ~0.0738)[/dim]")

    # Trova chiave più probabile se è un testo cifrato
    if args.find_key:
        console.print("\n[bold]Ricerca Chiave Piu Probabile:[/bold]\n")

        cipher = CaesarCipher(alphabet)
        best_key, score, decrypted = analyzer.find_best_key(text, alphabet, cipher.decrypt)

        console.print(f"  Chiave suggerita: [cyan]{best_key}[/cyan]")
        console.print(f"  Chi-quadrato: {score:.2f}")
        console.print(f"  Testo decifrato:\n    [green]{decrypted[:100]}...[/green]")


def encrypt_file_command(args):
    """Gestisce il comando file-encrypt"""
    cipher = CaesarCipher(get_alphabet(args.alphabet))
    handler = CaesarFileHandler(cipher)

    # Mostra info file
    info = handler.get_file_info(args.input)
    console.print(f"\n[bold]File da cifrare:[/bold] {info['name']}")
    console.print(f"  Dimensione: {info['size_chars']} caratteri")

    # Cripta file
    output_path = handler.encrypt_file(args.input, args.output, args.key)

    console.print(f"\n[green][OK][/green] File cifrato salvato in: {output_path}")

    # Mostra anteprima
    with open(args.input, "r", encoding="utf-8") as f:
        original_preview = f.read(100)
    with open(output_path, "r", encoding="utf-8") as f:
        encrypted_preview = f.read(100)

    console.print(f"\n[bold]Anteprima:[/bold]")
    console.print(f"  Originale: {original_preview}...")
    console.print(f"  Cifrato:   [cyan]{encrypted_preview}[/cyan]...")


def decrypt_file_command(args):
    """Gestisce il comando file-decrypt"""
    cipher = CaesarCipher(get_alphabet(args.alphabet))
    handler = CaesarFileHandler(cipher)

    # Mostra info file
    info = handler.get_file_info(args.input)
    console.print(f"\n[bold]File da decifrare:[/bold] {info['name']}")
    console.print(f"  Dimensione: {info['size_chars']} caratteri")

    # Decripta file
    output_path = handler.decrypt_file(args.input, args.output, args.key)

    console.print(f"\n[green][OK][/green] File decifrato salvato in: {output_path}")

    # Mostra anteprima
    with open(output_path, "r", encoding="utf-8") as f:
        decrypted_preview = f.read(100)

    console.print(f"\n[bold]Anteprima:[/bold]")
    console.print(f"  Decifrato: [green]{decrypted_preview}[/green]...")


def info_command(args):
    """Mostra informazioni sul cifrario di Caesar"""
    info = """
    [bold cyan]Storia del Cifrario di Caesar[/bold cyan]

    Il cifrario di Caesar e uno dei piu antichi sistemi di crittografia conosciuti,
    prende il nome da [bold]Gaio Giulio Cesare[/bold], che lo usava per comunicare
    con i suoi generali.

    [yellow]Come Funziona:[/yellow]
    * Ogni lettera del testo viene sostituita da quella che si trova
      un numero fisso di posizioni dopo nell'alfabeto
    * Questo numero fisso e chiamato [bold]"chiave"[/bold] o "shift"
    * Cesare usava tipicamente un shift di 3

    [yellow]Esempio con chiave 3:[/yellow]
    A -> D, B -> E, C -> F, ..., X -> A, Y -> B, Z -> C

    [bold red]Perche NON e Sicuro:[/bold red]

    1. [bold]Spazio delle chiavi limitato[/bold]
       * Solo 25 chiavi possibili (per alfabeto di 26 lettere)
       * Facile da provare tutte (brute force)

    2. [bold]Analisi delle frequenze[/bold]
       * Ogni lingua ha frequenze caratteristiche delle lettere
       * In italiano: E (11.79%), A (11.74%), I (11.28%)
       * Le frequenze restano invariate nel cifrario

    3. [bold]Attacchi con testo noto[/bold]
       * Conoscendo anche solo una parola del testo originale,
         e facile trovare la chiave

    [yellow]Matematica:[/yellow]

    Cifratura:  C = (P + K) mod N
    Decifratura: P = (C - K) mod N

    Dove:
    * P = carattere del plaintext (testo in chiaro)
    * C = carattere del ciphertext (testo cifrato)
    * K = chiave (shift)
    * N = lunghezza dell'alfabeto
    * mod = operazione di modulo (resto della divisione)

    [green]Alternative Moderne Sicure:[/green]

    * [bold]AES[/bold] - Advanced Encryption Standard (simmetrico)
    * [bold]RSA[/bold] - Crittografia asimmetrica a chiave pubblica
    * [bold]ChaCha20[/bold] - Stream cipher moderno e veloce

    Questi usano:
    * Spazi delle chiavi enormi (128, 256, 2048+ bit)
    * Complessita computazionale molto alta
    * Mathematical hardness problems (fattorizzazione, log discreti)
    """

    console.print(Panel(info, title="[bold]Informazioni Educative[/bold]", border_style="cyan"))


def list_alphabets_command(args):
    """Mostra la lista degli alfabeti disponibili"""
    alphabets = list_alphabets()

    table = Table(title="Alfabeti Disponibili", box=box.ROUNDED)
    table.add_column("Nome", style="cyan")
    table.add_column("Descrizione")
    table.add_column("Lettere")

    for name, desc in alphabets.items():
        letters = ALPHABETS[name]
        table.add_row(name, desc, f"{len(letters)} lettere")

    console.print(table)


def main():
    """Funzione principale del CLI"""
    parser = argparse.ArgumentParser(
        description="Caesar Cipher Tool - Strumento Educativo di Crittografia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Sottocomandi
    subparsers = parser.add_subparsers(dest="command", help="Comando da eseguire")

    # Comando encrypt
    encrypt_parser = subparsers.add_parser("encrypt", help="Cripta un testo")
    encrypt_parser.add_argument("text", help="Testo da criptare")
    encrypt_parser.add_argument("--key", "-k", type=int, default=3, help="Chiave di cifratura (default: 3)")
    encrypt_parser.add_argument("--alphabet", "-a", default="english", help="Alfabeto da usare (default: english)")
    encrypt_parser.add_argument("--visual", "-v", action="store_true", help="Mostra rappresentazione visiva")
    encrypt_parser.add_argument("--output", "-o", help="Salva risultato su file")

    # Comando decrypt
    decrypt_parser = subparsers.add_parser("decrypt", help="Decripta un testo")
    decrypt_parser.add_argument("text", help="Testo da decriptare")
    decrypt_parser.add_argument("--key", "-k", type=int, default=3, help="Chiave di decifratura (default: 3)")
    decrypt_parser.add_argument("--alphabet", "-a", default="english", help="Alfabeto da usare (default: english)")
    decrypt_parser.add_argument("--output", "-o", help="Salva risultato su file")

    # Comando brute-force
    brute_parser = subparsers.add_parser("brute-force", help="Tenta tutte le chiavi possibili")
    brute_parser.add_argument("text", help="Testo cifrato")
    brute_parser.add_argument("--alphabet", "-a", default="english", help="Alfabeto da usare (default: english)")
    brute_parser.add_argument("--output", "-o", help="Salva risultati su file")

    # Comando analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analizza frequenze di un testo")
    analyze_parser.add_argument("--text", "-t", help="Testo da analizzare")
    analyze_parser.add_argument("--file", "-f", help="File da analizzare")
    analyze_parser.add_argument("--alphabet", "-a", default="english", help="Alfabeto/Lingua (default: english)")
    analyze_parser.add_argument("--find-key", action="store_true", help="Trova la chiave più probabile")

    # Comando file-encrypt
    file_encrypt_parser = subparsers.add_parser("file-encrypt", help="Cripta un file")
    file_encrypt_parser.add_argument("input", help="File di input")
    file_encrypt_parser.add_argument("--key", "-k", type=int, default=3, help="Chiave di cifratura (default: 3)")
    file_encrypt_parser.add_argument("--alphabet", "-a", default="english", help="Alfabeto da usare (default: english)")
    file_encrypt_parser.add_argument("--output", "-o", help="File di output (opzionale)")

    # Comando file-decrypt
    file_decrypt_parser = subparsers.add_parser("file-decrypt", help="Decripta un file")
    file_decrypt_parser.add_argument("input", help="File cifrato")
    file_decrypt_parser.add_argument("--key", "-k", type=int, default=3, help="Chiave di decifratura (default: 3)")
    file_decrypt_parser.add_argument("--alphabet", "-a", default="english", help="Alfabeto da usare (default: english)")
    file_decrypt_parser.add_argument("--output", "-o", help="File di output (opzionale)")

    # Comando info
    info_parser = subparsers.add_parser("info", help="Mostra informazioni sul cifrario di Caesar")

    # Comando alphabets
    alphabets_parser = subparsers.add_parser("alphabets", help="Lista alfabeti disponibili")

    # Parsing argomenti
    args = parser.parse_args()

    # Stampa banner e avviso
    print_banner()
    print_warning()

    if not args.command:
        parser.print_help()
        console.print("\n[bold cyan]Esempi:[/bold]")
        console.print("  python main.py encrypt \"Hello World\" --key 3")
        console.print("  python main.py decrypt \"Khoor Zruog\" --key 3")
        console.print("  python main.py brute-force \"Khoor Zruog\"")
        console.print("  python main.py analyze --file esempio.txt")
        console.print("  python main.py info")
        return

    # Esegui comando
    if args.command == "encrypt":
        encrypt_command(args)
    elif args.command == "decrypt":
        decrypt_command(args)
    elif args.command == "brute-force":
        brute_force_command(args)
    elif args.command == "analyze":
        if not args.text and not args.file:
            console.print("[red]Errore: Specifica --text o --file[/red]")
            return
        analyze_command(args)
    elif args.command == "file-encrypt":
        encrypt_file_command(args)
    elif args.command == "file-decrypt":
        decrypt_file_command(args)
    elif args.command == "info":
        info_command(args)
    elif args.command == "alphabets":
        list_alphabets_command(args)


if __name__ == "__main__":
    main()
