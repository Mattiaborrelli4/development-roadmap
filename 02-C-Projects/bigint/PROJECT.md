# C BigInt Library - Project Overview

## Descrizione del Progetto

Una libreria C completa per gestire numeri interi arbitrariamente grandi, superando le limitazioni dei tipi primitivi come `long` o `long long`. La libreria supporta operazioni aritmetiche fondamentali con numeri positivi e negativi di qualsiasi dimensione (limitata solo dalla memoria disponibile).

## Struttura del Progetto

```
bigint/
├── bigint.h          # Header file con definizioni e API
├── bigint.c          # Implementazione della libreria
├── main.c            # Suite di test completa (45 test)
├── examples.c        # Esempi di utilizzo avanzato
├── Makefile          # Build automation
├── README.md         # Documentazione completa
├── QUICKREF.md       # Quick reference guide
└── PROJECT.md        # Questo file
```

## Specifiche Tecniche

### Rappresentazione dei Dati
- **Formato:** Array dinamico di cifre decimali (0-9)
- **Ordine:** Little-endian (cifre invertite per facilitare operazioni)
- **Segno:** Gestito separatamente (+1 o -1)
- **Memoria:** Allocazione dinamica con realloc per ottimizzazione

### Algoritmi Implementati

| Operazione | Algoritmo | Complessità |
|-----------|-----------|-------------|
| Addizione | Schoolbook con carry | O(n) |
| Sottrazione | Schoolbook con borrow | O(n) |
| Moltiplicazione | Schoolbook (grade-school) | O(n²) |
| Divisione | Sottrazione successiva | O(n × m) |
| Modulo | Divisione + moltiplicazione | O(n × m) |

### Funzionalità Principali

1. **Creazione e Conversione**
   - `bigint_create(long)` - Da intero primitivo
   - `bigint_from_string(char*)` - Da stringa (supporta +/-)
   - `bigint_to_string(BigInt*)` - A stringa
   - `bigint_copy(BigInt*)` - Copia profonda

2. **Operazioni Aritmetiche**
   - `bigint_add(a, b)` - Addizione
   - `bigint_subtract(a, b)` - Sottrazione
   - `bigint_multiply(a, b)` - Moltiplicazione
   - `bigint_divide(a, b)` - Divisione intera
   - `bigint_mod(a, b)` - Modulo

3. **Confronto**
   - `bigint_compare(a, b)` - Confronto completo (-1, 0, 1)
   - `bigint_is_zero(a)` - Verifica zero

4. **I/O**
   - `bigint_print(a)` - Stampa su stdout
   - Gestione memoria con `bigint_free(a)`

## Test Suite

Il file `main.c` include 45 test completi:

| Categoria | Test | Stato |
|-----------|------|-------|
| Creazione/Conversione | 9 | ✓ Pass |
| Confronto | 7 | ✓ Pass |
| Addizione | 6 | ✓ Pass |
| Sottrazione | 5 | ✓ Pass |
| Moltiplicazione | 6 | ✓ Pass |
| Divisione | 5 | ✓ Pass |
| Modulo | 3 | ✓ Pass |
| Numeri Grandi | 4 | ✓ Pass |

**Totale:** 45/45 test passati (100%)

## Esempi Avanzati (examples.c)

1. **Fattoriale** - Calcolo di 50! e 100!
2. **Fibonacci** - Fibonacci(100) e Fibonacci(200)
3. **Potenza** - 2^64, 3^40 (esponenziazione veloce)
4. **MCD** - Massimo Comun Divisore (algoritmo di Euclide)
5. **Serie Geometrica** - Somma di serie
6. **Verifica Primalità** - Test naive per numeri primi

## Compilazione e Esecuzione

### Compilazione Standard
```bash
gcc -Wall -Wextra -O2 -o bigint bigint.c main.c
./bigint
```

### Con Makefile
```bash
make              # Compila
make test         # Compila + test
make interactive   # Modalità interattiva
make clean        # Pulisci
```

### Esempi
```bash
gcc -Wall -Wextra -O2 -o examples examples.c bigint.c
./examples
```

## Requisiti di Sistema

- **Compilatore:** GCC (MinGW su Windows) con supporto C99
- **OS:** Cross-platform (Windows, Linux, macOS)
- **Dipendenze:** Solo standard library (stdlib.h, stdio.h, string.h)

## Casi d'Uso

### Matematica
- Calcolo di fattoriali grandi
- Numeri di Fibonacci
- Potenze elevate
- Numeri primi

### Crittografia (Educativo)
- Operazioni modulari
- Esponenziazione modulare
- Algoritmi RSA base

### Calcolo Scientifico
- Precisione arbitraria
- Numeri interi overflow-safe
- Serie numeriche

## Limitazioni Attuali

1. **Performance:** Moltiplicazione O(n²) - lenta per numeri molto grandi
2. **Divisione:** Algoritmo naive - ottimizzabile con Knuth/DAC
3. **Input:** Solo base 10 (non supporta esadecimale/binario)
4. **Memoria:** Nessun limite massimo hardcoded (solo RAM)

## Miglioramenti Futuri

- [ ] Algoritmo Karatsuba per moltiplicazione O(n^1.585)
- [ ] Divisione ottimizzata (algoritmo di Knuth)
- [ ] Supporto per altre basi (hex, binary)
- [ ] Operazioni bitwise (AND, OR, XOR, shift)
- [ ] Radice quadrata intera
- [ ] GCD ottimizzato (algoritmo binario)
- [ ] Serializzazione binaria
- [ ] Benchmark suite

## File Chiave

### bigint.h (3.4 KB)
Interfaccia pubblica con commenti Doxygen. Definisce struct `BigInt` e tutte le funzioni API.

### bigint.c (12.2 KB)
Implementazione completa con funzioni helper interne. Include:
- Gestione dinamica memoria
- Algoritmi aritmetici
- Utilità di trimming/confronto

### main.c (16.2 KB)
Test suite con colori ANSI e macro per assertion. Include:
- 45 test distribuiti in 8 categorie
- Modalità interattiva per esperimenti
- Riepilogo colorato dei risultati

### examples.c (7.4 KB)
6 esempi completi dimostrativi con output formattato.

### README.md (9.4 KB)
Documentazione completa in italiano con:
- Guida API dettagliata
- Esempi di codice
- Spiegazione algoritmi
- Troubleshooting

## Metriche del Codice

| Metrica | Valore |
|---------|--------|
| Righe totali | ~850 |
| Funzioni | ~30 |
| API pubbliche | 15 |
| Test | 45 |
| Coverage | 100% funzioni API |
| Warning compilazione | 0 (con -Wall -Wextra) |

## Conclusione

Questo progetto dimostra una solida implementazione di una struttura dati per precisione arbitraria in C puro. La libreria è:
- **Funzionale:** Tutti i test passano
- **Documentata:** README + QUICKREF + commenti codice
- **Educativa:** Esempi e spiegazioni algoritmi
- **Manutenibile:** Codice pulito e strutturato
- **Portabile:** Standard C, cross-platform

## Risorse

- [Algoritmi Moltiplicazione](https://en.wikipedia.org/wiki/Multiplication_algorithm)
- [Arbitrary-Precision Arithmetic](https://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic)
- [GMP Library](https://gmplib.org/) - Riferimento professionale

---

**Autore:** Progetto educativo per portfolio
**Linguaggio:** C (C99 standard)
**Licenza:** MIT
**Anno:** 2025
