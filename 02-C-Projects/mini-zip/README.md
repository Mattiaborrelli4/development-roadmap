# Mini-Zip - Utility di Compressione RLE

Una semplice utility per la compressione e decompressione di file utilizzando l'algoritmo **Run-Length Encoding (RLE)**. Scritta in C puro, è un progetto educativo perfetto per comprendere i concetti base della compressione dati.

## 📋 Sommario

- [Descrizione](#descrizione)
- [Caratteristiche](#caratteristiche)
- [Come Funziona RLE](#come-funziona-rle)
- [Requisiti](#requisiti)
- [Compilazione](#compilazione)
- [Utilizzo](#utilizzo)
- [Esempi](#esempi)
- [Limitazioni](#limitazioni)
- [Struttura del Progetto](#struttura-del-progetto)
- [Implementazione Tecnica](#implementazione-tecnica)
- [Licenza](#licenza)

## 🎯 Descrizione

Mini-Zip è un programma a riga di comando che permette di comprimere e decomprimere file utilizzando l'algoritmo RLE. È particolarmente efficace su file con molti caratteri ripetuti (come immagini monocromatiche, log di testo, etc.).

## ✨ Caratteristiche

- ✅ **Compressione RLE**: Comprime file usando Run-Length Encoding
- ✅ **Decompressione**: Ripristina i file compressi allo stato originale
- ✅ **Compression Ratio**: Mostra le statistiche di compressione
- ✅ **Gestione Errori**: Verifica esistenza file e validità dati
- ✅ **CLI Interface**: Interfaccia a riga di comando intuitiva
- ✅ **Auto-naming**: Genera automaticamente nomi file di output
- ✅ **Cross-platform**: Funziona su Windows, Linux, macOS

## 🧠 Come Funziona RLE

**Run-Length Encoding (RLE)** è uno degli algoritmi di compressione più semplici. Funziona così:

1. **Scansione**: Legge il file byte per byte
2. **Rilevamento**: Identifica sequenze di byte identici consecutivi
3. **Codifica**: Sostituisce ogni sequenza con una coppia `(count, byte)`
4. **Limite**: Se una sequenza supera 255 byte, viene divisa

**Esempio pratico:**

```
Originale:  AAAAAABBBBBCCCC
Compresso:  6A 5B 4C
            |  |  |
            |  |  +-- Byte: 'C' ripetuto 4 volte
            |  +----- Byte: 'B' ripetuto 5 volte
            +-------- Byte: 'A' ripetuto 6 volte
```

## 📦 Requisiti

### Sistema
- **Windows**: MinGW, MSVC, o WSL
- **Linux**: GCC o Clang
- **macOS**: Xcode Command Line Tools (incluso Clang)

### Compiler
- GCC 4.x o superiore
- Clang 3.x o superiore
- Qualsiasi compilatore compatibile C99

### Librerie
- Nessuna dipendenza esterna (solo standard C library)

## 🔨 Compilazione

### Linux / macOS

```bash
# Compila il programma
make

# Oppure usando gcc direttamente
gcc -Wall -Wextra -O2 -std=c99 -o mini-zip mini-zip.c

# Per il debugging
make debug
```

### Windows (CMD/PowerShell)

```bash
# Usa MinGW
gcc -Wall -Wextra -O2 -std=c99 -o mini-zip.exe mini-zip.c

# Oppure usa il Makefile (con MinGW)
mingw32-make
```

### Pulizia

```bash
# Linux / macOS
make clean

# Windows
del mini-zip.exe
```

## 🚀 Utilizzo

### Sintassi

```bash
mini-zip <comando> <file_input> [file_output]
```

### Comandi

| Comando | Alias | Descrizione |
|---------|-------|-------------|
| `compress` | `c` | Comprime un file |
| `decompress` | `d` | Decomprimi un file RLE |
| `help` | `h` | Mostra l'aiuto |

### Compressione

```bash
# Comprimi un file (output automatico: documento.txt.rle)
mini-zip compress documento.txt

# Specifica il nome del file di output
mini-zip c documento.txt documento_compresso.rle

# Usa l'alias breve
mini-zip c immagine.bmp immagine.rle
```

### Decompressione

```bash
# Decomprimi un file (rimuove automaticamente .rle)
mini-zip decompress documento.txt.rle

# Specifica il nome del file di output
mini-zip d documento.txt.rle documento_ripristinato.txt
```

## 📚 Esempi

### Esempio 1: Comprimere un file di testo

```bash
$ cat esempio.txt
AAAAAAAABBBCCCCCCDDDDDE

$ mini-zip c esempio.txt
Compressione in corso...

Compressione completata!
Dimensione originale:      27 bytes
Dimensione compressa:      10 bytes
Compression ratio:         37.04%
Spazio risparmiato:        17 bytes

$ ls -lh esempio.txt*
-rw-r--r-- 1 user user 27 Feb 12 10:00 esempio.txt
-rw-r--r-- 1 user user 14 Feb 12 10:00 esempio.txt.rle
```

### Esempio 2: Decomprimere un file

```bash
$ mini-zip d esempio.txt.rle esempio_ripristinato.txt
Decompressione in corso...

Decompressione completata!
Dimensione decompressa:    27 bytes
Dimensione originale:      27 bytes

$ diff esempio.txt esempio_ripristinato.txt
# Nessuna differenza - decompressione perfetta!
```

### Esempio 3: Gestione errori

```bash
$ mini-zip c file_inesistente.txt
Errore: Impossibile aprire il file 'file_inesistente.txt'

$ mini-zip d file_corrotto.bin
Errore: Formato file non valido (non e' un file RLE)
```

## ⚠️ Limitazioni

1. **Compressione ridondante**: Su file già compressi (ZIP, JPEG, MP3), RLE potrebbe aumentare le dimensioni
2. **No sub-255 sequences**: Sequenze di 2 byte ripetuti occupano più spazio (2 byte invece di 2)
3. **Memory buffering**: File molto grandi richiedono memoria proporzionata
4. **Max count 255**: Per evitare overflow, ogni sequenza è limitata a 255 byte

### Quando RLE funziona BENE:
- ✅ Immagini monocromatiche o con poche colori
- ✅ File con molti spazi o caratteri ripetuti
- ✅ Log di testo pattern-based
- ✅ Dati sensoriali con valori costanti

### Quando RLE funziona MALE:
- ❌ File già compressi (ZIP, GZIP, etc.)
- ❌ File binari casuali (criptati, etc.)
- ❌ Testo naturale con alta entropia
- ❌ File multimediali già compressi (JPEG, MP3)

## 📁 Struttura del Progetto

```
mini-zip/
├── mini-zip.c      # Sorgente principale
├── Makefile        # Build automation
├── README.md       # Documentazione (questo file)
└── mini-zip        # Eseguibile compilato (dopo make)
```

## 🔧 Implementazione Tecnica

### Struttura Header

```c
typedef struct {
    uint8_t magic[4];      // "RLE\0" - Signature per validazione
    uint32_t original_size; // Dimensione file originale
} RLEHeader;
```

### Algoritmo di Compressione

```c
for ogni byte nel file:
    conta = 1
    mentre byte_successivo == byte_corrente E conta < 255:
        conta++
    scrivi(counta, byte_corrente)
```

### Algoritmo di Decompressione

```c
leggi header
finché ci sono dati:
    leggi(count, byte)
    ripeti byte 'count' volte
```

### Gestione della Memoria

- Buffer di lettura: 4096 byte
- Buffer di scrittura: 8192 byte (massimo espansione 2x)
- Allocazione dinamica con malloc/free
- Controllo errori su tutte le allocazioni

### Gestione Errori

- ✅ File non trovato
- ✅ File vuoto
- ✅ Memoria insufficiente
- ✅ Errore scrittura file
- ✅ Formato file non valido
- ✅ File corrotto durante decompressione

## 🎓 Concetti Appresi

Questo progetto dimostra competenza in:

1. **File I/O**: fopen, fread, fwrite, fseek
2. **Memory Management**: malloc, free, buffer allocation
3. **Bit Manipulation**: Working con bytes e struct
4. **Error Handling**: Gestione robusta degli errori
5. **CLI Design**: Interfaccia utente a riga di comando
6. **Algorithm Design**: Implementazione algoritmo RLE
7. **Binary Data**: Understanding del formato binario
8. **Cross-platform Code**: Codice portabile

## 📝 Note Tecniche

- **Standard**: C99 (compatibile con la maggior parte dei compilatori)
- **Endianness**: Usa little-endian (standard x86/x64)
- **Platform-independent**: Codice portabile Windows/Linux/macOS
- **No dependencies**: Solo standard C library

## 🔜 Possibili Miglioramenti

- [ ] Supporto per compressioni multipli (algoritmi ibridi)
- [ ] Compressione streaming per file giganti
- [ ] Opzione -v per verbose mode
- [ ] Opzione -f per force overwrite
- [ ] Supporto per pipe stdin/stdout
- [ ] Compressione con dizionario (LZW)
- [ ] GUI semplice con ncurses

## 👨‍💻 Autore

**Matti**
- Progetto educativo per portfolio
- Anno: 2026

## 📄 Licenza

Questo progetto è released nel Public Domain (CC0). Sentiti libero di usarlo, modificarlo e distribuirlo come preferisci per scopi educativi o commerciali.

---

**Buon coding!** 🚀
