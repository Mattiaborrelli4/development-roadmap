# ⚙️ System Programming - OS & Low-Level Development
**Current Skill Level: 10%** ⚠️ **ADVANCED - Da costruire!**

---

## 🟢 **BASICS - Command Line Tools**

### 1. 📁 **File Manager (CLI)**
- **Obiettivo**: File I/O, directory operations
- **Features**:
  - Navigate directories
  - Copy/move/delete files
  - Search by name/pattern
  - Show file info (size, permissions)
  - Batch operations
- **Concetti**: File system, paths, permissions
- **Tempo**: 5-7 giorni
- **Portfolio Value**: MEDIO
- **Languages**: C, Python, Rust

### 2. 📊 **System Monitor**
- **Obiettivo**: Process management, system info
- **Features**:
  - CPU usage % per core
  - Memory usage (RAM/Swap)
  - Process list with PID
  - Kill processes
  - Disk usage by mount
- **Concetti**: Process management, system calls, /proc filesystem
- **Tempo**: 7-10 giorni
- **Portfolio Value**: ALTO

### 3. 📝 **Log File Analyzer**
- **Obiettivo**: Text processing, file parsing
- **Features**:
  - Parse log files (Apache, nginx, custom)
  - Filter by level/time
  - Statistics (errors per hour, top IPs)
  - Export report
  - Real-time tail mode
- **Concetti**: File I/O, regex, parsing
- **Tempo**: 7-10 giorni
- **Portfolio Value**: ALTO

---

## 🟡 **INTERMEDIATE - Systems & Processes**

### 4. ⚡ **Process Manager** ⭐
- **Obiettivo**: Process control, signals
- **Features**:
  - List all processes (tree view)
  - Search by name/PID
  - Kill/Suspend/Resume
  - Set priority (nice values)
  - Resource usage per process
  - Auto-kill rules
- **Concetti**: Fork, exec, signals, priorities
- **Tempo**: 10-14 giorni
- **Portfolio Value**: MOLTO ALTO

### 5. 🔌 **Device Driver (Simple)**
- **Obiettivo**: Kernel module basics
- **Features**:
  - Character device driver
  - Read/write operations
  - IOCTL interface
  - /proc entry
  - Debug logging
- **Concetti**: Kernel modules, device files, ioctl
- **Tempo**: 14-21 giorni
- **Portfolio Value**: MOLTO ALTO
- **Languages**: C (Linux), C++ (Windows)

### 6. 🌐 **Network Daemon**
- **Obiettivo**: Socket programming, daemonization
- **Features**:
  - TCP/UDP server
  - Handle multiple clients
  - Config file
  - Logging
  - Graceful shutdown
- **Concetti**: Sockets, multiprocessing, signals
- **Tempo**: 14-21 giorni
- **Portfolio Value**: ALTO

### 7. 📦 **Package Manager**
- **Obiettivo**: File management, dependencies
- **Features**:
  - Install packages (archives)
  - Track dependencies
  - Remove packages
  - Update system
  - Database tracking
- **Concetti**: Database, file management, dependencies
- **Tempo**: 14-21 giorni
- **Portfolio Value**: MOLTO ALTO

---

## 🔴 **ADVANCED - Kernel & Performance**

### 8. 🖥️ **Custom Shell** ⭐
- **Obiettivo**: Process creation, parsing
- **Features**:
  - Command parsing
  - Execute external programs
  - Pipes (|) redirection
  - Background jobs (&)
  - Built-in commands (cd, pwd, exit)
  - Environment variables
  - Tab completion (bonus)
- **Concetti**: Fork, exec, pipes, signals, environment
- **Tempo**: 21-28 giorni
- **Portfolio Value**: MASSIMO
- **Languages**: C, Rust

### 9. 💾 **File System Implementation**
- **Obiettivo**: FS structure, disk I/O
- **Features**:
  - Create virtual FS in file
  - Directory tree
  - Create/delete/read/write files
  - Metadata (permissions, timestamps)
  - Simple block allocation
- **Concetti**: Inodes, blocks, directory structure
- **Tempo**: 21-28 giorni
- **Portfolio Value**: MASSIMO

### 10. 🔥 **Memory Allocator**
- **Obiettivo**: Memory management
- **Features**:
  - Malloc/free implementation
  - Handle fragmentation
  - Memory pools
  - Debug mode (detect leaks)
  - Performance metrics
- **Concetti**: Heap, fragmentation, algorithms
- **Tempo**: 14-21 giorni
- **Portfolio Value**: MOLTO ALTO

### 11. 📊 **Performance Profiler**
- **Obiettivo**: Performance measurement
- **Features**:
  - CPU sampling profiler
  - Function call trace
  - Memory usage tracking
  - Flame graph visualization
  - Hotspot detection
- **Concetti**: Perf counters, sampling, tracing
- **Tempo**: 21-28 giorni
- **Portfolio Value**: MOLTO ALTO

### 12. 🔄 **Thread Pool**
- **Obiettivo**: Concurrency, synchronization
- **Features**:
  - Worker thread pool
  - Task queue
  - Work stealing
  - Load balancing
  - Shutdown gracefully
- **Concetti**: Threads, mutexes, condition variables
- **Tempo**: 14-21 giorni
- **Portfolio Value**: ALTO

---

## 🏆 **Progetti MUST DO**

1. 🎯 **File Manager** - File system basics
2. 🎯 **Process Manager** - Process control
3. 🎯 **Custom Shell** - MASSIMO value
4. 🎯 **Network Daemon** - Socket programming

---

## ⚡ **SYSTEM PROGRAMMING CRASH COURSE**

### **Settimana 1: File System**
```c
// File operations
FILE *f = fopen("file.txt", "r");
fread(buffer, 1, size, f);
fwrite(buffer, 1, size, f);
fclose(f);

// System calls (Linux)
open(), read(), write(), close()
stat(), lstat(), fstat()
opendir(), readdir()
```

### **Settimana 2: Processes**
```c
// Process creation
pid_t pid = fork();

if (pid == 0) {
    // Child
    execvp(program, args);
} else {
    // Parent
    wait(&status);
}

// Signals
signal(SIGINT, handler);
kill(pid, SIGTERM);
```

### **Settimana 3: IPC (Inter-Process Communication)**
```c
// Pipes
int pipefd[2];
pipe(pipefd);

// Shared memory
shmget(), shmat(), shmdt()

// Message queues
msgget(), msgsnd(), msgrcv()

// Sockets
socket(), bind(), listen(), accept()
```

### **Settimana 4: Threads**
```c
// POSIX threads
pthread_create(&thread, NULL, func, arg);
pthread_join(thread, NULL);

// Synchronization
pthread_mutex_lock(&mutex);
pthread_mutex_unlock(&mutex);
pthread_cond_wait(&cond, &mutex);
```

---

## 📚 **Risorse per Imparare**

### Libri Fondamentali
- **"The Linux Programming Interface"** - Michael Kerrisk
- **"Advanced Programming in the UNIX Environment"** - W. Richard Stevens
- **"Understanding the Linux Kernel"** - Bovet & Cesati
- **"Systems Programming with Rust"** - Jim Blandy

### Corsi Online
- **Linux Foundation: Linux System Programming**
- **Coursera: Operating Systems** (University of++)
- **Udemy: Linux Kernel Programming**
- **YouTube: Low Level Learning**

### Documentazione Ufficiale
- **Linux Kernel Documentation** - kernel.org/doc
- **POSIX Standard** - IEEE Std 1003.1
- **Man Pages** - `man 2 syscall`

### Practice Platforms
- **Exercism C Track** - Mentored practice
- **Codewars C/C++** - Katas
- **LeetCode System Design** - Architecture

---

## 🛠️ **Setup Ambiente**

### **Linux Development**
```bash
# Install tools
sudo apt install build-essential gdb man-db

# Kernel headers (per modules)
sudo apt install linux-headers-$(uname -r)

# Strumenti di debug
sudo apt install valgrind strace ltrace

# Documentazione
sudo apt install manpages-dev glibc-doc
```

### **Debugging Tools**
```bash
# GDB - Debugger
gdb ./program
(gdb) run
(gdb) backtrace
(gdb) print variable

# Valgrind - Memory leaks
valgrind --leak-check=full ./program

# Strace - System call tracing
strace ./program

# ltrace - Library call tracing
ltrace ./program
```

---

## 🌍 **Platform Specific**

### **Linux**
- **System calls**: POSIX standard
- **Kernel modules**: .ko files, insmod/rmmod
- **Proc filesystem**: /proc, /sys
- **Tools**: strace, ltrace, gdb, valgrind

### **Windows**
- **Win32 API**: CreateProcess, VirtualAlloc
- **Drivers**: WDM/WDF model
- **Registry**: Configuration database
- **Tools**: Process Explorer, WinDbg, API Monitor

### **Embedded**
- **Microcontrollers**: Arduino, STM32, ESP32
- **RTOS**: FreeRTOS, Zephyr
- **Tools**: JTAG, OpenOCD, GDB

---

## 🎯 **Roadmap Consigliata**

```
Mese 1: File operations + CLI tools
Mese 2: Processes + signals + fork/exec
Mese 3: IPC (pipes, shared memory, sockets)
Mese 4: Threads + synchronization
Mese 5: Custom shell (major project)
Mese 6: Kernel modules OR file system
```

**Obiettivo**: System Programming 10% → 50% in 6 mesi

---

## 💡 **Tips per System Programming**

### **Best Practices**
1. **Error handling** - Controlla TUTTI i return values
2. **Memory leaks** - Usa valgrind regolarmente
3. **Race conditions** - Attenzione alla concorrenza
4. **Signal safety** - Usa solo async-signal-safe functions in handlers
5. **Resource cleanup** - Chiudi file, libera memoria

### **Debugging Strategy**
```
1. Compila con -Wall -Wextra -g
2. Usa valgrind per memory leaks
3. Usa strace per vedere system calls
4. GDB per execution flow
5. Add logging (syslog, fprintf(stderr))
```

### **Common Pitfalls**
- ❌ Buffer overflows - Usa strncpy, snprintf
- ❌ Memory leaks - Free tutto allochi
- ❌ Deadlocks - Ordine lock consistente
- ❌ Race conditions - Proteggi shared data
- ❌ Signal safety - Evita funzioni non reentrant

---

## 🔥 **Projects by Language**

### **C (Best for Linux Sysdev)**
- Process Manager
- Custom Shell
- Kernel Modules
- Device Drivers

### **C++ (System + App logic)**
- Thread Pool
- Performance Profiler
- Network Daemon

### **Rust (Modern System Programming)**
- File System (safe!)
- Memory Allocator
- CLI Tools

### **Go (Concurrency-focused)**
- Network Services
- Distributed Systems
- Orchestrators
