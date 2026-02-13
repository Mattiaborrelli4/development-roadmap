# 📋 Guida Rapida al Testing

## Compilazione

### Windows
```bash
# Opzione 1: Usa lo script batch
build.bat

# Opzione 2: Compila manualmente con GCC
gcc -Wall -Wextra -O2 server.c -o server.exe -lws2_32

# Opzione 3: Usa Make (se disponibile)
make
```

### Linux
```bash
# Rendi eseguibile lo script
chmod +x build.sh

# Compila
./build.sh

# Oppure usa il Makefile
make
```

## Avvio del Server

### Avvio Base
```bash
# Windows
server.exe

# Linux
./server
```

Il server si avvierà su `http://localhost:8080`

### Avvio con Porta Personalizzata
```bash
# Porta 3000
server.exe 3000   # Windows
./server 3000     # Linux
```

## Testing con Browser

1. **Homepage**
   ```
   http://localhost:8080/
   ```

2. **Pagina di Test**
   ```
   http://localhost:8080/test.html
   ```

3. **Seconda Pagina**
   ```
   http://localhost:8080/page2.html
   ```

4. **Test 404**
   ```
   http://localhost:8080/nonexistent.html
   ```

## Testing con cURL

### Test Base
```bash
curl http://localhost:8080/
```

### Test Verboso (mostra headers)
```bash
curl -v http://localhost:8080/
```

### Test Solo Headers
```bash
curl -I http://localhost:8080/
```

### Test Content-Type CSS
```bash
curl -I http://localhost:8080/style.css
```

### Test Content-Type JavaScript
```bash
curl -I http://localhost:8080/script.js
```

### Test con User-Agent
```bash
curl -A "Mozilla/5.0" http://localhost:8080/
```

## Testing Multi-Client

### Test Manuale
1. Apri più tab del browser contemporaneamente
2. Naviga su diverse pagine
3. Verifica che tutte le richieste vengano servite

### Test con Apache Bench
```bash
# Installa Apache Bench se non presente
# Ubuntu/Debian: sudo apt-get install apache2-utils

# Test con 100 richieste, 10 concorrenti
ab -n 100 -c 10 http://localhost:8080/

# Test con 1000 richieste, 50 concorrenti
ab -n 1000 -c 50 http://localhost:8080/
```

## Testing con Telnet

```bash
telnet localhost 8080

# Poi digita (premi Invio dopo ogni riga):
GET / HTTP/1.1
Host: localhost

[Premi Invio un'altra volta]
```

## Output del Server

Quando avvii il server, dovresti vedere:
```
========================================
  Server HTTP in C
========================================
Porta: 8080
Directory: ./public
Server URL: http://localhost:8080
========================================
Premi Ctrl+C per terminare
```

Quando un client si connette:
```
Nuova connessione da 127.0.0.1:54321
Richiesta ricevuta:
GET / HTTP/1.1
Host: localhost:8080
...
Connessione chiusa
```

## Verifica Funzionalità

### ✅ Socket Programming
- Server si avvia correttamente
- Bind sulla porta specificata
- Accettazione connessioni multiple

### ✅ HTTP/1.1
- Parser request line corretto
- Response headers formattati correttamente
- Status codes appropriati (200, 404, 405)

### ✅ File Statici
- HTML servito come text/html
- CSS servito come text/css
- JavaScript servito come application/javascript
- Immagini servite con tipo corretto

### ✅ Multi-Threading
- Più client simultanei supportati
- Nessun blocco durante caricamenti

### ✅ Content-Type
- `.html` → `text/html` ✅
- `.css` → `text/css` ✅
- `.js` → `application/javascript` ✅
- Altri tipi riconosciuti ✅

### ✅ Error Handling
- 404 per file non esistenti ✅
- 405 per metodi non GET ✅
- 500 per errori server ✅

## Troubleshooting

### Porta Già in Uso
```
Errore nel bind. La porta 8080 potrebbe essere in uso.
```
**Soluzione**: Usa una porta diversa
```bash
server.exe 3000
```

### File Non Trovati
Il server restituisce 404 per file inesistenti.

### Compilation Error
Assicurati di avere GCC installato e nel PATH.

## Note
- Il server logga tutte le richieste ricevute
- Ogni connessione usa un thread separato
- Le connessioni vengono chiuse dopo ogni richiesta
- Il server serve solo richieste GET (POST non implementato)
