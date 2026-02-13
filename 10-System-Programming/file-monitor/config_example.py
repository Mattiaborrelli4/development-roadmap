#!/usr/bin/env python3
"""
File Monitor - Esempio di Configurazione Avanzata
=================================================

Questo esempio mostra come estendere e personalizzare il File Monitor
per casi d'uso avanzati.
"""

import time
import json
from pathlib import Path
from file_monitor import FileMonitor, FileMonitorHandler
from watchdog.events import FileSystemEventHandler


class JSONLogHandler(FileSystemEventHandler):
    """
    Gestore che salva gli eventi in formato JSON.
    Utile per integrazione con altri sistemi.
    """

    def __init__(self, log_file="events.json"):
        super().__init__()
        self.log_file = Path(log_file)
        self.events = []

    def on_any_event(self, event):
        """Cattura tutti gli eventi e li salva in JSON."""
        event_data = {
            "timestamp": time.time(),
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory
        }

        if hasattr(event, 'dest_path'):
            event_data["dest_path"] = event.dest_path

        self.events.append(event_data)

        # Salva su disco
        with open(self.log_file, 'w') as f:
            json.dump(self.events, f, indent=2)


class FilteredHandler(FileMonitorHandler):
    """
    Gestore con filtri personalizzati.
    Monitora solo certi tipi di file o directory.
    """

    def __init__(self, *args, extensions=None, ignore_patterns=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.extensions = set(extensions or [])
        self.ignore_patterns = ignore_patterns or []

    def _should_process(self, path):
        """Determina se l'evento deve essere processato."""
        path_obj = Path(path)

        # Controlla estensioni
        if self.extensions:
            if path_obj.suffix.lower() not in self.extensions:
                return False

        # Controlla pattern da ignorare
        for pattern in self.ignore_patterns:
            if pattern in str(path):
                return False

        return True

    def on_created(self, event):
        if self._should_process(event.src_path):
            super().on_created(event)

    def on_modified(self, event):
        if self._should_process(event.src_path):
            super().on_modified(event)

    def on_deleted(self, event):
        if self._should_process(event.src_path):
            super().on_deleted(event)

    def on_moved(self, event):
        if self._should_process(event.dest_path):
            super().on_moved(event)


class StatisticsHandler(FileMonitorHandler):
    """
    Gestore che raccoglie statistiche sugli eventi.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = {
            "created": 0,
            "modified": 0,
            "deleted": 0,
            "moved": 0,
            "directories": 0,
            "files": 0
        }

    def on_created(self, event):
        super().on_created(event)
        self.stats["created"] += 1
        if event.is_directory:
            self.stats["directories"] += 1
        else:
            self.stats["files"] += 1

    def on_modified(self, event):
        super().on_modified(event)
        self.stats["modified"] += 1

    def on_deleted(self, event):
        super().on_deleted(event)
        self.stats["deleted"] += 1

    def on_moved(self, event):
        super().on_moved(event)
        self.stats["moved"] += 1

    def get_statistics(self):
        """Restituisce le statistiche correnti."""
        return self.stats.copy()

    def print_statistics(self):
        """Stampa le statistiche in modo leggibile."""
        print("\n" + "="*50)
        print("📊 STATISTICHE EVENTI")
        print("="*50)
        for key, value in self.stats.items():
            print(f"  {key.capitalize():15s}: {value}")
        print("="*50 + "\n")


def example_json_logging():
    """Esempio 1: Logging in formato JSON."""
    print("Esempio 1: JSON Logging")
    print("-" * 40)

    handler = JSONLogHandler("events.json")

    from watchdog.observers import Observer
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    try:
        print("Monitoraggio attivo... (Ctrl+C per fermare)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    print(f"\nSalvati {len(handler.events)} eventi in events.json")


def example_filtered_monitoring():
    """Esempio 2: Monitoraggio con filtri."""
    print("\nEsempio 2: Monitoraggio Filtrato")
    print("-" * 40)

    # Monitora solo file Python e ignora __pycache__
    handler = FilteredHandler(
        extensions=['.py', '.txt'],
        ignore_patterns=['__pycache__', '.git', 'venv'],
        verbose=True
    )

    monitor = FileMonitor(
        path=".",
        recursive=True,
        verbose=True
    )

    # Sostituisci il handler con quello filtrato
    monitor.event_handler = handler

    try:
        monitor.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()


def example_statistics():
    """Esempio 3: Raccolta statistiche."""
    print("\nEsempio 3: Raccolta Statistiche")
    print("-" * 40)

    handler = StatisticsHandler(verbose=True)

    from watchdog.observers import Observer
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    try:
        print("Monitoraggio attivo... (Ctrl+C per vedere le statistiche)")
        while True:
            time.sleep(5)
            handler.print_statistics()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    print("\nStatistiche finali:")
    handler.print_statistics()


def example_custom_directory():
    """Esempio 4: Monitoraggio directory personalizzata."""
    print("\nEsempio 4: Directory Personalizzata")
    print("-" * 40)

    # Crea una directory di test
    test_dir = Path("./test_monitoring")
    test_dir.mkdir(exist_ok=True)

    print(f"Monitoraggio: {test_dir.resolve()}")

    monitor = FileMonitor(
        path=test_dir,
        recursive=True,
        verbose=True,
        log_file="test_monitoring.log"
    )

    try:
        monitor.start()
        print("\nApporta modifiche alla directory test_monitoring...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()


if __name__ == "__main__":
    import sys

    examples = {
        "1": ("JSON Logging", example_json_logging),
        "2": ("Monitoraggio Filtrato", example_filtered_monitoring),
        "3": ("Raccolta Statistiche", example_statistics),
        "4": ("Directory Personalizzata", example_custom_directory),
    }

    print("="*50)
    print("ESEMPI DI CONFIGURAZIONE AVANZATA")
    print("="*50)
    print()

    for key, (name, _) in examples.items():
        print(f"{key}. {name}")

    print()
    choice = input("Seleziona esempio (1-4): ").strip()

    if choice in examples:
        name, func = examples[choice]
        print(f"\nEsecuzione: {name}\n")
        func()
    else:
        print("Scelta non valida!")
        sys.exit(1)
