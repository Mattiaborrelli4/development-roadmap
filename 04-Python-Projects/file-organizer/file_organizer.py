#!/usr/bin/env python3
"""
================================================================================
FILE ORGANIZER - Organizzatore di File
================================================================================
Un tool Python per organizzare, rinominare e gestire file duplicati.
Scopo didattico e portfolio - Usa solo librerie standard Python.

Autore: Student Project
Versione: 1.0.0
Librerie: os, shutil, pathlib, hashlib, sys
================================================================================
"""

import os
import sys
import shutil
from pathlib import Path
from hashlib import md5
from datetime import datetime
from collections import defaultdict


# ============================================================================
# CONFIGURAZIONE
# ============================================================================

# Mappa estensioni -> cartelle di destinazione
EXTENSION_MAP = {
    # Immagini
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.bmp': 'Images',
    '.svg': 'Images',
    '.webp': 'Images',
    '.ico': 'Images',
    '.tiff': 'Images',
    '.tif': 'Images',

    # Documenti
    '.pdf': 'Documents',
    '.doc': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.rtf': 'Documents',
    '.odt': 'Documents',
    '.xls': 'Documents',
    '.xlsx': 'Documents',
    '.ppt': 'Documents',
    '.pptx': 'Documents',
    '.csv': 'Documents',
    '.json': 'Documents',
    '.xml': 'Documents',
    '.md': 'Documents',

    # Video
    '.mp4': 'Videos',
    '.avi': 'Videos',
    '.mkv': 'Videos',
    '.mov': 'Videos',
    '.wmv': 'Videos',
    '.flv': 'Videos',
    '.webm': 'Videos',
    '.m4v': 'Videos',
    '.mpeg': 'Videos',
    '.mpg': 'Videos',

    # Audio
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.flac': 'Audio',
    '.aac': 'Audio',
    '.ogg': 'Audio',
    '.wma': 'Audio',
    '.m4a': 'Audio',
    '.opus': 'Audio',

    # Archivi
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.7z': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.bz2': 'Archives',
    '.xz': 'Archives',
    '.tgz': 'Archives',
}

# Dimensione chunk per calcolo hash (4KB)
CHUNK_SIZE = 4096


# ============================================================================
# FUNZIONI DI UTILITA'
# ============================================================================

def print_header(text: str, width: int = 80) -> None:
    """
    Stampa un'intestazione formattata.

    Args:
        text: Il testo da stampare nell'intestazione
        width: Larghezza totale della riga (default: 80)

    Returns:
        None
    """
    separator = "=" * width
    print(f"\n{separator}")
    print(f"{text.center(width)}")
    print(f"{separator}\n")


def print_section(title: str, width: int = 80) -> None:
    """
    Stampa un separatore di sezione.

    Args:
        title: Titolo della sezione
        width: Larghezza totale della riga (default: 80)

    Returns:
        None
    """
    print(f"\n{'-' * width}")
    print(f"  {title}")
    print(f"{'-' * width}\n")


def validate_directory(directory: str) -> Path:
    """
    Valida che la directory esista e sia accessibile.

    Args:
        directory: Percorso della directory da validare

    Returns:
        Path: Oggetto Path della directory validata

    Raises:
        SystemExit: Se la directory non esiste o non e' accessibile
    """
    dir_path = Path(directory).resolve()

    if not dir_path.exists():
        print(f"[!] Errore: La directory '{directory}' non esiste.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"[!] Errore: '{directory}' non e' una directory.")
        sys.exit(1)

    if not os.access(dir_path, os.R_OK):
        print(f"[!] Errore: Permessi insufficienti per leggere '{directory}'.")
        sys.exit(1)

    return dir_path


def calculate_file_hash(file_path: Path) -> str:
    """
    Calcola l'hash MD5 di un file.

    Legge il file a chunk per gestire file di grandi dimensioni
    senza caricarli interamente in memoria.

    Args:
        file_path: Percorso del file da analizzare

    Returns:
        str: Stringa esadecimale dell'hash MD5

    Raises:
        IOError: Se il file non puo' essere letto
    """
    hash_obj = md5()

    try:
        with open(file_path, 'rb') as f:
            # Leggi il file a chunk per usare poca memoria
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
                hash_obj.update(chunk)
    except (IOError, OSError) as e:
        print(f"[!] Errore nella lettura di {file_path.name}: {e}")
        raise

    return hash_obj.hexdigest()


def sanitize_filename(filename: str) -> str:
    r"""
    Rimuove caratteri non validi da un nome file.

    Caratteri rimossi: < > : " / \ | ? *
    Sostituiti con underscore '_'

    Args:
        filename: Nome del file da pulire

    Returns:
        str: Nome file sanificato
    """
    # Caratteri non validi in Windows
    invalid_chars = '<>:"/\\|?*'

    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')

    return sanitized


def get_unique_filename(dest_path: Path) -> Path:
    """
    Genera un nome file unico aggiungendo suffissi.

    Se il file esiste, aggiunge un numero progressivo o timestamp.

    Args:
        dest_path: Percorso di destinazione desiderato

    Returns:
        Path: Percorso con nome file unico
    """
    if not dest_path.exists():
        return dest_path

    # Estrai stem e suffisso
    stem = dest_path.stem
    suffix = dest_path.suffix
    parent = dest_path.parent

    # Prova con numeri progressivi
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1

        # Fallback al timestamp se troppi tentativi
        if counter > 1000:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{stem}_{timestamp}{suffix}"
            return parent / new_name


def get_category(file_path: Path) -> str:
    """
    Determina la categoria di un file in base alla sua estensione.

    Args:
        file_path: Percorso del file da categorizzare

    Returns:
        str: Nome della categoria ('Others' se estensione non mappata)
    """
    # Ottieni estensione in minuscolo
    ext = file_path.suffix.lower()

    # Cerca nella mappa delle estensioni
    return EXTENSION_MAP.get(ext, 'Others')


# ============================================================================
# FUNZIONI PRINCIPALI
# ============================================================================

def organize_files(source_dir: Path, dry_run: bool = False) -> dict:
    """
    Organizza i file per estensione in sottocartelle.

    Sposta i file dalle directory root alle cartelle categorizzate.
    Gestisce conflitti di nomi e crea report.

    Args:
        source_dir: Directory source da organizzare
        dry_run: Se True, simula senza modificare

    Returns:
        dict: Report con statistiche dell'operazione
    """
    print_section("ORGANIZZAZIONE FILE PER ESTENSIONE")

    # Statistiche
    stats = {
        'total': 0,
        'moved': 0,
        'skipped': 0,
        'errors': 0,
        'categories': defaultdict(int)
    }

    # Crea cartelle per ogni categoria (se non dry run)
    categories = set(EXTENSION_MAP.values()) | {'Others'}

    if not dry_run:
        for category in categories:
            category_path = source_dir / category
            category_path.mkdir(exist_ok=True)
            print(f"[*] Cartella creata/verificata: {category}/")
    else:
        print("[*] Modalita' DRY RUN - Nessuna modifica verra' effettuata")

    print()

    # Raccogli tutti i file nella directory root (non in sottocartelle)
    files = [
        f for f in source_dir.iterdir()
        if f.is_file() and f.parent == source_dir
    ]

    stats['total'] = len(files)

    if stats['total'] == 0:
        print("[*] Nessun file da organizzare nella directory root.")
        return stats

    print(f"[*] Trovati {stats['total']} file da processare\n")

    # Processa ogni file
    for file_path in files:
        try:
            # Determina categoria
            category = get_category(file_path)
            stats['categories'][category] += 1

            # Percorso di destinazione
            dest_dir = source_dir / category
            dest_path = dest_dir / file_path.name

            # Gestisci conflitti nomi
            if dest_path.exists():
                dest_path = get_unique_filename(dest_path)
                action = "rinominato e spostato"
            else:
                action = "spostato"

            # Esegui o simula lo spostamento
            if dry_run:
                print(f"[SIMULATE] {file_path.name} -> {category}/{dest_path.name}")
                stats['moved'] += 1
            else:
                shutil.move(str(file_path), str(dest_path))
                print(f"[OK] {file_path.name} -> {category}/{dest_path.name}")
                stats['moved'] += 1

        except Exception as e:
            print(f"[!] Errore con {file_path.name}: {e}")
            stats['errors'] += 1

    return stats


def find_duplicates(source_dir: Path, use_hash: bool = True) -> dict:
    """
    Trova file duplicati nella directory.

    Puo' confrontare per nome file o per hash MD5 per duplicati veri.

    Args:
        source_dir: Directory da analizzare
        use_hash: Se True, usa hash MD5; altrimenti confronta solo nomi

    Returns:
        dict: Report duplicati con gruppi di file
    """
    method = "HASH MD5" if use_hash else "NOME FILE"
    print_section(f"RICERCA DUPLICATI ({method})")

    duplicates = {
        'by_name': defaultdict(list),
        'by_hash': defaultdict(list),
        'total_files': 0,
        'duplicates_found': 0
    }

    # Raccogli tutti i file ricorsivamente
    all_files = []
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = Path(root) / filename
            all_files.append(file_path)

    duplicates['total_files'] = len(all_files)

    if duplicates['total_files'] == 0:
        print("[*] Nessun file trovato per l'analisi duplicati.")
        return duplicates

    print(f"[*] Analisi di {duplicates['total_files']} file...\n")

    # Raggruppa per nome
    for file_path in all_files:
        duplicates['by_name'][file_path.name].append(file_path)

    # Filtra solo i gruppi con duplicati per nome
    dup_by_name = {
        name: paths for name, paths in duplicates['by_name'].items()
        if len(paths) > 1
    }

    if dup_by_name:
        print(f"[*] Trovati {len(dup_by_name)} gruppi di file con lo stesso nome:\n")
        for name, paths in dup_by_name.items():
            print(f"  {name} ({len(paths)} copie):")
            for p in paths:
                rel_path = p.relative_to(source_dir)
                print(f"    - {rel_path}")

    # Calcola hash se richiesto
    if use_hash:
        print("\n[*] Calcolo hash MD5 per confronto preciso...\n")

        for file_path in all_files:
            try:
                file_hash = calculate_file_hash(file_path)
                duplicates['by_hash'][file_hash].append(file_path)
            except IOError:
                # File non leggibile, skip
                continue

        # Filtra solo i gruppi con duplicati per hash
        dup_by_hash = {
            h: paths for h, paths in duplicates['by_hash'].items()
            if len(paths) > 1
        }

        duplicates['duplicates_found'] = len(dup_by_hash)

        if dup_by_hash:
            print(f"[*] TROVATI {len(dup_by_hash)} GRUPPI DI DUPLICATI VERI:\n")

            for i, (file_hash, paths) in enumerate(dup_by_hash.items(), 1):
                print(f"  Gruppo {i}: {len(paths)} file identici")
                print(f"  Hash: {file_hash[:16]}...")
                print(f"  Dimensione: {paths[0].stat().st_size:,} bytes")

                for p in paths:
                    rel_path = p.relative_to(source_dir)
                    print(f"    - {rel_path}")

                # Calcola spazio recuperabile
                total_size = sum(p.stat().st_size for p in paths)
                recoverable = total_size - paths[0].stat().st_size
                print(f"  Spazio recuperabile: {recoverable:,} bytes ({recoverable/1024/1024:.2f} MB)\n")
        else:
            print("[OK] Nessun duplicato trovato (hash univoci).")
    else:
        # Solo per nome
        duplicates['duplicates_found'] = len(dup_by_name)

    return duplicates


def rename_files(source_dir: Path, pattern: str = 'timestamp',
                 dry_run: bool = False) -> dict:
    """
    Rinomina file batch con pattern specifici.

    Pattern disponibili:
    - 'timestamp': Aggiunge timestamp al nome
    - 'sequential': Aggiunge numero progressivo
    - 'sanitize': Rimuove solo caratteri speciali

    Args:
        source_dir: Directory con i file da rinominare
        pattern: Pattern di rinomina ('timestamp', 'sequential', 'sanitize')
        dry_run: Se True, simula senza modificare

    Returns:
        dict: Report con statistiche
    """
    print_section(f"RINOMINA BATCH (Pattern: {pattern.upper()})")

    stats = {
        'total': 0,
        'renamed': 0,
        'skipped': 0,
        'errors': 0
    }

    # Raccogli file (solo directory root)
    files = [
        f for f in source_dir.iterdir()
        if f.is_file() and f.parent == source_dir
    ]

    stats['total'] = len(files)

    if stats['total'] == 0:
        print("[*] Nessun file da rinominare.")
        return stats

    print(f"[*] Trovati {stats['total']} file da rinominare\n")

    if dry_run:
        print("[*] Modalita' DRY RUN - Nessuna modifica verra' effettuata\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for idx, file_path in enumerate(files, 1):
        try:
            old_name = file_path.name
            stem = file_path.stem
            suffix = file_path.suffix

            # Applica pattern
            if pattern == 'timestamp':
                new_stem = f"{stem}_{timestamp}"
            elif pattern == 'sequential':
                new_stem = f"{idx:03d}_{stem}"
            elif pattern == 'sanitize':
                new_stem = sanitize_filename(stem)
            else:
                print(f"[!] Pattern non riconosciuto: {pattern}")
                return stats

            new_name = f"{new_stem}{suffix}"
            new_path = file_path.parent / new_name

            # Verifica che il nuovo nome sia diverso
            if new_name == old_name:
                print(f"[-] {old_name} (già conforme)")
                stats['skipped'] += 1
                continue

            # Gestisci conflitti
            if new_path.exists() and new_path != file_path:
                new_path = get_unique_filename(new_path)
                new_name = new_path.name

            # Esegui o simula
            if dry_run:
                print(f"[SIMULATE] {old_name} -> {new_name}")
                stats['renamed'] += 1
            else:
                file_path.rename(new_path)
                print(f"[OK] {old_name} -> {new_name}")
                stats['renamed'] += 1

        except Exception as e:
            print(f"[!] Errore con {file_path.name}: {e}")
            stats['errors'] += 1

    return stats


def generate_report(organize_stats: dict, duplicate_stats: dict,
                    rename_stats: dict, output_file: str = None) -> str:
    """
    Genera un report formattato di tutte le operazioni.

    Args:
        organize_stats: Statistiche organizzazione
        duplicate_stats: Statistiche duplicati
        rename_stats: Statistiche rinomina
        output_file: Se specificato, salva il report in questo file

    Returns:
        str: Report formattato
    """
    report_lines = []
    width = 80

    # Header
    report_lines.append("=" * width)
    report_lines.append("REPORT ORGANIZZAZIONE FILE".center(width))
    report_lines.append("=" * width)
    report_lines.append(f"Generato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Sezione Organizzazione
    if organize_stats and organize_stats.get('total', 0) > 0:
        report_lines.append("-" * width)
        report_lines.append("1. ORGANIZZAZIONE PER ESTENSIONE")
        report_lines.append("-" * width)
        report_lines.append(f"File totali analizzati: {organize_stats['total']}")
        report_lines.append(f"File spostati: {organize_stats['moved']}")
        report_lines.append(f"File saltati: {organize_stats['skipped']}")
        report_lines.append(f"Errori: {organize_stats['errors']}")
        report_lines.append("")

        if organize_stats['categories']:
            report_lines.append("File per categoria:")
            for category, count in sorted(organize_stats['categories'].items()):
                report_lines.append(f"  {category}: {count} file")
            report_lines.append("")

    # Sezione Duplicati
    if duplicate_stats:
        report_lines.append("-" * width)
        report_lines.append("2. ANALISI DUPLICATI")
        report_lines.append("-" * width)
        report_lines.append(f"File analizzati: {duplicate_stats['total_files']}")
        report_lines.append(f"Gruppi duplicati trovati: {duplicate_stats['duplicates_found']}")
        report_lines.append("")

    # Sezione Rinomina
    if rename_stats and rename_stats.get('total', 0) > 0:
        report_lines.append("-" * width)
        report_lines.append("3. RINOMINA BATCH")
        report_lines.append("-" * width)
        report_lines.append(f"File processati: {rename_stats['total']}")
        report_lines.append(f"File rinominati: {rename_stats['renamed']}")
        report_lines.append(f"File saltati: {rename_stats['skipped']}")
        report_lines.append(f"Errori: {rename_stats['errors']}")
        report_lines.append("")

    # Footer
    report_lines.append("=" * width)
    report_lines.append("FINE REPORT".center(width))
    report_lines.append("=" * width)

    # Converti in stringa
    report = "\n".join(report_lines)

    # Stampa a schermo
    print_section("REPORT FINALE")
    print(report)

    # Salva su file se richiesto
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n[OK] Report salvato in: {output_file}")
        except Exception as e:
            print(f"\n[!] Errore salvataggio report: {e}")

    return report


# ============================================================================
# INTERFACCIA CLI INTERATTIVA
# ============================================================================

def get_yes_no(prompt: str, default: bool = False) -> bool:
    """
    Chiede conferma all'utente (sì/no).

    Args:
        prompt: Messaggio da mostrare
        default: Risposta predefinita

    Returns:
        bool: True per sì, False per no
    """
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        response = input(prompt + suffix + ": ").strip().lower()

        if not response:
            return default

        if response in ('y', 's', 'yes', 'si'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("[!] Rispondi y (yes) o n (no)")


def print_menu() -> None:
    """Stampa il menu principale delle opzioni."""
    print_header("FILE ORGANIZER - Menu Principale")
    print("Scegli le operazioni da eseguire:\n")
    print("  [1] Organizza file per estensione")
    print("  [2] Trova duplicati")
    print("  [3] Rinomina file batch")
    print("  [4] Esegui tutto (1+2+3)")
    print("  [0] Esci")
    print()


def interactive_mode():
    """
    Esegue il programma in modalità interattiva.

    Permette all'utente di selezionare le operazioni e configurare le opzioni.
    """
    print_header("FILE ORGANIZER v1.0 - Modo Interattivo")

    # Ottieni directory
    while True:
        print("Inserisci il percorso della directory da organizzare")
        print("(lascia vuoto per usare la directory corrente)")

        dir_input = input("> ").strip()

        if not dir_input:
            target_dir = Path.cwd()
            break

        try:
            target_dir = validate_directory(dir_input)
            break
        except SystemExit:
            continue

    print(f"\n[OK] Directory selezionata: {target_dir}\n")

    # Menu principale
    while True:
        print_menu()
        choice = input("Scelta [0-4]: ").strip()

        if choice == '0':
            print("\n[*] Uscita dal programma.")
            break

        elif choice in '1234':
            # Conferma per ogni operazione
            dry_run = True  # Default dry-run per sicurezza

            if choice in '14':
                dry_run = not get_yes_no(
                    "Modalita' DRY RUN? (simulazione senza modifiche)",
                    default=True
                )

            # Variabili statistiche
            org_stats = {}
            dup_stats = {}
            ren_stats = {}

            try:
                # Organizza
                if choice in '14':
                    org_stats = organize_files(target_dir, dry_run=dry_run)

                # Trova duplicati
                if choice in '24':
                    use_hash = get_yes_no(
                        "Usare hash MD5 per duplicati veri? (più lento ma preciso)",
                        default=True
                    )
                    dup_stats = find_duplicates(target_dir, use_hash=use_hash)

                # Rinomina
                if choice in '34':
                    print("\nPattern di rinomina:")
                    print("  [1] Timestamp (aggiunge data/ora)")
                    print("  [2] Sequenziale (aggiunge numero)")
                    print("  [3] Sanitize (rimuove caratteri speciali)")

                    pat_choice = input("Scelta [1-3]: ").strip()

                    pattern_map = {'1': 'timestamp', '2': 'sequential', '3': 'sanitize'}
                    pattern = pattern_map.get(pat_choice, 'timestamp')

                    ren_stats = rename_files(target_dir, pattern=pattern, dry_run=dry_run)

                # Genera report
                if any([org_stats, dup_stats, ren_stats]):
                    save_report = get_yes_no("\nSalvare il report su file?", default=False)

                    report_file = None
                    if save_report:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        report_file = target_dir / f"report_{timestamp}.txt"

                    generate_report(org_stats, dup_stats, ren_stats, report_file)

            except KeyboardInterrupt:
                print("\n\n[!] Operazione interrotta dall'utente.")
                continue
            except Exception as e:
                print(f"\n[!] Errore imprevisto: {e}")
                import traceback
                traceback.print_exc()

            # Pausa prima di tornare al menu
            input("\nPremi Enter per continuare...")

        else:
            print("[!] Scelta non valida. Riprova.")


def print_usage():
    """Stampa le istruzioni per l'uso da riga di comando."""
    print_header("FILE ORGANIZER - Istruzioni")
    print("""
Uso:
  python file_organizer.py                          # Modo interattivo
  python file_organizer.py <directory>             # Modo veloce con directory

Esempi:
  python file_organizer.py
  python file_organizer.py "C:\\Users\\matti\\Downloads"
  python file_organizer.py .

Funzionalita':
  - Organizza file automaticamente per estensione
  - Trova duplicati per nome o hash MD5
  - Rinomina file in batch
  - Genera report dettagliato
  - Modalita' dry-run per test sicuri

Organizza automaticamente i file in:
  - Images/     (jpg, png, gif, bmp, svg, webp, ...)
  - Documents/  (pdf, doc, txt, xls, ppt, ...)
  - Videos/     (mp4, avi, mkv, mov, ...)
  - Audio/      (mp3, wav, flac, ...)
  - Archives/   (zip, rar, 7z, tar, ...)
  - Others/     (tutto il resto)
""")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Funzione principale del programma."""
    # Controlla argomenti riga di comando
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        # Help
        if arg in ('-h', '--help', 'help'):
            print_usage()
            sys.exit(0)

        # Directory specificata
        try:
            target_dir = validate_directory(arg)
            print(f"[OK] Directory: {target_dir}")

            # Conferma operazioni
            dry_run = not get_yes_no("Procedere con l'organizzazione?", default=False)

            org_stats = organize_files(target_dir, dry_run=dry_run)
            dup_stats = find_duplicates(target_dir, use_hash=True)

            generate_report(org_stats, dup_stats, {}, None)

        except KeyboardInterrupt:
            print("\n\n[!] Operazione interrotta.")
            sys.exit(0)
    else:
        # Modo interattivo
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n[!] Programma terminato.")
            sys.exit(0)


if __name__ == "__main__":
    main()
