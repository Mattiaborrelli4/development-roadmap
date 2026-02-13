# BigInt Library - Quick Reference

## Compilazione

### Compilare il programma principale:
```bash
gcc -Wall -Wextra -O2 -o bigint bigint.c main.c
./bigint          # Esegui test
./bigint -i       # Modalità interattiva
```

### Compilare gli esempi:
```bash
gcc -Wall -Wextra -O2 -o examples examples.c bigint.c
./examples
```

### Usare Makefile:
```bash
make              # Compila tutto
make test         # Compila ed esegui test
make interactive  # Modalità interattiva
make clean        # Pulisci file oggetto
```

## API Principale

### Creazione
```c
BigInt *a = bigint_create(1234567890L);          // Da long
BigInt *b = bigint_from_string("12345...");        // Da stringa
BigInt *c = bigint_copy(a);                       // Copia
bigint_free(a);                                   // Libera memoria
```

### Operazioni Aritmetiche
```c
BigInt *sum = bigint_add(a, b);           // a + b
BigInt *diff = bigint_subtract(a, b);      // a - b
BigInt *prod = bigint_multiply(a, b);      // a * b
BigInt *quot = bigint_divide(a, b);        // a / b (divisione intera)
BigInt *rem = bigint_mod(a, b);            // a % b
```

### Conversioni
```c
char *str = bigint_to_string(a);           // BigInt -> stringa
printf("%s\n", str);
free(str);
```

### Confronto
```c
int cmp = bigint_compare(a, b);    // -1: a<b, 0: a==b, 1: a>b
if (bigint_is_zero(a)) { ... }     // Verifica se è zero
```

### Output
```c
bigint_print(a);                    // Stampa su stdout
printf("Risultato: ");
bigint_print(result);
printf("\n");
```

## Esempi Rapidi

### Fattoriale
```c
BigInt *fact = bigint_create(1);
for (int i = 2; i <= 100; i++) {
    BigInt *n = bigint_create(i);
    BigInt *temp = bigint_multiply(fact, n);
    bigint_free(fact);
    bigint_free(n);
    fact = temp;
}
// Usa fact...
bigint_free(fact);
```

### Potenza
```c
BigInt *base = bigint_create(2);
BigInt *result = bigint_create(1);
for (int i = 0; i < 64; i++) {
    BigInt *temp = bigint_multiply(result, base);
    bigint_free(result);
    result = temp;
}
// result = 2^64
bigint_free(base);
bigint_free(result);
```

### Fibonacci
```c
BigInt *a = bigint_create(0);  // F(0)
BigInt *b = bigint_create(1);  // F(1)
for (int i = 2; i <= 100; i++) {
    BigInt *next = bigint_add(a, b);
    bigint_free(a);
    a = b;
    b = next;
}
// b = F(100)
bigint_free(a);
bigint_free(b);
```

## Note Importanti

1. **Gestione Memoria:** Tutte le funzioni che creano BigInt allocano memoria. È necessario chiamare `bigint_free()` per liberarla.

2. **Immutabilità:** Le operazioni non modificano gli operandi; creano nuovi BigInt.

3. **Divisione per Zero:** `bigint_divide()` e `bigint_mod()` restituiscono `NULL` se il divisore è zero.

4. **Parsing:** `bigint_from_string()` supporta:
   - Numeri positivi: `"123456"`
   - Numeri negativi: `"-123456"`
   - Segno esplicito: `"+123456"`
   - Zeri leading: `"000123"` → `123`

5. **Performance:**
   - Addizione: O(n)
   - Moltiplicazione: O(n²)
   - Divisione: O(n × m) - lenta per numeri grandi

## Troubleshooting

### Linker Errors
```bash
# Assicurati di includere bigint.c
gcc -o program program.c bigint.c
```

### Memory Leaks
Usa Valgrind o AddressSanitizer:
```bash
gcc -fsanitize=address -g -o program program.c bigint.c
./program
```

### Numeri Troppo Grandi
La libreria usa memoria heap. Se hai problemi:
- Controlla lo spazio disponibile
- Limita la dimensione delle operazioni
- Libera i BigInt temporanei immediatamente

## Struttura Interna

```
BigInt {
    char *digits;    // [0-9], little-endian (cifre invertite)
    size_t length;   // Numero di cifre
    int sign;        // 1 o -1
}
```

Esempio: `12345` → `digits=[5,4,3,2,1], length=5, sign=1`

## Riferimenti

- **bigint.h** - Dichiarazioni complete
- **bigint.c** - Implementazione
- **main.c** - Suite di test
- **examples.c** - Esempi avanzati
- **README.md** - Documentazione completa
