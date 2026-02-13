# 🚀 HTTP Server C++ - Server HTTP Multi-threaded

Server HTTP completo implementato in C++17 con supporto multi-threading, socket TCP e serving di file statici.

## ✨ Caratteristiche

- **Socket TCP Programming**: Comunicazione tramite socket TCP/IP
- **Protocollo HTTP/1.1**: Parsing completo delle richieste HTTP
- **Multi-threading**: Thread pool per gestire richieste concorrenti
- **Static File Serving**: Serving di file statici con Content-Type corretto
- **Cross-platform**: Supporto Windows (Winsock2) e Linux (sys/socket.h)

## 📁 Struttura del Progetto

```
http-server-cpp/
├── server.h              # Header del server HTTP
├── server.cpp            # Implementazione del server
├── thread_pool.h         # Header del thread pool
├── thread_pool.cpp       # Implementazione del thread pool
├── main.cpp              # Entry point con gestione signal
├── public/               # Directory file statici
│   ├── index.html        # Homepage di esempio
│   ├── styles.css        # Foglio di stile
│   └── script.js         # JavaScript lato client
├── README.md             # Questo file
└── CMakeLists.txt        # Build configuration (opzionale)
```

## 🛠️ Tecnologie Utilizzate

- **Linguaggio**: C++17
- **Socket**:
  - Windows: `winsock2.h`, `ws2tcpip.h`
  - Linux: `sys/socket.h`, `netinet/in.h`, `arpa/inet.h`
- **Threading**: `std::thread`, `std::mutex`, `std::condition_variable`
- **I/O File**: `std::ifstream` (modalità binary)

## 🚀 Compilazione ed Esecuzione

### Linux / GCC

```bash
# Compilazione
g++ -std=c++17 -pthread -o server server.cpp thread_pool.cpp main.cpp

# Esecuzione
./server
```

### Windows / MSVC

```bash
# Compilazione con cl.exe
cl /EHsc /std:c++17 /Fe:server.exe server.cpp thread_pool.cpp main.cpp ws2_32.lib

# Esecuzione
server.exe
```

### Windows / MinGW

```bash
# Compilazione
g++ -std=c++17 -pthread -o server.exe server.cpp thread_pool.cpp main.cpp -lws2_32

# Esecuzione
server.exe
```

### CMake (Cross-platform)

```bash
mkdir build && cd build
cmake ..
cmake --build .
./server          # Linux
# oppure
server.exe        # Windows
```

## ⚙️ Configurazione

Opzioni command-line:

```bash
# Porta personalizzata
./server --port 3000

# Web root directory personalizzata
./server --root /var/www

# Numero di thread worker
./server --threads 8

# Combinazione di opzioni
./server --port 8080 --root ./public --threads 4

# Help
./server --help
```

**Valori default:**
- Porta: `8080`
- Web Root: `./public`
- Thread Pool: `4 worker threads`

## 📡 Protocollo HTTP

### HTTP Request Format

```
GET /path/to/resource.html HTTP/1.1\r\n
Host: localhost:8080\r\n
User-Agent: Mozilla/5.0\r\n
\r\n
```

### HTTP Response Format

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Content-Length: 1234\r\n
Connection: close\r\n
\r\n
[content bytes]
```

## 🎯 Funzionalità Implementate

### 1. Socket TCP
- Bind su porta configurabile (default 8080)
- Listen con backlog `SOMAXCONN`
- Accept non-blocking con dispatch al thread pool
- Gestione errori socket completa

### 2. HTTP Request Parser
- Parsing della request line: `METHOD PATH VERSION`
- Supporto metodo GET
- URL decoding (%20 per spazi, ecc.)
- Gestione query string
- Path traversal protection (base path = web root)

### 3. Thread Pool
- Queue di task (std::queue)
- N worker threads configurabili
- Condition variable per signaling
- Mutex per sincronizzazione
- Graceful shutdown

### 4. Static File Serving
- Lettura file binaria con `std::ifstream`
- Content-Type corretto per estensione:
  - `.html`, `.htm` → `text/html`
  - `.css` → `text/css`
  - `.js` → `application/javascript`
  - `.json` → `application/json`
  - `.png` → `image/png`
  - `.jpg`, `.jpeg` → `image/jpeg`
  - `.gif` → `image/gif`
  - `.svg` → `image/svg+xml`
  - `.ico` → `image/x-icon`
- Auto index.html per directory

### 5. Status Codes
- `200 OK` - File trovato e servito
- `404 Not Found` - File non esistente
- `500 Server Error` - Errore interno (placeholder)

## 🧪 Test

1. Avviare il server:
```bash
./server
```

2. Aprire browser:
```
http://localhost:8080
```

3. Testare vari path:
```
http://localhost:8080/index.html
http://localhost:8080/styles.css
http://localhost:8080/script.js
http://localhost:8080/nonexistent.html  # 404
```

4. Testare concorrenza:
```bash
# Linux
for i in {1..100}; do curl http://localhost:8080 & done

# Windows (PowerShell)
1..100 | ForEach-Object { Start-ThreadJob { Invoke-WebRequest http://localhost:8080 } }
```

## 📊 Architettura

```
┌─────────────┐
│   main()    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ HTTPServer  │
└──────┬──────┘
       │
       ├──► createSocket() ─────► socket(AF_INET, SOCK_STREAM)
       │
       ├──► bindSocket() ──────► bind(port 8080)
       │
       ├──► listenSocket() ────► listen(SOMAXCONN)
       │
       └──► acceptConnections() ───► accept() loop
                   │
                   ▼
          ┌────────────────┐
          │  Thread Pool   │
          └────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    Thread 1   Thread 2   Thread N
        │          │          │
        └──────────┼──────────┘
                   │
                   ▼
          ┌────────────────┐
          │ handleClient() │
          └────────────────┘
                   │
                   ├──► parseRequest()
                   ├──► readFile()
                   ├──► buildResponse()
                   └──► send()
```

## 🔐 Sicurezza

**Nota**: Questo è un progetto educativo. Per produzione utilizzare:
- Validazione path completa (path traversal protection)
- Limiti dimensione request
- Timeout connessioni
- Rate limiting
- Logging degli accessi
- HTTPS/TLS

## 📝 Code Highlights

### Thread Pool Implementation

```cpp
class ThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queueMutex;
    std::condition_variable condition;

    void enqueue(F&& task) {
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            tasks.push(std::forward<F>(task));
        }
        condition.notify_one();
    }
};
```

### HTTP Response Building

```cpp
std::string buildResponse(int statusCode, const std::string& statusText,
                         const std::string& contentType, const std::string& content) {
    std::ostringstream response;
    response << "HTTP/1.1 " << statusCode << " " << statusText << "\r\n";
    response << "Content-Type: " << contentType << "\r\n";
    response << "Content-Length: " << content.length() << "\r\n";
    response << "Connection: close\r\n";
    response << "\r\n";
    response << content;
    return response.str();
}
```

## 🐛 Troubleshooting

### Windows - WSAStartup Error
Assicurarsi di linkare `ws2_32.lib`

### Linux - Permission Denied
Porte < 1024 richiedono privilegi root:
```bash
sudo ./server --port 80
```

### Address Already in Use
Un'altra istanza è in esecuzione sulla stessa porta:
```bash
# Linux
lsof -i :8080
kill -9 <PID>

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

## 📚 Estensioni Possibili

- [ ] Supporto POST/PUT/DELETE
- [ ] Multi-part file upload
- [ ] WebSocket support
- [ ] CGI/ FastCGI
- [ ] Virtual hosting
- [ ] Logging degli accessi
- [ ] Compressoine gzip
- [ ] Caching headers
- [ ] HTTPS/TLS
- [ ] Authentication

## 👨‍💻 Autore

Progetto realizzato per dimostrare:
- Socket TCP programming
- HTTP protocol implementation
- Multi-threading con std::thread
- Thread pool pattern
- Cross-platform development

## 📄 Licenza

Questo progetto è a scopo educativo. Feel free to use and modify!

---

**Divertiti a sperimentare con il tuo server HTTP C++! 🎉**
