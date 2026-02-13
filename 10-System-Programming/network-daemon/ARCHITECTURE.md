# Network Daemon Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                 │
├─────────────────────────────────────────────────────────────────┤
│  TCP Client 1     │  TCP Client 2     │  UDP Client            │
│  (Port 8888)     │  (Port 8888)     │  (Port 8889)           │
└────────┬──────────┴──────────┬────────┴──────────┬────────────┘
         │                     │                   │
         ▼                     ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ECHO DAEMON                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Main Process (PID)                     │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  • Load Configuration (YAML)                              │  │
│  │  • Setup Logging (file + rotation)                         │  │
│  │  • Daemonize (double-fork + setsid)                       │  │
│  │  • Create PID File                                         │  │
│  │  • Setup Signal Handlers (SIGTERM/SIGINT/SIGHUP)          │  │
│  │  • Spawn TCP Server Process                                │  │
│  │  • Spawn UDP Server Process                                │  │
│  │  • Wait for Shutdown Signal                                │  │
│  │  • Cleanup Resources                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                      │
│         ┌──────────────────┴──────────────────┐                  │
│         │                                      │                  │
│         ▼                                      ▼                  │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  TCP Process     │              │  UDP Process     │        │
│  ├──────────────────┤              ├──────────────────┤        │
│  │ socket()         │              │ socket()         │        │
│  │ bind(8888)       │              │ bind(8889)       │        │
│  │ listen()         │              │                  │        │
│  │ accept() loop    │              │ recvfrom() loop  │        │
│  │   │              │              │                  │        │
│  │   ├─fork()──┐    │              │ recv()           │        │
│  │   │         │    │              │ sendto()         │        │
│  │   ▼         │    │              └──────────────────┘        │
│  │ Client 1    │    │                                       │
│  │ Process    │    │     ┌─────────────────────┐           │
│  │   ┌────────┤    │     │   Client Process     │           │
│  │   │ recv() │    │     │   (per connection)   │           │
│  │   │ send() │    │     ├─────────────────────┤           │
│  │   │ close()│    │     │  recv() loop         │           │
│  │   └────────┤    │     │  sendall()           │           │
│  │            │    │     │  close()             │           │
│  │ Client 2   │    │     └─────────────────────┘           │
│  │ Process    │    │                                       │
│  │   ┌────────┤    │                                       │
│  │   │ recv() │    │                                       │
│  │   │ send() │    │                                       │
│  │   │ close()│    │                                       │
│  │   └────────┤    │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────┐
        │              FILE SYSTEM                   │
        ├───────────────────────────────────────────┤
        │  /var/log/echo-daemon.log          (logs) │
        │  /var/run/echo-daemon.pid          (PID)  │
        │  config/config.yaml               (cfg)  │
        └───────────────────────────────────────────┘
```

## Data Flow

### TCP Connection Flow
```
Client                    Server Daemon
  │                            │
  │  1. SYN                   │
  │──────────────────────────>│
  │                            │
  │  2. SYN-ACK               │
  │<──────────────────────────│
  │                            │
  │  3. ACK                   │
  │──────────────────────────>│
  │  (TCP Connection Established)   │
  │                            │
  │  4. send("Hello")         │
  │──────────────────────────>│
  │                            │  5. accept()
  │                            │  6. fork() → Client Process
  │                            │  7. recv("Hello")
  │                            │
  │  8. sendall("Hello")      │
  │<──────────────────────────│
  │                            │
  │  9. close()               │
  │──────────────────────────>│
  │                            │  10. close()
  │                            │  11. Process exit
```

### UDP Data Flow
```
Client                    Server Daemon
  │                            │
  │  1. sendto("Hi")          │
  │──────────────────────────>│
  │                            │  2. recvfrom("Hi")
  │                            │
  │  3. sendto("Hi")          │
  │<──────────────────────────│
  │                            │
  │  4. Connectionless (no close)│
```

## Signal Handling Flow

```
Signal Sent              Signal Handler           Main Process
    │                          │                        │
    │ SIGTERM/SIGINT          │                        │
    │─────────────────────────>│                        │
    │                          │                        │
    │                          │ shutdown_flag = True   │
    │                          │───────────────────────>│
    │                          │                        │
    │                          │                        │
    │                          │                        │  accept() returns
    │                          │                        │
    │                          │                        │  Check flag
    │                          │                        │
    │                          │                        │  Stop accepting
    │                          │                        │
    │                          │                        │  Terminate clients
    │                          │                        │
    │                          │                        │  Close sockets
    │                          │                        │
    │                          │                        │  Remove PID file
    │                          │                        │
    │                          │                        │  Exit(0)
```

## Daemonization Flow

```
Parent Process            Child 1              Child 2 (Daemon)
    │                        │                      │
    │ fork()                │                      │
    │─────────────────────>  │                      │
    │ exit(0)                │                      │
    │                        │                      │
    │                        │ setsid()             │
    │                        │ (new session)        │
    │                        │                      │
    │                        │ fork()               │
    │                        │─────────────────────> │
    │                        │ exit(0)               │
    │                        │                      │
    │                        │                      │ chdir("/")
    │                        │                      │ umask(0)
    │                        │                      │ redirect std*
    │                        │                      │
    │                        │                      │ ● Daemon Running
```

## Process Lifecycle

```
   Start
     │
     ├─> Load Configuration
     │
     ├─> Setup Logging
     │
     ├─> Daemonize (if enabled)
     │     ├─> Fork 1
     │     ├─> setsid()
     │     └─> Fork 2
     │
     ├─> Create PID File
     │
     ├─> Setup Signal Handlers
     │
     ├─> Fork TCP Server Process
     │     └─> Listen + Accept Loop
     │           └─> Fork Client Processes
     │
     ├─> Fork UDP Server Process
     │     └─> recvfrom/sendto Loop
     │
     ├─> Wait for Signal (pause())
     │     │
     │     ├─> SIGTERM/SIGINT
     │     └─> Shutdown
     │
     ├─> Cleanup
     │     ├─> Stop TCP Server
     │     ├─> Stop UDP Server
     │     └─> Remove PID File
     │
     └─> Exit
```

## Module Dependencies

```
echo_daemon.py (Main)
    │
    ├─> utils/daemon.py
    │     ├─> os (fork, setsid, chdir, umask)
    │     ├─> sys
    │     └─> signal (per check processo)
    │
    ├─> utils/signal.py
    │     ├─> signal (SIGTERM, SIGINT, etc.)
    │     └─> logging
    │
    ├─> utils/log.py
    │     ├─> logging
    │     ├─> logging.handlers (RotatingFileHandler)
    │     └─> os
    │
    ├─> socket (TCP/UDP operations)
    ├─> multiprocessing (Process)
    ├─> yaml (config parsing)
    └─> argparse (CLI)
```

## File I/O Operations

```
Daemon Startup                     Daemon Runtime
     │                                  │
     ├─> READ config.yaml              │
     │                                  │
     ├─> CREATE pid_file                │
     │   (write current PID)            │
     │                                  │
     ├─> CREATE log_file                │
     │                                  │
     ├─> APPEND log_file               ├─> APPEND log_file
     │   (startup messages)             │   (connection logs,
     │                                  │    error logs)
     │                                  │
     │                                  │
Daemon Shutdown                   Daemon Runtime (cont.)
     │                                  │
     ├─> APPEND log_file               └─> ROTATE log_file
     │   (shutdown messages)               (when size > max)
     │                                       ├─> Rename to .1
     │                                       └─> Create new file
     │
     └─> DELETE pid_file
```

## Memory Layout (Per Process)

```
┌─────────────────────────────────────────┐
│            Text (Code)                  │
│  • Read-only executable instructions   │
├─────────────────────────────────────────┤
│            Data                         │
│  • Initialized global/static vars       │
├─────────────────────────────────────────┤
│            BSS                          │
│  • Uninitialized global/static vars    │
├─────────────────────────────────────────┤
│            Heap                         │
│  • Dynamic allocation (malloc/new)      │
│  • Python objects                      │
│  ▲ (grows upward)                       │
├─────────────────────────────────────────┤
│            Stack                        │
│  • Local variables                     │
│  • Function frames                     │
│  ▼ (grows downward)                    │
└─────────────────────────────────────────┘
```

## Socket Buffer Flow

```
Application          Kernel Socket Buffer         Network
    │                        │                        │
    │ sendall(data)         │                        │
    │──────────────────────>│                        │
    │                        │                        │
    │                        │ [TCP: segment]        │
    │                        │──────────────────────>│
    │                        │                        │
    │                        │ [UDP: datagram]       │
    │                        │──────────────────────>│
    │                        │                        │
    │                        │                        │
    │                        │ [TCP: ACK]            │
    │                        │<──────────────────────│
    │                        │                        │
    │                        │                        │
    │ recv(data)            │                        │
    │<──────────────────────│                        │
    │                        │                        │
    │                        │ [UDP: datagram]       │
    │                        │<──────────────────────│
    │                        │                        │
    │ recvfrom(data)        │                        │
    │<──────────────────────│                        │
```

## Configuration Loading

```
config.yaml
    │
    ├─> YAML Parser
    │     ├─> Parse keys
    │     ├─> Parse values
    │     ├─> Type conversion
    │     └─> Validation
    │
    └─> Config Dictionary
          │
          ├─> TCP Config
          │     ├─> port: 8888
          │     ├─> max_clients: 10
          │     └─> buffer_size: 4096
          │
          ├─> UDP Config
          │     ├─> udp_port: 8889
          │     └─> buffer_size: 4096
          │
          ├─> Logging Config
          │     ├─> log_file: path
          │     ├─> log_level: INFO
          │     └─> max_log_size: bytes
          │
          └─> Daemon Config
                ├─> pid_file: path
                └─> daemonize: true/false
```

## Logging Flow

```
Application Code          Logger          Handler          File
    │                        │               │               │
    │ logger.info("msg")     │               │               │
    │──────────────────────>│               │               │
    │                        │               │               │
    │                        │ Format        │               │
    │                        │ timestamp      │               │
    │                        │ level          │               │
    │                        │ PID            │               │
    │                        │               │               │
    │                        │───────────────>│               │
    │                        │ formatted msg │               │
    │                        │               │               │
    │                        │               │ Write          │
    │                        │               │───────────────>│
    │                        │               │               │
    │                        │               │               │
    │                        │               │  [File Size > Max]
    │                        │               │               │
    │                        │               │ Close         │
    │                        │               │ Rename to .1  │
    │                        │               │ Rename .1->.2 │
    │                        │               │ Create new    │
    │                        │               │───────────────>│
```

---

*Architecture documentation for Network Echo Daemon*
*Educational system programming project*
