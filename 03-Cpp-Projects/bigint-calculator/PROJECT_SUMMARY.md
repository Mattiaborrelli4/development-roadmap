# 📊 Riepilogo Progetto - BigInt Calculator

## Panoramica

**Progetto**: BigInt Calculator
**Linguaggio**: C++17+
**Autore**: Matti
**Data**: Febbraio 2025
**Posizione**: `03-Cpp-Projects/bigint-calculator/`

## 📦 Componenti del Progetto

### File Sorgente

| File | Righe | Descrizione |
|------|-------|-------------|
| `bigint.h` | ~190 | Dichiarazione classe BigInt con documentazione Doxygen |
| `bigint.cpp` | ~380 | Implementazione completa algoritmi aritmetici |
| `main.cpp` | ~340 | Suite di test + calcolatrice interattiva |
| **Totale** | **~910** | Righe di codice C++ |

### File di Supporto

- `README.md` - Documentazione completa in italiano
- `GUIDE_RAPIDA.md` - Guida rapida per avvio veloce
- `Makefile` - Build automation GNU Make
- `CMakeLists.txt` - Configurazione CMake cross-platform
- `.gitignore` - File da ignorare in version control

## ✨ Funzionalità Implementate

### Operatori Aritmetici
- ✓ Addizione (`+`)
- ✓ Sottrazione (`-`)
- ✓ Moltiplicazione (`*`)
- ✓ Divisione intera (`/`)
- ✓ Modulo (`%`)
- ✓ Menos unario (negazione)

### Operatori di Confronto
- ✓ Uguaglianza (`==`, `!=`)
- ✓ Relazionali (`<`, `>`, `<=`, `>=`)

### I/O Stream
- ✓ Output operator (`<<`)
- ✓ Input operator (`>>`)

### Conversioni
- ✓ `toString()` - Conversione a stringa
- ✓ `toLong()` - Conversione a long con overflow check
- ✓ `toInt()` - Conversione a int con overflow check

### Metodi Utili
- ✓ `absolute()` - Valore assoluto
- ✓ `isNegative()` - Verifica segno negativo
- ✓ `isZero()` - Verifica se zero
- ✓ `numDigits()` - Conta cifre

## 🏗️ Architettura Tecnica

### Rappresentazione Interna
```cpp
std::vector<int> digits;  // Cifre 0-9, ordine inverso
bool negative;            // Flag segno
```

### Algoritmi

| Operazione | Algoritmo | Complessità |
|------------|-----------|-------------|
| Addizione | Schoolbook con carry | O(n) |
| Sottrazione | Schoolbook con borrow | O(n) |
| Moltiplicazione | Schoolbook O(n×m) | O(n×m) |
| Divisione | Long division | O(n²) |
| Modulo | Division + sottrazione | O(n²) |

## 🧪 Testing

### Suite di Test Completa
- **11 categorie** di test
- **60+ casi** di test individuali
- **100% pass rate** su tutte le funzionalità

### Test Categories
1. Costruttori (default, long, string, copy)
2. Addizione (positivi, negativi, misti)
3. Sottrazione
4. Moltiplicazione
5. Divisione intera
6. Modulo
7. Menos unario
8. Operatori di confronto
9. Conversioni
10. Metodi utility
11. Stream I/O

### Calcolatrice Interattiva
Modalità interattiva per testare espressioni:
```
>> 12345678901234567890 + 98765432109876543210
   = 111111111011111111100
```

## 🎯 Concetti C++ Dimostrati

### OOP
- Classi e oggetti
- Incapsulamento (private/public)
- Costruttori multipli
- Distruttore (RAII)
- Copia e assegnazione

### Operator Overloading
- Aritmetici binari (+, -, *, /, %)
- Unario (-)
- Confronto (==, !=, <, >, <=, >=)
- Stream (<<, >>)

### Gestione Errori
- `std::invalid_argument`
- `std::runtime_error`
- `std::overflow_error`

### STL
- `std::vector` - Container dinamico
- `std::string` - Manipolazione stringhe
- `std::ostream`/`std::istream` - I/O
- `std::reverse`, `std::max` - Algoritmi

### Best Practices
- Const correctness
- Reference passing per efficienza
- Rule of Three (copy ctor, assignment, dtor)
- Documentazione Doxygen

## 📊 Statistiche

| Metrica | Valore |
|---------|--------|
| Righe di codice | ~910 |
| Righe documentazione | ~350 |
| Numero classi | 1 |
| Metodi pubblici | 25+ |
| Operatori overload | 15 |
| Test cases | 60+ |
| Tasso di successo test | 100% |

## 🚀 Comandi Utili

### Compilazione
```bash
g++ -std=c++17 -Wall -Wextra -O2 main.cpp bigint.cpp -o bigint_calc
```

### Esecuzione Test
```bash
./bigint_calc        # Rispondi 'n' per solo test
```

### Calcolatrice Interattiva
```bash
./bigint_calc        # Rispondi 's' per modalità interattiva
```

### Build con Make
```bash
make run
```

### Build con CMake
```bash
mkdir build && cd build
cmake .. && cmake --build .
./bigint_calc
```

## 🎓 Punti Didattici

Questo progetto è eccellente per imparare:
1. **Operator Overloading** - Capire come C++ permette di ridefinire operatori
2. **Gestione Memoria** - RAII con std::vector
3. **Algoritmi** - Implementazione algoritmi aritmetici base
4. **Eccezioni** - Gestione errori robusta
5. **Design OOP** - Strutturazione classe completa
6. **Testing** - Scrittura suite di test completa

## 🔮 Possibili Estensioni

1. **Algoritmo Karatsuba** per moltiplicazione O(n^1.585)
2. **Operatori bitwise** (&, |, ^, ~, <<, >>)
3. **Potenza** (fast exponentiation)
4. **MCD/mcm** (Euclide, Stein)
5. **Conversioni base** (binario, hex, octal)
6. **Ottimizzazioni** (cifre 32-bit invece di decimali)
7. **Serializzazione** (save/load da file)

## 📝 Note Tecniche

### Scelte Design
- **Rappresentazione inversa** delle cifre per efficienza carry/borrow
- **Separazione** tra valore assoluto e segno per semplicità algoritmi
- **Long division** invece di Newton-Raphson per chiarezza didattica

### Limitazioni Note
- Moltiplicazione O(n²) - può essere migliorata con Karatsuba
- Divisione O(n²) - accettabile per didattica, ottimizzabile
- Solo base 10 - per performance usare base 2^32

## ✅ Checklist Progetto

- [x] Classe BigInt completa
- [x] Tutti operatori aritmetici
- [x] Tutti operatori confronto
- [x] Stream I/O
- [x] Conversioni da/a stringa
- [x] Gestione segno
- [x] Error handling completo
- [x] Suite di test completa
- [x] Calcolatrice interattiva
- [x] Documentazione italiana
- [x] Makefile
- [x] CMakeLists.txt
- [x] README.md dettagliato
- [x] .gitignore

---

**Stato**: ✅ COMPLETO
**Test**: ✅ 100% PASSING
**Documentazione**: ✅ ITALIANO COMPLETO
