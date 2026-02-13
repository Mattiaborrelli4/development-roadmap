# Network Echo Daemon

Un daemon di rete educativo per apprendere la programmazione di sistema in Python. Questo progetto implementa server TCP/UDP echo con gestione multi-client, signal handling, e daemonizzazione completa.

## 🎯 Scopo Educativo

Questo progetto insegna concetti fondamentali di system programming:

- **Socket Programming**: API socket, TCP vs UDP, client-server architecture
- **Process Management**: fork(), multiprocessing, concorrenza
- **Signal Handling**: SIGTERM, SIGINT, SIGHUP, graceful shutdown
- **Daemonization**: doppio fork, setsid(), PID file management
- **Unix/Linux System Calls**: bind(), listen(), accept(), recv(), send()
- **Logging**: Rotazione log, file I/O, thread-safety
- **Configuration**: YAML parsing, runtime configuration

## 📋 Requisiti

- Python 3.10+
- Linux/Unix OS (o WSL su Windows)
- Librerie:
  - `pyyaml` - Per parsing configurazione
  - Moduli standard: `socket`, `signal`, `multiprocessing`, `logging`

### Installazione Dipendenze

```bash
pip install pyyaml
```

## 🚀 Installazione

1. Clona o naviga nella directory del progetto:
```bash
cd network-daemon/
```

2. Verifica la struttura:
```bash
ls -la
# echo_daemon.py
# config/
# utils/
# tests/
```

## 📁 Struttura Progetto

```
network-daemon/
├── echo_daemon.py          # Main daemon executable
├── config/
│   └── config.yaml         # Configuration file
├── utils/
│   ├── daemon.py           # Daemonization utilities
│   ├── signal.py           # Signal handling
│   └── log.py              # Logging setup
├── tests/
│   ├── client.py           # Test client
│   └── test.sh             # Test automation script
└── README.md               # This file
```

## ⚙️ Configurazione

Il file `config/config.yaml` contiene tutti i parametri:

```yaml
# Porte TCP/UDP
port: 8888              # Porta TCP
udp_port: 8889          # Porta UDP

# Limiti client
max_clients: 10         # Max connessioni concorrenti

# Path file
log_file: /var/log/echo-daemon.log
pid_file: /var/run/echo-daemon.pid

# Logging
log_level: INFO         # DEBUG, INFO, WARNING, ERROR, CRITICAL
max_log_size: 10485760  # 10 MB
log_backup_count: 5

# Performance
buffer_size: 4096       # 4 KB buffer
client_timeout: 300     # 5 minuti

# Network
bind_host: "0.0.0.0"    # Tutte le interfacce

# Modalità
daemonize: true         # true = daemon, false = foreground
```

## 🏃 Utilizzo

### Avvio del Daemon

```bash
# Avvio come background daemon
python echo_daemon.py start

# Avvio in foreground (utile per debug)
# Modifica config.yaml: daemonize: false
python echo_daemon.py start
```

### Controllo del Daemon

```bash
# Verifica stato
python echo_daemon.py status
# Output: Status: RUNNING (PID 12345)

# Ferma daemon
python echo_daemon.py stop
# Output: Invio SIGTERM al daemon (PID 12345)
```

### Test con Client

```bash
# Test TCP echo
python tests/client.py --protocol tcp --message "Hello!"

# Test UDP echo
python tests/client.py --protocol udp --message "Hello!"

# Test multiple messaggi
python tests/client.py --protocol tcp --count 10

# Test payload grande
python tests/client.py --protocol tcp --large

# Test continuo (10 secondi)
python tests/client.py --protocol tcp --continuous 10

# Esegui tutti i test
python tests/client.py --all
```

### Test Automatizzati

```bash
# Su Linux/Unix
chmod +x tests/test.sh
./tests/test.sh

# Oppure con bash
bash tests/test.sh
```

## 🔍 Concetti Tecnici

### Socket Programming

**TCP (Transmission Control Protocol)**:
- Connection-oriented con handshake (SYN, SYN-ACK, ACK)
- Reliable, ordered delivery
- Flow control e congestion control
- Stream-based (nessun boundary messaggi)

```python
# Server TCP
sock = socket.socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(backlog)
client, addr = sock.accept()
data = client.recv(4096)
client.sendall(data)
```

**UDP (User Datagram Protocol)**:
- Connectionless (nessun handshake)
- Unreliable, unordered delivery
- Message-based (preserva boundaries)
- Bassa latenza

```python
# Server UDP
sock = socket.socket(AF_INET, SOCK_DGRAM)
sock.bind((host, port))
data, addr = sock.recvfrom(4096)
sock.sendto(data, addr)
```

### Daemonization

Il processo di daemonizzazione segue lo standard UNIX:

1. **Primo fork**: Parent exit, child continua
   - Disassocia dal parent process
   - Init (PID 1) adotta il child

2. **setsid()**: Crea nuova sessione
   - Diventa session leader
   - Perde controlling terminal

3. **Secondo fork**: Parent exit
   - Previene riacquisizione TTY
   - Child non può mai aprire terminal

4. **chdir("/")**: Cambia directory radice
   - Non blocca filesystem unmount

5. **umask(0)**: Reset permessi file
   - Permetti creazione file controllata

6. **Redirect stdin/stdout/stderr**: Chiudi/redirect
   - Isola dal parent environment

### Signal Handling

Segnali gestiti dal daemon:

- **SIGTERM (15)**: Shutdown ordinato
  - Inviato da: `systemctl stop`, `kill`
  - Cleanup risorse prima di exit

- **SIGINT (2)**: Interrupt da keyboard
  - Inviato da: Ctrl+C
  - Stesso comportamento di SIGTERM

- **SIGHUP (1)**: Hangup detected
  - Inviato da: shell logout, logrotate
  - Usato per reload configurazione

- **SIGPIPE (13)**: Broken pipe
  - Ignorato per prevenire crash
  - Write su socket chiuso ritorna EPIPE

**Signal-Safe Pattern**:
```python
# Handler MINIMALISTA (solo flag)
def handler(signum, frame):
    shutdown_requested = True  # Solo flag atomico

# Main loop polla flag
while not shutdown_requested:
    # ... codice main ...
```

### Multiprocessing

Ogni client TCP viene gestito in un processo separato:

```python
def handle_client(client_socket):
    while True:
        data = client_socket.recv(4096)
        if not data: break
        client_socket.sendall(data)  # Echo

# Fork processo
process = Process(target=handle_client, args=(client_socket,))
process.start()
```

**Vantaggi**:
- True parallelism (multi-core)
- Isolation (crash client non crasha server)
- Simple shared state

### PID File Management

Il PID file traccia il daemon in esecuzione:

```python
# Crea file con lock
pid_file = "/var/run/echo-daemon.pid"
fd = os.open(pid_file, O_WRONLY | O_CREAT | O_EXCL, 0644)
os.write(fd, str(os.getpid()))

# Verifica se running
old_pid = read(pid_file)
os.kill(old_pid, 0)  # Check esistenza

# Cleanup all'uscita
os.remove(pid_file)
```

## 📊 Logging

Il daemon logga su file con rotation:

```
/var/log/echo-daemon.log     # Log corrente
/var/log/echo-daemon.log.1   # Backup 1 (più recente)
/var/log/echo-daemon.log.2   # Backup 2
...
```

**Formato log**:
```
2025-02-12 10:30:45 | INFO     | PID:12345 | Server TCP avviato su 0.0.0.0:8888
2025-02-12 10:30:50 | INFO     | PID:12345 | Client 192.168.1.100:54321 - connected
2025-02-12 10:30:55 | INFO     | PID:12345 | Client 192.168.1.100:54321 - disconnected
```

**Rotation**: Quando il log raggiunge `max_log_size`, viene rinominato con `.1` e un nuovo file vuoto è creato. I backup più vecchi vengono rinominati `.2`, `.3`, ecc.

## 🛠️ Troubleshooting

### "Address already in use"

Il server è già in esecuzione o la porta è in uso:

```bash
# Verifica cosa usa la porta
sudo lsof -i :8888

# Oppure
sudo netstat -tulpn | grep 8888

# Ferma il daemon
python echo_daemon.py stop

# Se processo zombie, kill manualmente
sudo kill -9 <PID>
```

### "Permission denied" su /var/log o /var/run

I path standard richiedono privilegi root:

```bash
# Esegui come root
sudo python echo_daemon.py start

# Oppure modifica config.yaml per path user-space:
log_file: ./logs/echo-daemon.log
pid_file: ./echo-daemon.pid
```

### Daemon non parte

Controlla i log:

```bash
# Se daemonize: true, logga solo su file
tail -f /var/log/echo-daemon.log

# Se daemonize: false, logga anche su console
python echo_daemon.py start
```

### Client non riesce a connettersi

Verifica firewall:

```bash
# Su Linux (ufw)
sudo ufw allow 8888/tcp
sudo ufw allow 8889/udp

# Su Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 8888 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 8889 -j ACCEPT
```

Verifica server in ascolto:

```bash
# TCP
netstat -tlnp | grep 8888

# UDP
netstat -ulnp | grep 8889
```

## 📚 Spiegazione Sistema Operativo

### Perché il doppio fork?

Il **doppio fork** è necessario perché:

1. **Primo fork + setsid()**: Crea nuova sessione, perde il controlling terminal
2. **Secondo fork**: Garantisce che il processo non sia mai session leader
   - Solo session leader può riacquisire un controlling terminal
   - Diventando non-leader, il daemon è immune a TTY acquisition

### Perché redirect stdin/stdout/stderr?

In un daemon non esiste un terminal:
- `stdin` rediretto a `/dev/null` - nessuna input
- `stdout` rediretto a `/dev/null` - output ignorato (o log)
- `stderr` rediretto a `/dev/null` - errori loggati

Questo previene:
- Crash su write a chiuso terminal
- Interferenza con parent process
- Resource leak

### Differenza TCP vs UDP

| Caratteristica | TCP | UDP |
|---------------|-----|-----|
| Orientato alla connessione | Sì | No |
| Affidabile | Sì | No |
| Ordinato | Sì | No |
| Controllo flusso | Sì | No |
| Overhead | Alto | Basso |
| Use case | File transfer, HTTP | DNS, streaming, gaming |

### Perché multiprocessing invece di threading?

Vantaggi multiprocessing in Python:
- **GIL bypass**: True parallelism su multi-core
- **Isolation**: Crash in un processo non affli gli altri
- **Memory isolation**: Ogni processo ha spazio indirizzi separato

Svantaggi threading in Python:
- **GIL (Global Interpreter Lock)**: Solo un thread esegue bytecode Python alla volta
- **Non-parallel per CPU-bound**: Thread non aiuta per CPU work
- **Race conditions**: Condividere stato tra thread è complesso

## 🔒 Sicurezza

Considerazioni di sicurezza per deployment produzione:

1. **Drop privileges**: Avvia come root, poi cambia utente non-root
   ```python
   # Dopo bind() su porta privilegiata (<1024)
   os.setgroups([])
   os.setgid(gid)
   os.setuid(uid)
   ```

2. **Chroot jail**: Isola processo in subset filesystem
   ```python
   os.chroot('/var/empty/echo-daemon')
   os.chdir('/')
   ```

3. **Resource limits**: Previ denial-of-service
   ```python
   import resource
   resource.setrlimit(resource.RLIMIT_NOFILE, (1024, 2048))
   resource.setrlimit(resource.RLIMIT_NPROC, (50, 100))
   ```

4. **Input validation**: Sanitizza tutti i dati da client

5. **Rate limiting**: Limita connessioni per IP

## 📖 Risorse

### Documentazione Python
- [socket](https://docs.python.org/3/library/socket.html) - Low-level networking
- [signal](https://docs.python.org/3/library/signal.html) - Signal handlers
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) - Process-based parallelism
- [logging](https://docs.python.org/3/library/logging.html) - Event logging

### Libri
- *"Unix Network Programming"* by W. Richard Stevens
- *"Advanced Programming in the UNIX Environment"* by W. Richard Stevens
- *"Linux System Programming"* by Robert Love

### Online
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
- [The Linux Programming Interface](http://man7.org/tlpi/)
- [Linux syscalls](https://man7.org/linux/man-pages/man2/syscalls.2.html)

## 🤝 Contributi

Questo è un progetto educativo. Suggerimenti e miglioramenti sono benvenuti!

## 📄 Licenza

Educational use. Libero utilizzo per apprendimento.
