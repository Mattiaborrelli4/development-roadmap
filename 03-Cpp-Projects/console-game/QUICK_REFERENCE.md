# 🚀 Guida Rapida - C++ Snake Game

## Compilazione Veloce

### Windows
```bash
# Opzione 1: Usa lo script di build
build.bat

# Opzione 2: Manuale con MinGW
g++ -std=c++17 -o snake.exe ConsoleGame.cpp
./snake.exe

# Opzione 3: Con Visual Studio
cl /EHsc /std:c++17 ConsoleGame.cpp
snake.exe
```

### Linux/macOS
```bash
# Opzione 1: Usa il Makefile
make run

# Opzione 2: Manuale
g++ -std=c++17 -o snake ConsoleGame.cpp
./snake
```

## Struttura del Codice in 60 Secondi

```
┌─────────────────────────────────────────────────────────┐
│                      main()                              │
│  Crea l'oggetto GiocoSnake e avvia il game loop         │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Classe Posizione│     │ Classe GiocoSnake│
│  - x, y (coord) │     │ - serpente       │
│  - operator==   │     │ - cibo           │
└─────────────────┘     │ - punteggio      │
                        │ - aggiorna()     │
                        │ - renderizza()   │
                        └─────────────────┘
```

## Concetti Chiave

### 1. Classi e Oggetti
```cpp
class Posizione {
    int x, y;           // Dati (privati)
public:
    Posizione(int x, int y);  // Costruttore
    int getX() const;         // Getter
};

Posizione p(5, 10);    // Crea un oggetto
int x = p.getX();      // Usa l'oggetto
```

### 2. Incapsulamento
```cpp
private:  // Accessibile solo dentro la classe
    int dato;

public:   // Accessibile da fuori
    int getDato() { return dato; }
```

### 3. STL Containers
```cpp
std::deque<Posizione> serpente;  // Lista a doppia estremità
serpente.push_front(pos);         // Aggiungi all'inizio
serpente.pop_back();              // Rimuovi dalla fine
```

### 4. Const Correctness
```cpp
void metodo() { /* può modificare */ }
void metodo() const { /* NON può modificare */ }
```

## Game Loop Pattern

```
while (!giocoFinito) {
    leggiInput();     // 1. Leggi tastiera
    aggiornaStato();  // 2. Muovi serpente, verifica collisioni
    disegna();        // 3. Mostra a schermo
}
```

## Modifiche Semplici da Provare

### 1. Cambia velocità
```cpp
// In GiocoSnake::aggiorna(), cerca:
const int FPS = 10;

// Cambia in:
const int FPS = 20;  // Più veloce!
```

### 2. Cambia caratteri
```cpp
// In GiocoSnake::renderizza(), cerca:
cout << " O ";  // Testa
cout << " o ";  // Corpo
cout << " * ";  // Cibo

// Cambia in:
cout << " @ ";  // Testa
cout << " # ";  // Corpo
cout << " $ ";  // Cibo
```

### 3. Cambia dimensioni
```cpp
// In main(), cerca:
GiocoSnake gioco(20, 15);

// Cambia in:
GiocoSnake gioco(30, 20);  // Griglia più grande!
```

### 4. Modifica punteggio
```cpp
// In GiocoSnake::aggiorna(), cerca:
punteggio += 10;

// Cambia in:
punteggio += 50;  // Più punti!
```

## Troubleshooting Comune

### Errore: "g++ not found"
**Windows:** Installa [MSYS2](https://www.msys2.org/)
**Linux:** `sudo apt-get install build-essential`
**macOS:** `brew install gcc`

### Il gioco va troppo veloce/lento
**Soluzione:** Modifica il valore `FPS` nel codice
- FPS più alto = più veloce
- FPS più basso = più lento

### Caratteri strani a schermo
**Soluzione:** Assicurati che il terminale supporti UTF-8

### Compilation warnings
**Soluzione:** Sono normali! Per ora ignorali. Se vuoi fixarli:
- Aggiungi `-Wall` per vedere tutti i warning
- Correggi ciò che indica il compilatore

## Prossimi Passi

1. ✅ Capisci come funziona il codice attuale
2. ✅ Fai le modifiche suggerite sopra
3. ✅ Leggi i commenti nel codice sorgente
4. ✅ Prova gli esercizi nel README
5. ✅ Crea la tua feature personalizzata!

## Risorse

- 📖 [C++ Reference](https://en.cppreference.com/)
- 📹 [Tutorial C++ YouTube](https://youtube.com)
- 💬 [Stack Overflow C++](https://stackoverflow.com/questions/tagged/c%2b%2b)

## Buon Divertimento! 🎮

Ricorda: La programmazione si impara facendo, non solo leggendo!
