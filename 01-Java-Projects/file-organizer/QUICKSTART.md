# Guida Rapida - File Organizer

## 🚀 Setup in 2 Minuti

### Passo 1: Scarica Gson
Vai su https://github.com/google/gson/releases e scarica `gson-2.10.1.jar`

Metti il file nella cartella `lib/`:
```
file-organizer/
└── lib/
    └── gson-2.10.1.jar  ← Qui
```

### Passo 2: Compila
**Windows:**
```bash
build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

### Passo 3: Esegui
**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

## 📁 Cosa Succede

1. L'applicazione monitora la tua cartella **Downloads**
2. Quando scarichi un file, viene spostato automaticamente:
   - `documento.pdf` → `Downloads/Documenti/`
   - `foto.png` → `Downloads/Immagini/`
   - `canzone.mp3` → `Downloads/Musica/`

## 🎯 Cartella Personalizzata

```bash
# Windows
run.bat "C:\Users\matti\Desktop\DaOrganizzare"

# Linux/Mac
./run.sh "/home/matti/Desktop/Unorganized"
```

## 📊 Esempio Log

```
[2026-02-12 15:30:45] [INFO] === AVVIO FILE ORGANIZER ===
[2026-02-12 15:30:45] [INFO] Directory monitorata: C:\Users\matti\Downloads
[2026-02-12 15:30:46] [INFO] File esistenti organizzati: 23
[2026-02-12 15:31:20] [INFO] Nuovo file rilevato: manuale.pdf
[2026-02-12 15:31:20] [INFO] [SPSTATO] manuale.pdf -> Documenti/
```

## ⚙️ Modificare Regole

Apri `config.json` e modifica:

```json
{
  "Documenti": ["pdf", "doc"],
  "I miei PDF": ["pdf"],  ← Nuova categoria
  "Lavoro": ["docx", "xlsx"]  ← Altra categoria
}
```

Riavvia l'applicazione per applicare le modifiche.

## 🛑 Fermare

Premi **CTRL+C** nella finestra della console.

---

**Problemi?** Vedi README.md completo per troubleshooting.
