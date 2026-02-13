# MyDev - Simple Character Device Driver

> ⚠️ **PROGETTO EDUCATIVO** - Questo è un driver di dispositivo virtuale per imparare la programmazione dei moduli kernel Linux. Nessuna manipolazione hardware reale.

Un semplice driver per dispositivo a caratteri Linux per scopi educativi. Perfetto per imparare i concetti di base della programmazione di sistema e dei driver di dispositivo.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Struttura del Progetto](#struttura-del-progetto)
- [Concetti Appresi](#concetti-appresi)
- [Risoluzione Problemi](#risoluzione-problemi)
- [Risorse](#risorse)

## ✨ Caratteristiche

- **Dispositivo a caratteri**: Registrazione in `/dev/mydev`
- **Operazioni file supportate**: `open`, `close`, `read`, `write`
- **Comandi IOCTL**: Controllo personalizzato del dispositivo
- **Interfaccia /proc**: Statistiche in `/proc/mydev_stats`
- **Buffer circolare**: Gestione sicura dei dati
- **Sincronizzazione**: Mutex per la protezione da race conditions
- **Gestione errori**: Controlli rigorosi e logging kernel

## 🔧 Prerequisiti

### Sistema Operativo
- Linux (testato su Ubuntu 20.04+, Debian, Fedora)
- Kernel headers per il tuo kernel

### Installazione Kernel Headers

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r)
```

**Fedora/RHEL:**
```bash
sudo dnf install kernel-devel kernel-headers
sudo dnf groupinstall "Development Tools"
```

**Arch Linux:**
```bash
sudo pacman -S base-devel linux-headers
```

## 📦 Installazione

### 1. Clone o Naviga nella Directory
```bash
cd device-driver/
```

### 2. Compila il Modulo
```bash
make
```

Questo genera:
- `mydev.ko` - Modulo kernel
- `mydev.mod.c`, `mydev.mod.o` - File oggetto intermedi
- `Module.symvers` - Simboli del modulo

### 3. Compila il Programma di Test
```bash
make test
```

Genera il binario `test` per il testing userspace.

## 🚀 Utilizzo

### Metodo 1: Script Automatico (Consigliato)
```bash
chmod +x test.sh
sudo ./test.sh
```

Questo script:
1. Compila il modulo e il test
2. Carica il modulo kernel
3. Verifica i file dispositivo
4. Esegue i test
5. Mostra le statistiche
6. Offre di scaricare il modulo

### Metodo 2: Passo Passo

#### Carica il Modulo
```bash
sudo insmod mydev.ko
```

#### Verifica il Caricamento
```bash
# Verifica che il modulo sia caricato
lsmod | grep mydev

# Controlla i messaggi del kernel
dmesg | tail -20

# Verifica il file dispositivo
ls -l /dev/mydev

# Verifica l'entry proc
cat /proc/mydev_stats
```

#### Esegui il Programma di Test
```bash
sudo ./test
```

Output atteso:
```
==============================================
  Test Program: MyDev Character Device
  Educational Kernel Module Testing
==============================================

[INFO] Test 1: Open/Close device
  Device aperto correttamente (fd=3)
  Device chiuso correttamente
[SUCCESSO] Test 1 SUPERATO

[INFO] Test 2: Write and Read
  Scritti 12 byte: "Ciao Kernel!"
  Letti 12 byte: "Ciao Kernel!"
  Dati verificati con successo
[SUCCESSO] Test 2 SUPERATO

...
```

#### Interazione Manuale

**Scrivi dati:**
```bash
echo "Hello Kernel!" | sudo dd of=/dev/mydev
```

**Leggi dati:**
```bash
sudo dd if=/dev/mydev of=output.txt
cat output.txt
```

**Usa IOCTL (tramite test program):**
```bash
# Il test program mostra come usare:
# - MYDEV_IOCTL_RESET: Resetta la posizione di lettura
# - MYDEV_IOCTL_GET_SIZE: Ottiene la dimensione dei dati
# - MYDEV_IOCTL_CLEAR: Pulisce il buffer
```

#### Visualizza Statistiche
```bash
cat /proc/mydev_stats
```

Output:
```
=== MyDev Statistics ===
Device name: mydev
Major number: 240
Minor number: 0
Open count: 0
Read count: 5
Write count: 5
Buffer size: 1024 bytes
Data in buffer: 12 bytes
Read position: 0
```

#### Scarica il Modulo
```bash
sudo rmmod mydev
```

## 📁 Struttura del Progetto

```
device-driver/
├── mydev.c              # Sorgente del modulo kernel
├── Makefile             # Build system per il modulo
├── test.c               # Programma di test userspace
├── test.sh              # Script di build e test automatico
├── README.md            # Questo file
└── ARCHITECTURE.md      # Documentazione architetturale

File generati durante la compilazione:
├── mydev.ko             # Modulo kernel compilato
├── mydev.o              # File oggetto
├── test                 # Binario di test
├── Module.symvers       # Simboli esportati
└── .mydev.ko.cmd       # Dipendenze di compilazione
```

## 🎓 Concetti Appresi

Questo progetto insegna i seguenti concetti di programmazione di sistema:

### 1. Kernel Module Programming
- Ciclo di vita dei moduli (`module_init`, `module_exit`)
- Macro del kernel (`MODULE_LICENSE`, `MODULE_AUTHOR`, etc.)
- Logging kernel (`printk`, `pr_info`, `pr_err`)

### 2. Character Device Drivers
- Registrazione dispositivi (`alloc_chrdev_region`, `register_chrdev`)
- Struttura `file_operations`
- Operazioni: open, release, read, write, ioctl

### 3. User-Kernel Space Communication
- `copy_to_user` - Dati dal kernel allo userspace
- `copy_from_user` - Dati dall'userspace al kernel
- IOCTL per controllo del dispositivo

### 4. Synchronization
- Mutex per proteggere dati condivisi
- Prevenzione di race conditions

### 5. Kernel Subsystems
- **Device Model**: Classi e dispositivi
- **Proc Filesystem**: Interfaccia `/proc`
- **VFS (Virtual File System)**: astrazione file system

### 6. Memory Management
- Allocazione dinamica in kernel space
- Gestione buffer e limiti

## 🐛 Risoluzione Problemi

### Errore: "Permission denied" su /dev/mydev
**Soluzione:**
```bash
sudo chmod 666 /dev/mydev
# Oppure esegui il test con sudo
sudo ./test
```

### Errore: "Operation not permitted" durante insmod
**Causa:** Moduli con firma obbligatoria (Secure Boot)
**Soluzione:**
```bash
# Disabilita Secure Boot OPPURE
# Firma il modulo (avanzato)
```

### Errore: "Invalid module format"
**Causa:** Mismatch versione kernel
**Soluzione:**
```bash
# Verifica versione kernel
uname -r
# Assicurati di avere gli header corretti
ls /lib/modules/$(uname -r)/build
```

### Errore: "Unknown symbol"
**Soluzione:**
```bash
# Pulisci e ricompila
make clean
make
```

### Dispositivo non creato in /dev/
**Verifica:**
```bash
# Controlla dmesg per errori
dmesg | grep mydev

# Verifica major number
cat /proc/devices | grep mydev

# Crea manualmente se necessario
sudo mknod /dev/mydev c <major> 0
sudo chmod 666 /dev/mydev
```

### Debug Avanzato
```bash
# Log kernel in tempo reale
sudo tail -f /var/log/kern.log

# Oppure
dmesg -w

# Trace system calls
strace -e openat,read,write,ioctl ./test
```

## 📚 Risorse

### Libri e Documentazione
- **LDD3**: *Linux Device Drivers 3* - https://lwn.net/Kernel/LDD3/
- **Kernel Documentation**: https://www.kernel.org/doc/html/latest/
- **The Linux Kernel Module Programming Guide**: https://sysprog21.github.io/lkmpg/

### Reference Online
- **Linux Kernel API**: https://www.kernel.org/doc/html/latest/core-api/index.html
- **Device Drivers**: https://www.kernel.org/doc/html/latest/driver-api/
- **LWN.net**: Articoli approfonditi sul kernel Linux

### Comandi Utili
```bash
# Informazioni modulo
modinfo mydev.ko

# Lista moduli caricati
lsmod

# Dipendenze modulo
modshow --show mydev.ko

# System map
grep mydev /proc/kallsyms
```

## 🔒 Sicurezza

⚠️ **AVVERTENZE IMPORTANTI:**

1. **Solo Scopi Educativi**: Questo driver è per apprendimento, non per produzione
2. **Privilegi Root**: Richiede `sudo` per caricare moduli kernel
3. **Test Environment**: Usa una VM o sistema di test
4. **Backup**: Fai backup prima di esperimenti kernel
5. **Kernel Panic**: Bug possono crashare il sistema (ma questo driver è sicuro)

## 🤝 Contributi

Questo è un progetto educativo. Suggerimenti e miglioramenti sono benvenuti!

## 📄 Licenza

GPL v2 - Standard per i moduli kernel Linux

## 👨‍🏫 Autore

Progetto educativo per imparare la System Programming in Linux.

---

**Buon apprendimento! 🎓**
