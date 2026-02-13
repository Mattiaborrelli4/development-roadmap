/**
 * ================================================
 * TEST_STRINGLIB.C - Programma di Test
 * ================================================
 *
 * Questo programma dimostra l'uso di tutte le funzioni
 * della libreria stringlib con esempi pratici.
 *
 * Compilazione:
 *   gcc test_stringlib.c stringlib.c -o test_stringlib
 *
 * Esecuzione:
 *   ./test_stringlib (Linux/Mac)
 *   test_stringlib.exe (Windows)
 */

#include <stdio.h>
#include <stdlib.h>
#include "stringlib.h"

/**
 * Funzione helper per stampare separatori visivi
 */
void print_separator(title)
    const char *title;
{
    printf("\n");
    printf("==============================================\n");
    printf("%s\n", title);
    printf("==============================================\n");
}

/**
 * Funzione helper per visualizzare il risultato dei test
 */
void print_test_result(test_name, passed)
    const char *test_name;
    int passed;
{
    printf("[ %s ] %s\n", passed ? "OK" : "FAIL", test_name);
}

/**
 * ============================================
 * TEST 1: Dimostrazione stringlib_strlen
 * ============================================
 */
void test_strlen(void)
{
    char *test_strings[] = {
        "",
        "Hello",
        "Programming in C",
        "1234567890"
    };
    int num_tests;
    int i;
    size_t len;
    size_t null_len;

    print_separator("TEST 1: stringlib_strlen");

    num_tests = sizeof(test_strings) / sizeof(test_strings[0]);

    for (i = 0; i < num_tests; i++) {
        len = stringlib_strlen(test_strings[i]);
        printf("Stringa: \"%s\" -> Lunghezza: %lu\n",
               test_strings[i], (unsigned long)len);
    }

    /*
     * TEST NULL POINTER:
     * Dimostriamo che la funzione gestisce puntatori NULL
     */
    printf("\nTest con NULL: ");
    null_len = stringlib_strlen(NULL);
    printf("Lunghezza stringa NULL = %lu\n", (unsigned long)null_len);
}

/**
 * ============================================
 * TEST 2: Dimostrazione stringlib_strcpy
 * ============================================
 */
void test_strcpy(void)
{
    char dest[50];
    char buffer[100];
    char *src;

    print_separator("TEST 2: stringlib_strcpy");

    src = "Hello, World!";

    printf("Prima della copia:\n");
    printf("  Source: \"%s\"\n", src);

    /*
     * Eseguiamo la copia
     */
    stringlib_strcpy(dest, src);

    printf("Dopo la copia:\n");
    printf("  Dest:   \"%s\"\n", dest);

    /*
     * Dimostriamo che le copie sono indipendenti
     */
    dest[0] = 'h';  /* Modifichiamo solo dest */
    printf("\nModifichiamo dest[0] = 'h':\n");
    printf("  Source: \"%s\" (non modificata)\n", src);
    printf("  Dest:   \"%s\" (modificata)\n", dest);

    /*
     * Copia multipla
     */
    printf("\nCopia multipla concatenata:\n");
    stringlib_strcpy(buffer, "Prima ");
    stringlib_strcat(buffer, "Seconda ");
    stringlib_strcat(buffer, "Terza");
    printf("  Risultato: \"%s\"\n", buffer);
}

/**
 * ============================================
 * TEST 3: Dimostrazione stringlib_strcat
 * ============================================
 */
void test_strcat(void)
{
    char buffer[100];
    char str[200];
    char *addition;
    size_t i;

    print_separator("TEST 3: stringlib_strcat");

    addition = ", World!";
    stringlib_strcpy(buffer, "Hello");

    printf("Buffer iniziale: \"%s\"\n", buffer);
    printf("Da aggiungere:   \"%s\"\n", addition);

    /*
     * Concatenazione
     */
    stringlib_strcat(buffer, addition);

    printf("\nDopo stringlib_strcat:\n");
    printf("  Buffer: \"%s\"\n", buffer);

    /*
     * Concatenazione multipla
     */
    printf("\nConcatenazione multipla:\n");
    stringlib_strcpy(str, "");
    stringlib_strcat(str, "Questa ");
    stringlib_strcat(str, "e' ");
    stringlib_strcat(str, "una ");
    stringlib_strcat(str, "stringa ");
    stringlib_strcat(str, "concatenata.");
    printf("  Risultato: \"%s\"\n", str);

    /*
     * Visualizzazione della memoria
     */
    printf("\nRappresentazione in memoria (primi 20 bytes):\n");
    printf("  ");
    for (i = 0; i < 20 && str[i] != '\0'; i++) {
        printf("[%c]=%d ", str[i], str[i]);
    }
    printf("[%c]=0\n", str[i]);  /* Terminatore */
}

/**
 * ============================================
 * TEST 4: Dimostrazione funzioni di sicurezza
 * ============================================
 */
void test_safe_functions(void)
{
    char small_buffer[5];
    char cat_buffer[10];
    char *long_string;
    char *to_add;
    size_t total_len;

    print_separator("TEST 4: Funzioni di Sicurezza");

    /*
     * Test strlcpy
     */
    printf("Test stringlib_strlcpy (copia con limite):\n");
    long_string = "Questa e' una stringa molto lunga";

    printf("  Buffer size: 5 caratteri\n");
    printf("  Source: \"%s\" (%lu chars)\n",
           long_string,
           (unsigned long)stringlib_strlen(long_string));

    total_len = stringlib_strlcpy(small_buffer, long_string, 5);
    printf("  Copiato: \"%s\"\n", small_buffer);
    printf("  Lunghezza totale della source: %lu (troncata)\n",
           (unsigned long)total_len);

    /*
     * Test strlcat
     */
    printf("\nTest stringlib_strlcat (concat con limite):\n");
    stringlib_strcpy(cat_buffer, "Hi");
    to_add = ", World!";

    printf("  Buffer iniziale: \"%s\" (len=%lu)\n",
           cat_buffer,
           (unsigned long)stringlib_strlen(cat_buffer));
    printf("  Da aggiungere: \"%s\"\n", to_add);

    total_len = stringlib_strlcat(cat_buffer, to_add, 10);
    printf("  Risultato: \"%s\"\n", cat_buffer);
    printf("  Lunghezza totale desiderata: %lu\n",
           (unsigned long)total_len);
    printf("  NOTA: La stringa e' stata troncata!\n");
}

/**
 * ============================================
 * TEST 5: Dimostrazione stringlib_strcmp
 * ============================================
 */
void test_strcmp(void)
{
    struct {
        char *s1;
        char *s2;
    } test_cases[] = {
        {"Hello", "Hello"},
        {"Apple", "Banana"},
        {"Banana", "Apple"},
        {"hello", "Hello"},
        {"abc", "abcd"}
    };
    int num_tests;
    int i;
    int result;

    print_separator("TEST 5: stringlib_strcmp");

    num_tests = sizeof(test_cases) / sizeof(test_cases[0]);

    for (i = 0; i < num_tests; i++) {
        result = stringlib_strcmp(test_cases[i].s1, test_cases[i].s2);
        printf("Compara \"%s\" vs \"%s\":\n", test_cases[i].s1, test_cases[i].s2);
        printf("  Risultato: %d ", result);

        if (result == 0) {
            printf("(UGUALI)\n");
        } else if (result < 0) {
            printf("(PRIMA < SECONDA)\n");
        } else {
            printf("(PRIMA > SECONDA)\n");
        }
    }
}

/**
 * ============================================
 * TEST 6: Dimostrazione stringlib_strchr
 * ============================================
 */
void test_strchr(void)
{
    char *text;
    char chars_to_find[] = {'o', 'W', 'z', '!'};
    char *result;
    int i;
    int count;
    char *pos;
    char modifiable[] = "Hello, World!";

    print_separator("TEST 6: stringlib_strchr");

    text = "Hello, World!";

    printf("Stringa di ricerca: \"%s\"\n\n", text);

    for (i = 0; i < 4; i++) {
        result = stringlib_strchr(text, chars_to_find[i]);
        printf("Cerco '%c': ", chars_to_find[i]);

        if (result != NULL) {
            printf("TROVATO all'indice %ld\n", result - text);
            printf("  Sottostringa da quella posizione: \"%s\"\n", result);
        } else {
            printf("NON TROVATO\n");
        }
    }

    /*
     * Dimostriamo l'uso del puntatore ritornato
     */
    printf("\nUso pratico: sostituiamo tutte le 'l' con 'L'\n");
    pos = modifiable;
    count = 0;

    while ((pos = stringlib_strchr(pos, 'l')) != NULL) {
        *pos = 'L';
        pos++;  /* Spostiamo al prossimo carattere */
        count++;
    }

    printf("  Originale: \"Hello, World!\"\n");
    printf("  Modificata: \"%s\" (%d sostituzioni)\n", modifiable, count);
}

/**
 * ============================================
 * TEST 7: Dimostrazione stringlib_strstr
 * ============================================
 */
void test_strstr(void)
{
    char *haystack;
    char *needles[] = {"gram", "C", "fun", "Python", ""};
    char *result;
    int i;

    print_separator("TEST 7: stringlib_strstr");

    haystack = "Programming in C is fun";

    printf("Testo: \"%s\"\n\n", haystack);

    for (i = 0; i < 5; i++) {
        result = stringlib_strstr(haystack, needles[i]);
        printf("Cerco \"%s\": ", needles[i]);

        if (result != NULL) {
            printf("TROVATO all'indice %ld\n", result - haystack);
            printf("  Contesto: \"%.10s...\"\n", result);
        } else {
            printf("NON TROVATO\n");
        }
    }
}

/**
 * ============================================
 * TEST 8: Dimostrazione stringlib_strdup
 * ============================================
 */
void test_strdup(void)
{
    char *original;
    char *duplicate;

    print_separator("TEST 8: stringlib_strdup");

    original = "Stringa da duplicare";

    printf("Stringa originale: \"%s\"\n", original);
    printf("Indirizzo originale: %p\n\n", (void *)original);

    /*
     * Duplicazione
     */
    duplicate = stringlib_strdup(original);

    if (duplicate != NULL) {
        printf("Stringa duplicata: \"%s\"\n", duplicate);
        printf("Indirizzo duplicato: %p\n\n", (void *)duplicate);

        printf("Le stringhe sono %s\n",
               stringlib_strcmp(original, duplicate) == 0 ? "UGUALI" : "DIVERSE");
        printf("Gli indirizzi sono %s\n",
               original == duplicate ? "UGUALI" : "DIVERSI");

        /*
         * IMPORTANTE: Dimostriamo che sono indipendenti
         */
        printf("\nModifichiamo il duplicato:\n");
        duplicate[0] = 'S';
        printf("  Originale: \"%s\"\n", original);
        printf("  Duplicato: \"%s\"\n", duplicate);

        /*
         * LIBERAZIONE MEMORIA:
         * Cruciale! Dobbiamo liberare la memoria allocata
         */
        printf("\nLiberiamo la memoria allocata...\n");
        free(duplicate);
        printf("Memoria liberata correttamente.\n");
    } else {
        printf("ERRORE: Allocazione memoria fallita!\n");
    }
}

/**
 * ============================================
 * TEST 9: Dimostrazione dei puntatori
 * ============================================
 */
void test_pointer_demonstration(void)
{
    char str[] = "ABCDE";
    char *ptr;
    int i;
    int same;

    print_separator("TEST 9: Dimostrazione Puntatori");

    ptr = str;

    printf("Stringa: \"%s\"\n", str);
    printf("Indirizzo base: %p\n\n", (void *)str);

    printf("Traversamento con puntatori:\n");
    for (i = 0; i < 5; i++) {
        printf("  Iterazione %d:\n", i);
        printf("    ptr + %d = %p\n", i, (void *)(ptr + i));
        printf("    *(ptr + %d) = '%c'\n", i, *(ptr + i));
        printf("    ptr[%d] = '%c'\n", i, ptr[i]);
    }

    printf("\nArithmetica dei puntatori:\n");
    printf("  ptr + 1 aggiunge %ld byte (sizeof(char))\n",
           (long)((char *)(ptr + 1) - ptr));

    /*
     * Dimostriamo che ptr[i] == *(ptr + i)
     */
    printf("\nEquivalenza notazioni:\n");
    for (i = 0; i < 5; i++) {
        same = (ptr[i] == *(ptr + i));
        printf("  ptr[%d] == *(ptr + %d): %s\n", i, i, same ? "VERO" : "FALSO");
    }
}

/**
 * ============================================
 * TEST 10: Esempio pratico - Parser CSV
 * ============================================
 */
void test_practical_csv_parser(void)
{
    char csv_line[] = "Mario,Rossi,25,Programmatore";
    char *fields[10];
    int field_count;
    char *current;
    char *comma;
    char *field_names[] = {"Nome", "Cognome", "Eta'", "Professione"};
    int i;

    print_separator("TEST 10: Esempio Pratico - Parser CSV Semplice");

    field_count = 0;

    printf("Linea CSV: \"%s\"\n\n", csv_line);

    /*
     * Parsing manuale usando le nostre funzioni
     */
    current = csv_line;

    while (*current != '\0' && field_count < 10) {
        /*
         * Troviamo la prossima virgola o la fine della stringa
         */
        comma = stringlib_strchr(current, ',');

        if (comma != NULL) {
            /*
             * Trovato separatore: sostituiamo con '\0' per terminare il campo
             */
            *comma = '\0';
            fields[field_count++] = current;
            current = comma + 1;  /* Spostiamo al prossimo carattere */
        } else {
            /*
             * Ultimo campo: nessuna virgola trovata
             */
            fields[field_count++] = current;
            break;
        }
    }

    /*
     * Stampa dei campi
     */
    printf("Campi estratti (%d):\n", field_count);
    for (i = 0; i < field_count; i++) {
        printf("  Campo %d (%s): \"%s\"\n", i + 1, field_names[i], fields[i]);
    }
}

/**
 * ============================================
 * MAIN - Entry Point
 * ============================================
 */
int main(void)
{
    printf("\n");
    printf("======================================================\n");
    printf("   LIBRERIA STRINGHE - PROGRAMMA DI TEST             \n");
    printf("   Implementazione didattica in C                    \n");
    printf("======================================================\n");

    /*
     * Eseguiamo tutti i test
     */
    test_strlen();
    test_strcpy();
    test_strcat();
    test_safe_functions();
    test_strcmp();
    test_strchr();
    test_strstr();
    test_strdup();
    test_pointer_demonstration();
    test_practical_csv_parser();

    print_separator("FINE DEI TEST");
    printf("\nTutti i test completati con successo!\n");
    printf("\nNOTE EDUCATIVE:\n");
    printf("1. Le stringhe C sono array di char terminati da '\\0'\n");
    printf("2. I puntatori permettono accesso efficiente alla memoria\n");
    printf("3. Attenzione ai buffer overflow - usa sempre funzioni safe!\n");
    printf("4. Ricorda di liberare la memoria allocata con malloc/free\n");
    printf("\nPer compilare:\n");
    printf("  gcc test_stringlib.c stringlib.c -o test_stringlib\n");
    printf("\n");

    return 0;
}
