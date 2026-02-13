# Guida Rapida - String Library Reference

## Compilazione Rapida

```bash
# Compila e esegui
gcc test_stringlib.c stringlib.c -o test && ./test

# Con Makefile
make test
```

## Sintassi Veloce

| Funzione | Scopo | Esempio |
|----------|-------|---------|
| `strlen(s)` | Lunghezza stringa | `size_t n = stringlib_strlen("ciao");` |
| `strcpy(d,s)` | Copia stringa | `stringlib_strcpy(buf, "test");` |
| `strcat(d,s)` | Concatena | `stringlib_strcat(buf, " aggiunta");` |
| `strcmp(s1,s2)` | Confronta | `if (stringlib_strcmp(a, b) == 0)` |
| `strchr(s,c)` | Trova carattere | `char *p = stringlib_strchr(s, 'a');` |
| `strstr(s,sub)` | Trova sottostringa | `char *p = stringlib_strstr(s, "test");` |
| `strdup(s)` | Duplica (malloc) | `char *copy = stringlib_strdup(s);` |
| `strlcpy(d,s,n)` | Copia sicura | `stringlib_strlcpy(buf, src, sizeof(buf));` |
| `strlcat(d,s,n)` | Concat sicura | `stringlib_strlcat(buf, src, sizeof(buf));` |

## Pattern Comuni

### 1. Leggere stringhe in sicurezza

```c
char buffer[100];
stringlib_strlcpy(buffer, user_input, sizeof(buffer));
```

### 2. Concatenare multiple stringhe

```c
char result[256] = "";
stringlib_strcat(result, "Parte1");
stringlib_strcat(result, " ");
stringlib_strcat(result, "Parte2");
```

### 3. Cercare e sostituire

```c
char *pos = stringlib_strchr(text, 'a');
if (pos != NULL) {
    *pos = 'A';  // Sostituisci
}
```

### 4. Parsare token

```c
char *line = "nome,cognome,eta";
char *comma = stringlib_strchr(line, ',');
if (comma != NULL) {
    *comma = '\0';
    char *nome = line;
    char *cognome = comma + 1;
}
```

## Pitfalls da Evitare

| Problema | Soluzione |
|----------|-----------|
| Buffer overflow | Usa `strlcpy/strlcat` |
| Memory leak | Ricorda `free()` dopo `strdup()` |
| NULL pointer | Controlla sempre i return |
| Dangling pointer | Setta a `NULL` dopo `free()` |

## Dimensionamento Buffer

```c
// Copia
char dest[strlen(src) + 1];  // +1 per '\0'

// Concatenazione
char dest[strlen(s1) + strlen(s2) + 1];

// Sicuro (preferito)
char dest[256];
strlcpy(dest, src, sizeof(dest));
```

## Cheat Sheet Puntatori

```c
char *p = str;     // p punta a str[0]
*p                 // Valore di str[0]
p[0]               // Equivalente a *p
p++                // Avanza a str[1]
*(p+1)             // Equivalente a p[1]
p - str            // Distanza/indice
```

## Debug Tips

```c
// Stampa indirizzo memoria
printf("Indirizzo: %p\n", (void *)ptr);

// Stampa carattere e codice ASCII
printf("Carattere: '%c' (ASCII: %d)\n", c, c);

// Calcola differenza puntatori
ptrdiff_t diff = p2 - p1;
printf("Distanza: %td caratteri\n", diff);
```

## Test Quick Check

```bash
# Compila con tutti i warning
gcc -Wall -Wextra test_stringlib.c stringlib.c -o test

# Esegui
./test

# Dovresti vedere 10 sezioni di test con [OK]
```

## Mantra da Ricordare

1. **Ogni stringa C finisce con `\0`**
2. **I buffer hanno dimensione fissa**
3. **I puntatori sono potenti ma pericolosi**
4. **Free tutto ciò che malloc**
5. **Controlla sempre i return value**

---

Per dettagli completi: vedi `README.md`
Per codice: vedi i commenti in `stringlib.c`
