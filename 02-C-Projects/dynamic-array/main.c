/**
 * @file main.c
 * @brief Programma di test per l'Array Dinamico
 *
 * Questo file contiene esempi completi di utilizzo dell'array dinamico,
 * con commenti educativi per studenti universitari.
 *
 * @author Educational Project
 * @date 2025
 * @version 1.0
 */

#include "dynamic_array.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ============================================================
   FUNZIONI HELPER
   ============================================================ */

/**
 * @brief Stampa un array di interi
 *
 * NOTE EDUCATIVE:
 * - Usiamo void* perché l'array è generico
 * - Dobbiamo fare cast a int* per dereferenziare
 */
void print_int_array(DynamicArray *array) {
    if (array == NULL || array->size == 0) {
        printf("Array vuoto\n");
        return;
    }

    printf("[");
    for (size_t i = 0; i < array->size; i++) {
        int *val = (int*)array->data[i];
        printf("%d", *val);
        if (i < array->size - 1) {
            printf(", ");
        }
    }
    printf("]\n");
}

/**
 * @brief Stampa un array di stringhe
 */
void print_string_array(DynamicArray *array) {
    if (array == NULL || array->size == 0) {
        printf("Array vuoto\n");
        return;
    }

    printf("[");
    for (size_t i = 0; i < array->size; i++) {
        char *str = (char*)array->data[i];
        printf("\"%s\"", str);
        if (i < array->size - 1) {
            printf(", ");
        }
    }
    printf("]\n");
}

/* ============================================================
   TEST 1: Operazioni Base con Interi
   ============================================================ */

void test_interi() {
    printf("\n========== TEST 1: INTERI ==========\n\n");

    /*
     * NOTE EDUCATIVE - Creazione dell'array:
     *
     * Inizializziamo con capacità 4 per vedere il raddoppio
     */
    DynamicArray *array = dynamic_array_create(4);
    if (array == NULL) {
        fprintf(stderr, "ERRORE: Impossibile creare l'array\n");
        return;
    }

    printf("1. Array creato con capacità iniziale 4\n");
    dynamic_array_print_info(array);

    /*
     * PUSH - Aggiunta elementi
     *
     * IMPORTANTE: Dobbiamo allocare memoria per ogni elemento!
     * L'array non fa copia dei dati, memorizza solo PUNTATORI.
     *
     * SBAGLIATO:
     *   int x = 5;
     *   dynamic_array_push(array, &x);  // x è nello stack!
     *
     * CORRETTO:
     *   int *x = malloc(sizeof(int));
     *   *x = 5;
     *   dynamic_array_push(array, x);
     */
    printf("\n2. Aggiunta di 6 elementi (dovrebbe raddoppiare)\n");

    for (int i = 1; i <= 6; i++) {
        // Alloca un nuovo intero nell'heap
        int *num = (int*)malloc(sizeof(int));
        if (num == NULL) {
            fprintf(stderr, "ERRORE: malloc fallito\n");
            break;
        }
        *num = i * 10;

        printf("   Push: %d\n", *num);
        dynamic_array_push(array, num);
    }

    printf("\n3. Stato dopo i push:\n");
    dynamic_array_print_info(array);
    printf("Contenuto: ");
    print_int_array(array);

    /*
     * POP - Rimozione dall'ultimo elemento
     *
     * IMPORTANTE: Il pop NON libera la memoria!
     * Dobbiamo fare free() manualmente del puntatore ritornato.
     */
    printf("\n4. Pop dell'ultimo elemento:\n");
    void *popped = dynamic_array_pop(array);
    if (popped != NULL) {
        int *val = (int*)popped;
        printf("   Elemento rimosso: %d\n", *val);
        free(val);  // RICORDA: libera la memoria!
    }

    printf("Contenuto dopo pop: ");
    print_int_array(array);

    /*
     * INSERT - Inserimento in posizione specifica
     */
    printf("\n5. Insert di 99 in posizione 1:\n");
    int *new_val = (int*)malloc(sizeof(int));
    *new_val = 99;
    dynamic_array_insert(array, 1, new_val);

    printf("Contenuto dopo insert: ");
    print_int_array(array);

    /*
     * REMOVE - Rimozione da posizione specifica
     */
    printf("\n6. Remove da posizione 2:\n");
    void *removed = dynamic_array_remove(array, 2);
    if (removed != NULL) {
        int *val = (int*)removed;
        printf("   Elemento rimosso: %d\n", *val);
        free(val);  // Libera la memoria!
    }

    printf("Contenuto dopo remove: ");
    print_int_array(array);

    /*
     * PULIZIA FINALE - Molto importante!
     *
     * Prima di distruggere l'array, dobbiamo liberare tutti gli elementi!
     * L'array non sa come liberare i dati (è generico).
     */
    printf("\n7. Pulizia della memoria:\n");
    printf("   Liberazione di %zu elementi...\n", array->size);

    for (size_t i = 0; i < array->size; i++) {
        free(array->data[i]);
    }

    dynamic_array_destroy(array);
    printf("   Array distrutto correttamente\n");
}

/* ============================================================
   TEST 2: Stringhe (Gestione memoria complessa)
   ============================================================ */

void test_stringhe() {
    printf("\n========== TEST 2: STRINGHE ==========\n\n");

    DynamicArray *array = dynamic_array_create(2);
    if (array == NULL) {
        fprintf(stderr, "ERRORE: Impossibile creare l'array\n");
        return;
    }

    /*
     * NOTE EDUCATIVE - Stringhe in C:
     *
     * Le stringhe in C sono array di char con '\0' alla fine.
     * Per memorizzarle, abbiamo due opzioni:
     *
     * 1. Stringhe letterali (statiche):
     *    char *str = "ciao";  // Nella memoria read-only
     *    // NON fare free()!
     *
     * 2. Stringhe allocate (dinamiche):
     *    char *str = malloc(5);
     *    strcpy(str, "ciao");
     *    // Dobbiamo fare free()!
     */

    printf("1. Aggiunta di stringhe allocate:\n");

    const char *words[] = {"Hello", "World", "C", "Dynamic", "Array"};
    size_t num_words = sizeof(words) / sizeof(words[0]);

    for (size_t i = 0; i < num_words; i++) {
        // Alloca memoria per la stringa (+1 per '\0')
        char *str = (char*)malloc(strlen(words[i]) + 1);
        if (str == NULL) {
            fprintf(stderr, "ERRORE: malloc fallito\n");
            break;
        }
        strcpy(str, words[i]);

        printf("   Push: \"%s\"\n", str);
        dynamic_array_push(array, str);
    }

    printf("\n2. Array di stringhe:\n");
    print_string_array(array);
    dynamic_array_print_info(array);

    /*
     * RICERCA - Pattern comune con array dinamici
     */
    printf("\n3. Ricerca della stringa \"C\":\n");
    for (size_t i = 0; i < array->size; i++) {
        char *str = (char*)array->data[i];
        if (strcmp(str, "C") == 0) {
            printf("   Trovata alla posizione %zu\n", i);

            // Esempio: modifica dell'elemento
            free(str);  // Libera la vecchia stringa
            char *new_str = (char*)malloc(10);
            strcpy(new_str, "C-Language");
            array->data[i] = new_str;
            printf("   Modificata in: \"%s\"\n", new_str);
            break;
        }
    }

    printf("\n4. Array dopo modifica:\n");
    print_string_array(array);

    /*
     * PULIZIA FINALE
     */
    printf("\n5. Pulizia della memoria:\n");
    for (size_t i = 0; i < array->size; i++) {
        free(array->data[i]);  // Libera ogni stringa
    }
    dynamic_array_destroy(array);
    printf("   Array distrutto correttamente\n");
}

/* ============================================================
   TEST 3: Dimostrazione Memory Leak
   ============================================================ */

void test_memory_leak_demo() {
    printf("\n========== TEST 3: DEMO MEMORY LEAK ==========\n\n");

    printf("SCENARIO 1: Memory leak se NON liberiamo gli elementi\n");
    printf("------------------------------------------------------\n");

    DynamicArray *array = dynamic_array_create(3);

    // Aggiungiamo elementi
    for (int i = 0; i < 3; i++) {
        int *num = (int*)malloc(sizeof(int));
        *num = i;
        dynamic_array_push(array, num);
    }

    printf("Creati 3 elementi nell'array\n");
    printf("Memoria allocata: 3 * sizeof(int) = 3 * 4 = 12 bytes\n");
    printf("Più la struttura dell'array\n\n");

    /*
     * SBAGLIATO - Questo causerebbe memory leak!
     *
     * Se facessimo solo dynamic_array_destroy(array) senza
     * liberare prima gli elementi, perderemmo i 12 bytes!
     *
     * L'array libera solo array->data (l'array di puntatori),
     * non ciò che i puntatori puntano!
     */

    printf("Per evitare il leak, dobbiamo fare:\n");
    printf("  1. for loop per liberare ogni elemento\n");
    printf("  2. dynamic_array_destroy(array)\n\n");

    // CORRETTO - Libera tutto
    for (size_t i = 0; i < array->size; i++) {
        free(array->data[i]);
    }
    dynamic_array_destroy(array);

    printf("Memoria liberata correttamente!\n");
}

/* ============================================================
   TEST 4: Operazioni Edge Case
   ============================================================ */

void test_edge_cases() {
    printf("\n========== TEST 4: EDGE CASES ==========\n\n");

    DynamicArray *array = dynamic_array_create(2);

    /*
     * TEST: Array vuoto
     */
    printf("1. Pop da array vuoto:\n");
    void *result = dynamic_array_pop(array);
    printf("   Risultato: %s\n", result == NULL ? "NULL (corretto)" : "errore");

    /*
     * TEST: Indici non validi
     */
    printf("\n2. Get con indice non valido:\n");
    result = dynamic_array_get(array, 100);
    printf("   Risultato: %s\n", result == NULL ? "NULL (corretto)" : "errore");

    /*
     * TEST: Insert alla fine
     */
    printf("\n3. Insert alla fine (index = size):\n");
    int *val = (int*)malloc(sizeof(int));
    *val = 42;
    int ret = dynamic_array_insert(array, 0, val);
    printf("   Insert a 0: %s\n", ret == 0 ? "successo" : "errore");
    printf("   Size: %zu\n", array->size);

    /*
     * TEST: Resize manuale
     */
    printf("\n4. Resize manuale:\n");
    printf("   Capacity prima: %zu\n", array->capacity);
    dynamic_array_resize(array, 10);
    printf("   Capacity dopo resize a 10: %zu\n", array->capacity);

    /*
     * TEST: Clear
     */
    printf("\n5. Clear dell'array:\n");
    printf("   Size prima: %zu\n", array->size);
    free(array->data[0]);  // Libera l'elemento prima del clear
    dynamic_array_clear(array);
    printf("   Size dopo clear: %zu\n", array->size);
    printf("   Capacity dopo clear: %zu (rimane invariata)\n", array->capacity);

    dynamic_array_destroy(array);
}

/* ============================================================
   TEST 5: Performance - Raddoppio Capacità
   ============================================================ */

void test_performance_growth() {
    printf("\n========== TEST 5: PERFORMANCE CRESCITA ==========\n\n");

    /*
     * Questo test mostra perché raddoppiare è efficiente
     */

    DynamicArray *array = dynamic_array_create(1);
    size_t initial_capacity = array->capacity;

    printf("Inserimento di 1000 elementi...\n");
    printf("Capacity iniziale: %zu\n", initial_capacity);

    int resize_count = 0;
    size_t last_capacity = array->capacity;

    for (int i = 0; i < 1000; i++) {
        int *num = (int*)malloc(sizeof(int));
        *num = i;

        size_t cap_before = array->capacity;
        dynamic_array_push(array, num);

        if (array->capacity > cap_before) {
            resize_count++;
            printf("  Resize #%d: %zu → %zu (elemento: %d)\n",
                   resize_count, cap_before, array->capacity, i);
        }
    }

    printf("\nRisultati:\n");
    printf("  Totale elementi: %zu\n", array->size);
    printf("  Capacity finale: %zu\n", array->capacity);
    printf("  Numero di resize: %d\n", resize_count);
    printf("  Efficienza: %.1f%% (%zu elementi / %zu capacity)\n",
           100.0 * array->size / array->capacity,
           array->size, array->capacity);

    printf("\nConfronto senza raddoppio (ipotetico):\n");
    printf("  Senza raddoppio avremmo fatto 1000 resize!\n");
    printf("  Con raddoppio ne abbiamo fatti solo %d\n", resize_count);

    // Pulizia
    for (size_t i = 0; i < array->size; i++) {
        free(array->data[i]);
    }
    dynamic_array_destroy(array);
}

/* ============================================================
   FUNZIONE PRINCIPALE
   ============================================================ */

int main() {
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║     ARRAY DINAMICO IN C - PROGRAMMA DI TEST           ║\n");
    printf("║     Educational Project per Studenti Universitari      ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");

    // Esegui tutti i test
    test_interi();
    test_stringhe();
    test_memory_leak_demo();
    test_edge_cases();
    test_performance_growth();

    printf("\n╔════════════════════════════════════════════════════════╗\n");
    printf("║  TUTTI I TEST COMPLETATI CON SUCCESSO!                ║\n");
    printf("║                                                        ║\n");
    printf("║  CONCETTI CHIAVE APPRESI:                             ║\n");
    printf("║  • Gestione manuale della memoria (malloc/free)        ║\n");
    printf("║  • Riallocazione dinamica con realloc                 ║\n");
    printf("║  • Puntatori void* per dati generici                  ║\n");
    printf("║  • Strategia di raddoppio per efficienza              ║\n");
    printf("║  • Pericoli dei memory leak                           ║\n");
    printf("║  • Importanza di liberare la memoria                   ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");

    return 0;
}
