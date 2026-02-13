# 📦 Struttura Progetto - File Organizer

## Albero delle Cartelle

```
file-organizer/
│
├── 📄 README.md                    # Documentazione principale (italiano)
├── 📄 QUICKSTART.md               # Guida rapida per iniziare
├── 📄 PROJECT_STRUCTURE.md        # Questo file
├── 📄 pom.xml                     # Configurazione Maven (opzionale)
├── 📄 .gitignore                  # File ignorati da Git
│
├── 🔧 build.bat                   # Script compilazione Windows
├── 🔧 run.bat                     # Script esecuzione Windows
├── 🔧 build.sh                    # Script compilazione Linux/Mac
├── 🔧 run.sh                      # Script esecuzione Linux/Mac
│
├── 📂 src/                        # Codice sorgente
│   └── main/
│       ├── java/
│       │   └── com/
│       │       └── organizer/
│       │           └── FileOrganizer.java    # Classe principale
│       │
│       └── resources/
│           └── config.json                    # Regole di organizzazione
│
├── 📂 lib/                        # Librerie esterne
│   └── gson-2.10.1.jar            # Gson JSON parser (da scaricare)
│
├── 📂 out/                        # File compilati (.class)
│   ├── com/
│   │   └── organizer/
│   │       └── FileOrganizer.class
│   └── config.json                # Copia del config
│
├── 📂 logs/                       # Cartella log (creata in runtime)
│
└── 📄 organizer.log               # Log dell'applicazione (generato)
```

## 📁 File Principali

### FileOrganizer.java
**Percorso:** `src/main/java/com/organizer/FileOrganizer.java`

**Classe principale** che implementa:
- `WatchService` per monitorare la directory
- Caricamento regole da JSON
- Organizzazione automatica dei file
- Sistema di logging con timestamp
- Gestione duplicati

**Metodi chiave:**
- `startWatching(Path directory)` - Avvia il monitoraggio
- `organizeFile(Path file)` - Sposta i file nella cartella corretta
- `loadRules(Path configPath)` - Carica regole JSON
- `processEvents()` - Loop di monitoraggio eventi

### config.json
**Percorso:** `src/main/resources/config.json`

**File di configurazione** che definisce le regole di organizzazione:
```json
{
  "Documenti": ["pdf", "doc", "docx", "txt"],
  "Immagini": ["jpg", "png", "gif"],
  "Video": ["mp4", "avi", "mkv"],
  "Musica": ["mp3", "flac"],
  "Archivi": ["zip", "rar"]
}
```

### organizer.log
**Percorso:** `organizer.log` (nella root del progetto)

**File di log** generato automaticamente con:
- Timestamp per ogni operazione
- Livello di log (INFO, WARNING, SEVERE)
- Tracciamento di tutti i movimenti file

## 🔄 Flusso di Esecuzione

```
1. MAIN()
   ├─ Legge args (cartella, config)
   ├─ Verifica esistenza config.json
   ├─ Crea FileOrganizer
   └─ Chiama startWatching()

2. STARTWATCHING()
   ├─ Crea sottocartelle categorie
   ├─ Registra WatchService
   ├─ Organizza file esistenti
   └─ Avvia processEvents()

3. PROCESSEVENTS() [LOOP]
   ├─ Attende eventi filesystem
   ├─ ENTRY_CREATE → organizeFile()
   └─ ENTRY_MODIFY → organizeFile()

4. ORGANIZEFILE()
   ├─ Estrae estensione
   ├─ Cerca regola in config
   ├─ Gestisce duplicati
   ├─ Sposta file
   └─ Logga operazione
```

## 🔧 Script di Build

### build.bat / build.sh
1. Verifica installazione Java
2. Verifica presenza Gson
3. Crea directory `out/`
4. Compila `FileOrganizer.java`
5. Copia `config.json` in `out/`

### run.bat / run.sh
1. Verifica compilazione
2. Verifica config.json
3. Esegue `java -cp "out;lib/*" com.organizer.FileOrganizer`
4. Accetta parametri opzionali:
   - `$1` = Cartella da monitorare
   - `$2` = Path config.json alternativo

## 📊 Dipendenze

### Richiesta
- **Gson 2.10.1** - Parsing JSON
  - Download: https://github.com/google/gson/releases
  - Posizione: `lib/gson-2.10.1.jar`

### Opzionale (Maven)
- **JUnit 4.13.2** - Testing (non usato in questo progetto)

## 🎯 Classi e Package

```
com.organizer
└── FileOrganizer
    ├── Campi
    │   ├── WatchService watchService
    │   ├── Map<String, String> rules
    │   ├── Logger logger
    │   └── Path watchDir
    │
    └── Metodi
        ├── setupLogger()
        ├── loadRules()
        ├── startWatching()
        ├── createCategoryFolders()
        ├── registerDirectory()
        ├── organizeExistingFiles()
        ├── processEvents()
        ├── organizeFile()
        ├── handleDuplicate()
        ├── getFileExtension()
        └── stop()
```

## 🔐 Gestione Errori

| Situazione | Comportamento |
|-----------|---------------|
| config.json mancante | Crea config di default |
| Estensione sconosciuta | Warning nel log, file ignorato |
| Cartella inesistente | Errore fatale con log |
| File duplicato | Rinomina con `_1`, `_2`, etc. |
| WatchService interrotto | Log SEVERE e terminazione |

## 📝 Log Example

```
[2026-02-12 15:30:45] [INFO] === AVVIO FILE ORGANIZER ===
[2026-02-12 15:30:45] [INFO] Directory monitorata: C:\Users\matti\Downloads
[2026-02-12 15:30:45] [INFO] Regole caricate: 45 estensioni
[2026-02-12 15:30:46] [INFO] [SPSTATO] doc.pdf -> Documenti/
[2026-02-12 15:30:46] [INFO] [SPSTATO] img.png -> Immagini/
[2026-02-12 15:31:20] [INFO] Nuovo file rilevato: song.mp3
[2026-02-12 15:31:20] [INFO] [SPSTATO] song.mp3 -> Musica/
```

## 🚀 Comandi Utili

### Compilazione
```bash
# Windows
build.bat

# Linux/Mac
chmod +x build.sh && ./build.sh
```

### Esecuzione
```bash
# Windows - Cartella Downloads (default)
run.bat

# Windows - Cartella personalizzata
run.bat "C:\Users\matti\Desktop\DaOrganizzare"

# Linux/Mac - Cartella personalizzata
./run.sh "/home/matti/Desktop/Messy"
```

### Manuale
```bash
# Compila manualmente
javac -cp "lib/*" -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java

# Esegui manualmente
java -cp "out;lib/*" com.organizer.FileOrganizer "C:\Downloads"
```

## 📌 Note Importanti

- **WatchService** funziona solo su filesystem locali
- La cartella monitorata deve esistere prima dell'avvio
- I file vengono **spostati** (non copiati)
- Le sottocartelle vengono create automaticamente
- CTRL+C ferma il monitoraggio in modo pulito
- Il log è in append (non sovrascrive le esecuzioni precedenti)

---

**Ultimo aggiornamento:** Febbraio 2026
