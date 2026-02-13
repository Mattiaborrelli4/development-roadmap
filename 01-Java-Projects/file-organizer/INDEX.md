# 📚 Indice Documentazione - File Organizer

## 🎯 Dove Cominciare?

**Se vuoi iniziare subito:** Leggi [QUICKSTART.md](QUICKSTART.md)

**Se vuoi capire come funziona:** Leggi [README.md](README.md)

**Se vuoi fare dei test:** Leggi [DEMO.md](DEMO.md)

---

## 📖 Documenti Disponibili

### 🚀 Guide Principali
| Documento | Scopo | Quando leggerlo |
|-----------|-------|-----------------|
| [README.md](README.md) | Documentazione completa | Prima di usare l'app |
| [QUICKSTART.md](QUICKSTART.md) | Guida rapida 2 minuti | Per iniziare subito |
| [DEMO.md](DEMO.md) | Guida ai test | Per testare l'applicazione |

### 📚 Documentazione Tecnica
| Documento | Scopo | Quando leggerlo |
|-----------|-------|-----------------|
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Struttura cartelle e file | Per capire il progetto |
| [OVERVIEW.md](OVERVIEW.md) | Panoramica architetturale | Per capire l'architettura |

### 📋 File di Riferimento
| Documento | Scopo |
|-----------|-------|
| [INDEX.md](INDEX.md) | Questo file - indice documentazione |
| [sample-log.txt](sample-log.txt) | Esempio di log generato |
| [.gitignore](.gitignore) | File ignorati da Git |
| [pom.xml](pom.xml) | Configurazione Maven (opzionale) |

---

## 🗂️ Struttura Progetto

```
file-organizer/
│
├── 📖 DOCUMENTAZIONE
│   ├── README.md              # Documentazione principale
│   ├── QUICKSTART.md          # Guida rapida
│   ├── DEMO.md                # Guida ai test
│   ├── PROJECT_STRUCTURE.md   # Struttura progetto
│   ├── OVERVIEW.md            # Panoramica architetturale
│   └── INDEX.md               # Questo file
│
├── 💻 CODICE
│   ├── src/main/java/com/organizer/
│   │   └── FileOrganizer.java     # Classe principale
│   └── src/main/resources/
│       └── config.json            # Configurazione regole
│
├── 🔧 SCRIPTS
│   ├── build.bat / build.sh       # Compilazione
│   └── run.bat / run.sh           # Esecuzione
│
├── 📦 BUILD
│   ├── pom.xml                    # Maven (opzionale)
│   └── lib/                       # Dipendenze (creare)
│
└── 📝 OUTPUT
    ├── out/                       # File compilati
    ├── organizer.log              # Log runtime
    └── sample-log.txt             # Esempio log
```

---

## 🎯 Roadmap Lettura Consigliata

### Livello 1: Utente (15 minuti)
1. Leggi [QUICKSTART.md](QUICKSTART.md) - Setup rapido
2. Esegui l'applicazione
3. Leggi [README.md](README.md) sezione "Caratteristiche"
4. Fai un test da [DEMO.md](DEMO.md)

### Livello 2: Sviluppatore (30 minuti)
1. Completa Livello 1
2. Leggi [README.md](README.md) completo
3. Leggi [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
4. Esamina `FileOrganizer.java`
5. Studia `config.json`

### Livello 3: Architetto (45 minuti)
1. Completa Livello 2
2. Leggi [OVERVIEW.md](OVERVIEW.md)
3. Analizza i design patterns
4. Studia le API usate
5. Considera miglioramenti

---

## 📊 Riepilogo Rapido

| Info | Dettaglio |
|------|----------|
| **Linguaggio** | Java 11+ |
| **Tipo** | Console Application |
| **Core Feature** | WatchService (NIO.2) |
| **Config** | JSON + Gson |
| **Logging** | java.util.logging |
| **OS** | Windows, Linux, Mac |
| **Setup Time** | 5 minuti |
| **Dipendenze** | Gson JAR |

---

## 🔗 Link Rapidi

### Compilazione
```bash
# Windows
build.bat

# Linux/Mac
./build.sh
```

### Esecuzione
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### Download Gson
https://github.com/google/gson/releases

---

## ❓ FAQ Rapida

**D: È difficile da usare?**
R: No, bastano 2 minuti per iniziare (vedi QUICKSTART.md)

**D: Funziona su Mac?**
R: Sì, è multipiattaforma (Windows, Linux, Mac)

**D: Serve installare Maven?**
R: No, puoi usare gli script build.bat/build.sh

**D: È sicuro?**
R: Sì, opera solo sul tuo filesystem locale

**D: Posso modificare le regole?**
R: Sì, modifica config.json

**D: Perdiamo i file?**
R: No, i file vengono solo spostati, non cancellati

---

## 🎓 Cosa Imparerai

Studiando questo progetto imparerai:
- ✅ Java NIO.2 e WatchService
- ✅ File system operations
- ✅ JSON parsing con Gson
- ✅ Logging in Java
- ✅ Configuration management
- ✅ Exception handling
- ✅ Build automation

---

## 📞 Supporto

Per problemi o domande:
1. Controlla README.md sezione "Risoluzione Problemi"
2. Vedi DEMO.md sezione "Troubleshooting Test"
3. Verifica sample-log.txt per esempi

---

**Buon divertimento con File Organizer!** 🚀

---

*Questo indice fa parte del progetto File Organizer - Febbraio 2026*
