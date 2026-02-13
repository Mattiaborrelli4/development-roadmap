# Quick Reference Card - Chat Server

## Comandi Essenziali

### Avvio Server
```bash
cd src\server
java server.ChatServer [porta]
# Default porta: 9999
```

### Avvio Client
```bash
cd src\client
java client.ChatClient [nickname] [host] [porta]
# Esempio: java client.ChatClient Mario localhost 9999
```

## Comandi Chat

| Comando | Sintassi | Descrizione |
|---------|----------|-------------|
| Messaggio | `testo` | Invia messaggio alla room corrente |
| `/join` | `/join <room>` | Entra in una room |
| `/leave` | `/leave` | Torna alla room "general" |
| `/whisper` | `/whisper <nick> <msg>` | Messaggio privato |
| `/list` | `/list` | Lista tutte le room |
| `/users` | `/users` | Lista utenti nella room |
| `/quit` | `/quit` | Esci dalla chat |
| `/help` | `/help` | Mostra aiuto |

## Protocollo

### Client → Server
```
NICK nickname
JOIN room
MSG testo
WHISPER nick testo
```

### Server → Client
```
OK messaggio
ERROR errore
MSG nick: testo
WHISPER nick: testo
JOINED nick
LEFT nick
INFO info
```

## File

| File | Descrizione |
|------|-------------|
| `ChatServer.java` | Server principale |
| `ClientHandler.java` | Gestore singolo client |
| `ChatClient.java` | Client console |
| `chat.log` | Log messaggi (autogenerato) |
| `README.md` | Documentazione completa |
| `GUIDA_TEST.md` | Guida al testing |
| `DETTAGLI_TECNICI.md` | Dettagli architettura |

## Struttura

```
src/
├── server/
│   ├── ChatServer.java      + .class
│   ├── ClientHandler.java   + .class
│   └── chat.log            (generato)
└── client/
    └── ChatClient.java      + .class
```

## Troubleshooting Rapido

| Problema | Soluzione |
|----------|----------|
| Porta in uso | Cambia porta o chiudi altri server |
| Nickname usato | Usa nickname diverso |
| Connection refused | Avvia server prima dei client |
| Client non risponde | Ctrl+C e riavvia |

## Testing Rapido

1. Terminale 1: `start-server.bat`
2. Terminale 2: `start-client.bat Mario`
3. Terminale 3: `start-client.bat Luigi`
4. Mario: `Ciao!`
5. Luigi vede il messaggio!

## Caratteristiche Tecniche

- **Multi-threading**: 1 thread per client
- **Thread-safe**: ConcurrentHashMap
- **Pool**: Cached ThreadPoolExecutor
- **Persistence**: BufferedWriter su chat.log
- **Protocollo**: TCP Socket (java.net)

---

Per dettagli: vedi `README.md`
Per testing: vedi `GUIDA_TEST.md`
Per architettura: vedi `DETTAGLI_TECNICI.md`
