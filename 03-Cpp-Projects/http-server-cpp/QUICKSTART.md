# 🚀 Guida Rapida - HTTP Server C++

## Prerequisiti

### Windows
- **MinGW-w64**: [Download](https://www.mingw-w64.org/)
  - Aggiungere `bin/` al PATH
- **OPPURE Visual Studio Build Tools**
- **OPPURE CMake** (per build cross-platform)

### Linux
- **GCC/G++**: `sudo apt install build-essential`
- **CMake** (opzionale): `sudo apt install cmake`

## 📦 Compilazione Rapida

### Windows (MinGW)
```batch
build.bat
```

### Windows (MSVC)
Aprire "Developer Command Prompt for VS", poi:
```batch
build-msvc.bat
```

### Linux / macOS
```bash
chmod +x build.sh
./build.sh
```

### CMake (Tutte le piattaforme)
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

## 🎮 Esecuzione

### Avvio Base
```batch
# Windows
server.exe

# Linux/macOS
./server
```

### Configurazione Avanzata
```batch
# Porta personalizzata
server.exe --port 3000

# Directory web root personalizzata
server.exe --root C:/mysite

# Thread pool personalizzato
server.exe --threads 8

# Tutte le opzioni
server.exe --port 80 --root ./public --threads 16
```

## 🌐 Test nel Browser

Apri il browser e visita:
```
http://localhost:8080
```

**Test vari:**
- http://localhost:8080/ - Homepage
- http://localhost:8080/index.html - Homepage esplicito
- http://localhost:8080/styles.css - Foglio di stile
- http://localhost:8080/script.js - JavaScript
- http://localhost:8080/nonexistent.html - Test 404

## 🧪 Test da CLI

### curl
```bash
# Test base
curl http://localhost:8080

# Test headers
curl -I http://localhost:8080

# Test verbose
curl -v http://localhost:8080/index.html

# Test 404
curl http://localhost:8080/notfound
```

### PowerShell
```powershell
# Test base
Invoke-WebRequest http://localhost:8080

# Test headers
Invoke-WebRequest -Uri http://localhost:8080 -Method Head

# Test response
$response = Invoke-WebRequest http://localhost:8080
$response.Content
```

## 📊 Output Console

Esempio di output quando il server è in esecuzione:

```
========================================
   HTTP Server C++ - Multi-threaded
========================================
Configurazione:
  - Porta: 8080
  - Web Root: ./public
  - Thread Pool: 4 worker threads
========================================

Server in ascolto su http://localhost:8080
Web root: ./public
Premi Ctrl+C per fermare il server
Connessione da 127.0.0.1
Thread 12345 - GET /index.html
Connessione da 127.0.0.1
Thread 12346 - GET /styles.css
```

## 🛑 Arresto

Premere `Ctrl+C` nella console per arrestare il server in modo sicuro.

## 🔍 Troubleshooting

### "Address already in use"
Un'altra istanza è in esecuzione. Chiuderla o usare una porta diversa:
```batch
server.exe --port 8081
```

### "Permission denied" (Linux)
Porte < 1024 richiedono root:
```bash
sudo ./server --port 80
```

### Firewall Windows
Consenti l'accesso su Windows Firewall quando richiesto.

## 📁 Struttura File Statici

```
public/
├── index.html          # Homepage
├── styles.css          # Stili
├── script.js           # JavaScript
├── images/             # Cartella immagini (da creare)
│   ├── logo.png
│   └── photo.jpg
└── subdir/             # Sottodirectory
    └── page.html
```

## ✅ Verifica Funzionamento

1. **Compilazione**: Nessun errore
2. **Avvio**: Server in ascolto sulla porta
3. **Browser**: Homepage caricata correttamente
4. **Console**: Log delle richieste visualizzate
5. **CSS/JS**: Stili e script caricati
6. **404**: Pagina non trovata restituisce errore

## 🎓 Prossimi Passi

- Esplora il codice sorgente
- Modifica `public/index.html` per personalizzare
- Aggiungi nuovi file in `public/`
- Sperimenta con diverse configurazioni
- Leggi `README.md` per dettagli tecnici

---

**Buon divertimento con il tuo server HTTP C++! 🎉**
