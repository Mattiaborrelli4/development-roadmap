# ⚡ Quick Start - HTTP Server in C

## 🚀 Avvio Rapido

### 1. Compila
```bash
# Windows
build.bat

# Linux
chmod +x build.sh && ./build.sh
```

### 2. Esegui
```bash
# Windows
server.exe

# Linux
./server
```

### 3. Naviga
Apri il browser: **http://localhost:8080**

## ✅ Verifica Funzionamento

Dovresti vedere una pagina con:
- Titolo: "Server HTTP in C"
- 4 card con le funzionalità
- Tabella delle informazioni tecniche
- Link di navigazione

## 📁 Files Importanti

| File | Descrizione |
|------|-------------|
| `server.c` | Codice sorgente (470 righe) |
| `server.exe` | Eseguibile compilato |
| `public/` | File statici da servire |

## 🧪 Testing Rapido

```bash
# Test con curl
curl http://localhost:8080/

# Test 404
curl http://localhost:8080/nonexistent.html

# Test Content-Type CSS
curl http://localhost:8080/style.css
```

## 🛑 Stop Server

**Ctrl+C** nella finestra del server

## 📖 Documentazione

- `README.md` - Documentazione completa
- `TESTING.md` - Guida dettagliata al testing
- `DIAGRAMMI.md` - Architettura e diagrammi

## 🎯 Caratteristiche Principali

✅ Socket TCP/IP
✅ HTTP/1.1 Parser
✅ File Statici
✅ Multi-Threading
✅ Content-Type corretti
✅ Error 404
✅ Cross-platform (Windows/Linux)

## 🔧 Porta Personalizzata

```bash
server.exe 3000
```

## 💡 Note

- Il server serve solo richieste **GET**
- Directory web: `./public`
- Log richieste nella console
- Un thread per ogni connessione

---

**Progetto completato e testato!**
