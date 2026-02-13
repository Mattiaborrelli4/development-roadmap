# Guida al Testing del Chat Server

## Avvio Rapido

### 1. Avvia il Server

Apri un terminale e avvia il server:

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\chat-server"
start-server.bat
```

Oppure manualmente:

```bash
cd src\server
java server.ChatServer
```

Dovresti vedere:
```
Chat Server avviato sulla porta 9999
In attesa di connessioni...
```

### 2. Avvia il Primo Client

Apri un **nuovo terminale** e avvia il primo client:

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\chat-server"
start-client.bat Mario
```

Oppure manualmente:

```bash
cd src\client
java client.ChatClient Mario
```

### 3. Avvia il Secondo Client

Apri un **terzo terminale** e avvia il secondo client:

```bash
start-client.bat Luigi
```

### 4. Test la Chat

Nel terminale di Mario, scrivi:
```
Ciao a tutti!
```

Dovresti vedere il messaggio in **entrambi** i terminali!

## Comandi da Provare

### Test Room

Nel terminale di Mario:
```
/join gaming
```

Mario ora è nella room "gaming". Luigi non vedrà più i messaggi di Mario.

Nel terminale di Luigi:
```
/join gaming
```

Ora entrambi sono nella room "gaming" e possono vedersi.

### Test Whisper

Nel terminale di Mario:
```
/whisper Luigi Ciao Luigi, come va?
```

Solo Luigi vedrà questo messaggio (apparirà con [PRIVATO]).

### Test List

In qualsiasi client:
```
/list
```

Vedrai: `[INFO] Room disponibili: general, gaming`

### Test Users

In qualsiasi client:
```
/users
```

Vedrai gli utenti nella tua room corrente.

### Test Leave

Nel terminale di Mario:
```
/leave
```

Mario torna alla room "general".

### Test Multi-Room

1. Avvia un terzo client:
```bash
start-client.bat Princess
```

2. Princess entra in "general" (default)
3. Mario è in "general"
4. Luigi è in "gaming"

Messaggi:
- Mario e Princess si vedono (stessa room)
- Luigi non vede nessuno (da solo in "gaming")

## Scenari di Test Completi

### Scenario 1: Tre Room Diverse

```
Terminale 1: Mario
Terminale 2: Luigi
Terminale 3: Princess

1. Mario: /join gaming
2. Luigi: /join music
3. Princess: /join movies

Ogni utente è in una room diversa.
4. Mario: "Qualcuno vuole giocare?"
   → Nessuno vede il messaggio (solo Mario)
5. Luigi: /join gaming
6. Ora Luigi vede Mario!
7. Mario: "Bentornato Luigi!"
   → Luigi vede il messaggio
```

### Scenario 2: Messaggi Privati

```
1. Avvia 4 client: Mario, Luigi, Princess, Toad
2. Tutti in "general"
3. Mario: /whisper Luigi Segreto!
   → Solo Luigi vede [PRIVATO] Mario: Segreto!
4. Princess e Toad non vedono nulla
5. Luigi: /whisper Mario Tutto ok!
   → Solo Mario vede [PRIVATO] Luigi: Tutto ok!
```

### Scenario 3: Naviazione tra Room

```
1. Mario in "general"
2. Mario: /join gaming
   → Mario è in "gaming"
3. Mario: "Chi vuole giocare?"
   → Solo in "gaming" si vede
4. Mario: /join general
   → Mario è tornato in "general"
5. Mario: "Sono tornato!"
   → Solo in "general" si vede
```

### Scenario 4: Test Comandi Error

```
1. /whisper
   → [ERRORE] Uso: /whisper <nick> <messaggio>

2. /join
   → [ERRORE] Uso: /join <room>

3. /comandoSconosciuto
   → [ERRORE] Comando non riconosciuto. Usa /help
```

## Verifica del Log File

Dopo aver inviato alcuni messaggi, verifica che `chat.log` sia stato creato:

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\chat-server\src\server"
type chat.log
```

Dovresti vedere:
```
[2026-02-12 14:30:15] SERVER: Server avviato
[2026-02-12 14:30:20] Mario: [general] Ciao a tutti!
[2026-02-12 14:30:22] Luigi: [general] Ciao Mario!
[2026-02-12 14:30:25] Mario: [WHISPER to Luigi] Ti va di giocare?
```

## Test di Stress (Opzionale)

### Multi-Client Stress Test

Crea un file batch `test-multiple-clients.bat`:

```batch
@echo off
start cmd /k "start-client.bat Client1"
timeout /t 1 /nobreak
start cmd /k "start-client.bat Client2"
timeout /t 1 /nobreak
start cmd /k "start-client.bat Client3"
timeout /t 1 /nobreak
start cmd /k "start-client.bat Client4"
timeout /t 1 /nobreak
start cmd /k "start-client.bat Client5"
```

Eseguilo per avviare 5 client contemporaneamente!

## Risoluzione dei Problemi

### Errore: "Address already in use"

Il server è già in esecuzione. Chiudilo prima di riavviarlo.

Premi `Ctrl+C` nel terminale del server.

### Errore: "Connection refused"

Il server non è in esecuzione. Avvialo prima dei client.

### Errore: "Nickname già in uso"

Scegli un nickname diverso per ogni client.

### Client non risponde

Premi `Ctrl+C` per chiudere il client e riavvialo.

## Riepilogo File

Dopo il test, dovresti avere:

```
chat-server/
├── start-server.bat           # Script avvio server
├── start-client.bat           # Script avvio client
├── GUIDA_TEST.md              # Questa guida
├── README.md                  # Documentazione completa
├── src/
│   ├── server/
│   │   ├── ChatServer.java
│   │   ├── ChatServer.class
│   │   ├── ClientHandler.java
│   │   ├── ClientHandler.class
│   │   └── chat.log          # Generato dopo il test
│   └── client/
│       ├── ChatClient.java
│       └── ChatClient.class
```

## Comandi Riepilogo Rapido

| Comando | Descrizione |
|---------|-------------|
| `start-server.bat` | Avvia il server |
| `start-client.bat Mario` | Avvia client con nickname "Mario" |
| `/join <room>` | Entra in una room |
| `/leave` | Torna a "general" |
| `/whisper <nick> <msg>` | Messaggio privato |
| `/list` | Lista rooms |
| `/users` | Lista utenti nella room |
| `/quit` | Esci |
| `Ctrl+C` | Termina server/client |

Buon testing! 🚀
