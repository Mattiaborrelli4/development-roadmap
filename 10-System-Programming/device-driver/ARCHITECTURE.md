# Architettura del Driver MyDev

> Documentazione tecnica dettagliata del funzionamento interno del driver

## 📊 Panoramica Architetturale

```
┌─────────────────────────────────────────────────────────────┐
│                     Userspace                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  test.c  │───▶│ /dev/... │◀───│  cat     │              │
│  │ Program  │    │ Device   │    │ /proc/   │              │
│  └──────────┘    └────┬─────┘    └──────────┘              │
│                        │                                        │
└────────────────────────│───────────────────────────────────────┘
                         │ System Call Interface
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Kernel Space                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              VFS (Virtual File System)              │   │
│  │  - File operations dispatch                         │   │
│  │  - Buffer management                               │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       │                                       │
│                       ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            MyDev Character Device Driver            │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  File Operations (mydev_fops)              │    │   │
│  │  │  - open:    mydev_open()                  │    │   │
│  │  │  - release: mydev_release()               │    │   │
│  │  │  - read:    mydev_read()                  │    │   │
│  │  │  - write:   mydev_write()                 │    │   │
│  │  │  - ioctl:   mydev_ioctl()                 │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  Device Data (mydev)                      │    │   │
│  │  │  - dev:        Device number               │    │   │
│  │  │  - cdev:       Character device structure  │    │   │
│  │  │  - class:      Device class               │    │   │
│  │  │  - buffer[1024]: Data buffer               │    │   │
│  │  │  - mutex:      Synchronization lock       │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                       │                                       │
│                       ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             Kernel Subsystems                       │   │
│  │  - Device Model (/sys)                             │   │
│  │  - Proc Filesystem (/proc)                         │   │
│  │  - Memory Management                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Componenti Principali

### 1. Struttura del Dispositivo

```c
struct mydev_device {
    dev_t dev;                    // Major e minor number
    struct cdev cdev;            // Character device structure
    struct class *class;         // Device class (per /sys)
    struct device *device;       // Device structure
    char buffer[BUF_LEN];        // Buffer dati (1024 bytes)
    size_t data_size;            // Byte presenti nel buffer
    size_t read_pos;             // Posizione lettura corrente
    struct mutex lock;           // Mutex per sincronizzazione
    unsigned long open_count;    // Contatore aperture
    unsigned long read_count;    // Contatore letture
    unsigned long write_count;   // Contatore scritture
};
```

**Flusso Dati:**
```
Write Path:
User Space ──copy_from_user──▶ Kernel Buffer ──data_size++
                                      │
                                      ▼
Read Path:
User Space ◀─copy_to_user─── Kernel Buffer ──read_pos++
```

### 2. Inizializzazione del Modulo

```c
module_init(mydev_init)
    │
    ├─▶ mutex_init(&mydev.lock)
    │      └─ Inizializza mutex per sincronizzazione
    │
    ├─▶ alloc_chrdev_region(&mydev.dev, 0, 1, "mydev")
    │      ├─ Alloca major number dinamico
    │      ├─ Registra con kernel (0 = first available minor)
    │      └─ Restituisce dev_t (major << 20 | minor)
    │
    ├─▶ cdev_init(&mydev.cdev, &mydev_fops)
    │      └─ Collega operazioni file al dispositivo
    │
    ├─▶ cdev_add(&mydev.cdev, mydev.dev, 1)
    │      └─ Aggiunge cdev al kernel (device visibile)
    │
    ├─▶ class_create("mydev_class")
    │      └─ Crea classe in /sys/class/
    │
    ├─▶ device_create(mydev.class, NULL, mydev.dev, NULL, "mydev")
    │      ├─ Crea dispositivo in /dev/
    │      ├─ Crea entry in /sys/class/mydev_class/
    │      └─ Crea uevent per udev
    │
    └─▶ proc_create("mydev_stats", 0666, NULL, &proc_fops)
           └─ Crea interfaccia /proc
```

### 3. File Operations

#### 3.1 Open (`mydev_open`)
```c
int mydev_open(struct inode *inode, struct file *filp)
{
    // 1. Estrai device da inode
    struct mydev_device *dev = container_of(inode->i_cdev,
                                            struct mydev_device, cdev);

    // 2. Salva in private_data per altre operazioni
    filp->private_data = dev;

    // 3. Aggiorna statistiche (thread-safe)
    mutex_lock(&dev->lock);
    dev->open_count++;
    mutex_unlock(&dev->lock);

    return 0;
}
```

**Perché `private_data`?**
- Permette a read/write/ioctl di accedere ai dati del dispositivo
- Il kernel non passa il device direttamente alle altre operazioni
- Standard pattern in tutti i driver Linux

#### 3.2 Read (`mydev_read`)
```c
ssize_t mydev_read(struct file *filp, char __user *buf,
                  size_t count, loff_t *ppos)
{
    struct mydev_device *dev = filp->private_data;

    mutex_lock(&dev->lock);

    // 1. Verifica dati disponibili
    if (dev->data_size == 0) {
        mutex_unlock(&dev->lock);
        return 0;  // EOF
    }

    // 2. Calcola byte da leggere
    bytes_to_read = dev->data_size - dev->read_pos;
    if (bytes_to_read > count)
        bytes_to_read = count;  // Limita a richiesta user

    // 3. Copia allo user space
    if (copy_to_user(buf, dev->buffer + dev->read_pos, bytes_to_read)) {
        mutex_unlock(&dev->lock);
        return -EFAULT;
    }

    // 4. Aggiorna stato
    dev->read_pos += bytes_to_read;
    dev->read_count++;

    mutex_unlock(&dev->lock);
    return bytes_to_read;
}
```

**Flow Diagram:**
```
User:  read(fd, buf, 100)
         │
         ▼
Kernel: VFS → mydev_read()
              │
              ├─ mutex_lock()        [Previene race conditions]
              │
              ├─ check data_size     [EOF se 0]
              │
              ├─ copy_to_user()      [Copia buffer → user space]
              │     └─ Verifica indirizzi user
              │     └─ Gestiona page faults
              │
              ├─ update read_pos     [Avanza puntatore]
              │
              ├─ dev->read_count++   [Statistiche]
              │
              ├─ mutex_unlock()
              │
              └─ return bytes_read
```

#### 3.3 Write (`mydev_write`)
```c
ssize_t mydev_write(struct file *filp, const char __user *buf,
                   size_t count, loff_t *ppos)
{
    struct mydev_device *dev = filp->private_data;

    mutex_lock(&dev->lock);

    // 1. Reset buffer per nuova scrittura
    dev->data_size = 0;
    dev->read_pos = 0;

    // 2. Limita dimensione
    bytes_to_write = count;
    if (bytes_to_write > BUF_LEN)
        bytes_to_write = BUF_LEN;

    // 3. Copia da user space
    if (copy_from_user(dev->buffer, buf, bytes_to_write)) {
        mutex_unlock(&dev->lock);
        return -EFAULT;
    }

    // 4. Aggiorna stato
    dev->data_size = bytes_to_write;
    dev->write_count++;

    mutex_unlock(&dev->lock);
    return bytes_to_write;
}
```

**Policy Buffer:**
```
Write Operation:
┌──────────────────────────────┐
│ Buffer (1024 bytes)          │
├──────────────────────────────┤
│ [Nuovi dati sovrascrivono]   │
└──────────────────────────────┘
     ↑              ↑
     data_size     read_pos

Cosa succede:
1. Reset completo (data_size=0, read_pos=0)
2. Scrivi nuovi dati
3. Tronca se > 1024 bytes
```

#### 3.4 IOCTL (`mydev_ioctl`)
```c
long mydev_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    struct mydev_device *dev = filp->private_data;

    mutex_lock(&dev->lock);

    switch (cmd) {
    case MYDEV_IOCTL_RESET:
        // Resetta posizione lettura
        dev->read_pos = 0;
        break;

    case MYDEV_IOCTL_GET_SIZE:
        // Restituisce dimensione dati
        size = dev->data_size;
        copy_to_user((int __user *)arg, &size, sizeof(int));
        break;

    case MYDEV_IOCTL_CLEAR:
        // Pulisce buffer
        dev->data_size = 0;
        dev->read_pos = 0;
        memset(dev->buffer, 0, BUF_LEN);
        break;
    }

    mutex_unlock(&dev->lock);
    return 0;
}
```

**IOCTL Number Encoding:**
```c
// Magic number (identifica driver)
#define MYDEV_IOCTL_MAGIC 'M'

// Comandi
#define MYDEV_IOCTL_RESET _IO(MYDEV_IOCTL_MAGIC, 1)
//                              │         │
//                           magic    command number

#define MYDEV_IOCTL_GET_SIZE _IOR(MYDEV_IOCTL_MAGIC, 2, int)
//                               │          │     │
//                            magic  command  data type (Read)

#define MYDEV_IOCTL_CLEAR _IO(MYDEV_IOCTL_MAGIC, 3)
```

### 4. Interfaccia /proc

#### 4.1 Proc Entry Creation
```c
proc_entry = proc_create("mydev_stats", 0666, NULL, &proc_fops);
//                                  │        │    │       │
//                               name  permissions  parent  operations
```

#### 4.2 Seq_file Operations
```c
static int proc_show(struct seq_file *m, void *v)
{
    seq_printf(m, "=== MyDev Statistics ===\n");
    seq_printf(m, "Open count: %lu\n", dev->open_count);
    seq_printf(m, "Read count: %lu\n", dev->read_count);
    // ...
    return 0;
}
```

**Proc Filesystem:**
```
User: cat /proc/mydev_stats
         │
         ▼
VFS: [rileva file in /proc]
         │
         ▼
Proc: [chiama proc_open]
         │
         ▼
Seq_file: [chiama proc_show]
              │
              ├─ seq_printf() → formatted output
              └─ return 0
```

## 🔄 Sincronizzazione

### Mutex Usage

**Perché il Mutex?**
```c
// Scenario senza mutex:
Thread 1: write("Hello")   ─┐
Thread 2: write("World")   ─┼─▶ Race condition!
Thread 3: read()           ─┘

// Con mutex:
mutex_lock()   // Solo un thread alla volta
// ... operazioni critiche ...
mutex_unlock() // Rilascia per altri thread
```

**Protected Sections:**
```c
// 1. Open/Close
mutex_lock(&dev->lock);
dev->open_count++;  // Race condition qui senza mutex
mutex_unlock(&dev->lock);

// 2. Read
mutex_lock(&dev->lock);
bytes = dev->data_size - dev->read_pos;  // Coerenza dati
copy_to_user(...);
dev->read_pos += bytes;  // Aggiornamento atomico
mutex_unlock(&dev->lock);

// 3. Write
mutex_lock(&dev->lock);
dev->data_size = 0;  // Reset atomico
copy_from_user(...);
dev->data_size = bytes_written;
mutex_unlock(&dev->lock);
```

## 📝 Kernel Logging

### Livelli di Log
```c
pr_info("Device opened\n");     // INFO level
pr_warn("Unknown IOCTL\n");      // WARNING
pr_err("copy_to_user failed\n"); // ERROR
```

### Visualizzazione Log
```bash
# Tutti i messaggi kernel
dmesg

# Filtra per nostro driver
dmesg | grep mydev

# Monitor in tempo reale
dmesg -w

# Log specifici
tail -f /var/log/kern.log
```

## 🔐 User-Kernel Boundary

### Sicurezza: copy_to_user/copy_from_user

```c
// ⚠️ SBAGLIATO - Unsafe!
char kernel_buf[100];
memcpy(kernel_buf, user_ptr, size);  // Crash se user_ptr invalido!

// ✅ CORRETTO - Safe!
if (copy_from_user(kernel_buf, user_ptr, size)) {
    return -EFAULT;  // Gestione errore sicura
}
```

**Cosa fa copy_from_user:**
1. Verifica che user_ptr sia in user space (non kernel space)
2. Gestiona page faults se indirizzo invalido
3. Restituisce errore invece di crashare
4. Copia solo dati validi

## 🎯 Flusso Completo: Write + Read

```
USERSPACE                    KERNEL SPACE
─────────────────────────────────────────────────────────

Program:
  fd = open("/dev/mydev", O_RDWR)
         │
         │ syscall(SYS_open, "/dev/mydev", ...)
         ▼
     VFS: resolve_path("/dev/mydev")
         │
         │ lookup in device tree
         ▼
    Driver: mydev_open(inode, file)
              ├─ container_of() → device
              ├─ filp->private_data = dev
              ├─ mutex_lock()
              ├─ dev->open_count++
              └─ mutex_unlock()
         │
         └─ return fd to user

  write(fd, "Hello", 5)
         │
         │ syscall(SYS_write, fd, "Hello", 5)
         ▼
     VFS: fd → struct file → file_operations
         │
         ▼
    Driver: mydev_write(file, "Hello", 5, offset)
              ├─ filp->private_data → dev
              ├─ mutex_lock()
              ├─ dev->data_size = 0
              ├─ dev->read_pos = 0
              ├─ copy_from_user(dev->buffer, "Hello", 5)
              │    └─ "Hello" → kernel buffer
              ├─ dev->data_size = 5
              ├─ dev->write_count++
              └─ mutex_unlock()
         │
         └─ return 5 to user

  ioctl(fd, MYDEV_IOCTL_RESET, 0)
         │
         │ syscall(SYS_ioctl, ...)
         ▼
    Driver: mydev_ioctl(file, RESET, 0)
              ├─ mutex_lock()
              ├─ dev->read_pos = 0  // Reset!
              └─ mutex_unlock()

  read(fd, buf, 100)
         │
         │ syscall(SYS_read, ...)
         ▼
    Driver: mydev_read(file, buf, 100, offset)
              ├─ mutex_lock()
              ├─ bytes = 5 - 0 = 5
              ├─ copy_to_user(buf, dev->buffer, 5)
              │    └─ "Hello" → user buffer
              ├─ dev->read_pos = 5
              ├─ dev->read_count++
              └─ mutex_unlock()
         │
         └─ return 5 to user

  close(fd)
         │
         │ syscall(SYS_close, fd)
         ▼
    Driver: mydev_release(inode, file)
              ├─ dev->open_count--
              └─ return 0
```

## 🧪 Test Architecture

### Test Program Structure
```c
test.c
├── test_open_close()
│   └─ Verifica apertura/chiusura base
│
├── test_write_read(data)
│   ├─ Scrivi dati
│   ├─ Reset posizione
│   ├─ Leggi dati
│   └─ Verifica corrispondenza
│
├── test_large_write()
│   └─ Verifica troncamento buffer
│
├── test_ioctl_commands()
│   ├─ Test RESET
│   ├─ Test GET_SIZE
│   └─ Test CLEAR
│
└── test_multiple_operations()
    └─ Verifica no memory leak
```

## 📊 Statistiche e Monitoring

### /proc/mydev_stats Output
```
=== MyDev Statistics ===
Device name: mydev
Major number: 240
Minor number: 0
Open count: 10
Read count: 25
Write count: 20
Buffer size: 1024 bytes
Data in buffer: 5 bytes
Read position: 0
```

### Metriche Monitorate
- **open_count**: Quante volte aperto (non decrementato correttamente?)
- **read_count**: Numero operazioni read
- **write_count**: Numero operazioni write
- **data_size**: Byte correnti nel buffer
- **read_pos**: Posizione lettura corrente

## 🚀 Cleanup Module

```c
module_exit(mydev_exit)
    │
    ├─▶ remove_proc_entry("mydev_stats", NULL)
    │      └─ Rimuove /proc/mydev_stats
    │
    ├─▶ device_destroy(mydev.class, mydev.dev)
    │      └─ Rimuove /dev/mydev
    │
    ├─▶ class_destroy(mydev.class)
    │      └─ Rimuove /sys/class/mydev_class/
    │
    ├─▶ cdev_del(&mydev.cdev)
    │      └─ Rimuove character device
    │
    └─▶ unregister_chrdev_region(mydev.dev, 1)
           └─ Libera major/minor number
```

## 🎓 Concetti Chiave

1. **Space Separation**: User vs Kernel space
2. **System Calls**: Bridge tra user e kernel
3. **VFS Abstraction**: File system universale
4. **File Operations**: Interface standard driver
5. **Synchronization**: Mutex per concorrenza
6. **Error Handling**: Codici errore standard
7. **Resource Management**: Cleanup corretto
8. **Security**: Verifiche user pointers

---

**Prossimi Passi:**
- Studia il codice sorgente (`mydev.c`)
- Esegui il programma di test
- Analizza `dmesg` per capire il flusso
- Modifica e sperimenta! 🧪
