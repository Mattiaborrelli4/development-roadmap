# Process Manager - Esempi di Utilizzo

Questo documento contiene esempi pratici di utilizzo del Process Manager.

## Indice
- [Esempio 1: Lista Processi Base](#esempio-1-lista-processi-base)
- [Esempio 2: Albero dei Processi](#esempio-2-albero-dei-processi)
- [Esempio 3: Ricerca e Filtro](#esempio-3-ricerca-e-filtro)
- [Esempio 4: Modalità Watch](#esempio-4-modalit%C3%A0-watch)
- [Esempio 5: Dettagli Processo](#esempio-5-dettagli-processo)
- [Esempio 6: Terminazione Processo](#esempio-6-terminazione-processo)

---

## Esempio 1: Lista Processi Base

### Lista semplice (ordinata per CPU)

```bash
$ python main.py list
```

**Output:**
```
💻 Statistiche di sistema:
   CPU: 15.3% (8 cores)
   Memory: 8.2GB / 16.0GB (51%)
   Processi totali: 247

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  chrome                   45.2%    512.3   S         12
 5678  python                   23.1%    128.5   R          4
 9012  node                     12.3%     89.2   S          8
 3456  firefox                   8.7%    423.1   S         16
 7890  code                      5.2%    345.6   S         24
```

### Ordinamento per memoria

```bash
$ python main.py list --sort memory --limit 5
```

**Output:**
```
💻 Statistiche di sistema:
   CPU: 12.1% (8 cores)
   Memory: 8.2GB / 16.0GB (51%)

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  chrome                    2.1%   1024.5   S         12
 3456  firefox                   1.2%    512.3   S         16
 7890  code                      3.4%    345.6   S         24
 2345  electron                 1.1%    234.5   S          8
 6789  teams                     0.8%    189.2   S         10
```

### Filtraggio per nome

```bash
$ python main.py list --filter python
```

**Output:**
```
🔍 Filtrando per nome: 'python'
   Trovati 8 processi

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 5678  python                   23.1%    128.5   R          4
 6789  python3.9                 12.2%     89.3   S          2
 8901  python                    8.1%      45.2   S          1
```

---

## Esempio 2: Albero dei Processi

### Albero completo

```bash
$ python main.py tree
```

**Output:**
```
🌳 Albero completo dei processi

Alberi trovati: 3

--- Albero 1 ---
systemd (1)
├─ sshd (1234)
│  └─ bash (5678)
│     └─ python (8901)
│        ├─ python (9012)
│        └─ python (9013)
├─ NetworkManager (2345)
│  ├─ dhclient (3456)
│  └─ dnsmasq (4567)
└─ gnome-shell (5678)
   ├─ gnome-terminal (6789)
   │  └─ bash (7890)
   │     └─ main.py (8901)
   └─ code (9012)
      ├─ node (9123)
      └─ node (9134)
```

### Sottoalbero specifico

```bash
$ python main.py tree --pid 8901
```

**Output:**
```
🌳 Albero processi (radice: PID 8901)

python (8901) CPU:23.1% MEM:128.5MB
├─ python (9012) CPU:12.3% MEM:45.2MB
└─ python (9013) CPU:8.7% MEM:34.1MB

📊 Statistiche:
   Totale processi: 3
   Profondità massima: 1
   Processi foglia: 2
```

---

## Esempio 3: Ricerca e Filtro

### Ricerca semplice

```bash
$ python main.py search chrome
```

**Output:**
```
🔍 Ricerca: 'chrome'

Trovati 15 processi:

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  chrome                   45.2%    512.3   S         12
 2345  chrome                   23.1%    234.5   S          8
 3456  chrome                   12.3%    189.2   S          6
 4567  chrome                    8.7%    145.6   S          4
 5678  chrome                    5.2%    123.4   S          3
...
```

### Ricerca case-sensitive

```bash
$ python main.py search Python --case-sensitive
```

**Output:**
```
🔍 Ricerca: 'Python'

Trovati 2 processi:

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 5678  Python                   23.1%    128.5   R          4
 8901  Python                    8.1%      45.2   S          1
```

---

## Esempio 4: Modalità Watch

### Watch con refresh ogni 2 secondi

```bash
$ python main.py watch
```

**Output (si aggiorna automaticamente):**
```
🔄 Modalità Watch (refresh ogni 2s, ordinato per cpu)
   Premi Ctrl+C per uscire

⏱️  Iterazione 1 - 14:32:15

💻 Statistiche di sistema:
   CPU: 15.3% (8 cores)
   Memory: 8.2GB / 16.0GB (51%)
   Processi totali: 247

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  chrome                   45.2%    512.3   S         12
 5678  python                   23.1%    128.5   R          4
 9012  node                     12.3%     89.2   S          8

⏱️  Iterazione 2 - 14:32:17

💻 Statistiche di sistema:
   CPU: 18.2% (8 cores)
   Memory: 8.3GB / 16.0GB (52%)
   Processi totali: 248

PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  chrome                   48.7%    513.1   S         12
 5678  python                   26.4%    129.2   R          4
 9012  node                     14.1%     89.5   S          8
```

### Watch con ordinamento per memoria

```bash
$ python main.py watch --sort memory --interval 5
```

---

## Esempio 5: Dettagli Processo

### Visualizza tutti i dettagli

```bash
$ python main.py details 1234
```

**Output:**
```
📋 Dettagli processo 1234

📌 Informazioni Base:
   PID: 1234
   Nome: chrome
   Eseguibile: /opt/google/chrome/chrome
   Directory: /home/user
   Stato: S
   Cmdline: /opt/google/chrome/chrome --new-window

👤 Contesto Utente:
   Username: user
   UID: 1000

💾 Memoria:
   RSS: 512.3 MB
   VMS: 2048.7 MB
   Percent: 3.2%

🧵 Thread:
   Totale: 12

📂 File Aperti (24):
   FD 3: /opt/google/chrome/resources.pak
   FD 4: /opt/google/chrome/locales/it.pak
   FD 5: /home/user/.config/google-chrome/Default/History
   FD 6: /home/user/.config/google-chrome/Default/Preferences
   FD 7: socket:[12345]
   ... e altri 18

🌐 Connessioni (8):
   192.168.1.100:54321 -> 142.250.184.78:443 (ESTABLISHED)
   192.168.1.100:54322 -> 142.250.184.78:443 (ESTABLISHED)
   127.0.0.1:9999 -> 127.0.0.1:12345 (ESTABLISHED)
   ... e altre 5
```

---

## Esempio 6: Terminazione Processo

### Terminazione con SIGTERM (default)

```bash
$ python main.py kill 12345
```

**Output:**
```
⚡ Terminazione processo 12345 (metodo: SIGTERM)

⚠️  Sei sicuro di voler terminare questo processo?
   PID: 12345
   Nome: python
   CPU: 12.3%
   Memoria: 128.5 MB
   Metodo: SIGTERM (15) - Termination request

   Terminare? (s/N): s

   ✅ Processo terminato con successo
```

### Terminazione forzata senza conferma

```bash
$ python main.py kill 12345 --force
```

**Output:**
```
⚡ Terminazione processo 12345 (metodo: SIGTERM)

   ✅ Processo terminato con successo
```

### Terminazione con SIGKILL

```bash
$ python main.py kill 12345 --method sigkill
```

**Output:**
```
⚡ Terminazione processo 12345 (metodo: SIGKILL)

⚠️  Sei sicuro di voler terminare questo processo?
   PID: 12345
   Nome: python
   CPU: 12.3%
   Memoria: 128.5 MB
   Metodo: SIGKILL (9) - Immediate termination

   Terminare? (s/N): s

   ✅ Processo terminato con successo
```

### Accesso negato

```bash
$ python main.py kill 1
```

**Output:**
```
⚡ Terminazione processo 1 (metodo: SIGTERM)

⚠️  Sei sicuro di voler terminare questo processo?
   PID: 1
   Nome: systemd
   CPU: 0.1%
   Memoria: 8.2 MB
   Metodo: SIGTERM (15) - Termination request

   Terminare? (s/N): s

   🔒 Permesso negato (richiede root/sudo)
```

---

## Esempio 7: Statistiche Sistema

```bash
$ python main.py stats
```

**Output:**
```
📊 Statistiche di Sistema

💻 CPU:
   Utilizzo: 15.3%
   Core: 8

💾 Memoria:
   Totale: 16.0 GB
   Usata: 8.2 GB (51%)
   Disponibile: 7.8 GB

💿 Swap:
   Totale: 2.0 GB
   Usato: 0.1 GB (5%)

📋 Processi: 247 totali

🔥 Top 5 CPU:
   chrome                  CPU: 45.2%
   python                  CPU: 23.1%
   node                    CPU: 12.3%
   firefox                 CPU:  8.7%
   code                    CPU:  5.2%

🐘 Top 5 Memoria:
   chrome                  MEM: 1024.5 MB
   firefox                 MEM:  512.3 MB
   code                    MEM:  345.6 MB
   electron                MEM:  234.5 MB
   teams                   MEM:  189.2 MB
```

---

## Esempio 8: Workflow Completo

### Scenario: Trova e analizza un processo

```bash
# 1. Cerca il processo
$ python main.py search myapp

# Output:
🔍 Ricerca: 'myapp'
Trovati 2 processi
PID    Nome                      CPU %    Mem MB  Stato    Thread
------ ------------------------ ------- -------- -------- ------
 1234  myapp                    12.3%    256.7   S          8
 5678  myapp-helper              2.1%     45.2   S          2

# 2. Guarda i dettagli del processo principale
$ python main.py details 1234

# 3. Visualizza l'albero per vedere i figli
$ python main.py tree --pid 1234

# 4. Se necessario, termina il processo
$ python main.py kill 12345

# 5. Verifica che sia terminato
$ python main.py search myapp
```

---

## Tips per l'Uso

### Pipe con altri comandi

```bash
# Salva output in file
$ python main.py list > processi.txt

# Conta processi Python
$ python main.py search python | grep -c "^[0-9]"
```

### Scripting

```bash
# Trova processi che usano più di 500MB
$ for pid in $(python main.py list --sort memory --limit 100 | grep -E "^\s*[0-9]+" | awk '$5 > 500 {print $1}'); do
    echo "Processo $id usa molta memoria"
    python main.py details $pid
done
```

### Combinazioni utili

```bash
# Monitora processi specifici
$ watch -n 1 "python main.py search chrome"

# Trova e uccidi processi zombie
$ python main.py list | grep -i zombie
```

---

## Risoluzione Problemi

### Errori comuni

**Errore: Access Denied**
```
🔒 Permesso negato (richiede root/sudo)
```
Soluzione: Il processo appartiene a un altro utente o richiede privilegi elevati.

**Errore: Process Not Found**
```
❓ Processo non trovato
```
Soluzione: Il processo è terminato tra quando l'hai cercato e quando hai provato a terminarlo.

**Errore: Module Not Found**
```
ModuleNotFoundError: No module named 'psutil'
```
Soluzione: `pip install -r requirements.txt`

---

Per più esempi e documentazione, vedi il [README.md](README.md).
