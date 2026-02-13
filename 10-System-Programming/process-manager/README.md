# Process Manager - Educational System Programming Tool

> **Strumento Educativo per la Gestione dei Processi**

Un tool educativo per imparare i concetti di system programming relativi alla gestione dei processi. Simile a `top` o `htop`, ma progettato specificamente per l'apprendimento.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Educational-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## 📚 Indice

- [Scopo Educativo](#scopo-educativo)
- [Concetti Trattati](#concetti-trattati)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Struttura del Progetto](#struttura-del-progetto)
- [Confronto con Tool Reali](#confronto-con-tool-reali)
- [Avvertenze di Sicurezza](#avvertenze-di-sicurezza)

---

## 🎓 Scopo Educativo

Questo progetto è stato creato come **strumento educativo** per imparare come funzionano i processi nei sistemi operativi moderni. A differenza di tool di produzione come `top` o `htop`, questo progetto enfatizza:

- **Comprensione dei concetti** oltre alle funzionalità
- **Codice commentato e documentato** per studiare l'implementazione
- **Sicurezza** con avvertenze e conferme per operazioni pericolose
- **Esempi pratici** di API di sistema

**Obiettivi di Apprendimento:**

1. Comprendere il **lifecycle** di un processo (creazione, esecuzione, terminazione)
2. Imparare il **modello di gerarchia** dei processi (padre-figlio)
3. Capire come il **kernel gestisce** risorse CPU e memoria
4. Utilizzare le **API di sistema** per monitorare e controllare i processi
5. Conoscere i **segnali** come meccanismo di IPC (Inter-Process Communication)

---

## 🧠 Concetti Trattati

### 1. PID (Process ID)

Ogni processo ha un identificatore univoco assegnato dal kernel:

- **PID 1**: `init` o `systemd` - il primo processo, padre di tutti
- **PID univoco**: Non ci sono due processi con lo stesso PID in un dato momento
- **PPID**: Parent PID, il processo che ha creato questo processo

```python
# Esempio dal codice
proc = psutil.Process(1234)
print(f"PID: {proc.pid}")      # 1234
print(f"PPID: {proc.ppid()}")  # 1 (se figlio di init)
```

### 2. Gerarchia dei Processi

I processi formano un **albero** con radice in `init`:

```
init (PID 1)
├─ sshd
│  └─ bash
│     └─ python
├─ systemd
│  ├─ NetworkManager
│  └─ gnome-shell
```

**Concetti Chiave:**
- **fork()**: System call per creare un processo figlio
- **exec()**: Sostituisce il programma del processo
- **Orphan Process**: Figlio il cui padre è terminato (adottato da init)
- **Zombie Process**: Figlio terminato ma ancora nella tabella processi

### 3. Stati del Processo

Un processo può trovarsi in diversi stati:

| Stato | Descrizione | Simbolo |
|-------|-------------|---------|
| **Running** | In esecuzione su una CPU | R |
| **Sleeping** | In attesa di I/O o evento | S |
| **Disk Sleep** | In attesa I/O disco uninterruptible | D |
| **Stopped** | Fermato da segnale | T |
| **Zombie** | Terminato ma non fatto cleanup | Z |

### 4. Signals

I segnali sono il meccanismo principale per comunicare con i processi:

| Segnale | Numero | Descrizione |
|---------|--------|-------------|
| **SIGTERM** | 15 | Termination request - permette cleanup graceful |
| **SIGKILL** | 9 | Immediate kill - non può essere ignorato |
| **SIGINT** | 2 | Interrupt (come Ctrl+C) |
| **SIGSTOP** | 19 | Stop/pause process |
| **SIGCONT** | 18 | Continue stopped process |

**Nota:** SIGTERM è più "educato" di SIGKILL perché permette al processo di:
1. Chiudere file aperti
2. Salvare stato
3. Terminare connessioni
4. Fare cleanup delle risorse

### 5. /proc Filesystem (Linux)

Su Linux, le informazioni sui processi sono nel filesystem virtuale `/proc`:

```
/proc/
├─ 1/           # Process info per PID 1
│  ├─ cmdline   # Linea di comando
│  ├─ status    # Status dettagliato
│  ├─ fd/       # File descriptors aperti
│  └─ task/     # Thread del processo
├─ 2/           # Process info per PID 2
...
```

Questo progetto usa `psutil` che astrae `/proc`, ma il concetto è importante.

### 6. Memory Management

**Tipi di Memoria:**
- **RSS (Resident Set Size)**: Memoria fisica usata
- **VMS (Virtual Memory Size)**: Memoria virtuale totale
- **Shared Memory**: Memoria condivisa tra processi
- **Swap**: Memoria su disco usata come estensione RAM

```python
# Esempio dal codice
memory_info = proc.memory_info()
print(f"RSS: {memory_info.rss / (1024**2):.1f} MB")    # Fisica
print(f"VMS: {memory_info.vms / (1024**2):.1f} MB")    # Virtuale
```

---

## 📦 Installazione

### Prerequisiti

- Python 3.10 o superiore
- Pip (gestore pacchetti Python)

### Dipendenze

```bash
# Installa le dipendenze richieste
pip install psutil

# Opzionale: per UI avanzata con colori
pip install rich

# Opzionale: per configurazione YAML
pip install pyyaml
```

### Clonazione/Setup

```bash
# Se hai il progetto
cd process-manager/

# Verifica installazione
python main.py --help
```

---

## 🚀 Utilizzo

### Comandi Base

```bash
# Lista tutti i processi
python main.py list

# Lista ordinata per memoria
python main.py list --sort memory

# Filtra per nome
python main.py list --filter chrome

# Mostra albero processi
python main.py tree

# Modalità watch (auto-refresh)
python main.py watch

# Cerca processi
python main.py search python

# Termina processo
python main.py kill 1234

# Mostra dettagli processo
python main.py details 1234

# Statistiche sistema
python main.py stats
```

### Esempi Pratici

#### 1. Trovare processi che consumano molta CPU

```bash
python main.py list --sort cpu --limit 10
```

Output:
```
💻 Statistiche di sistema:
   CPU: 12.3% (8 cores)
   Memory: 6.2GB / 16.0GB (39%)

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  chrome                   45.2%    512.3   S         12
 5678  python                   23.1%    128.5   R         4
```

#### 2. Visualizzare la gerarchia

```bash
python main.py tree --pid 1
```

Mostra l'albero completo partendo da `init`.

#### 3. Monitorare in tempo reale

```bash
python main.py watch --interval 1 --sort cpu
```

Refresh ogni secondo, ordinato per consumo CPU.

#### 4. Terminare un processo

```bash
# Primo: cerca il PID
python main.py search firefox

# Poi: termina
python main.py kill 12345

# Forza (senza conferma)
python main.py kill 12345 --force

# Con SIGKILL (immediato)
python main.py kill 12345 --method sigkill
```

---

## 📁 Struttura del Progetto

```
process-manager/
├── main.py           # Entry point, CLI interface
├── process.py        # Core: raccolta info processi
├── tree.py           # Visualizzazione gerarchia
├── filter.py         # Filtraggio e ricerca
├── sort.py           # Ordinamento processi
├── killer.py         # Terminazione processi
├── config/
│   └── settings.yaml # Configurazione
└── README.md         # Questo file
```

### Moduli

#### `process.py`
Modulo principale per ottenere informazioni sui processi:
- `ProcessManager`: Classe principale
- `ProcessInfo`: Dataclass per info processo
- `get_all_processes()`: Ottieni tutti i processi
- `get_process_by_pid()`: Info per PID specifico
- `get_system_stats()`: Statistiche CPU/RAM

#### `tree.py`
Costruzione e visualizzazione albero:
- `ProcessTreeBuilder`: Costruisce gerarchia
- `ProcessTreeRenderer`: Visualizza albero
- `build_tree()`: Crea struttura ad albero
- `build_subtree()`: Sottoalbero da PID

#### `filter.py`
Filtri avanzati:
- `ProcessFilter`: Filtri per nome, CPU, memoria, stato
- `ProcessSearcher`: Ricerca combinata
- `multi_filter()`: Filtri con logica AND/OR
- Supporto regex per pattern complessi

#### `sort.py`
Ordinamento:
- `ProcessSorter`: Ordina per vari campi
- `TopNProcesses`: Seleziona top N
- `ProcessGrouper`: Raggruppa e aggrega
- Supporta multi-key sorting

#### `killer.py`
Terminazione sicura:
- `ProcessKiller`: Gestisce terminazione
- Supporta SIGTERM, SIGKILL, SIGINT
- Conferme di sicurezza
- Gestione albero processi

---

## 📊 Confronto con Tool Reali

| Feature | Process Manager (Questo) | top | htop |
|---------|-------------------------|-----|------|
| **Lista processi** | ✅ | ✅ | ✅ |
| **Albero processi** | ✅ | ⚠️ | ✅ |
| **Auto-refresh** | ✅ | ✅ | ✅ |
| **Colori** | ✅ | ⚠️ | ✅ |
| **Termina processi** | ✅ | ✅ | ✅ |
| **Filtraggio** | ✅ | ❌ | ⚠️ |
| **Dettagli estesi** | ✅ | ⚠️ | ⚠️ |
| **Codice leggibile** | ✅ | ❌ | ❌ |
| **Educativo** | ✅ | ❌ | ❌ |

**Differenze Chiave:**

1. **top**: Tool Unix originale, molto compatto ma interfaccia datata
2. **htop**: Versione migliorata di top, con UI ncurses molto usata
3. **Questo progetto**: Focus educativo, codice chiaro, commenti didattici

**Perché non usare direttamente htop?**
- htop è ottimo per l'uso quotidiano
- Questo progetto serve per **imparare** come funzionano questi tool
- Puoi studiare il codice e modificarlo per esperimenti
- Include safety checks che tool reali non hanno

---

## ⚠️ Avvertenze di Sicurezza

### ⛔ NON FARE

```bash
# NON terminare processi di sistema
python main.py kill 1       # init/systemd - può crashare il sistema!
python main.py kill 2       # kthreadd - processo kernel

# Non terminare processi senza capire cosa fanno
python main.py kill 9999    # Potrebbe essere un servizio critico
```

### ✅ BUONE PRATICHE

1. **Identifica prima il processo**
   ```bash
   python main.py search nome_processo
   python main.py details PID
   ```

2. **Usa SIGTERM prima di SIGKILL**
   ```bash
   python main.py kill PID --method sigterm   # Default
   ```

3. **Termina alberi con attenzione**
   ```bash
   python main.py tree --pid PID  # Controlla prima
   ```

4. **Non usare come root** se possibile
   - Evita danni accidentali
   - Molti processi di sistema sono protetti comunque

### Processi Protetti per Default

Il tool protegge alcuni PID critici:

- **PID 1**: `init` / `systemd`
- **PID 2**: `kthreadd`

Questi richiedono l'opzione `--force` per terminare (ma **non farlo** su un sistema in produzione!)

---

## 🎯 Esercizi Educativi

### Esercizio 1: Esplorazione Processi

```bash
# 1. Trova i 10 processi che consumano più CPU
python main.py list --sort cpu --limit 10

# 2. Trova i 10 processi che consumano più memoria
python main.py list --sort memory --limit 10

# 3. Cerca tutti i processi python
python main.py search python

# 4. Visualizza l'albero di un processo
python main.py tree --pid <PID_di_un_processo>
```

### Esercizio 2: Analisi Dettagliata

```bash
# 1. Scegli un processo interessante
python main.py search chrome

# 2. Guarda i dettagli
python main.py details <PID>

# 3. Analizza: quanti thread? quanta memoria? file aperti?

# 4. Guarda i suoi figli
python main.py tree --pid <PID>
```

### Esercizio 3: Creazione e Terminazione

```bash
# 1. Crea un processo di test
python -c "import time; time.sleep(100)" &

# 2. Trovalo
python main.py search python

# 3. Terminalo con SIGTERM
python main.py kill <PID>

# 4. Verifica che sia terminato
python main.py search python
```

### Esercizio 4: Monitoraggio

```bash
# 1. Avvia watch
python main.py watch --interval 1

# 2. Apri qualche programma in un altro terminale

# 3. Osserva come cambiano CPU e memoria in tempo reale

# 4. Nota i processi che appaiono e scompaiono
```

---

## 📖 Risorse per Approfondire

### Concetti di Sistema

- **Operating Systems: Three Easy Pieces** [OSTEP] - Capitolo sui Processi
- **The Linux Programming Interface** - Capitolo su Process Creation
- **Advanced Programming in the UNIX Environment** (APUE)

### Manpage Utili

```bash
man ps         # Process status
man top        # Visualizzatore processi
man kill       # Invio segnali
man fork       # System call fork
 man exec       # System call exec
man signal     # Gestione segnali
```

### Filesystem /proc

```bash
# Esplora /proc su Linux
ls /proc/
cat /proc/1/status        # Info su init
cat /proc/meminfo        # Info memoria
cat /proc/cpuinfo        # Info CPU
```

---

## 🤝 Contribuire

Questo è un progetto educativo. Suggerimenti e miglioramenti sono benvenuti:

1. Fork il progetto
2. Crea un branch per la tua feature
3. Aggiungi commenti educativi
4. Invia una PR

**Aree di miglioramento:**
- Supporto completo per Windows (senza psutil)
- Metriche aggiuntive (I/O, network)
- Export dati in CSV/JSON
- Grafici in tempo reale

---

## 📄 Licenza

Questo progetto è rilasciato a scopo educativo. Puoi usarlo, modificarlo e distribuirlo liberamente per scopi didattici.

**Attenzione:** Il codice di terminazione processi può essere pericoloso se usato impropriamente. Usalo con cautela e mai su sistemi di produzione senza aver compreso cosa stai facendo.

---

## 🙏 Riconoscimenti

- **psutil**: Libreria Python per informazioni di sistema
- **top/htop**: Ispirazione per il design
- **OSTEP**: Eccellente libro di riferimento per OS concepts

---

**Buon apprendimento! 🎓**

Ricorda: L'obiettivo non è solo usare il tool, ma **capire** come funzionano i processi sotto il cofano. Studia il codice, sperimenta, e non aver paura di rompere le cose (in una VM!)
