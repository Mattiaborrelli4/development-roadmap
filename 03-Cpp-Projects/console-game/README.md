# 🐍 Console Game Engine - Snake in C++

![C++](https://img.shields.io/badge/C++-17-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Level](https://img.shields.io/badge/level-Beginner-yellow.svg)

Un motore di gioco console semplice ed educativo scritto in C++ moderno (C++17). Questo progetto è stato progettato specificamente per studenti universitari che desiderano apprendere i concetti della programmazione orientata agli oggetti (OOP) attraverso un esempio pratico e divertente.

## 📋 Indice

- [Descrizione del Progetto](#descrizione-del-progetto)
- [Caratteristiche Tecniche](#caratteristiche-tecniche)
- [Prerequisiti](#prerequisiti)
- [Compilazione ed Esecuzione](#compilazione-ed-esecuzione)
- [Come Giocare](#come-giocare)
- [Struttura del Codice](#struttura-del-codice)
- [Concetti OOP Dimostrati](#concetti-oop-dimostrati)
- [Architettura del Codice](#architettura-del-codice)
- [Esercizi Proposti](#esercizi-proposti)
- [Risorse Utili](#risorse-utili)

## 🎮 Descrizione del Progetto

Questo progetto implementa il classico gioco **Snake** utilizzando C++ moderno. Il codice è stato scritto con un forte focus educativo, con commenti dettagliati che spiegano ogni concetto di programmazione utilizzato.

### Obiettivi Educativi

✅ Comprendere i principi della programmazione orientata agli oggetti
✅ Imparare a utilizzare la Standard Template Library (STL)
✅ Implementare un game loop funzionante
✅ Gestire l'input utente in tempo reale
✅ Strutturare un progetto C++ in modo professionale

## 🛠️ Caratteristiche Tecniche

### Linguaggio e Standard
- **Linguaggio**: C++17
- **Compilatore supportato**: GCC 7+, Clang 5+, MSVC 2017+
- **Librerie**: Solo STL (nessuna dipendenza esterna)

### Componenti STL Utilizzati
- `std::deque` - Container per il serpente (operazioni efficienti all'inizio/fine)
- `std::vector` - Container dinamico
- `std::random` - Generatore di numeri casuali moderno (C++11+)
- `std::chrono` - Gestione del tempo e frame rate
- `std::iostream` - Input/output stream

### Design Pattern
- **Encapsulation**: Dati privati con metodi pubblici
- **Separation of Concerns**: Logica separata dalla visualizzazione
- **Single Responsibility**: Ogni classe ha una responsabilità unica

## 📦 Prerequisiti

### Opzione 1: Windows (Visual Studio)

1. Installa [Visual Studio Community](https://visualstudio.microsoft.com/) (gratuito)
2. Durante l'installazione, assicurati di selezionare:
   - "Desktop development with C++"
   - Windows SDK

### Opzione 2: Windows (MinGW)

1. Installa [MSYS2](https://www.msys2.org/)
2. Apri MSYS2 MinGW 64-bit terminal ed esegui:
   ```bash
   pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-make
   ```

### Opzione 3: Linux/macOS

1. Installa i build tools essenziali:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install build-essential

   # macOS (con Homebrew)
   brew install gcc
   ```

## 🔨 Compilazione ed Esecuzione

### Windows (Visual Studio)

```bash
# 1. Apri "Developer Command Prompt for VS"
# 2. Naviga nella directory del progetto
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\03-Cpp-Projects\console-game"

# 3. Compila il programma
cl /EHsc /std:c++17 ConsoleGame.cpp

# 4. Esegui
ConsoleGame.exe
```

### Windows (MinGW/GCC)

```bash
# 1. Apri MSYS2 MinGW 64-bit terminal
# 2. Naviga nella directory del progetto
cd "/c/Users/matti/Desktop/Project Ideas Portfolio/03-Cpp-Projects/console-game"

# 3. Compila il programma
g++ -std=c++17 -o snake.exe ConsoleGame.cpp

# 4. Esegui
./snake.exe
```

### Linux/macOS

```bash
# 1. Apri il terminale
# 2. Naviga nella directory del progetto
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\03-Cpp-Projects\console-game"

# 3. Compila il programma
g++ -std=c++17 -o snake ConsoleGame.cpp

# 4. Esegui
./snake
```

### Opzioni di Compilazione Spiegate

| Flag | Descrizione |
|------|-------------|
| `-std=c++17` | Usa lo standard C++17 |
| `-o nome` | Specifica il nome del file di output |
| `/EHsc` (MSVC) | Abilita la gestione delle eccezioni |
| `-Wall` (opzionale) | Abilita tutti i warning (raccomandato!) |
| `-Wextra` (opzionale) | Abilita warning extra (per codice più pulito) |

## 🎯 Come Giocare

### Controlli

| Tasto | Azione |
|-------|--------|
| **W** | Muovi verso l'alto |
| **S** | Muovi verso il basso |
| **A** | Muovi verso sinistra |
| **D** | Muovi verso destra |
| **Q** | Esci dal gioco |

### Obiettivo

- 🟢 Controlla il serpente rappresentato da `O` (testa) e `o` (corpo)
- ⭐ Mangia il cibo `*` per crescere e guadagnare punti
- ⚠️ Evita di colpire i bordi o te stesso
- 🏆 Cerca di ottenere il punteggio più alto!

### Punteggio

- Ogni pezzo di cibo mangiato: **+10 punti**
- Il gioco termina quando colpisci un bordo o te stesso

## 📚 Struttura del Codice

Il progetto è composto da un unico file sorgente organizzato in sezioni logiche:

```
ConsoleGame.cpp
├── Include Headers
│   ├── <iostream>     - Input/Output
│   ├── <vector>       - Container dinamico
│   ├── <deque>        - Container a doppia coda
│   ├── <random>       - Numeri casuali
│   └── <chrono>       - Gestione del tempo
│
├── Classe Posizione
│   ├── Membri privati (x, y)
│   ├── Costruttore
│   ├── Getter/Setter
│   └── Operator overloading (==)
│
├── Classe GiocoSnake
│   ├── Membri privati
│   │   ├── Stato del gioco
│   │   ├── Serpente (deque<Posizione>)
│   │   └── Generatore casuale
│   │
│   ├── Metodi privati (helper)
│   │   ├── generaCibo()
│   │   ├── èFuoriBordi()
│   │   ├── verificaCollisione()
│   │   └── calcolaNuovaTesta()
│   │
│   └── Metodi pubblici (interfaccia)
│       ├── aggiorna()
│       ├── processaInput()
│       ├── renderizza()
│       └── èTerminato()
│
└── Funzione main()
    ├── Inizializzazione
    ├── Game Loop
    └── Cleanup
```

## 🎓 Concetti OOP Dimostrati

### 1. **Incapsulamento (Encapsulation)**

```cpp
class Posizione {
private:        // Dati nascosti
    int x;
    int y;

public:         // Interfaccia pubblica
    int getX() const { return x; }  // Getter
    void setX(int nuovoX) { x = nuovoX; }  // Setter
};
```

**Benefici:**
- Protezione dei dati interni
- Controllo su come i dati vengono modificati
- Possibilità di cambiare l'implementazione senza rompere il codice esterno

### 2. **Costruttori e Distruttori**

```cpp
// Costruttore: inizializza l'oggetto
GiocoSnake(int w, int h)
    : larghezza(w), altezza(h) {  // Member initializer list
    // Codice di inizializzazione
}

// Distruttore: pulisce le risorse
~GiocoSnake() {
    // Cleanup code
}
```

**Benefici:**
- Garantisce che l'oggetto sia sempre in uno stato valido
- Gestione automatica delle risorse (RAII - Resource Acquisition Is Initialization)

### 3. **Operator Overloading**

```cpp
// Permette di confrontare oggetti naturalmente
bool operator==(const Posizione& altra) const {
    return x == altra.x && y == altra.y;
}

// Utilizzo:
if (posizione1 == posizione2) {  // Sintassi naturale!
    // ...
}
```

### 4. **Const Correctness**

```cpp
// Metodi che non modificano lo stato sono marcati const
int getX() const { return x; }

bool èTerminato() const { return giocoTerminato; }
```

**Benefici:**
- Documenta l'intento del metodo
- Permette ottimizzazioni del compilatore
- Previene modifiche accidentali

### 5. **Separation of Concerns**

```cpp
// Logica di gioco
void aggiorna() { /* ... */ }

// Visualizzazione
void renderizza() const { /* ... */ }

// Input
void processaInput(char tasto) { /* ... */ }
```

## 🏗️ Architettura del Codice

### Game Loop Pattern

Il cuore del gioco è il **Game Loop**, che segue questo schema:

```
┌─────────────────────────────────────┐
│         GAME LOOP                   │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────┐    ┌─────────┐        │
│  │  INPUT  │───▶│  UPDATE │───┐    │
│  └─────────┘    └─────────┘   │    │
│       ▲                        │    │
│       │                        ▼    │
│       │                   ┌─────────┐│
│       │                   │  RENDER ││
│       │                   └─────────┘│
│       │                        ▲     │
│       └────────────────────────┘     │
│                                     │
│      Fino a giocoTerminato          │
└─────────────────────────────────────┘
```

### FLUSSO DI ESECUZIONE

1. **INPUT**: Raccogli l'input dall'utente
2. **UPDATE**: Aggiorna lo stato del gioco
3. **RENDER**: Disegna lo stato corrente
4. **REPEAT**: Ripeti finché il gioco non termina

### Gestione del Tempo

```cpp
// Frame rate control
const int FPS = 10;
const auto durataFrame = std::chrono::milliseconds(1000 / FPS);

auto ultimoAggiornamento = std::chrono::steady_clock::now();

// Nel game loop:
auto tempoTrascorso = ora - ultimoAggiornamento;
if (tempoTrascorso >= durataFrame) {
    gioco.aggiorna();
    ultimoAggiornamento = ora;
}
```

Questo garantisce che il gioco giri alla stessa velocità su computer diversi.

## 💡 Esercizi Proposti

Metti alla prova le tue conoscenze con questi esercizi!

### Livello Principiante

1. **Modifica dimensioni griglia**
   ```cpp
   // Cambia la dimensione della griglia di gioco
   GiocoSnake gioco(30, 20);  // Invece di 20x15
   ```

2. **Aggiungi livello di difficoltà**
   ```cpp
   // Aggiungi velocità variabile (Easy/Medium/Hard)
   // Suggerimento: modifica il valore FPS
   ```

3. **Personalizza caratteri**
   ```cpp
   // Cambia i caratteri usati per il serpente e il cibo
   // Testa: '@' invece di 'O'
   // Cibo: '$' invece di '*'
   ```

### Livello Intermedio

4. **Implementa High Score**
   ```cpp
   // Salva il punteggio più alto in un file
   // Caricalo all'avvio del gioco
   // Suggerimento: usa <fstream>
   ```

5. **Aggiungi ostacoli**
   ```cpp
   // Crea una classe Ostacolo simile a Posizione
   // Genera ostacoli casuali all'inizio
   // Verifica collisioni con gli ostacoli
   ```

6. **Sistema di vite**
   ```cpp
   // Invece di Game Over immediato, dai 3 vite
   // Resetta il serpente quando colpisci, ma mantieni il punteggio
   ```

### Livello Avanzato

7. **Bonus food types**
   ```cpp
   // Cibo speciale che dà punti extra (rosso: +50)
   // Cibo che velocizza (blu: +20 ma aumenta velocità)
   // Cibo che rallenta (verde: +10 ma rallenta)
   ```

8. **Menu principale**
   ```cpp
   // Implementa un menu con:
   // - Nuovo gioco
   // - Continua
   // - High score
   // - Esci
   ```

9. **Power-ups**
   ```cpp
   // Crea un sistema di power-up temporanei:
   // - Attraversa i muri
   // - Invincibilità
   // - Raddoppio punti
   ```

10. **Rifattoring in file multipli**
    ```cpp
    // Separa il codice in file multipli:
    // - Posizione.h / Posizione.cpp
    // - GiocoSnake.h / GiocoSnake.cpp
    // - main.cpp
    ```

### Sfida Extra: AI Player

```cpp
// Implementa un'IA che gioca da sola
// Suggerimenti:
// - Algoritmo A* per pathfinding
// - Euristica per evitare collisioni
// - Modalità demo quando l'utente non preme tasti
```

## 📖 Risorse Utili

### Tutorial e Guide

- [C++ Reference](https://en.cppreference.com/) - Documentazione completa C++
- [LearnCpp.com](https://www.learncpp.com/) - Tutorial eccellente
- [Cplusplus.com](https://www.cplusplus.com/) - Guide e reference

### Video Corsi (Italiano)

- [C++ Corso Completo](https://www.youtube.com/results?search_query=c+++corso+completo+italiano)
- [Programmazione OOP C++](https://www.youtube.com/results?search_query=oop+c+++italiano)

### Libri Consigliati

1. **"C++ Primer"** di Lippman et al. - Per principianti
2. **"Effective C++"** di Scott Meyers - Best practices
3. **"The C++ Programming Language"** di Bjarne Stroustrup - Riferimento completo

### Strumenti di Sviluppo

- **IDE**: Visual Studio Code, CLion, Visual Studio
- **Debugger**: GDB, LLDB, Visual Studio Debugger
- **Formatter**: clang-format
- **Linter**: clang-tidy

### Community

- [Stack Overflow - C++ Tag](https://stackoverflow.com/questions/tagged/c%2b%2b)
- [Reddit - r/cpp](https://www.reddit.com/r/cpp/)
- [Italian C++ Community](https://www.cppitalia.org/)

## 🤝 Contribuire

Questo è un progetto educativo, ma se hai suggerimenti per migliorarlo:

1. Fai una fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/MiaFeature`)
3. Commit i tuoi cambiamenti (`git commit -m 'Aggiunta MiaFeature'`)
4. Push al branch (`git push origin feature/MiaFeature`)
5. Apri una Pull Request

## 📝 Licenza

Questo progetto è rilasciato sotto la licenza MIT. Sei libero di usarlo per scopi educativi e commerciali.

## 👨‍🏫 Note per l'Insegnante

Questo progetto può essere utilizzato come:

- **Esempio pratico** per lezioni di OOP
- **Base per progetti studenteschi**
- **Template** per altri giochi console
- **Esercizio di refactoring** (separare in file multipli)

### Suggerimenti Didattici

1. Inizia mostrando solo la classe `Posizione`
2. Aggiungi gradualmente i metodi di `GiocoSnake`
3. Fai implementare agli studenti una nuova feature
4. Usa il code for analizzare il codice insieme
5. Incoraggia esperimenti e modifiche

## 🎉 Conclusioni

Congratulazioni per aver scelto di imparare C++ attraverso un progetto pratico! La programmazione di giochi è un modo eccellente per solidificare i concetti di programmazione orientata agli oggetti.

Ricorda:
- ✨ La pratica rende perfetti
- 🐛 Non aver paura di fare errori
- 📚 Consulta la documentazione ufficiale
- 🤝 Chiedi aiuto alla community

Buon coding e buon divertimento con Snake! 🐍🎮

---

**Creato con ❤️ per studenti universitari**

*Ultimo aggiornamento: 2026*
