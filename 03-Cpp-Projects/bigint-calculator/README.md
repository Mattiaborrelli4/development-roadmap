# BigInt Calculator

## 📋 Descrizione

La **BigInt Calculator** è un progetto C++ che implementa una classe per gestire numeri interi arbitrariamente grandi, superando le limitazioni dei tipi primitivi del linguaggio (`int`, `long`, `long long`).

Il progetto è ideale per comprendere:
- L'**operator overloading** in C++
- La **gestione dinamica della memoria** con RAII
- Gli **algoritmi aritmetici** su base multi-cifra
- La **gestione del segno** in operazioni matematiche
- L'interazione con gli **stream** C++

## ✨ Caratteristiche

### Funzionalità Implementate

#### Operatori Aritmetici
- **Addizione** (`+`) : Somma di due BigInt
- **Sottrazione** (`-`) : Differenza tra due BigInt
- **Moltiplicazione** (`*`) : Prodotto con algoritmo schoolbook
- **Divisione** (`/`) : Divisione intera
- **Modulo** (`%`) : Resto della divisione
- **Menos unario** (`-`) : Inversione del segno

#### Operatori di Confronto
- `==` , `!=` : Uguaglianza e disuguaglianza
- `<` , `>` : Minore e maggiore
- `<=` , `>=` : Minore/uguale e maggiore/uguale

#### Operatori di Stream
- `<<` : Output verso ostream (es. `std::cout`)
- `>>` : Input da istream (es. `std::cin`)

#### Metodi di Conversione
- `toString()` : Conversione a stringa
- `toLong()` : Conversione a `long`
- `toInt()` : Conversione a `int`

#### Altri Metodi
- `absolute()` : Valore assoluto
- `isNegative()` : Verifica se il numero è negativo
- `isZero()` : Verifica se il numero è zero
- `numDigits()` : Numero di cifre

## 🏗️ Architettura Tecnica

### Rappresentazione Interna

Il numero è memorizzato utilizzando:
- **`std::vector<int>`** : Contiene le cifre decimali (0-9)
  - Le cifre sono memorizzate in **ordine inverso** (cifra meno significativa prima)
  - Questo facilita le operazioni aritmetiche con carry
- **`bool negative`** : Flag per indicare il segno

Esempio: il numero `12345` è memorizzato come:
```cpp
digits = {5, 4, 3, 2, 1}  // ordine inverso
negative = false
```

### Algoritmi Implementati

#### Addizione e Sottrazione
Algoritmo **schoolbook** O(n) che elabora le cifre una alla volta gestendo carry/borrow.

#### Moltiplicazione
Algoritmo **schoolbook** O(n×m) che simula la moltiplicazione manuale:
```cpp
    123
  × 456
  -----
    738   (123 × 6)
   615    (123 × 5, shiftato)
  492     (123 × 4, shiftato)
  -----
  56088
```

#### Divisione
Algoritmo **long division** che:
1. Costruisce il risultato cifra per cifra
2. Utilizza ripetute sottrazioni per ogni posizione
3. Complessità: O(n²) nel caso peggiore

## 📁 Struttura del Progetto

```
bigint-calculator/
├── bigint.h          # Dichiarazione della classe BigInt
├── bigint.cpp        # Implementazione dei metodi
├── main.cpp          # Suite di test e calcolatrice interattiva
└── README.md         # Questo file
```

## 🚀 Compilazione ed Esecuzione

### Requisiti
- Compilatore C++ che supporta **C++17** o superiore
- CMake (opzionale, per build avanzati)

### Compilazione Manuale

#### Linux / macOS (g++ / clang++)
```bash
g++ -std=c++17 -Wall -Wextra -O2 main.cpp bigint.cpp -o bigint_calc
```

#### Windows (MSVC)
```cmd
cl /std:c++17 /EHsc /W4 main.cpp bigint.cpp
```

#### Windows (MinGW)
```bash
g++ -std=c++17 -Wall -Wextra -O2 main.cpp bigint.cpp -o bigint_calc.exe
```

### Esecuzione
```bash
# Linux / macOS
./bigint_calc

# Windows
bigint_calc.exe
```

## 🧪 Esempi di Utilizzo

### Codice C++

```cpp
#include "bigint.h"
#include <iostream>

int main() {
    // Costruttori
    BigInt a(12345678901234567890LL);
    BigInt b("98765432109876543210");
    BigInt c = -100;

    // Operazioni aritmetiche
    BigInt sum = a + b;
    BigInt diff = a - b;
    BigInt prod = a * b;
    BigInt div = a / BigInt(10);
    BigInt mod = a % BigInt(7);

    // Operatori di confronto
    if (a > b) {
        std::cout << "a è maggiore di b\n";
    }

    // Operatori di stream
    std::cout << "a = " << a << "\n";
    std::cout << "a + b = " << sum << "\n";

    // Metodi di conversione
    std::string s = a.toString();
    long l = a.toLong();
    int i = a.toInt();

    // Metodi utili
    BigInt abs = a.absolute();
    bool neg = a.isNegative();
    size_t digits = a.numDigits();

    return 0;
}
```

### Calcolatrice Interattiva

Il programma include una calcolatrice interattiva:

```
>> 12345678901234567890 + 98765432109876543210
   = 111111111011111111100

>> 99999999999999999999 * 9
   = 899999999999999999991

>> 100000000000000000000 / 1000
   = 100000000000000000

>> q
Uscita dalla calcolatrice.
```

## 🧮 Esempi di Output

### Test Suite

All'esecuzione, il programma esegue automaticamente una suite di test completa:

```
============================================================
  TEST COSTRUTTORI
============================================================
Costruttore default (deve essere 0)                [PASSO]
Costruttore default - isZero()                     [PASSO]
Costruttore da long(12345)                         [PASSO]
...

============================================================
  TEST ADDIZIONE
============================================================
123 + 456 = 579                                    [PASSO]
123 + (-100) = 23                                  [PASSO]
...
```

## 📊 Complessità Algoritmica

| Operazione | Complessità Temporale | Complessità Spaziale |
|------------|----------------------|---------------------|
| Costruzione | O(n) | O(n) |
| Addizione | O(n) | O(n) |
| Sottrazione | O(n) | O(n) |
| Moltiplicazione | O(n×m) | O(n+m) |
| Divisione | O(n²) | O(n) |
| Modulo | O(n²) | O(n) |
| Confronto | O(n) | O(1) |

Dove `n` e `m` sono il numero di cifre degli operandi.

## 🔧 Estensioni Possibili

Il progetto può essere esteso con:

1. **Algoritmo Karatsuba** per moltiplicazione più efficiente (O(n^1.585))
2. **Operatori bitwise** (`&`, `|`, `^`, `~`, `<<`, `>>`)
3. **Potenza** (`operator^` o metodo `pow()`)
4. **Massimo Comun Divisore** (MCD) e **minimo comune multiplo**
5. **Conversioni da/a base binaria/esadecimale**
6. **Ottimizzazioni memoria** con cifre a 32/64 bit invece di decimali
7. **Serializzazione** per salvare/caricare BigInt da file

## 📚 Concetti C++ Dimostrati

- **Classi e Oggetti** : Incapsulamento di dati e comportamenti
- **Costruttori** : Default, da parametro, da stringa, di copia
- **Distruttore** : RAII per gestione risorse
- **Operator Overloading** : Aritmetico, di confronto, di stream
- **Gestione Eccezioni** : `std::invalid_argument`, `std::runtime_error`, `std::overflow_error`
- **STL Containers** : `std::vector`
- **STL Algorithms** : `std::max`, `std::reverse`
- **Friend Functions** : Per operatori di stream
- **Const Correctness** : Metodi const dove appropriato
- **References** : Passaggio per riferimento per efficienza

## 🐛 Gestione Errori

La classe gestisce diversi casi di errore:

- **Stringa non valida** : `std::invalid_argument`
- **Divisione per zero** : `std::runtime_error`
- **Overflow in conversioni** : `std::overflow_error`
- **Input fallito da stream** : Flag `failbit` impostato

## 👨‍💻 Autore

Developed by **Matti** 🚀

## 📄 Licenza

Questo progetto è fornito a scopo educativo. Sentiti libero di utilizzarlo, modificarlo e distribuirlo.

---

**Nota** : Questo progetto fa parte del portfolio "03-Cpp-Projects" e dimostra competenze avanzate nella programmazione C++ moderna.
