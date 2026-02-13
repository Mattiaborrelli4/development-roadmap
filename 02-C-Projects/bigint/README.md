# BigInt Library - Libreria C per Numeri Interi Arbitrariamente Grandi

Libreria C completa per gestire numeri interi di dimensione arbitraria, superando i limiti dei tipi primitivi come `long` o `long long`.

## Caratteristiche

- Numeri interi arbitrariamente grandi (solo limitati dalla memoria disponibile)
- Supporto completo per numeri positivi e negativi
- Operazioni aritmetiche di base: addizione, sottrazione, moltiplicazione, divisione, modulo
- Parsing da stringa e conversione a stringa
- Implementazione efficiente con array di cifre decimali
- Codice ben documentato e testato

## Struttura del BigInt

I numeri sono rappresentati usando la struttura `BigInt`:

```c
typedef struct {
    char *digits;    // Array di cifre decimali (0-9), ordine little-endian
    size_t length;   // Numero di cifre nel numero
    int sign;        // 1 = positivo, -1 = negativo
} BigInt;
```

### Little-Endian
Le cifre sono memorizzate in ordine inverso (little-endian):
- Il numero `12345` è memorizzato come `[5, 4, 3, 2, 1]`
- Questo facilita le operazioni aritmetiche con carry

## Compilazione

### Compilare il programma di test:
```bash
gcc -Wall -Wextra -O2 -o bigint bigint.c main.c
```

### Compilare solo la libreria:
```bash
gcc -Wall -Wextra -O2 -c bigint.c -o bigint.o
```

### Eseguire i test:
```bash
./bigint
```

### Modalità interattiva:
```bash
./bigint -i
```

## API

### Creazione e Distruzione

#### `BigInt* bigint_create(long n)`
Crea un BigInt da un `long`.

```c
BigInt *num = bigint_create(1234567890123456789L);
BigInt *neg = bigint_create(-42);
BigInt *zero = bigint_create(0);
```

#### `BigInt* bigint_from_string(const char *str)`
Crea un BigInt da una stringa. Supporta segno `+` e `-`.

```c
BigInt *big = bigint_from_string("123456789012345678901234567890");
BigInt *neg = bigint_from_string("-987654321");
```

#### `void bigint_free(BigInt *bi)`
Libera la memoria allocata per un BigInt.

```c
bigint_free(num);
```

#### `BigInt* bigint_copy(const BigInt *bi)`
Crea una copia di un BigInt.

```c
BigInt *copy = bigint_copy(original);
```

### Operazioni Aritmetiche

#### `BigInt* bigint_add(const BigInt *a, const BigInt *b)`
Restituisce un nuovo BigInt con la somma `a + b`.

```c
BigInt *result = bigint_add(a, b);
// a e b non vengono modificati
```

#### `BigInt* bigint_subtract(const BigInt *a, const BigInt *b)`
Restituisce un nuovo BigInt con la sottrazione `a - b`.

```c
BigInt *result = bigint_subtract(a, b);
```

#### `BigInt* bigint_multiply(const BigInt *a, const BigInt *b)`
Restituisce un nuovo BigInt con il prodotto `a * b`.
Usa l'algoritmo schoolbook O(n²).

```c
BigInt *result = bigint_multiply(a, b);
```

#### `BigInt* bigint_divide(const BigInt *a, const BigInt *b)`
Restituisce un nuovo BigInt con la divisione intera `a / b`.

```c
BigInt *quotient = bigint_divide(a, b);
// Divisione per zero restituisce NULL e stampa errore
```

#### `BigInt* bigint_mod(const BigInt *a, const BigInt *b)`
Restituisce un nuovo BigInt con il modulo `a % b`.

```c
BigInt *remainder = bigint_mod(a, b);
```

### Conversione e Confronto

#### `char* bigint_to_string(const BigInt *bi)`
Converte un BigInt in stringa. La stringa deve essere liberata dal chiamante.

```c
char *str = bigint_to_string(num);
printf("Numero: %s\n", str);
free(str);
```

#### `int bigint_compare(const BigInt *a, const BigInt *b)`
Confronta due BigInt.
- Restituisce `-1` se `a < b`
- Restituisce `0` se `a == b`
- Restituisce `1` se `a > b`

```c
int cmp = bigint_compare(a, b);
if (cmp < 0) {
    printf("a è minore di b\n");
}
```

#### `void bigint_print(const BigInt *bi)`
Stampa un BigInt su stdout.

```c
printf("Risultato: ");
bigint_print(result);
printf("\n");
```

#### `int bigint_is_zero(const BigInt *bi)`
Verifica se un BigInt è zero.

```c
if (bigint_is_zero(num)) {
    printf("Il numero è zero\n");
}
```

## Esempi di Utilizzo

### Esempio 1: Calcolo Base

```c
#include "bigint.h"
#include <stdio.h>

int main() {
    // Crea due numeri grandi
    BigInt *a = bigint_from_string("12345678901234567890");
    BigInt *b = bigint_from_string("98765432109876543210");

    // Somma
    BigInt *sum = bigint_add(a, b);
    char *sum_str = bigint_to_string(sum);
    printf("Somma: %s\n", sum_str);  // 111111111011111111100
    free(sum_str);

    // Moltiplicazione
    BigInt *prod = bigint_multiply(a, b);
    char *prod_str = bigint_to_string(prod);
    printf("Prodotto: %s\n", prod_str);
    free(prod_str);

    // Pulizia
    bigint_free(a);
    bigint_free(b);
    bigint_free(sum);
    bigint_free(prod);

    return 0;
}
```

### Esempio 2: Fattoriale

```c
BigInt* factorial(int n) {
    BigInt *result = bigint_create(1);
    BigInt *temp;

    for (int i = 2; i <= n; i++) {
        BigInt *factor = bigint_create(i);
        temp = bigint_multiply(result, factor);
        bigint_free(result);
        bigint_free(factor);
        result = temp;
    }

    return result;
}

int main() {
    BigInt *fact100 = factorial(100);
    char *fact_str = bigint_to_string(fact100);
    printf("100! = %s\n", fact_str);
    free(fact_str);
    bigint_free(fact100);

    return 0;
}
```

### Esempio 3: Fibonacci

```c
BigInt* fibonacci(int n) {
    if (n <= 0) return bigint_create(0);
    if (n == 1) return bigint_create(1);

    BigInt *a = bigint_create(0);
    BigInt *b = bigint_create(1);
    BigInt *temp, *next;

    for (int i = 2; i <= n; i++) {
        next = bigint_add(a, b);
        temp = b;
        b = next;
        a = temp;
    }

    bigint_free(a);
    return b;
}

int main() {
    BigInt *fib1000 = fibonacci(1000);
    char *fib_str = bigint_to_string(fib1000);
    printf("Fibonacci(1000) ha %d cifre\n", (int)strlen(fib_str));
    free(fib_str);
    bigint_free(fib1000);

    return 0;
}
```

## Algoritmi Implementati

### Addizione
- **Algoritmo:** Schoolbook con carry
- **Complessità:** O(n) dove n è il numero di cifre del numero più grande
- **Metodo:** Somma cifra per cifra con propagazione del carry

### Sottrazione
- **Algoritmo:** Schoolbook con borrow
- **Complessità:** O(n)
- **Metodo:** Sottrazione cifra per cifra con propagazione del borrow

### Moltiplicazione
- **Algoritmo:** Schoolbook (grade-school multiplication)
- **Complessità:** O(n²)
- **Metodo:** Moltiplicazione cifra per cifra con somma dei parziali

### Divisione
- **Algoritmo:** Sottrazione successiva (naive)
- **Complessità:** O(n × m) dove m è il quoziente
- **Nota:** Implementazione semplice ma lenta per numeri molto grandi

## Note di Implementazione

### Gestione della Memoria
- Tutte le funzioni che creano un BigInt allocano memoria dinamicamente
- È responsabilità del chiamante liberare la memoria con `bigint_free()`
- Le funzioni aritmetiche non modificano gli operandi, creano nuovi BigInt

### Gestione del Segno
- Il segno è gestito separatamente dalle cifre
- Le operazioni aritmetiche determinano il segno del risultato in base ai segni degli operandi
- Zero è sempre rappresentato con segno positivo

### Trim degli Zeri
- Dopo ogni operazione, gli zeri superflui vengono rimossi
- Questo mantiene le rappresentazioni canoniche

## Limitazioni

1. **Divisione:** L'implementazione attuale usa sottrazione successiva, che è lenta per numeri molto grandi. Una versione ottimizzata userebbe l'algoritmo di Knuth o long division.

2. **Performance:** La moltiplicazione è O(n²). Per numeri estremamente grandi, Karatsuba (O(n^1.585)) o FFT (O(n log n)) sarebbero più efficienti.

3. **Input:** La funzione `bigint_from_string` accetta solo cifre decimali. Non supporta altre basi (esadecimale, binario).

4. **Overflow:** Non c'è protezione contro l'esaurimento della memoria per numeri estremamente grandi.

## Miglioramenti Futuri

- [ ] Implementare algoritmo di Karatsuba per moltiplicazione
- [ ] Implementare divisione più efficiente (algoritmo di Knuth)
- [ ] Supporto per altre basi (esadecimale, binario)
- [ ] Operazioni bitwise (AND, OR, XOR, shift)
- [ ] Funzioni matematiche avanzate (potenza, radice, GCD)
- [ ] Serializzazione/deserializzazione
- [ ] Unit test framework più robusto
- [ ] Benchmark delle performance

## Test Suite

Il file `main.c` include una suite di test completa con:
- Test di creazione e conversione
- Test di confronto
- Test di addizione (inclusi casi edge)
- Test di sottrazione (inclusi casi edge)
- Test di moltiplicazione
- Test di divisione
- Test di modulo
- Test con numeri molto grandi

Per eseguire i test:
```bash
./bigint
```

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Sentiti libero di usarlo e modificarlo come desideri.

## Autore

Creato come progetto educativo per dimostrare l'implementazione di una struttura dati per numeri interi arbitrariamente grandi in C.

## Risorse

- [Algoritmi per moltiplicazione di grandi interi](https://en.wikipedia.org/wiki/Multiplication_algorithm#Karatsuba_multiplication)
- [Arbitrary-precision arithmetic](https://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic)
- [GMP Library](https://gmplib.org/) - Libreria professionale per precisione arbitraria
