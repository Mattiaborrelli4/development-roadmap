# Changelog - File Monitor

Tutte le note importanti per questo progetto sono documentate in questo file.

## [1.0.0] - 2024-02-15

### Aggiunto
- **Core Functionality**
  - Monitoraggio in tempo reale del file system
  - Rilevamento creazione file/directory
  - Rilevamento modifica file/directory
  - Rilevamento eliminazione file/directory
  - Rilevamento spostamento/rinomina file/directory
  - Monitoraggio ricorsivo opzionale
  - Sistema di logging flessibile (console + file)
  - Timestamp per ogni evento
  - Gestione graceful interruzioni (Ctrl+C)

- **Interfaccia CLI**
  - Argomenti linea di comando completi
  - Opzione verbose per output dettagliato
  - Specifica file di log personalizzato
  - Modalità non ricorsiva
  - Guida integrata (--help)
  - Versione (--version)

- **Script Utilità**
  - `test_operations.py`: Test automatizzati
  - `start_monitor.bat`: Quick start Windows
  - `start_monitor.sh`: Quick start Linux/macOS
  - `config_example.py`: Esempi configurazione avanzata

- **Documentazione**
  - README.md completo in italiano
  - QUICKSTART.md per avvio rapido
  - PROJECT_STRUCTURE.md con architettura dettagliata
  - Commenti estesi nel codice

### Tecnologie
- Python 3.7+
- watchdog 3.0.0+ per monitoraggio cross-platform
- Libreria standard logging
- pathlib per gestione percorsi

### Piattaforme
- Windows 10+ (ReadDirectoryChangesW)
- Linux 2.6+ (inotify)
- macOS 10.7+ (FSEvents)

### Statistiche Progetto
- **File Python**: 3 (737 righe di codice)
- **Documentazione**: 3 file (742 righe)
- **Script Shell**: 2 (163 righe)
- **Totale**: 9 file, ~1650 righe

---

## Prossime Versioni (Roadmap)

### [1.1.0] - Piano
- Filtri per estensioni file
- Pattern di esclusione (.git, __pycache__, etc.)
- Limitazione dimensione log
- Rotazione log files

### [1.2.0] - Piano
- Output JSON/CSV
- Web dashboard semplice
- Statistiche in tempo reale
- Export eventi

### [2.0.0] - Piano
- Multi-directory monitoring
- Configuration file (YAML/TOML)
- Plugin system
- Command execution su eventi
- Alert system (email/webhook)
- Database storage

---

## Note Versione

### Formato Versioning
Questo progetto segue [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambiamenti incompatibili API
- **MINOR**: Funzionalità backward-compatible
- **PATCH**: Bug fix backward-compatible

### Tipi di Cambiamento
- **Aggiunto**: Nuove funzionalità
- **Modificato**: Cambiamenti a funzionalità esistenti
- **Deprecato**: Funzionalità che saranno rimosse
- **Rimosso**: Funzionalità eliminate
- **Fissato**: Bug fix
- **Sicurezza**: Fix problemi di sicurezza
