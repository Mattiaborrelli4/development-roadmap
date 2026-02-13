# 🧪 Guida al Test - File Organizer

## 🎯 Come Testare l'Applicazione

### Metodo 1: Test con la Cartella Downloads (Più Semplice)

1. **Avvia l'applicazione:**
   ```bash
   # Windows
   run.bat

   # Linux/Mac
   ./run.sh
   ```

2. **Scarica alcuni file di test:**
   - Una immagine (es. da browser)
   - Un PDF
   - Un file MP3
   - Un file ZIP

3. **Osserva:**
   - I file verranno automaticamente spostati nelle sottocartelle
   - Controlla `organizer.log` per i dettagli

### Metodo 2: Test con Cartella Demo

#### 1. Crea Cartella di Test
```bash
# Windows
mkdir C:\Users\matti\Desktop\TestOrganizer

# Linux/Mac
mkdir -p ~/Desktop/TestOrganizer
```

#### 2. Crea File di Test
Crea manualmente questi file nella cartella di test:

**Windows (PowerShell):**
```powershell
cd C:\Users\matti\Desktop\TestOrganizer
New-Item -ItemType File -Name "documento.pdf"
New-Item -ItemType File -Name "foto.png"
New-Item -ItemType File -Name "canzone.mp3"
New-Item -ItemType File -Name "video.mkv"
New-Item -ItemType File -Name "archivio.zip"
New-Item -ItemType File -Name "codice.java"
```

**Linux/Mac:**
```bash
cd ~/Desktop/TestOrganizer
touch documento.pdf foto.png canzone.mp3 video.mkv archivio.zip codice.java
```

#### 3. Avvia Organizer sulla Cartella di Test
```bash
# Windows
run.bat "C:\Users\matti\Desktop\TestOrganizer"

# Linux/Mac
./run.sh ~/Desktop/TestOrganizer
```

#### 4. Risultato Atteso
Dovresti vedere questa struttura:
```
TestOrganizer/
├── Documenti/
│   └── documento.pdf
├── Immagini/
│   └── foto.png
├── Musica/
│   └── canzone.mp3
├── Video/
│   └── video.mkv
├── Archivi/
│   └── archivio.zip
└── Codice/
    └── codice.java
```

### Metodo 3: Test con File Reali

#### Scarica file di test da internet:
- **PDF:** https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
- **Immagini:** Qualsiasi immagine da Google Images
- **Video:** Piccolo video sample
- **Audio:** File MP3 di prova

## 🧪 Casi di Test

### Test 1: File Singolo
- [ ] Crea un file `test.txt`
- [ ] Verifica che venga spostato in `Documenti/`
- [ ] Controlla il log

**Risultato atteso:**
```
[INFO] [SPSTATO] test.txt -> Documenti/
```

### Test 2: File Duplicati
- [ ] Crea `doc.pdf`
- [ ] Crea un altro `doc.pdf`
- [ ] Verifica che vengano rinominati

**Risultato atteso:**
```
Documenti/doc.pdf
Documenti/doc_1.pdf
```

### Test 3: Estensione Sconosciuta
- [ ] Crea un file `test.xyz`
- [ ] Verifica il warning nel log

**Risultato atteso:**
```
[WARNING] Nessuna regola per estensione .xyz (test.xyz)
```

### Test 4: Monitoraggio Real-time
- [ ] Avvia l'organizer
- [ ] Mentre è in esecuzione, scarica un file
- [ ] Verifica che venga organizzato immediatamente

### Test 5: Cartella Personalizzata
- [ ] Crea una cartella `C:\TestMessy`
- [ ] Metti vari file dentro
- [ ] Esegui: `run.bat "C:\TestMessy"`
- [ ] Verifica l'organizzazione

### Test 6: Config Personalizzata
- [ ] Modifica `config.json` aggiungendo:
  ```json
  "MiaCartella": ["test"]
  ```
- [ ] Crea un file `file.test`
- [ ] Riavvia l'organizer
- [ ] Verifica che vada in `MiaCartella/`

## 📊 Checklist Funzionalità

- [ ] **WatchService** funziona correttamente
- [ ] **Spostamento automatico** dei nuovi file
- [ ] **Creazione automatica** delle sottocartelle
- [ ] **Gestione duplicati** con suffissi
- [ ] **Parsing JSON** delle regole
- [ ] **Logging** con timestamp
- [ ] **Shutdown** pulito con CTRL+C
- [ ] **Rilevamento estensioni** (case insensitive)
- [ ] **File senza estensione** ignorati correttamente
- [ ] **Config di default** creato se mancante

## 🐛 Troubleshooting Test

### I file non vengono spostati
1. Verifica che l'estensione sia in `config.json`
2. Controlla `organizer.log` per errori
3. Assicurati che WatchService sia partito

### "File non trovato"
1. Verifica il path della cartella
2. Usa path assoluti, non relativi
3. Su Windows, usa le virgolette: `"C:\Path Con Spazi"`

### "NoClassDefFoundError: Gson"
1. Scarica gson-2.10.1.jar
2. Mettilo nella cartella `lib/`
3. Ricompila con `build.bat`

### Log non viene creato
1. Verifica permessi di scrittura
2. Controlla che la cartella esista
3. Guarda la console per errori

## 📸 Screenshot Output Console

Ecco cosa dovresti vedere:

```
========================================
  Java File Organizer
========================================

Monitoraggio cartella: C:\Users\matti\Downloads

[2026-02-12 15:30:45] [INFO] === AVVIO FILE ORGANIZER ===
[2026-02-12 15:30:45] [INFO] Directory monitorata: C:\Users\matti\Downloads
[2026-02-12 15:30:45] [INFO] Regole caricate: 45 estensioni configurate
[2026-02-12 15:30:45] [INFO] Creata cartella: Documenti
[2026-02-12 15:30:45] [INFO] Creata cartella: Immagini
[2026-02-12 15:30:45] [INFO] Directory registrata: C:\Users\matti\Downloads
[2026-02-12 15:30:45] [INFO] Organizzazione file esistenti...
[2026-02-12 15:30:46] [INFO] File esistenti organizzati: 0
[2026-02-12 15:30:46] [INFO] Monitoraggio attivo. Premi CTRL+C per terminare.

[2026-02-12 15:31:00] [INFO] Nuovo file rilevato: documento.pdf
[2026-02-12 15:31:00] [INFO] [SPSTATO] documento.pdf -> Documenti/
```

## 🎓 Esercizi di Apprendimento

### Esercizio 1: Aggiungi Nuova Categoria
Aggiungi una categoria "Ebooks" per `.epub` e `.mobi`

### Esercizio 2: Modifica Logger
Modifica il formatter per includere il thread ID

### Esercizio 3: Statistiche
Aggiungi un contatore di file organizzati e stampalo all'uscita

### Esercizio 4: File di Config Predefinito
Se config.json non esiste, crealo con 5 categorie base

---

**Buon testing!** 🚀
