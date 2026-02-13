# Struttura del Progetto File Monitor

## 📁 Albero delle Directory

```
file-monitor/
├── file_monitor.py           # Applicazione principale (370 righe)
├── test_operations.py        # Script di test automatizzati (150 righe)
├── config_example.py         # Esempi di configurazione avanzata (200 righe)
├── requirements.txt          # Dipendenze Python
├── README.md                 # Documentazione completa
├── PROJECT_STRUCTURE.md      # Questo file
├── .gitignore               # File ignorati da Git
├── start_monitor.bat        # Quick Start per Windows
└── start_monitor.sh         # Quick Start per Linux/macOS
```

## 🔄 Flusso di Dati

```
┌─────────────────────────────────────────────────────────────┐
│                     UTENTE                                   │
│  (Modifica file: crea, modifica, elimina, sposta)          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              FILE SYSTEM (OS)                               │
│  - Windows: ReadDirectoryChangesW                           │
│  - Linux:   inotify                                         │
│  - macOS:   FSEvents                                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│            WATCHDOG.OBSERVER                                │
│  (Libreria cross-platform per monitoraggio)                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│         FILEMONITORHANDLER                                  │
│  - on_created()    → FILE CREATO                            │
│  - on_modified()   → FILE MODIFICATO                        │
│  - on_deleted()    → FILE ELIMINATO                         │
│  - on_moved()      → FILE SPOSTATO                          │
└────────┬──────────────────────────────────┬─────────────────┘
         │                                  │
         ▼                                  ▼
┌────────────────────┐          ┌────────────────────┐
│    CONSOLE          │          │    FILE LOG        │
│  (stdout/stderr)    │          │  (*.log)           │
└────────────────────┘          └────────────────────┘
```

## 🏗️ Architettura delle Classi

```
FileSystemEventHandler (watchdog.events)
         ↑
         │ inherits
         │
┌────────────────────────────────────────┐
│   FileMonitorHandler                   │
├────────────────────────────────────────┤
│ Attributes:                             │
│   - logger: Logger                      │
│   - verbose: bool                       │
│   - event_count: int                    │
│                                         │
│ Methods:                                │
│   + on_created(event)                  │
│   + on_modified(event)                 │
│   + on_deleted(event)                  │
│   + on_moved(event)                    │
│   - _log_event(type, path, info)       │
└────────────────────────────────────────┘
         ↑
         │ uses
         │
┌────────────────────────────────────────┐
│   FileMonitor                          │
├────────────────────────────────────────┤
│ Attributes:                             │
│   - path: Path                          │
│   - recursive: bool                     │
│   - verbose: bool                       │
│   - log_file: str                       │
│   - observer: Observer                  │
│   - event_handler: Handler              │
│                                         │
│ Methods:                                │
│   + __init__(path, ...)                │
│   + start()                            │
│   + stop()                             │
│   + run()                              │
│   - _setup_logging()                   │
└────────────────────────────────────────┘
```

## 📊 Gestione degli Eventi

### 1. Creazione File
```
User creates file.txt
    ↓
OS detects change
    ↓
Watchdog receives event
    ↓
FileMonitorHandler.on_created()
    ↓
Log: [timestamp] FILE CREATO: path/to/file.txt
    ↓
Console output + optional file log
```

### 2. Modifica File
```
User edits file.txt
    ↓
OS detects change
    ↓
Watchdog receives event
    ↓
FileMonitorHandler.on_modified()
    ↓
Log: [timestamp] FILE MODIFICATO: path/to/file.txt
```

### 3. Eliminazione File
```
User deletes file.txt
    ↓
OS detects change
    ↓
Watchdog receives event
    ↓
FileMonitorHandler.on_deleted()
    ↓
Log: [timestamp] FILE ELIMINATO: path/to/file.txt
```

### 4. Spostamento File
```
User moves file.txt to new.txt
    ↓
OS detects change
    ↓
Watchdog receives event
    ↓
FileMonitorHandler.on_moved()
    ↓
Log: [timestamp] FILE SPOSTATO: new.txt - da: file.txt
```

## 🎯 Casi d'Uso

### 1. Monitoraggio Base
```bash
python file_monitor.py
```
- Directory corrente
- Output su console
- Monitoraggio ricorsivo

### 2. Monitoraggio con Log
```bash
python file_monitor.py -l monitor.log
```
- Salva tutti gli eventi su file
- Utile per audit trail

### 3. Monitoraggio Verbose
```bash
python file_monitor.py -v
```
- Output dettagliato in tempo reale
- Feedback visivo immediato

### 4. Monitoraggio Non Ricorsivo
```bash
python file_monitor.py --no-recursive
```
- Solo directory specificata
- Ignora sottodirectory

## 🔧 Configurazioni Avanzate (config_example.py)

### 1. JSON Logging
- Salva eventi in formato JSON
- Utile per integrazione con altri sistemi
- Analisi dati successiva

### 2. Filtri Personalizzati
- Monitora solo determinate estensioni
- Ignora pattern specifici
- Riduce il rumore nei log

### 3. Statistiche
- Conta tipi di eventi
- Distinguie tra file e directory
- Reportistica dettagliata

## 🧪 Testing

### test_operations.py
Script automatizzato che:

1. **Creazione**: Crea 3 file + 1 sottodirectory con 2 file
2. **Modifica**: Modifica 2 file esistenti
3. **Rinomina**: Rinomina 1 file
4. **Eliminazione**: Elimina 2 file + 1 sottodirectory
5. **Operazioni Miste**: Crea, modifica, elimina rapidamente

Uso:
```bash
# Terminale 1
python file_monitor.py -v

# Terminale 2
python test_operations.py
```

## 📈 Performance

| Metrica | Valore |
|---------|--------|
| CPU Usage (idle) | < 1% |
| Memory Usage | ~20-30 MB |
| Event Latency | < 100ms |
| Max Files | Illimitato (dipende dal filesystem) |
| Thread Count | 2 (main + observer) |

## 🛡️ Gestione Errori

1. **Directory Non Esistente**
   - Errore chiaro con percorso
   - Exit code 1

2. **Permesso Negato**
   - Messaggio di errore specifico
   - Suggerimento soluzione

3. **Interruzione (Ctrl+C)**
   - Arresto graceful dell'observer
   - Cleanup risorse
   - Statistiche finali

4. **File System Errors**
   - Catturati e loggati
   - Monitor continua se possibile

## 🌍 Cross-Platform

| Piattaforma | API Utilizzata | Status |
|-------------|-----------------|--------|
| Windows 10+ | ReadDirectoryChangesW | ✅ Testato |
| Linux 2.6+   | inotify | ✅ Supportato |
| macOS 10.7+  | FSEvents | ✅ Supportato |

## 🔄 Ciclo di Vita

```
1. Avvio (start())
   - Verifica esistenza directory
   - Crea Observer
   - Registra Handler
   - Avvia thread Observer

2. Monitoraggio (run())
   - Loop infinito
   - Attesa eventi
   - Gestione segnali

3. Interruzione
   - Cattura Ctrl+C
   - Ferma Observer
   - Cleanup risorse
   - Statistiche finali
```

## 📚 Estensioni Future

Possibili miglioramenti:

1. **Web Dashboard**: Interfaccia web per visualizzazione eventi
2. **Alert System**: Notifiche email/webhook su eventi
3. **Pattern Matching**: Regex per file specifici
4. **Command Execution**: Esegui comandi su eventi
5. **Database Storage**: Salva eventi in database
6. **API REST**: Endpoint per query eventi
7. **Configuration File**: YAML/TOML config
8. **Multi-Directory**: Monitora più directory
9. **Diff Tracking**: Mostra differenze file modificati
10. **Compression**: Comprimi log vecchi
