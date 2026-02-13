#!/usr/bin/env python3
"""
File Monitor - Sistema di Monitoraggio File
===========================================

Questo strumento monitora una directory e registra tutti i cambiamenti dei file
(creazione, modifica, eliminazione, spostamento) in tempo reale.

Autore: System Programming Project
Linguaggio: Python 3
Dipendenze: watchdog
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FileMonitorHandler(FileSystemEventHandler):
    """
    Gestore degli eventi del file system.

    Cattura e registra tutti gli eventi dei file: creazione, modifica,
    eliminazione e spostamento.
    """

    def __init__(self, logger=None, verbose=False):
        """
        Inizializza il gestore degli eventi.

        Args:
            logger: Logger personalizzato (opzionale)
            verbose: Mostra output dettagliato
        """
        super().__init__()
        self.logger = logger or logging.getLogger(__name__)
        self.verbose = verbose
        self.event_count = 0

    def _log_event(self, event_type, path, extra_info=""):
        """
        Registra un evento nel log.

        Args:
            event_type: Tipo di evento
            path: Percorso del file
            extra_info: Informazioni aggiuntive
        """
        self.event_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = f"[{timestamp}] {event_type}: {path}"
        if extra_info:
            log_message += f" - {extra_info}"

        self.logger.info(log_message)

        if self.verbose:
            print(f"✓ {log_message}")

    def on_created(self, event):
        """Chiamato quando un file o directory viene creato."""
        if event.is_directory:
            self._log_event("DIRECTORY CREATA", event.src_path)
        else:
            self._log_event("FILE CREATO", event.src_path)

    def on_modified(self, event):
        """Chiamato quando un file o directory viene modificato."""
        # Evita di loggare eventi duplicati rapidi
        if event.is_directory:
            self._log_event("DIRECTORY MODIFICATA", event.src_path)
        else:
            self._log_event("FILE MODIFICATO", event.src_path)

    def on_deleted(self, event):
        """Chiamato quando un file o directory viene eliminato."""
        if event.is_directory:
            self._log_event("DIRECTORY ELIMINATA", event.src_path)
        else:
            self._log_event("FILE ELIMINATO", event.src_path)

    def on_moved(self, event):
        """Chiamato quando un file o directory viene spostato/rinominato."""
        if event.is_directory:
            self._log_event(
                "DIRECTORY SPOSTATA",
                event.dest_path,
                f"da: {event.src_path}"
            )
        else:
            self._log_event(
                "FILE SPOSTATO",
                event.dest_path,
                f"da: {event.src_path}"
            )


class FileMonitor:
    """
    Monitor di File System principale.

    Gestisce l'osservatore e il gestore di eventi per monitorare
    i cambiamenti in una directory.
    """

    def __init__(self, path, recursive=True, verbose=False, log_file=None):
        """
        Inizializza il monitor di file.

        Args:
            path: Percorso della directory da monitorare
            recursive: Monitora anche le sottodirectory
            verbose: Mostra output dettagliato a console
            log_file: File di log (opzionale)
        """
        self.path = Path(path).resolve()
        self.recursive = recursive
        self.verbose = verbose
        self.log_file = log_file
        self.observer = None
        self.event_handler = None

        # Configura il logging
        self._setup_logging()

    def _setup_logging(self):
        """Configura il sistema di logging."""
        log_format = "%(asctime)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        handlers = [logging.StreamHandler(sys.stdout)]

        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(
                logging.FileHandler(self.log_file, encoding='utf-8')
            )

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=handlers
        )

        self.logger = logging.getLogger(__name__)

    def start(self):
        """Avvia il monitoraggio della directory."""
        if not self.path.exists():
            raise FileNotFoundError(
                f"La directory non esiste: {self.path}"
            )

        if not self.path.is_dir():
            raise NotADirectoryError(
                f"Il percorso non è una directory: {self.path}"
            )

        # Crea il gestore di eventi
        self.event_handler = FileMonitorHandler(
            logger=self.logger,
            verbose=self.verbose
        )

        # Crea e avvia l'osservatore
        self.observer = Observer()
        self.observer.schedule(
            self.event_handler,
            str(self.path),
            recursive=self.recursive
        )
        self.observer.start()

        self.logger.info("=" * 70)
        self.logger.info("FILE MONITOR - AVVIATO")
        self.logger.info("=" * 70)
        self.logger.info(f"Directory monitorata: {self.path}")
        self.logger.info(f"Monitoraggio ricorsivo: {self.recursive}")
        self.logger.info(f"File di log: {self.log_file or 'Console'}")
        self.logger.info("=" * 70)
        self.logger.info("In attesa di eventi... (Premi Ctrl+C per interrompere)")
        self.logger.info("")

    def stop(self):
        """Ferma il monitoraggio."""
        if self.observer:
            self.observer.stop()
            self.observer.join()

        self.logger.info("")
        self.logger.info("=" * 70)
        self.logger.info("FILE MONITOR - FERMATO")
        self.logger.info(f"Totale eventi registrati: {self.event_handler.event_count}")
        self.logger.info("=" * 70)

    def run(self):
        """Esegue il monitoraggio fino a interruzione."""
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⚠ Interruzione rilevata. Arresto in corso...")
            self.stop()
        except Exception as e:
            self.logger.error(f"Errore durante il monitoraggio: {e}")
            raise


def print_banner():
    """Stampa il banner del programma."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           📂 FILE MONITOR - Sistema di Monitoraggio       ║
║                                                           ║
║           Monitoraggio in tempo reale delle directory     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Funzione principale del programma."""
    import argparse

    # Parser degli argomenti
    parser = argparse.ArgumentParser(
        description="File Monitor - Sistema di Monitoraggio File System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  # Monitora directory corrente
  python file_monitor.py

  # Monitora directory specifica
  python file_monitor.py /percorso/directory

  # Monitora con output dettagliato e file di log
  python file_monitor.py /percorso/directory -v -l monitor.log

  # Monitora solo la directory (non ricorsivo)
  python file_monitor.py /percorso/directory --no-recursive
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Percorso della directory da monitorare (default: directory corrente)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostra output dettagliato a console'
    )

    parser.add_argument(
        '-l', '--log-file',
        metavar='FILE',
        help='Salva i log in un file specifico'
    )

    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Non monitorare le sottodirectory'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='File Monitor v1.0.0'
    )

    args = parser.parse_args()

    # Stampa banner
    print_banner()

    # Crea e avvia il monitor
    monitor = FileMonitor(
        path=args.path,
        recursive=not args.no_recursive,
        verbose=args.verbose,
        log_file=args.log_file
    )

    try:
        monitor.run()
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
