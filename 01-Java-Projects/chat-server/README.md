# Server di Chat in Tempo Reale - Java

Server di chat multi-client in Java con supporto per chat rooms, messaggi privati e persistenza su file.

## Caratteristiche

- **Multi-client simultanei**: Gestisce più client connessi contemporaneamente usando `ThreadPoolExecutor`
- **Chat rooms pubbliche**: Supporta multiple stanze di discussione (room di default: "general")
- **Messaggi privati (whisper)**: Invia messaggi diretti a utenti specifici
- **Persistenza su file**: Tutti i messaggi vengono salvati in `chat.log`
- **Protocollo testuale semplice**: Facile da implementare e debuggare
- **Thread per client**: Ogni client ha il proprio thread per gestione ottimale

## Architettura

### Componenti Principali

- **ChatServer.java**: Server principale che gestisce tutte le connessioni
  - `ServerSocket` per accettare connessioni TCP
  - `ThreadPoolExecutor` per gestire i client in modo efficiente
  - `ConcurrentHashMap` per rooms e clients (thread-safe)
  - `BufferedWriter` per persistenza su file

- **ClientHandler.java**: Gestisce la connessione con un singolo client
  - Un thread per client
  - Protocollo di comunicazione custom
  - Gestione comandi e messaggi

- **ChatClient.java**: Client console per testing
  - Interfaccia testuale semplice
  - Supporto tutti i comandi del server

## Protocollo di Comunicazione

### Client → Server

```
NICK nickname          - Registrazione del nickname
JOIN room             - Entra in una room
MSG text              - Invia messaggio alla room corrente
WHISPER nick text     - Invia messaggio privato
```

### Server → Client

```
OK                    - Operazione completata
ERROR msg            - Errore con messaggio
MSG from: text       - Messaggio nella room
WHISPER from: text   - Messaggio privato ricevuto
JOINED nick          - Utente entrato nella room
LEFT nick            - Utente uscito dalla room
INFO text            - Informazioni dal server
```

## Compilazione

### Compila il Server

```bash
cd src/server
javac ChatServer.java ClientHandler.java
```

### Compila il Client

```bash
cd src/client
javac ChatClient.java
```

## Esecuzione

### Avvia il Server

```bash
cd src/server
java server.ChatServer [porta]
```

Esempi:
```bash
java server.ChatServer          # Porta di default: 9999
java server.ChatServer 8080     # Porta personalizzata: 8080
```

### Avvia il Client

```bash
cd src/client
java client.ChatClient [nickname] [host] [porta]
```

Esempi:
```bash
java client.ChatClient                        # Nickname auto-generato, localhost:9999
java client.ChatClient Mario                  # Nickname "Mario"
java client.ChatClient Mario localhost 8080   # Host e porta personalizzati
```

## Comandi del Client

Una volta connesso, puoi usare i seguenti comandi:

| Comando | Descrizione | Esempio |
|---------|-------------|---------|
| `/join <room>` | Entra in una room | `/join gaming` |
| `/leave` | Esci dalla room corrente (torna a "general") | `/leave` |
| `/whisper <nick> <msg>` | Invia messaggio privato | `/whisper Mario Ciao!` |
| `/list` | Lista tutte le room disponibili | `/list` |
| `/users` | Lista utenti nella room corrente | `/users` |
| `/quit` | Esci dalla chat | `/quit` |

Inoltre, qualsiasi testo che non inizia con `/` viene inviato come messaggio alla room corrente.

## Esempio di Sessione

### Server
```bash
$ java server.ChatServer
Chat Server avviato sulla porta 9999
In attesa di connessioni...
Nuova connessione da: /127.0.0.1
Client registrato: Mario
Client registrato: Luigi
```

### Client 1 (Mario)
```bash
$ java client.ChatClient Mario
Connessione a localhost:9999 come Mario

=== CLIENT DI CHAT ===
Comandi disponibili:
  /join <room>   - Entra in una room
  /leave         - Esci dalla room corrente
  /whisper <nick> <msg> - Messaggio privato
  /list          - Lista delle room
  /users         - Lista utenti nella room corrente
  /quit          - Esci dalla chat
  Inserisci un messaggio e premi Invio per inviarlo alla room
=====================

[SUCCESS] Benvenuto nella chat! Room corrente: general
[INFO] Mario, Luigi
Ciao a tutti!
Mario: Ciao a tutti!
[JOIN] Luigi è entrato nella room
Luigi: Ciao Mario!
```

### Client 2 (Luigi)
```bash
$ java client.ChatClient Luigi
Connessione a localhost:9999 come Luigi
[SUCCESS] Benvenuto nella chat! Room corrente: general
[INFO] Mario, Luigi
Mario: Ciao a tutti!
Ciao Mario!
```

## Struttura del Log File

Il file `chat.log` contiene tutti i messaggi con timestamp:

```
[2026-02-12 14:30:15] SERVER: Server avviato
[2026-02-12 14:30:20] Mario: [general] Ciao a tutti!
[2026-02-12 14:30:22] Luigi: [general] Ciao Mario!
[2026-02-12 14:30:25] Mario: [WHISPER to Luigi] Ti va di giocare?
[2026-02-12 14:30:28] SERVER: Server arrestato
```

## Struttura del Progetto

```
chat-server/
├── src/
│   ├── server/
│   │   ├── ChatServer.java      # Server principale
│   │   └── ClientHandler.java   # Gestore client
│   └── client/
│       └── ChatClient.java      # Client console
├── chat.log                     # Log dei messaggi (generato automaticamente)
└── README.md                    # Questo file
```

## Tecnologie Utilizzate

- **java.net.ServerSocket**: Per accettare connessioni TCP
- **java.net.Socket**: Per comunicare con i client
- **java.util.concurrent.ThreadPoolExecutor**: Per gestire i thread dei client
- **java.util.concurrent.ConcurrentHashMap**: Per strutture dati thread-safe
- **java.io.BufferedWriter**: Per scrittura efficiente su file
- **java.io.BufferedReader**: Per lettura efficiente da socket
- **java.io.PrintWriter**: Per scrittura su socket

## Requisiti

- Java JDK 8 o superiore
- Nessuna dipendenza esterna (solo Java standard library)

## Possibili Miglioramenti

1. **Autenticazione**: Aggiungere password per proteggere le room
2. **Room private**: Creare room con accesso limitato
3. **Cronologia messaggi**: Inviare gli ultimi N messaggi quando un utente entra in una room
4. **Moderazione**: Comandi per kick/ban utenti
5. **GUI**: Interfaccia grafica invece di console
6. **Emojii support**: Interpretare e visualizzare emoji
7. **File transfer**: Supporto invio file tra utenti
8. **Persistenza rooms**: Salvare/ripristinare le room al riavvio
9. **Admin commands**: Comandi speciali per amministratori
10. **Multi-server**: Supporto per server distribuiti

## Troubleshooting

### Porta già in uso
Se ricevi l'errore "Address already in use", cambia la porta:
```bash
java server.ChatServer 8080
```

### Connection refused
Assicurati che il server sia avviato prima di lanciare i client.

### Nickname già in uso
Scegli un nickname diverso per ogni client.

### Log file permissions
Assicurati di avere permessi di scrittura nella directory del server.

## Note di Sicurezza

⚠️ **ATTENZIONE**: Questo è un progetto educativo. Non usare in produzione senza:

1. Crittografia delle comunicazioni (SSL/TLS)
2. Autenticazione degli utenti
3. Validazione rigorosa degli input
4. Rate limiting per prevenire flooding
5. Sanitizzazione dei messaggi per prevenire injection

## License

Questo progetto è creato a scopo educativo. Sentiti libero di usarlo e modificarlo.

## Autore

Progetto realizzato per portfolio personale.
