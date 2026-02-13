# Libreria di Manipolazione Stringhe in C

Una libreria educativa per la manipolazione delle stringhe in C, progettata per studenti universitari che desiderano comprendere profondamente i puntatori e la gestione della memoria.

## Indice

- [Descrizione](#descrizione)
- [Caratteristiche](#caratteristiche)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Documentazione delle Funzioni](#documentazione-delle-funzioni)
- [Concetti Chiave](#concetti-chiave)
- [Esempi](#esempi)
- [Compilazione](#compilazione)
- [Test](#test)
- [Note di Sicurezza](#note-di-sicurezza)
- [Risorse](#risorse)

## Descrizione

Questa libreria implementa le funzioni fondamentali per la manipolazione delle stringhe in C partendo da zero. Ogni funzione include commenti dettagliati che spiegano:

- Come funzionano i puntatori
- Come la memoria viene gestita
- Quali sono le insidie comuni da evitare
- Quali sono le best practices

L'obiettivo e fornire una base solida per comprendere non solo COME usare le stringhe, ma anche PERCHE funzionano in quel modo.

## Caratteristiche

Implementazioni originali di:

- `stringlib_strlen` - Calcola la lunghezza di una stringa
- `stringlib_strcpy` - Copia una stringa
- `stringlib_strcat` - Concatena due stringhe
- `stringlib_strlcpy` - Copia sicura con limite
- `stringlib_strlcat` - Concatenazione sicura con limite
- `stringlib_strcmp` - Confronta due stringhe
- `stringlib_strchr` - Cerca un carattere
- `stringlib_strstr` - Cerca una sottostringa
- `stringlib_strdup` - Duplica una stringa

## Prerequisiti

- Compilatore C (GCC, Clang, MSVC, o qualsiasi compilatore compatibile C89/C90)
- Conoscenza base di C (variabili, funzioni, cicli)
- Desiderio di imparare i puntatori e la gestione della memoria

## Installazione

1. Clona o scarica questo repository
2. Naviga nella cartella `string-library/`
3. Tutti i file sorgente sono già pronti all'uso

Non sono necessarie librerie esterne o dipendenze!

## Utilizzo

### Includere la Libreria

Nel tuo codice C:

```c
#include "stringlib.h"
```

### Esempio Base

```c
#include <stdio.h>
#include "stringlib.h"

int main(void) {
    char dest[50];
    char *src = "Hello, World!";

    // Calcola lunghezza
    size_t len = stringlib_strlen(src);
    printf("Lunghezza: %zu\n", len);

    // Copia stringa
    stringlib_strcpy(dest, src);
    printf("Copiata: %s\n", dest);

    // Concatenazione
    stringlib_strcat(dest, " - C Programming");
    printf("Concatenata: %s\n", dest);

    return 0;
}
```

## Documentazione delle Funzioni

### `size_t stringlib_strlen(const char *str)`

Calcola la lunghezza di una stringa contando i caratteri fino al terminatore `\0`.

**Parametri:**
- `str`: Puntatore alla stringa da misurare

**Ritorna:**
- Lunghezza della stringa (escluso il terminatore)

**Esempio:**
```c
char *text = "Hello";
size_t len = stringlib_strlen(text);  // len = 5
```

**Concetti Chiave:**
- Uso dei puntatori per attraversare un array
- Il terminatore `\0` segna la fine della stringa
- Complessita: O(n)

---

### `char *stringlib_strcpy(char *dest, const char *src)`

Copia una stringa da `src` a `dest`, incluso il terminatore.

**Parametri:**
- `dest`: Buffer di destinazione (DEVE avere abbastanza spazio!)
- `src`: Stringa sorgente da copiare

**Ritorna:**
- Puntatore a `dest`

**Esempio:**
```c
char buffer[20];
stringlib_strcpy(buffer, "Test");  // buffer = "Test"
```

**WARNING:**
- Devi garantire che `dest` abbia almeno `strlen(src) + 1` byte
- Overflow del buffer = bug di sicurezza grave!

---

### `char *stringlib_strcat(char *dest, const char *src)`

Aggiunge `src` alla fine di `dest`.

**Parametri:**
- `dest`: Stringa di destinazione (DEVE avere abbastanza spazio!)
- `src`: Stringa da aggiungere

**Ritorna:**
- Puntatore a `dest`

**Esempio:**
```c
char buffer[50] = "Hello ";
stringlib_strcat(buffer, "World");  // buffer = "Hello World"
```

**Spazio Necessario:**
```c
strlen(dest) + strlen(src) + 1  // +1 per il terminatore
```

---

### `size_t stringlib_strlcpy(char *dest, const char *src, size_t n)`

Versione SICURA di `strcpy` con limite di caratteri.

**Parametri:**
- `dest`: Buffer di destinazione
- `src`: Stringa sorgente
- `n`: Dimensione del buffer dest

**Ritorna:**
- Lunghezza della stringa sorgente (utile per detectare troncamenti)

**Vantaggi:**
- Previene buffer overflow
- Garantisce terminazione corretta
- Ritorna la lunghezza totale per verificare troncamenti

**Esempio:**
```c
char small[5];
size_t total = stringlib_strlcpy(small, "Very Long String", 5);
if (total > 4) {
    printf("Stringa troncata!\n");
}
```

---

### `size_t stringlib_strlcat(char *dest, const char *src, size_t n)`

Versione SICURA di `strcat` con limite del buffer.

**Parametri:**
- `dest`: Stringa di destinazione
- `src`: Stringa da aggiungere
- `n`: Dimensione totale del buffer dest

**Ritorna:**
- Lunghezza totale desiderata della stringa

**Esempio:**
```c
char buffer[10] = "Hi";
stringlib_strlcat(buffer, ", World!", 10);
// Buffer troppo piccolo, nessun overflow ma troncamento
```

---

### `int stringlib_strcmp(const char *s1, const char *s2)`

Confronta due stringhe lessicograficamente (alfabeticamente).

**Parametri:**
- `s1`: Prima stringa
- `s2`: Seconda stringa

**Ritorna:**
- `0` se le stringhe sono uguali
- `< 0` se `s1` viene prima di `s2`
- `> 0` se `s1` viene dopo `s2`

**Esempio:**
```c
if (stringlib_strcmp("apple", "banana") < 0) {
    printf("apple viene prima di banana\n");
}
```

**Nota:**
Il confronto e basato sui valori ASCII dei caratteri.

---

### `char *stringlib_strchr(const char *str, int c)`

Cerca un carattere in una stringa.

**Parametri:**
- `str`: Stringa in cui cercare
- `c`: Carattere da trovare

**Ritorna:**
- Puntatore al carattere trovato
- `NULL` se il carattere non esiste

**Esempio:**
```c
char *text = "Hello, World!";
char *pos = stringlib_strchr(text, 'W');
if (pos != NULL) {
    printf("Trovato alla posizione: %ld\n", pos - text);
}
```

---

### `char *stringlib_strstr(const char *haystack, const char *needle)`

Cerca una sottostringa in una stringa.

**Parametri:**
- `haystack`: Stringa in cui cercare
- `needle`: Sottostringa da trovare

**Ritorna:**
- Puntatore all'inizio della sottostringa trovata
- `NULL` se non trovata

**Esempio:**
```c
char *text = "Programming in C";
char *found = stringlib_strstr(text, "gram");
if (found != NULL) {
    printf("Trovato: %s\n", found);  // Stampa "gramming in C"
}
```

---

### `char *stringlib_strdup(const char *str)`

Duplica una stringa allocando nuova memoria.

**Parametri:**
- `str`: Stringa da duplicare

**Ritorna:**
- Puntatore alla nuova stringa
- `NULL` se l'allocazione fallisce

**IMPORTANTE:**
Devi chiamare `free()` sul risultato quando hai finito!

**Esempio:**
```c
char *original = "Test";
char *duplicate = stringlib_strdup(original);

// Usa duplicate...
printf("%s\n", duplicate);

// Libera la memoria
free(duplicate);
```

## Concetti Chiave

### 1. Le Stringhe in C

```c
char str[] = "Hello";
```

In memoria:
```
Indirizzo: 1000  1001  1002  1003  1004  1005
Valore:     'H'   'e'   'l'   'l'   'o'   '\0'
```

- Ogni carattere occupa 1 byte
- La stringa e terminata da `\0` (valore 0)
- La lunghezza "logica" e 5, ma occupa 6 byte in memoria

### 2. I Puntatori

```c
char *ptr = str;  // ptr punta all'indirizzo 1000
ptr++;            // ptr ora punta all'indirizzo 1001
*ptr = 'a';       // Modifica il carattere a 1001
```

**Visualizzazione:**

```
Array:      ['H']['e']['l']['l']['o']['\0']
Indirizzo:  1000 1001 1002 1003 1004 1005
                    ↑
                   ptr (dopo ptr++)
```

### 3. Dereferenziazione

```c
char x = *ptr;      // Legge il valore puntato
*ptr = 'A';         // Scrive il valore puntato
```

`*ptr` = "vai all'indirizzo ptr e prendi/scrivi il valore"

### 4. Aritmetica dei Puntatori

```c
ptr + 1  // Avanza di sizeof(char) byte = 1 byte
ptr + 5  // Avanza di 5 byte
```

Per array di altri tipi:
```c
int *arr = malloc(5 * sizeof(int));
arr + 1  // Avanza di sizeof(int) byte = 4 byte (di solito)
```

### 5. Memoria Dinamica

```c
char *str = malloc(100);  // Alloca 100 byte
// ... usa str ...
free(str);                // LIBERA SEMPRE la memoria!
```

**Regole d'oro:**
- Ogni `malloc()` deve avere un `free()`
- Mai usare memoria dopo `free()`
- Controlla sempre se `malloc()` ritorna `NULL`

## Esempi

### Esempio 1: Analisi di una Stringa

```c
char *text = "Programmazione";

// Conta vocali
int vowels = 0;
for (size_t i = 0; i < stringlib_strlen(text); i++) {
    char c = text[i];
    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
        vowels++;
    }
}
printf("Vocali: %d\n", vowels);
```

### Esempio 2: Inversione Stringa

```c
void reverse(char *str) {
    size_t len = stringlib_strlen(str);
    for (size_t i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

char text[] = "Hello";
reverse(text);  // text = "olleH"
```

### Esempio 3: Parsing di Stringhe

```c
char sentence[] = "Questa e' una frase";
char *word = sentence;

while (*word != '\0') {
    char *space = stringlib_strchr(word, ' ');

    if (space != NULL) {
        *space = '\0';          // Termina la parola
        printf("Parola: %s\n", word);
        word = space + 1;       // Prossima parola
    } else {
        printf("Parola: %s\n", word);
        break;
    }
}
```

### Esempio 4: Costruzione di Stringhe

```c
char full_name[100];
char first[] = "Mario";
char last[] = "Rossi";

stringlib_strcpy(full_name, first);      // "Mario"
stringlib_strcat(full_name, " ");        // "Mario "
stringlib_strcat(full_name, last);       // "Mario Rossi"

printf("Nome completo: %s\n", full_name);
```

## Compilazione

### Linux / macOS

```bash
gcc -Wall -Wextra -std=c99 test_stringlib.c stringlib.c -o test_stringlib
```

### Windows (MinGW)

```bash
gcc -Wall -Wextra -std=c99 test_stringlib.c stringlib.c -o test_stringlib.exe
```

### Spiegazione Flags:

- `-Wall`: Abilita tutti i warning principali
- `-Wextra`: Abilita warning extra
- `-std=c99`: Usa standard C99 (supporto for loop e dichiarazioni mid-function)
- `-o`: Specifica il nome dell'output

### Creazione di una Libreria Statica

```bash
# Compila l'oggetto
gcc -c stringlib.c -o stringlib.o

# Crea l'archivio
ar rcs libstringlib.a stringlib.o

# Usalo nei tuoi progetti
gcc my_program.c -L. -lstringlib -o my_program
```

## Test

Esegui il programma di test completo:

```bash
./test_stringlib        # Linux/Mac
test_stringlib.exe      # Windows
```

Il programma dimostra:

1. Uso di `strlen` con varie stringhe
2. Copia e concatenazione
3. Funzioni di sicurezza
4. Confronto tra stringhe
5. Ricerca di caratteri e sottostringhe
6. duplicazione di stringhe
7. Dimostrazioni sui puntatori
8. Esempio pratico di parser CSV

Output atteso:
```
╔════════════════════════════════════════════════╗
║   LIBRERIA STRINGHE - PROGRAMMA DI TEST       ║
║   Implementazione didattica in C              ║
╚════════════════════════════════════════════════╝

==============================================
TEST 1: stringlib_strlen
==============================================
Stringa: "" -> Lunghezza: 0
...

Tutti i test completati con successo!
```

## Note di Sicurezza

### Buffer Overflow

Il pericolo principale nella manipolazione delle stringhe:

```c
// DANGER! Overflow del buffer
char small[5];
stringlib_strcpy(small, "This is way too long");  // CRASH!

// CORRETTO
char small[5];
stringlib_strlcpy(small, "This is way too long", 5);  // Troncato ma sicuro
```

### Memory Leaks

Dimenticare di liberare la memoria:

```c
// WRONG - Memory leak!
char *str = stringlib_strdup("Test");
// ... usa str ...
// Nessun free!

// CORRETTO
char *str = stringlib_strdup("Test");
// ... usa str ...
free(str);
```

### NULL Pointer Dereference

```c
// WRONG - Crash se str e NULL
size_t len = stringlib_strlen(str);  // Non controlla NULL

// CORRETTO - La nostra funzione controlla
if (str != NULL) {
    size_t len = stringlib_strlen(str);
}
```

### Use After Free

```c
// WRONG - Usa memoria dopo liberarla
char *str = stringlib_strdup("Test");
free(str);
printf("%s\n", str);  // UNDEFINED BEHAVIOR!

// CORRETTO
char *str = stringlib_strdup("Test");
printf("%s\n", str);
free(str);
str = NULL;  // Buona pratica
```

## Risorse

### Libri Consigliati

1. **"The C Programming Language"** - Kernighan & Ritchie
   - La bibbia del C, scritto dai creatori del linguaggio

2. **"C Programming: A Modern Approach"** - K.N. King
   - Eccellente per studenti, molto chiaro

3. **"Pointers on C"** - Kenneth Reek
   - Focus specifico sui puntatori

### Online Risorse

- [C Programming Reference](https://en.cppreference.com/w/c)
- [Learn C.org](https://www.learn-c.org/)
- [C FAQ](http://c-faq.com/)

### Esercizi Consigliati

Pratica con questi esercizi per巩固 la comprensione:

1. Implementa una funzione `str_reverse` che inverte una stringa
2. Crea `str_replace` che sostituisce tutte le occorrenze di un carattere
3. Scrivi `str_trim` che rimuove spazi all'inizio e alla fine
4. Implementa `str_split` che divide una stringa in un array
5. Crea `str_to_upper` e `str_to_lower` per cambio maiuscolo/minuscolo

## Conclusione

Questa libreria e un punto di partenza per comprendere le basi della manipolazione delle stringhe in C. Le funzioni qui implementate sono simili a quelle della standard library, ma con commenti educativi dettagliati.

Ricorda:
- I puntatori sono potenti ma pericolosi
- La gestione della memoria richiede attenzione
- La sicurezza e piu importante delle prestazioni
- Leggere e comprendere il codice e fondamentale

Buon studio e buon coding in C!

---

**Autore:** Progetto Didattico
**Target:** Studenti Universitari
**Linguaggio:** C (ASCII)
**Anno:** 2024

Per domande o suggerimenti, consulta il tuo insegnante o la documentazione ufficiale del C.
