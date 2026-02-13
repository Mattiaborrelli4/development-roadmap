# 🚀 Guida Rapida - BigInt Calculator

## Compilazione Veloce

### Windows (MinGW)
```bash
g++ -std=c++17 main.cpp bigint.cpp -o bigint_calc.exe
```

### Linux / macOS
```bash
g++ -std=c++17 main.cpp bigint.cpp -o bigint_calc
```

### Con Make
```bash
make
```

### Con CMake
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

## Esecuzione dei Test

```bash
# Windows
bigint_calc.exe

# Linux/macOS
./bigint_calc
```

Rispondi `n` quando ti chiede della calcolatrice interattiva per vedere solo i test.

## Esempio di Utilizzo nel Codice

```cpp
#include "bigint.h"
#include <iostream>

int main() {
    BigInt a("12345678901234567890");
    BigInt b("98765432109876543210");

    std::cout << "Somma: " << (a + b) << "\n";
    std::cout << "Differenza: " << (a - b) << "\n";
    std::cout << "Prodotto: " << (a * b) << "\n";
    std::cout << "Divisione: " << (a / BigInt(10)) << "\n";

    return 0;
}
```

## Caratteristiche Principali

✓ **Numeri arbitrariamente grandi** - nessun limite di dimensione
✓ **Tutti gli operatori aritmetici** - +, -, *, /, %
✓ **Operatori di confronto** - ==, !=, <, >, <=, >=
✓ **Gestione del segno** - numeri positivi e negativi
✓ **Conversioni** - toString(), toLong(), toInt()
✓ **Operatori I/O** - << e >> per stream

## Troubleshooting

### Errore: "undefined reference"
Verifica di compilare **tutti** i file .cpp:
```bash
g++ -std=c++17 main.cpp bigint.cpp -o bigint_calc
```

### Errore: "C++17 required"
Assicurati che il compilatore supporti C++17:
```bash
g++ --version  # deve essere 7.0 o superiore
```

### Warning: "unused parameter"
Normali, sono dovuti ai parametri non usati nei metodi helper.

## File del Progetto

- `bigint.h` - Header con dichiarazione classe BigInt
- `bigint.cpp` - Implementazione metodi BigInt
- `main.cpp` - Test suite + calcolatrice interattiva
- `README.md` - Documentazione completa
- `Makefile` - Build automation per GNU Make
- `CMakeLists.txt` - Build configuration per CMake
- `.gitignore` - File da ignorare in Git

---

Per maggiori dettagli, vedi `README.md` completo.
