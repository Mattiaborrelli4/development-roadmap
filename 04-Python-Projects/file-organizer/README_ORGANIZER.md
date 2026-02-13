# 📁 File Organizer - Organizzatore di File Automatico

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style](https://img.shields.io/badge/Code%20Style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Level](https://img.shields.io/badge/Level-Intermediate-yellow.svg)](README.md)

> **Un utility Python per organizzare automaticamente i tuoi file per categoria, trovare duplicati e rinominare file in batch.**

---

## 📸 Screenshot del Programma

```
═══════════════════════════════════════════════════════════════════════════════
                      FILE ORGANIZER - Menu Principale
═══════════════════════════════════════════════════════════════════════════════
Scegli le operazioni da eseguire:

  [1] Organizza file per estensione
  [2] Trova duplicati
  [3] Rinomina file batch
  [4] Esegui tutto (1+2+3)
  [0] Esci
```

---

## ✨ Caratteristiche

- **🔄 Organizzazione Automatica**: Sposta i file in cartelle categorizzate in base all'estensione
- **🔍 Rilevamento Duplicati**: Trova file duplicati usando hash MD5 per identificazione precisa
- **✏️ Rinomina Batch**: Rinomina più file contemporaneamente con pattern personalizzati
- **📊 Report Dettagliati**: Genera report completi delle operazioni eseguite
- **🧪 Modalità Dry-Run**: Simula le operazioni senza modificare realmente i file
- **🛡️ Gestione Conflitti**: Gestione intelligente dei nomi file duplicati
- **🚀 Solo Librerie Standard**: Funziona senza dipendenze esterne

---

## 🎯 Perché Questo Progetto?

### Valore Didattico

Questo progetto è perfetto per studenti universitari e principianti perché:

- **Moduli Standard**: Impara a usare `os`, `shutil`, `pathlib`, `hashlib` - moduli essenziali per ogni programmatore Python
- **File System Operations**: Capire come Python interagisce con il sistema operativo
- **Gestione Errori**: Pratica con try/except per gestire permissions, file mancanti, errori I/O
- **Strutture Dati**: Usa dizionari, defaultdict, liste per organizzare le informazioni
- **CLI Interattiva**: Crea interfacce a riga di comando usabili e user-friendly
- **Type Hints**: Pratica con le annotazioni di tipo Python moderne

### Valore Portfolio

Per il tuo GitHub/LinkedIn, questo progetto dimostra:

- ✅ Capacità di scrivere utility pratiche e riutilizzabili
- ✅ Conoscenza del file system e gestione file
- ✅ Buone pratiche di coding (docstrings, type hints, PEP 8)
- ✅ Gestione errori robusta
- ✅ Esperienza con automazione e scripting

**NOTA**: I recruiter apprezzano molto i progetti di automazione file perché sono utilizzabili nel mondo reale!

### Casi d'Uso Reali

- **📥 Pulizia Downloads**: Organizza automaticamente la cartella Download caotica
- **📸 Gestione Foto**: Raggruppa foto per tipo (JPG, PNG, RAW)
- **📁 Backup Ordinato**: Prepara backup con struttura organizzata
- **🎓 Studio Universitario**: Organizza appunti, PDF, presentazioni per materia
- **💼 Lavoro**: Automatizza organizzazione documenti progetti

---

## 🚀 Installazione e Uso

### Prerequisiti

- **Python 3.7+** ([scarica qui](https://www.python.org/downloads/))
- Nessuna dipendenza esterna necessaria!

### Installazione

1. **Clona o scarica il progetto**:
   ```bash
   cd "04-Python-Projects/file-organizer"
   ```

2. **Verifica Python**:
   ```bash
   python --version
   # Output: Python 3.x.x
   ```

3. **Nessuna installazione richiesta**! Il codice usa solo librerie standard.

### Esecuzione

#### Modalità Interattiva (Consigliata)

```bash
python file_organizer.py
```

Segui le istruzioni a schermo per selezionare le operazioni.

#### Modalità Veloce

```bash
# Organizza una directory specifica
python file_organizer.py "C:\Users\matti\Downloads"

# Organizza la directory corrente
python file_organizer.py .

# Mostra aiuto
python file_organizer.py --help
```

---

## 📖 Esempi di Utilizzo

### Esempio 1: Organizzare Downloads

**Scenario**: Hai 100 file misti in Downloads e vuoi ordinarli.

```bash
python file_organizer.py
```

1. Seleziona `[1] Organizza file per estensione`
2. Inserisci percorso: `C:\Users\matti\Downloads`
3. Rispondi `n` a "Modalità DRY RUN?" per eseguire davvero

**Risultato**:
```
Downloads/
├── Images/         (foto, screenshot)
├── Documents/      (PDF, Word, Excel)
├── Videos/         (MP4, AVI)
├── Audio/          (MP3, WAV)
├── Archives/       (ZIP, RAR)
└── Others/         (tutto il resto)
```

### Esempio 2: Trovare Duplicati

**Scenario**: Sospetti di avere le stesse foto in più cartelle.

```bash
python file_organizer.py
```

1. Seleziona `[2] Trova duplicati`
2. Inserisci percorso della directory da analizzare
3. Rispondi `y` a "Usare hash MD5?" per confronto preciso

**Output**:
```
[*] TROVATI 3 GRUPPI DI DUPLICATI VERI:

  Gruppo 1: 2 file identici
  Hash: a3f5e9b2c4d1...
  Dimensione: 2,456,789 bytes
    - Photos/vacation.jpg
    - Backup/old_vacation.jpg
  Spazio recuperabile: 2,456,789 bytes (2.34 MB)
```

### Esempio 3: Rinomina Batch

**Scenario**: Hai file con spazi e caratteri strani da pulire.

```bash
python file_organizer.py
```

1. Seleziona `[3] Rinomina file batch`
2. Scegli pattern:
   - `[1] Timestamp` → `file_20250211_143022.txt`
   - `[2] Sequenziale` → `001_file.txt`, `002_file.txt`
   - `[3] Sanitize` → Rimuove caratteri speciali

### Esempio 4: Esegui Tutto

**Scenario**: Vuoi organizzare, trovare duplicati e rinominare in una volta.

```bash
python file_organizer.py
```

1. Seleziona `[4] Esegui tutto`
2. Conferma ogni operazione quando richiesto

---

## 🧩 Spiegazione del Codice

### Struttura del Programma

Il programma è organizzato in sezioni logiche:

```python
# 1. CONFIGURAZIONE
EXTENSION_MAP = {...}  # Mappa estensioni → cartelle
CHUNK_SIZE = 4096      # Dimensione chunk per hash

# 2. FUNZIONI UTILITY
print_header()          # Formatta output
validate_directory()    # Controlla path valido
calculate_file_hash()   # Calcola MD5
sanitize_filename()     # Pulisce nomi
get_unique_filename()   # Gestisce conflitti

# 3. FUNZIONI PRINCIPALI
organize_files()        # Sposta file per categoria
find_duplicates()       # Trova copie duplicate
rename_files()         # Rinomina in batch
generate_report()       # Crea report

# 4. INTERFACCIA UTENTE
interactive_mode()      # Menu interattivo
main()                  # Entry point
```

### Analisi Funzione per Funzione

#### `calculate_file_hash(file_path)`

**Scopo**: Calcola l'hash MD5 di un file per identificare duplicati.

**Come funziona**:
```python
def calculate_file_hash(file_path: Path) -> str:
    hash_obj = md5()

    # Legge il file a blocchi da 4KB
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()
```

**Concetti chiave**:
- **Lettura binaria** (`'rb'`): Necessaria per calcolare hash corretti
- **Lettura a chunk**: Evita di caricare file giganti in memoria
- **Hash MD5**: Algoritmo che produce una "firma" unica del file
- **`iter(lambda: ...)`**: Pattern Python per iterare con condizione di stop

**Perché MD5 e non SHA256?**
- MD5 è più veloce (sufficiente per trovare duplicati)
- SHA256 è più sicuro per crittografia, ma overkill qui

#### `organize_files(source_dir, dry_run)`

**Scopo**: Sposta i file nelle cartelle appropriate per categoria.

**Come funziona**:
```python
def organize_files(source_dir: Path, dry_run: bool = False) -> dict:
    # 1. Crea le cartelle delle categorie
    for category in categories:
        category_path = source_dir / category
        category_path.mkdir(exist_ok=True)

    # 2. Trova i file da organizzare
    files = [f for f in source_dir.iterdir()
             if f.is_file() and f.parent == source_dir]

    # 3. Sposta ogni file nella sua categoria
    for file_path in files:
        category = get_category(file_path)
        dest_path = dest_dir / file_path.name

        if dest_path.exists():
            dest_path = get_unique_filename(dest_path)

        if not dry_run:
            shutil.move(str(file_path), str(dest_path))
```

**Concetti chiave**:
- **`pathlib.Path`**: Metodo moderno per gestire percorsi (migliore di `os.path`)
- **List comprehension**: `[f for f in ...]` crea lista filtrata
- **`shutil.move()`**: Sposta file tra directory (come cut-paste)
- **`dry_run`**: Parametro booleano per simulare senza modificare
- **Operatori `/`**: `Path / "subdir"` crea percorsi in modo cross-platform

#### `find_duplicates(source_dir, use_hash)`

**Scopo**: Trova file duplicati confrontando hash.

**Come funziona**:
```python
def find_duplicates(source_dir: Path, use_hash: bool = True) -> dict:
    duplicates = {'by_hash': defaultdict(list)}

    # Raccogli tutti i file ricorsivamente
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = Path(root) / filename
            all_files.append(file_path)

    # Calcola hash e raggruppa
    for file_path in all_files:
        file_hash = calculate_file_hash(file_path)
        duplicates['by_hash'][file_hash].append(file_path)

    # Filtra solo i duplicati
    return {h: paths for h, paths in duplicates['by_hash'].items()
            if len(paths) > 1}
```

**Concetti chiave**:
- **`os.walk()`**: Visita directory ricorsivamente (albero completo)
- **`defaultdict(list)`**: Dizionario che crea liste automaticamente
- **Dictionary comprehension**: Crea dizionario filtrato in una riga

#### `rename_files(source_dir, pattern, dry_run)`

**Scopo**: Rinomina file in batch con pattern specifici.

**Pattern disponibili**:
```python
if pattern == 'timestamp':
    new_stem = f"{stem}_{timestamp}"  # file_20250211_143022
elif pattern == 'sequential':
    new_stem = f"{idx:03d}_{stem}"   # 001_file, 002_file
elif pattern == 'sanitize':
    new_stem = sanitize_filename(stem) # Rimuove caratteri speciali
```

**Concetti chiave**:
- **f-strings**: `f"{var}"` per formattazione stringhe moderne
- **`:03d`**: Formatta numero con 3 zeri padding (001, 002, ...)
- **`datetime.now()`**: Ottiene timestamp corrente

### Moduli Python Utilizzati

| Modulo | A cosa serve | Funzioni usate |
|--------|-------------|----------------|
| **`os`** | Operazioni sistema operativo | `os.walk()`, `os.access()` |
| **`shutil`** | Operazioni file high-level | `shutil.move()` |
| **`pathlib`** | Percorsi object-oriented | `Path()`, `.iterdir()`, `.mkdir()` |
| **`hashlib`** | Calcolo hash crittografici | `md5()`, `.hexdigest()` |
| **`datetime`** | Date e orari | `datetime.now()`, `.strftime()` |
| **`collections`** | Strutture dati specializzate | `defaultdict` |
| **`sys`** | Parametri sistema | `sys.argv`, `sys.exit()` |

---

## 📂 Struttura delle Cartelle

### Come Vengono Organizzati i File

Il programma crea automaticamente questa struttura:

```
directory_target/
├── Images/           # Tutti i file immagine
├── Documents/        # Documenti di testo e office
├── Videos/           # File video
├── Audio/            # File audio
├── Archives/         # Archivi compressi
└── Others/           # File non riconosciuti
```

### Mappa Completa Estensioni → Cartelle

#### 📸 Images
```
.jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico, .tiff, .tif
```

#### 📄 Documents
```
.pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx,
.csv, .json, .xml, .md
```

#### 🎬 Videos
```
.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpeg, .mpg
```

#### 🎵 Audio
```
.mp3, .wav, .flac, .aac, .ogg, .wma, .m4a, .opus
```

#### 📦 Archives
```
.zip, .rar, .7z, .tar, .gz, .bz2, .xz, .tgz
```

#### 📁 Others
```
Tutte le estensioni non elencate sopra
```

---

## 🔧 Funzionalità Avanzate

### 1. Trovare Duplicati con Hash

Il programma usa due metodi per trovare duplicati:

#### Per Nome File (Veloce)
```python
# Confronta solo i nomi
duplicates['by_name'][filename].append(file_path)
```

**Pro**: Molto veloce
**Contro**: Non rileva duplicati con nomi diversi

#### Per Hash MD5 (Preciso)
```python
# Confronta il contenuto reale
file_hash = calculate_file_hash(file_path)
duplicates['by_hash'][file_hash].append(file_path)
```

**Pro**: Rileva duplicati veri anche con nomi diversi
**Contro**: Più lento (deve leggere tutti i file)

**Perché due file con lo stesso nome non sono sempre duplicati?**
- `foto.jpg` in `Documenti/` potrebbe essere diverso da `foto.jpg` in `Backup/`
- L'hash confronta il **contenuto**, non il nome!

### 2. Rinomina Batch

Il programma supporta tre pattern di rinomina:

#### Timestamp
```python
# Prima: foto.jpg
# Dopo: foto_20250211_143022.jpg

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
new_stem = f"{stem}_{timestamp}"
```

**Uso**: Aggiunge data/ora per versionamento

#### Sequenziale
```python
# Prima: vacation.jpg, beach.jpg, sunset.jpg
# Dopo: 001_vacation.jpg, 002_beach.jpg, 003_sunset.jpg

for idx, file_path in enumerate(files, 1):
    new_stem = f"{idx:03d}_{stem}"
```

**Uso**: Crea sequenze numerate ordinate

#### Sanitize
```python
# Prima: file@#$%.txt
# Dopo: file_____.txt

invalid_chars = '<>:"/\\|?*'
for char in invalid_chars:
    sanitized = sanitized.replace(char, '_')
```

**Uso**: Pulisce nomi con caratteri non validi Windows

### 3. Report Generati

Il programma genera report automatici con:

```python
════════════════════════════════════════════════════════════════════
                         REPORT ORGANIZZAZIONE FILE
════════════════════════════════════════════════════════════════════
Generato: 2025-02-11 14:30:22

────────────────────────────────────────────────────────────────────────────────
1. ORGANIZZAZIONE PER ESTENSIONE
────────────────────────────────────────────────────────────────────────────────
File totali analizzati: 47
File spostati: 45
File saltati: 0
Errori: 2

File per categoria:
  Audio: 5 file
  Archives: 3 file
  Documents: 12 file
  Images: 20 file
  Others: 5 file
  Videos: 2 file

────────────────────────────────────────────────────────────────────────────────
2. ANALISI DUPLICATI
────────────────────────────────────────────────────────────────────────────────
File analizzati: 47
Gruppi duplicati trovati: 3

────────────────────────────────────────────────────────────────────────────────
3. RINOMINA BATCH
────────────────────────────────────────────────────────────────────────────────
File processati: 47
File rinominati: 10
File saltati: 37
Errori: 0
```

**Salvataggio report**:
```python
# Il report può essere salvato automaticamente
report_file = target_dir / f"report_{timestamp}.txt"
generate_report(org_stats, dup_stats, ren_stats, report_file)
```

---

## 🚀 Come Contribuire/Estendere

### Idee per Miglioramenti

#### 1. Nuove Categorie di File

Aggiungi nuove estensioni alla mappa:

```python
EXTENSION_MAP = {
    # ... codice esistente ...

    # Aggiungi eBook
    '.epub': 'Documents',
    '.mobi': 'Documents',
    '.azw': 'Documents',

    # Aggiungi Codice
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',

    # Aggiungi 3D Models
    '.obj': '3D',
    '.fbx': '3D',
    '.blend': '3D',
}
```

#### 2. Pattern di Rinomina Personalizzati

Crea il tuo pattern:

```python
def rename_files(source_dir: Path, pattern: str = 'timestamp', ...):
    # Aggiungi questo nel blocco if/elif
    elif pattern == 'lowercase':
        new_stem = stem.lower()  # Tutto minuscolo

    elif pattern == 'uppercase':
        new_stem = stem.upper()  # Tutto maiuscolo

    elif pattern == 'snake_case':
        new_stem = stem.replace(" ", "_").lower()  # Spazi → underscore

    elif pattern == 'remove_spaces':
        new_stem = stem.replace(" ", "")  # Rimuove spazi
```

#### 3. Spostamento Ricorsivo

Attualmente il programma organizza solo i file nella directory root. Per organizzare anche le sottocartelle:

```python
def organize_files_recursive(source_dir: Path, dry_run: bool = False):
    """Organizza file anche nelle sottocartelle."""

    for root, dirs, files in os.walk(source_dir):
        root_path = Path(root)

        # Salta le cartelle delle categorie
        if root_path.name in EXTENSION_MAP.values():
            continue

        for filename in files:
            file_path = root_path / filename

            # Determina categoria e sposta
            category = get_category(file_path)
            dest_dir = source_dir / category
            dest_path = dest_dir / filename

            if not dry_run:
                shutil.move(str(file_path), str(dest_path))
```

#### 4. Auto-Cancellazione Duplicati

Aggiungi un'opzione per cancellare automaticamente i duplicati:

```python
def remove_duplicates(duplicates: dict, dry_run: bool = True):
    """Rimuove i duplicati tenendo solo la prima copia."""

    for file_hash, file_list in duplicates.items():
        if len(file_list) > 1:
            # Tieni il primo, cancella gli altri
            original = file_list[0]
            copies = file_list[1:]

            print(f"[*] Mantenuto: {original}")

            for copy in copies:
                if dry_run:
                    print(f"[SIMULATE] Cancellerei: {copy}")
                else:
                    copy.unlink()
                    print(f"[DELETED] {copy}")
```

⚠️ **ATTENZIONE**: Fai sempre backup prima di cancellare!

#### 5. File di Configurazione

Salva le preferenze in un file JSON:

```python
import json

def load_config(config_file='config.json'):
    """Carica configurazione da file."""
    default_config = {
        'categories': EXTENSION_MAP,
        'auto_delete_duplicates': False,
        'default_pattern': 'timestamp'
    }

    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_config

def save_config(config, config_file='config.json'):
    """Salva configurazione su file."""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
```

**File `config.json`**:
```json
{
    "categories": {
        ".jpg": "Images",
        ".pdf": "Documents"
    },
    "auto_delete_duplicates": false,
    "default_pattern": "timestamp"
}
```

#### 6. Logging su File

Salva tutte le operazioni in un file di log:

```python
import logging

def setup_logging(log_file='file_organizer.log'):
    """Configura logging su file."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_operation(message: str):
    """Scrive messaggio nel log."""
    logging.info(message)
    print(message)  # Stampa anche a schermo
```

---

## 📚 Concetti Python Appresi

### 1. Type Hints (Python 3.5+)

```python
def organize_files(source_dir: Path, dry_run: bool = False) -> dict:
    #                    ^^^^^^           ^^^^^              ^^^^
    #                    parametro         tipo param.       tipo ritorno
```

**Vantaggi**:
- Documentazione integrata
- IDE ti avvisa se usi tipi sbagliati
- Più facile manutenzione

### 2. Context Managers (`with`)

```python
with open(file_path, 'rb') as f:
    # Codice che usa il file
# File automaticamente chiuso qui, anche se c'è errore
```

**Vantaggi**:
- Chiude automaticamente le risorse
- Gestisce errori correttamente
- Codice più pulito

### 3. Pathlib vs os.path

```python
# Vecchio stile (os.path)
path = os.path.join("folder", "subfolder", "file.txt")
exists = os.path.exists(path)

# Nuovo stile (pathlib) - MEGLIO!
path = Path("folder") / "subfolder" / "file.txt"
exists = path.exists()
```

**Vantaggi pathlib**:
- Sintassi più pulita con `/`
- Cross-platform (Windows/Linux/Mac)
- Metodi utili integrati (`.read_text()`, `.write_text()`)

### 4. Dictionary e List Comprehension

```python
# Lista file filtrata
files = [f for f in source_dir.iterdir() if f.is_file()]

# Dizionario filtrato
duplicates = {h: paths for h, paths in hash_dict.items()
              if len(paths) > 1}
```

**Vantaggi**:
- Più conciso di loop tradizionali
- Più Pythonic (stiloso)
- Spesso più veloce

### 5. Defaultdict

```python
from collections import defaultdict

# Senza defaultdict - soggetto a KeyError
d = {}
if 'key' not in d:
    d['key'] = []
d['key'].append(value)

# Con defaultdict - automatico!
d = defaultdict(list)
d['key'].append(value)  # Crea lista automaticamente
```

---

## 🐛 Risoluzione Problemi Comuni

### Errore: "Permission Denied"

**Causa**: Non hai permessi per leggere/scrivere nella directory.

**Soluzione**:
- Esegui come amministratore (Windows) o usa `sudo` (Linux/Mac)
- Scegli una directory dove hai permessi (es. Documents)

### Errore: "File in use"

**Causa**: Un file è aperto in un altro programma.

**Soluzione**:
- Chiudi Word, Excel, lettori PDF prima di eseguire
- Il programma salta i file in uso automaticamente

### File non vengono organizzati

**Causa**: L'estensione non è nella mappa `EXTENSION_MAP`.

**Soluzione**:
- Il file finirà in `Others/`
- Aggiungi l'estensione alla mappa nel codice

### Troppi file elaborati lentamente

**Causa**: Calcolo hash MD5 è lento su molti file grandi.

**Soluzione**:
- Usa `use_hash=False` per duplicati per nome (più veloce)
- La prima volta sarà lenta, poi puoi solo organizzare

---

## 📊 Metriche del Progetto

- **Righe di codice**: ~850
- **Funzioni**: 15
- **Moduli usati**: 7 (tutti standard library)
- **Tempo sviluppo stimato**: 5-7 giorni
- **Difficoltà**: Intermediate

---

## 🤝 Contribuire

Questo è un progetto didattico, ma se vuoi migliorarlo:

1. Fai fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/NuovaFunzione`)
3. Commit le tue modifiche (`git commit -m 'Aggiunta nuova funzionalità'`)
4. Push al branch (`git push origin feature/NuovaFunzione`)
5. Apri una Pull Request

---

## 📝 License

Questo progetto è rilasciato sotto la **MIT License**.

```
MIT License

Copyright (c) 2025 Student Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

Questo significa che puoi:
- ✅ Usare il codice per progetti personali/commerciali
- ✅ Modificare il codice
- ✅ Distribuire il codice modificato
- ❂ Devi includere la licenza originale

---

## 👨‍💻 Autore

**Student Project** - Portfolio Python Project

- 📧 Email: [tua email]
- 🔗 GitHub: [github.com/tuo-username]
- 💼 LinkedIn: [linkedin.com/in/tuo-profilo]

---

## 🙏 Riconoscimenti

- **Python Software Foundation**: Per le ottime librerie standard
- **Automate the Boring Stuff with Python**: Ispirazione per il progetto
- **PEP 8**: Style guide per Python

---

## 📚 Ulteriori Risorse

### Per Imparare Python

- [Python.org Tutorial](https://docs.python.org/3/tutorial/) - Ufficiale e gratuito
- [Automate the Boring Stuff](https://automatetheboringstuff.com/) - Libro gratuito
- [Real Python](https://realpython.com/) - Tutorial avanzati
- [freeCodeCamp Python](https://www.freecodecamp.org/learn/) - Corso completo

### Per Approfondire

- **pathlib documentation**: Gestione percorsi moderna
- **shutil documentation**: Operazioni file high-level
- **hashlib documentation**: Hash e crittografia
- **PEP 8**: Style guide ufficiale Python

---

## 📝 Changelog

### Versione 1.0.0 (2025-02-11)

**Features**:
- ✅ Organizzazione file per estensione
- ✅ Rilevamento duplicati con MD5
- ✅ Rinomina batch con 3 pattern
- ✅ Report automatici
- ✅ Modalità dry-run
- ✅ Interfaccia interattiva
- ✅ Gestione conflitti nomi

**Bug noti**:
- Nessuno al momento

---

## 🎓 Progetti Correlati

Altri progetti Python nel portfolio:

1. **To-Do List CLI** - Gestione task con JSON
2. **Number Guessing Game** - Gioco con random e loops
3. **Unit Converter** - Conversioni con matematica

---

## ⭐ Se questo progetto ti è stato utile

Lascia una stella su GitHub! Condividi con altri studenti.

**Happy Coding! 🐍**
