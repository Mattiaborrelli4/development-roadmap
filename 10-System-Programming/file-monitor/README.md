# 📂 File Monitor - Sistema di Monitoraggio File System

Un potente strumento di system programming per monitorare i cambiamenti del file system in tempo reale. Scritto in Python utilizzando la libreria `watchdog`, questo strumento cattura e registra tutti gli eventi dei file inclusi creazione, modifica, eliminazione e spostamento.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-working-success)

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Esempi](#esempi)
- [Architettura](#architettura)
- [Concetti di System Programming](#concetti-di-system-programming)
- [Troubleshooting](#troubleshooting)

## ✨ Caratteristiche

- **Monitoraggio in Tempo Reale**: Rileva istantaneamente i cambiamenti dei file
- **Eventi Completi**: Traccia creazione, modifica, eliminazione e spostamento
- **Monitoraggio Ricorsivo**: Opzionalmente monitora le sottodirectory
- **Logging Flessibile**: Output a console e/o file di log
- **Timestamp Precisi**: Ogni evento viene marcato con data e ora esatta
- **Gestione Robusta**: Gestisce gracefully errori e interruzioni
- **Multi-piattaforma**: Funziona su Windows, Linux e macOS
- **Configurabile**: Ampia gamma di opzioni da linea di comando

## 📦 Requisiti

- **Python**: 3.7 o superiore
- **Sistema Operativo**: Windows, Linux o macOS
- **Dipendenze**:
  - `watchdog` >= 3.0.0 (libreria per il monitoraggio del file system)
  - `colorama` >= 0.4.6 (opzionale, per colorazione output su Windows)

## 🚀 Installazione

### 1. Clona o Scarica il Progetto

```bash
cd file-monitor
```

### 2. Installa le Dipendenze

```bash
pip install -r requirements.txt
```

Oppure installa manualmente:

```bash
pip install watchdog
```

### 3. Verifica l'Installazione

```bash
python file_monitor.py --help
```

Dovresti vedere la guida completa dell'utilizzo.

## 🎯 Utilizzo

### Sintassi Base

```bash
python file_monitor.py [percorso] [opzioni]
```

### Argomenti

- `path` (opzionale): Percorso della directory da monitorare (default: directory corrente)

### Opzioni

| Opzione | Lungo | Descrizione |
|---------|-------|-------------|
| `-v` | `--verbose` | Mostra output dettagliato a console |
| `-l FILE` | `--log-file FILE` | Salva i log in un file specifico |
| `--no-recursive` | | Non monitorare le sottodirectory |
| `--version` | | Mostra la versione del programma |
| `-h` | `--help` | Mostra la guida |

### Comandi Base

#### 1. Monitora la Directory Corrente

```bash
python file_monitor.py
```

#### 2. Monitora una Directory Specifica

```bash
# Windows
python file_monitor.py "C:\Users\Utente\Documenti"

# Linux/macOS
python file_monitor.py /home/utente/documenti
```

#### 3. Monitora con Output Dettagliato

```bash
python file_monitor.py -v
```

#### 4. Monitora e Salva Log su File

```bash
python file_monitor.py -l monitor.log
```

#### 5. Monitora Solo la Directory (Non Ricorsivo)

```bash
python file_monitor.py --no-recursive
```

#### 6. Combinazione di Opzioni

```bash
python file_monitor.py /percorso/directory -v -l monitor.log
```

## 📚 Esempi

### Esempio 1: Monitoraggio Base

```bash
# Terminale 1 - Avvia il monitor
python file_monitor.py ./test_dir

# Terminale 2 - Apporta modifiche
cd test_dir
echo "test" > nuovo_file.txt
mv nuovo_file.txt rinominato.txt
rm rinominato.txt
```

### Esempio 2: Test con Script Automatizzato

```bash
# Terminale 1 - Avvia il monitor
python file_monitor.py -v

# Terminale 2 - Esegui script di test
python test_operations.py
```

### Esempio 3: Monitoraggio con Log Persistente

```bash
python file_monitor.py /percorso/importante -l attivita.log -v
```

Questo creerà un file `attivita.log` con tutti gli eventi registrati.

### Output Esempio

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           📂 FILE MONITOR - Sistema di Monitoraggio       ║
║                                                           ║
║           Monitoraggio in tempo reale delle directory     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

2024-02-15 10:30:45 - ======================================================================
2024-02-15 10:30:45 - FILE MONITOR - AVVIATO
2024-02-15 10:30:45 - ======================================================================
2024-02-15 10:30:45 - Directory monitorata: C:\Users\Utente\test_dir
2024-02-15 10:30:45 - Monitoraggio ricorsivo: True
2024-02-15 10:30:45 - File di log: Console
2024-02-15 10:30:45 - ======================================================================
2024-02-15 10:30:45 - In attesa di eventi... (Premi Ctrl+C per interrompere)
2024-02-15 10:30:45 -

[2024-02-15 10:30:48] FILE CREATO: C:\Users\Utente\test_dir\nuovo_file.txt
[2024-02-15 10:30:52] FILE SPOSTATO: C:\Users\Utente\test_dir\rinominato.txt - da: C:\Users\Utente\test_dir\nuovo_file.txt
[2024-02-15 10:30:55] FILE ELIMINATO: C:\Users\Utente\test_dir\rinominato.txt
```

## 🏗️ Architettura

### Componenti Principali

```
file-monitor/
├── file_monitor.py       # Main application
├── test_operations.py     # Test automation script
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Classi

#### 1. `FileMonitorHandler`
Gestore degli eventi del file system. Eredita da `FileSystemEventHandler` di watchdog.

**Metodi:**
- `on_created()`: Gestisce la creazione di file/directory
- `on_modified()`: Gestisce le modifiche
- `on_deleted()`: Gestisce le eliminazioni
- `on_moved()`: Gestisce spostamenti e rinomine

#### 2. `FileMonitor`
Classe principale che gestisce l'osservatore e la configurazione.

**Metodi:**
- `start()`: Avvia il monitoraggio
- `stop()`: Ferma il monitoraggio
- `run()`: Esegue il loop principale

### Flusso di Esecuzione

```
1. Parsing argomenti CLI
   ↓
2. Creazione FileMonitor
   ↓
3. Configurazione Logger
   ↓
4. Creazione Observer (watchdog)
   ↓
5. Avvio Monitoraggio
   ↓
6. Loop Infinito (attesa eventi)
   ↓
7. Gestione Eventi (on_created, on_modified, etc.)
   ↓
8. Interruzione (Ctrl+C)
   ↓
9. Cleanup e Chiusura
```

## 🔧 Concetti di System Programming

### 1. File System Events

Il monitor utilizza API native del sistema operativo per rilevare i cambiamenti:

- **Windows**: `ReadDirectoryChangesW`
- **Linux**: `inotify`
- **macOS**: `FSEvents`

### 2. Osservatore (Observer Pattern)

Il sistema implementa il pattern Observer:

```
Subject (File System) → Observer (watchdog.Observer) → Handler (FileMonitorHandler)
```

### 3. Thread e Concorrenza

L'osservatore esegue in un thread separato per non bloccare il thread principale:

```python
self.observer = Observer()  # Crea un nuovo thread
self.observer.start()       # Avvia il thread
```

### 4. Gestione Segnali

Intercetta `KeyboardInterrupt` (Ctrl+C) per arresto graceful:

```python
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    self.stop()  # Cleanup corretto
```

### 5. Time-to-live (TTL)

Evita duplicati gestendo eventi rapidi consecutivi.

## 🐛 Troubleshooting

### Problema: "Permission denied" su Windows

**Soluzione:** Esegui come amministratore o scegli una directory accessibile.

### Problema: Troppi eventi registrati

**Causa:** Alcuni editor creano file temporanei (es. `.swp` di Vim).

**Soluzione:** Usa filtri o ignora pattern specifici modificando il codice.

### Problema: Monitoraggio non funziona su network drive

**Causa:** Alcune network drive non supportano le notifiche di cambiamento.

**Soluzione:** Usa polling (non implementato in questa versione).

### Problema: Eventi duplicati

**Causa:** Il sistema operativo può generare più eventi per una singola azione.

**Soluzione:** Già gestito con timestamp e deduplicazione logica.

### Problema: Installazione watchdog fallisce

**Soluzione:**

```bash
# Aggiorna pip
python -m pip install --upgrade pip

# Installa con flags specifiche
pip install watchdog --no-cache-dir
```

## 📝 Note Tecniche

### Performance

- **CPU**: < 1% in idle
- **Memoria**: ~20-30 MB
- **Overhead**: Minimo, usando thread separato

### Limitazioni

1. **Network Drives**: Non supportati completamente
2. **File System Virtuali**: Comportamento indefinito
3. **Rapid Changes**: Potrebbero persi eventi estremamente rapidi (< 1ms)

### Estensioni Possibili

- Filtri per estensioni file
- Comandi personalizzati su eventi
- Output JSON/CSV
- Server HTTP per eventi in tempo reale
- Integrazione con database

## 📄 Licenza

Questo progetto è fornito come esempio educativo. Sentiti libero di utilizzarlo e modificarlo secondo le tue esigenze.

## 🤝 Contributi

Questo è un progetto educativo. Suggerimenti e miglioramenti sono benvenuti!

## 📚 Risorse

- [Watchdog Documentation](https://python-watchdog.readthedocs.io/)
- [Python File System Events](https://docs.python.org/3/library/os.html)
- [System Programming in Python](https://docs.python.org/3/library/sys.html)

---

**Creato per:** Portfolio - System Programming Projects
**Linguaggio:** Python 3
**Dipendenze:** watchdog
