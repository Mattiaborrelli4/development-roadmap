# 🎮 Snake Game C++ - Crea il tuo Console Game Engine!

**Benvenuto!** Questo è un progetto educativo completo per imparare C++ moderno attraverso la creazione di un gioco.

---

## 🚀 Inizia Subito (3 Minuti)

### 1. Vai nella directory del progetto
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\03-Cpp-Projects\console-game"
```

### 2. Compila il gioco

**Windows (Più facile):**
```bash
build.bat
```

**Windows (Manuale):**
```bash
g++ -std=c++17 -o snake.exe ConsoleGame.cpp
```

**Linux/macOS:**
```bash
make run
```

### 3. Gioca!
```bash
# Windows
snake.exe

# Linux/macOS
./snake
```

---

## 📁 Cosa Troverai

### 📄 File Principali
- **ConsoleGame.cpp** (~18KB) - Il codice sorgente completo del gioco
- **README.md** (~15KB) - Documentazione completa in italiano

### 📖 Guide Educative
- **QUICK_REFERENCE.md** - Guida rapida per iniziare subito
- **PROJECT_OVERVIEW.md** - Panoramica architetturale completa
- **CLASS_DIAGRAM.txt** - Diagrammi UML delle classi
- **EXERCISES.md** - 6 esercizi graduati con soluzioni

### 🔧 Strumenti di Build
- **build.bat** - Script automatico per Windows
- **Makefile** - Build automation per Linux/macOS
- **CMakeLists.txt** - Configurazione CMake moderna
- **.gitignore** - File da ignorare in Git

---

## 🎯 Per Chi È Questo Progetto?

### ✅ Perfetto Per:
- Studenti universitari del primo anno
- Chi conosce C base e vuole imparare C++
- Chi vuole capire la programmazione orientata agli oggetti
- Appassionati di retro-gaming e console games

### ❌ Non Per:
- Programmatori C++ esperti (troppo semplice)
- Chi non ha mai programmato (prima impara le basi)
- Chi cerca giochi 3D o con grafica moderna

---

## 📚 Percorso di Apprendimento Suggerito

### 🌟 Settimana 1 - Iniziare
- [ ] Compila e gioca il gioco
- [ ] Leggi `QUICK_REFERENCE.md`
- [ ] Capisci il game loop base
- [ ] Fai modifiche semplici (vedi QUICK_REFERENCE)

### 🌟 Settimana 2 - Capire le Classi
- [ ] Leggi i commenti in `ConsoleGame.cpp`
- [ ] Studia la classe `Posizione`
- [ ] Studia la classe `GiocoSnake`
- [ ] Capisci incapsulamento e costruttori

### 🌟 Settimana 3 - OOP Practice
- [ ] Completa Esercizio 1 (High Score)
- [ ] Completa Esercizio 2 (Livelli)
- [ ] Leggi `PROJECT_OVERVIEW.md`
- [ ] Studia i diagrammi in `CLASS_DIAGRAM.txt`

### 🌟 Settimana 4 - Sfide Avanzate
- [ ] Completa Esercizio 3 (Ostacoli)
- [ ] Completa Esercizio 4 (Vite)
- [ ] Prova Esercizio 5 (Cibo speciale)
- [ ] Aggiungi la tua feature originale!

---

## 🎮 Come Giocare

### Controlli
```
W / ↑   = Muovi su
S / ↓   = Muovi giù
A / ←   = Muovi a sinistra
D / →   = Muovi a destra
Q       = Esci dal gioco
P       = Pausa (se implementato)
```

### Simboli
```
O = Testa del serpente
o = Corpo del serpente
* = Cibo (mangialo!)
X = Ostacolo (se implementato)
```

### Obiettivo
- Mangia il cibo `*` per crescere
- Ogni cibo = +10 punti
- Evita i muri e te stesso!
- Punteggio più alto possibile = 🏆

---

## 💡 Idee per Modifiche Semplici

### 1. Cambia Velocità
Cerca `const int FPS = 10;` e modifica il valore:
- `FPS = 5` → Molto lento
- `FPS = 10` → Normale
- `FPS = 20` → Veloce

### 2. Cambia Dimensioni Griglia
Cerca `GiocoSnake gioco(20, 15);`:
- `GiocoSnake gioco(30, 20);` → Più grande
- `GiocoSnake gioco(15, 10);` → Più piccolo

### 3. Cambia Punti
Cerca `punteggio += 10;`:
- `punteggio += 50;` → Più punti!
- `punteggio += 5;` → Più difficile

### 4. Cambia Caratteri
Cerca `cout << " O ";` e cambia i caratteri:
- `cout << " @ ";` → Testa diversa
- `cout << " # ";` → Corpo diverso
- `cout << " $ ";` → Cibo diverso

---

## 📖 Documentazione Importante

### Per Iniziare Subito
👉 **QUICK_REFERENCE.md** - 5 minuti per capire tutto

### Per Capire Bene
👉 **README.md** - Documentazione completa
👉 **PROJECT_OVERVIEW.md** - Architettura del progetto

### Per Praticare
👉 **EXERCISES.md** - Esercizi con soluzioni

### Per Approfondire
👉 **CLASS_DIAGRAM.txt** - Diagrammi UML
👉 **Commenti nel codice** - Spiegazioni linea per linea

---

## 🛠️ Troubleshooting

### Errore: "g++ non trovato"
**Windows:** Installa [MSYS2](https://www.msys2.org/)
**Linux:** `sudo apt-get install build-essential`
**macOS:** `brew install gcc`

### Il gioco non si avvia
**Verifica:**
- Il file `snake.exe` (o `snake`) esiste?
- Hai i permessi di esecuzione?
- Sei nella directory giusta?

### Caratteri strani a schermo
**Soluzione:** Il terminale deve supportare UTF-8 (la maggior parte lo fa)

### Warning durante compilazione
**Normale!** I warning non impediscono l'esecuzione. Per fixarli, vedi README.md

---

## 🎓 Cosa Imparerai

### Concetti C++
- ✅ Classi e oggetti
- ✅ Costruttori e distruttori
- ✅ Incapsulamento
- ✅ Operator overloading
- ✅ STL (deque, vector, algorithm)
- ✅ Gestione memoria base

### Pattern di Design
- ✅ Game Loop Pattern
- ✅ Separation of Concerns
- ✅ Single Responsibility Principle
- ✅ Template Method Pattern

### Best Practices
- ✅ Const correctness
- ✅ Member initializer lists
- ✅ Reference semantics
- ✅ RAII principles

---

## 🔗 Risorse Online

### Tutorial C++
- [C++ Reference](https://en.cppreference.com/) - Documentazione ufficiale
- [LearnCpp.com](https://www.learncpp.com/) - Tutorial eccellente
- [Cplusplus.com](https://www.cplusplus.com/) - Guide e reference

### Video Corsi
- [C++ Tutorial Italiano YouTube](https://youtube.com)
- [Programming with Mosh - C++](https://youtube.com)

### Libri
- "C++ Primer" - Per principianti
- "Effective C++" - Best practices
- "The C++ Programming Language" - Riferimento completo

---

## 💬 Supporto e Community

### Hai Domande?
1. Controlla il README.md troubleshooting
2. Cerca online il problema specifico
3. Chiedi su [Stack Overflow](https://stackoverflow.com/questions/tagged/c%2b%2b)
4. Chiedi al tuo insegnante/tutor

### Condividi il Tuo Progetto!
- GitHub - Condividi il tuo fork
- Reddit - r/cpp o r/learnprogramming
- Discord - Server C++ learning

---

## 📊 Statistiche del Progetto

```
Linguaggio:        C++17
Righe di codice:   ~450
Classi:            2
Metodi:            13
Commenti:          ~150
Esercizi:          6
Pagine documentaz: ~50
Difficoltà:        ⭐⭐⭐☆☆
Tempo stimato:     2-4 settimane
```

---

## 🎉 Inizia Ora!

Scegli il tuo percorso:

### 🚀 Veloce
1. `build.bat` (o `make run`)
2. Gioca!
3. Leggi QUICK_REFERENCE.md
4. Fai modifiche

### 📚 Completo
1. Leggi README.md
2. Studia il codice
3. Completa esercizi
4. Crea feature originali

### 🎓 Accademico
1. Studia PROJECT_OVERVIEW.md
2. Analizza CLASS_DIAGRAM.txt
3. Implementa tutti gli esercizi
4. Scrivi documentazione
5. Presenta il progetto

---

## 📜 Licenza

MIT License - Sei libero di usarlo, modificarlo e condividerlo!

---

**Buon divertimento con C++ e Snake!** 🐍🎮

*"La miglior façon d'apprendre est de créer"* - La migliore maniera di imparare è creare

---

**Versione:** 1.0
**Data:** Febbraio 2026
**Autore:** Progetto educativo per studenti universitari
