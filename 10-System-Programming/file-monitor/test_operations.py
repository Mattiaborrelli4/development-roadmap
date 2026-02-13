#!/usr/bin/env python3
"""
Script di Test per File Monitor
================================

Questo script crea, modifica ed elimina file per testare il monitor.
Eseguire in una directory separata mentre il monitor è attivo.
"""

import os
import time
import tempfile
from pathlib import Path


def create_test_files(directory):
    """Crea file di test."""
    print("📝 Creazione file di test...")

    # Crea file singoli
    for i in range(3):
        filepath = directory / f"test_file_{i}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Contenuto del file di test {i}\n")
        print(f"   Creato: {filepath.name}")
        time.sleep(0.5)

    # Crea sottodirectory con file
    subdir = directory / "subdirectory_test"
    subdir.mkdir(exist_ok=True)
    print(f"   Creata directory: {subdir.name}")

    for i in range(2):
        filepath = subdir / f"sub_test_{i}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"File nella sottodirectory {i}\n")
        print(f"   Creato: {filepath.name}")
        time.sleep(0.5)


def modify_files(directory):
    """Modifica file esistenti."""
    print("\n✏️  Modifica file...")

    test_files = list(directory.glob("test_file_*.txt"))
    for filepath in test_files[:2]:  # Modifica solo primi 2 file
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"Aggiunta nuova riga: {time.strftime('%H:%M:%S')}\n")
        print(f"   Modificato: {filepath.name}")
        time.sleep(0.5)


def rename_files(directory):
    """Rinomina file."""
    print("\n🔄 Rinomina file...")

    old_file = directory / "test_file_0.txt"
    if old_file.exists():
        new_file = directory / "test_file_renamed.txt"
        old_file.rename(new_file)
        print(f"   Rinominato: {old_file.name} -> {new_file.name}")
        time.sleep(0.5)


def delete_files(directory):
    """Elimina file."""
    print("\n🗑️  Eliminazione file...")

    test_files = list(directory.glob("test_file_*.txt"))
    for filepath in test_files[:2]:  # Elimina solo primi 2 file
        filepath.unlink()
        print(f"   Eliminato: {filepath.name}")
        time.sleep(0.5)

    # Elimina sottodirectory
    subdir = directory / "subdirectory_test"
    if subdir.exists():
        for file in subdir.glob("*"):
            file.unlink()
            print(f"   Eliminato: {file.name}")
            time.sleep(0.3)
        subdir.rmdir()
        print(f"   Eliminata directory: {subdir.name}")


def create_mixed_operations(directory):
    """Esegue operazioni miste."""
    print("\n🎭 Operazioni miste...")

    # Crea, modifica ed elimina rapidamente
    for i in range(3):
        filepath = directory / f"temp_{i}.txt"
        with open(filepath, 'w') as f:
            f.write(f"File temporaneo {i}\n")
        print(f"   + Creato: {filepath.name}")

        time.sleep(0.3)

        with open(filepath, 'a') as f:
            f.write("Modifica rapida\n")
        print(f"   ~ Modificato: {filepath.name}")

        time.sleep(0.3)

        filepath.unlink()
        print(f"   - Eliminato: {filepath.name}")

        time.sleep(0.5)


def main():
    """Funzione principale."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║     🧪 SCRIPT DI TEST PER FILE MONITOR                   ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Usa directory temporanea
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)

        print(f"📁 Directory di test: {test_dir}")
        print("⚠️  Assicurati che il monitor sia attivo su questa directory!")
        print("\nPremi Ctrl+C per interrompere i test...\n")

        try:
            # Pausa iniziale
            print("⏳ Inizio tra 3 secondi...")
            time.sleep(3)

            # Esegui test
            create_test_files(test_dir)
            time.sleep(2)

            modify_files(test_dir)
            time.sleep(2)

            rename_files(test_dir)
            time.sleep(2)

            delete_files(test_dir)
            time.sleep(2)

            create_mixed_operations(test_dir)

            print("\n✅ Test completati!")
            print("\nRimango in attesa per 10 secondi...")
            print("(Puoi ancora apportare modifiche manualmente)")
            time.sleep(10)

        except KeyboardInterrupt:
            print("\n\n⚠️  Test interrotti dall'utente")


if __name__ == "__main__":
    main()
