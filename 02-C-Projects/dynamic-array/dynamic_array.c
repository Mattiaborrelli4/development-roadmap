/**
 * @file dynamic_array.c
 * @brief Implementazione di un Array Dinamico Generico in C
 *
 * Questo file contiene l'implementazione completa delle funzioni
 * per gestire un array dinamico con riallocazione automatica.
 *
 * CONCETTI CHIAVE:
 * - Gestione manuale della memoria (malloc, realloc, free)
 * - Puntatori a void per dati generici
 * - Riallocazione dinamica con strategia di crescita
 *
 * @author Educational Project
 * @date 2025
 * @version 1.0
 */

#include "dynamic_array.h"
#include <stdio.h>   // per printf
#include <stdlib.h>  // per malloc, realloc, free
#include <string.h>  // per memcpy (se necessario)

/* ============================================================
   COSTANTI GLOBALI
   ============================================================ */

/**
 * @brief Fattore di crescita dell'array quando è pieno
 *
 * STRATEGIA DI CRESCITA:
 * - Raddoppiamo la capacità ogni volta che l'array è pieno
 * - Questo garantisce amortized O(1) per le insert
 * - Perché? Raddoppiando raramente, quindi il costo medio è basso
 *
 * Esempio:
 *   Inserimenti: 1, 2, 3, 4, 5, 6, 7, 8, 9
 *   Capacity:     1, 2, 4, 4, 4, 4, 8, 8, 8
 *   Rialloca:    X   X       X           X
 *
 * Senza raddoppiamento, riallocheremmo ad ogni inserimento!
 */
#define GROWTH_FACTOR 2

/**
 * @brief Capacità iniziale di default
 */
#define DEFAULT_CAPACITY 4

/* ============================================================
   FUNZIONI DI GESTIONE BASE
   ============================================================ */

DynamicArray* dynamic_array_create(size_t initial_capacity) {
    /*
     * NOTE EDUCATIVE sull'allocazione della struttura:
     *
     * 1. malloc(sizeof(DynamicArray)) alloca SOLO la struttura, non i dati!
     * 2. La struttura contiene solo 3 puntatori/size_t (circa 24 bytes)
     * 3. L'array dei dati viene allocato separatamente dopo
     *
     * Layout in memoria:
     * [DynamicArray struct] -> [void* data[]] -> [actual data]
     *    24 bytes               capacity * 8 bytes
     */

    // Alloca la struttura dell'array
    DynamicArray *array = (DynamicArray*)malloc(sizeof(DynamicArray));
    if (array == NULL) {
        /*
         * GESTIONE ERRORI:
         * - malloc ritorna NULL se non c'è abbastanza memoria
         * - NON continuare mai con NULL! Causerà segmentation fault
         * - Ritorna NULL al chiamante per segnalare l'errore
         */
        fprintf(stderr, "ERRORE: Impossibile allocare memoria per DynamicArray\n");
        return NULL;
    }

    // Se initial_capacity è 0, usa il default
    if (initial_capacity == 0) {
        initial_capacity = DEFAULT_CAPACITY;
    }

    /*
     * NOTE EDUCATIVE sull'allocazione dell'array dati:
     *
     * sizeof(void*) = 8 bytes su sistemi 64-bit
     * Allochiamo un ARRAY di puntatori, non i dati stessi!
     *
     * Esempio con capacity = 4:
     * data = [ptr1][ptr2][ptr3][ptr4]
     *         8B    8B    8B    8B   = 32 bytes totali
     *
     * I dati puntati possono essere ovunque in memoria!
     */
    array->data = (void**)malloc(initial_capacity * sizeof(void*));
    if (array->data == NULL) {
        /*
         * GESTIONE ERRORI - Pulizia:
         * - Se fallisce la seconda allocazione, dobbiamo liberare la prima!
         * - Altrimenti abbiamo un memory leak di 24 bytes
         * - Regola d'oro: ogni malloc deve avere un free corrispondente
         */
        fprintf(stderr, "ERRORE: Impossibile allocare memoria per l'array dati\n");
        free(array);  // Pulisci la struttura già allocata
        return NULL;
    }

    // Inizializza i campi
    array->size = 0;
    array->capacity = initial_capacity;

    /*
     * NOTE EDUCATIVE - Inizializzazione esplicita:
     *
     * Non è strettamente necessario inizializzare a NULL perché:
     * - Gli elementi non inizializzati non sono accessibili (size = 0)
     * - Scriviamo solo nelle posizioni < size
     *
     * MA è buona pratica per debug e strumenti come valgrind
     */
    for (size_t i = 0; i < initial_capacity; i++) {
        array->data[i] = NULL;
    }

    return array;
}

void dynamic_array_destroy(DynamicArray *array) {
    if (array == NULL) {
        return;  // Protezione contro NULL (defensive programming)
    }

    /*
     * NOTE EDUCATIVE - Ordine di deallocazione:
     *
     * IMPORTANTE: Dealloca in ordine INVERSO rispetto all'allocazione!
     *
     * 1. PRIMA libera l'array dati (array->data)
     * 2. POI libera la struttura (array)
     *
     * Se facessimo il contrario, perderemmo il puntatore a data!
     *
     * Diagramma:
     *   array -> [struct con puntatore a data]
     *   array->data -> [array di puntatori]
     *
     * Se free(array) per primo:
     *   array->data è ORMAI INACCESSIBILE! Memory leak!
     */

    free(array->data);  // Libera l'array dei puntatori
    array->data = NULL;  // Buona pratica: evita dangling pointers

    free(array);         // Libera la struttura
    // array diventa un dangling pointer qui, ma il chiamante
    // dovrebbe impostarlo a NULL dopo la chiamata
}

/* ============================================================
   FUNZIONI DI MODIFICA ARRAY
   ============================================================ */

int dynamic_array_push(DynamicArray *array, void *element) {
    if (array == NULL) {
        fprintf(stderr, "ERRORE: Array NULL in dynamic_array_push\n");
        return -1;
    }

    /*
     * NOTE EDUCATIVE - Controllo capacità:
     *
     * Prima di inserire, verifichiamo se c'è spazio:
     * - size: numero di elementi attuali (0..capacity)
     * - capacity: spazio totale allocato
     *
     * Se size == capacity, l'array è PIENO!
     * Dobbiamo riallocare più memoria.
     */
    if (array->size >= array->capacity) {
        /*
         * CALCOLO NUOVA CAPACITÀ:
         *
         * Strategia: raddoppiamo (GROWTH_FACTOR = 2)
         *
         * Perché raddoppiare?
         * 1. Amortized O(1): anche se occasionally O(n), in media è O(1)
         * 2. Bilanciamento: non sprechiamo troppa memoria
         * 3. Semplice: new_capacity = capacity * 2
         *
         * Esempio con 10 elementi:
         *   Senza raddoppio: 10 riallocazioni (O(n^2) totale)
         *   Con raddoppio:   4 riallocazioni (O(n) totale)
         */
        size_t new_capacity = array->capacity * GROWTH_FACTOR;

        /*
         * PROTEZIONE CONTRO OVERFLOW:
         *
         * Se capacity è molto grande, moltiplicare può causare overflow!
         * Esempio: capacity = SIZE_MAX / 2 + 1
         *          new_capacity = SIZE_MAX + 2 = 1 (overflow!)
         *
         * In questo caso falliamo la resize
         */
        if (new_capacity < array->capacity) {
            fprintf(stderr, "ERRORE: Overflow capacità in dynamic_array_push\n");
            return -1;
        }

        // Chiamata alla funzione di resize
        if (dynamic_array_resize(array, new_capacity) != 0) {
            fprintf(stderr, "ERRORE: Fallimento resize in dynamic_array_push\n");
            return -1;
        }

        printf("[INFO] Array riallocato: nuova capacità = %zu\n", new_capacity);
    }

    /*
     * NOTE EDUCATIVE - Inserimento:
     *
     * Ora che c'è spazio, inseriamo alla posizione size:
     *
     * Esempio con size = 3, capacity = 8:
     *   data = [A][B][C][?][?][?][?][?]
     *          0  1  2  3  4  5  6  7
     *                ^
     *               size
     *
     * Inseriamo in data[3] e incrementiamo size a 4
     */
    array->data[array->size] = element;
    array->size++;

    return 0;  // Successo
}

void* dynamic_array_pop(DynamicArray *array) {
    if (array == NULL || array->size == 0) {
        /*
         * NOTE EDUCATIVE - Array vuoto:
         *
         - Non possiamo rimuovere da un array vuoto!
         * - Ritorniamo NULL per segnalare l'errore
         * - Il chiamante dovrebbe controllare array->size prima
         */
        return NULL;
    }

    /*
     * NOTE EDUCATIVE - Rimozione dall'ultimo elemento:
     *
     * Decrementiamo size PRIMA di accedere:
     *
     * Esempio con size = 4:
     *   Prima: data = [A][B][C][D][?][?]
     *          size = 4, puntiamo all'indice 4 (vuoto)
     *
     *   size-- → size = 3
     *
     *   Ora: data[3] = D (l'ultimo elemento)
     *
     * Ritorniamo D, e ora l'array "vede" solo A,B,C
     *
     * IMPORTANTE: NON rimuoviamo realmente D dalla memoria!
     * D è ancora in data[3], ma non è più accessibile perché
     * size = 3, quindi possiamo accedere solo a data[0..2]
     *
     * Questo è un'ottimizzazione: evitiamo riallocazioni
     * quando rimuoviamo elementi.
     */
    array->size--;
    void *element = array->data[array->size];

    // Opzionale: impostiamo a NULL per sicurezza (debugging)
    // array->data[array->size] = NULL;

    return element;
}

int dynamic_array_insert(DynamicArray *array, size_t index, void *element) {
    if (array == NULL) {
        fprintf(stderr, "ERRORE: Array NULL in dynamic_array_insert\n");
        return -1;
    }

    /*
     * VALIDAZIONE INDICE:
     *
     * Possiamo inserire in qualsiasi posizione da 0 a size (incluso!)
     *
     * Esempio con size = 3:
     *   data = [A][B][C]
     *          0  1  2
     *
     * Indici validi per insert: 0, 1, 2, 3
     * - Insert a 0: inserisce all'inizio
     * - Insert a 3: aggiunge alla fine (come push)
     */
    if (index > array->size) {
        fprintf(stderr, "ERRORE: Indice %zu non valido (size = %zu)\n",
                index, array->size);
        return -1;
    }

    // Verifica se dobbiamo riallocare
    if (array->size >= array->capacity) {
        size_t new_capacity = array->capacity * GROWTH_FACTOR;
        if (new_capacity < array->capacity ||
            dynamic_array_resize(array, new_capacity) != 0) {
            fprintf(stderr, "ERRORE: Fallimento resize in dynamic_array_insert\n");
            return -1;
        }
    }

    /*
     * NOTE EDUCATIVE - Shift degli elementi:
     *
     * Dobbiamo spostare tutti gli elementi da index in poi a destra:
     *
     * Esempio: insert(2, X) con size = 4
     *   Prima:  [A][B][C][D][?]
     *           0  1  2  3  4
     *
     *   Dopo:   [A][B][X][C][D]
     *           0  1  2  3  4
     *
     * ALGORITMO:
     * 1. Partiamo dall'ULTIMO elemento (size - 1)
     * 2. Copiamo ogni elemento una posizione a destra
     * 3. Fermiamoci quando arriviamo a index
     *
     * Perché dall'ultimo in poi?
     * Perché se andassimo da index alla fine, sovrascriveremmo
     * l'elemento che dobbiamo ancora spostare!
     *
     * Esempio sbagliato (da index a size):
     *   [A][B][C][D]
     *    ^  sposta C→D: [A][B][C][C]  D è PERSO!
     *
     * Esempio corretto (da size a index):
     *   [A][B][C][D]
     *           ^  sposta D→?: [A][B][C][D][_]
     *        ^     sposta C→D: [A][B][C][C][D]
     *     ^        sposta B→C: [A][B][B][C][D]
     */
    for (size_t i = array->size; i > index; i--) {
        array->data[i] = array->data[i - 1];
    }

    /*
     * Ora che abbiamo creato spazio, inseriamo il nuovo elemento
     */
    array->data[index] = element;
    array->size++;

    return 0;
}

void* dynamic_array_remove(DynamicArray *array, size_t index) {
    if (array == NULL || array->size == 0) {
        return NULL;
    }

    /*
     * VALIDAZIONE INDICE:
     *
     * Possiamo rimuovere solo da 0 a size - 1
     * (diversamente da insert che permette size!)
     */
    if (index >= array->size) {
        fprintf(stderr, "ERRORE: Indice %zu non valido (size = %zu)\n",
                index, array->size);
        return NULL;
    }

    /*
     * Salviamo l'elemento da rimuovere PRIMA di shiftare
     */
    void *element = array->data[index];

    /*
     * NOTE EDUCATIVE - Shift degli elementi:
     *
     * Dobbiamo spostare tutti gli elementi dopo index a SINISTRA:
     *
     * Esempio: remove(1) con size = 4
     *   Prima:  [A][B][C][D][?]
     *           0  1  2  3  4
     *
     *   Dopo:   [A][C][D][?][?]
     *           0  1  2  3  4
     *
     * ALGORITMO:
     * 1. Partiamo da index
     * 2. Copiamo ogni elemento dall'indice successivo
     * 3. Fermiamoci all'ultimo elemento (size - 2)
     *
     * Qui l'ordine NON importa perché andiamo verso destra,
     * non sovrascriviamo nulla che ci serve ancora.
     */
    for (size_t i = index; i < array->size - 1; i++) {
        array->data[i] = array->data[i + 1];
    }

    // Decrementa la dimensione
    array->size--;

    // Opzionale: pulisci l'ultimo elemento (ora fuori size)
    array->data[array->size] = NULL;

    return element;
}

/* ============================================================
   FUNZIONI DI ACCESSO E UTILITÀ
   ============================================================ */

void* dynamic_array_get(DynamicArray *array, size_t index) {
    if (array == NULL || index >= array->size) {
        return NULL;
    }

    return array->data[index];
}

int dynamic_array_set(DynamicArray *array, size_t index, void *element) {
    if (array == NULL) {
        fprintf(stderr, "ERRORE: Array NULL in dynamic_array_set\n");
        return -1;
    }

    if (index >= array->size) {
        fprintf(stderr, "ERRORE: Indice %zu non valido (size = %zu)\n",
                index, array->size);
        return -1;
    }

    /*
     * ATTENZIONE: Possibile memory leak!
     *
     * Se array->data[index] punta a memoria allocata,
     * sovrascrivendola perdiamo quel puntatore!
     *
     * Soluzione: il chiamante deve fare free() prima:
     *   free(array->data[index]);
     *   dynamic_array_set(array, index, new_value);
     */
    array->data[index] = element;
    return 0;
}

size_t dynamic_array_size(DynamicArray *array) {
    if (array == NULL) {
        return 0;
    }
    return array->size;
}

int dynamic_array_is_empty(DynamicArray *array) {
    if (array == NULL) {
        return 1;  // NULL array è considerato vuoto
    }
    return array->size == 0;
}

int dynamic_array_resize(DynamicArray *array, size_t new_capacity) {
    if (array == NULL) {
        fprintf(stderr, "ERRORE: Array NULL in dynamic_array_resize\n");
        return -1;
    }

    /*
     * VALIDAZIONE:
     * - Non possiamo ridurre sotto size ( perderemmo dati!)
     * - new_capacity = 0 è valido? Dipende, ma di solito no
     */
    if (new_capacity < array->size) {
        fprintf(stderr, "ERRORE: Nuova capacità %zu < size attuale %zu\n",
                new_capacity, array->size);
        return -1;
    }

    if (new_capacity == array->capacity) {
        return 0;  // Già della giusta dimensione, niente da fare
    }

    /*
     * NOTE EDUCATIVE - realloc() è TRICKY!
     *
     * realloc(ptr, new_size) fa tre cose possibili:
     *
     * 1. ESTENDE in-place:
     *    - Se c'è spazio contiguo dopo ptr
     *    - RITORNA LO STESSO PUNTATORE (ptr)
     *    - Molto veloce (nessuna copia)
     *
     * 2. RIALLOCA e COPIA:
     *    - Se non c'è spazio contiguo
     *    - Alloca nuova memoria altrove
     *    - COPIA tutti i dati
     *    - Libera la vecchia memoria
     *    - RITORNA NUOVO PUNTATORE (diverso da ptr!)
     *
     * 3. FALLISCE:
     *    - Se non c'è abbastanza memoria
     *    - RITORNA NULL
     *    - VECCHIA MEMORIA RIMANE ALLOCATA! (importante!)
     *
     * PERICOLO: se facciamo array->data = realloc(array->data, size)
     * e realloc fallisce → array->data = NULL → PERDIAMO I DATI!
     *
     * SOLUZIONE: Usare sempre un puntatore temporaneo!
     */
    void **new_data = (void**)realloc(array->data, new_capacity * sizeof(void*));

    if (new_data == NULL) {
        /*
         * FALLIMENTO realloc:
         * - array->data è ancora valido (non l'abbiamo sovrascritto)
         * - Possiamo continuare a usare l'array vecchio
         * - Ritorniamo errore ma non perdiamo dati
         */
        fprintf(stderr, "ERRORE: Fallimento realloc per capacità %zu\n", new_capacity);
        return -1;
    }

    /*
     * SUCCESSO!
     *
     * Ora possiamo aggiornare array->data
     * Nota: new_data può essere uguale a array->data (estensione in-place)
     * oppure diverso (riallocazione con copia)
     */
    array->data = new_data;
    array->capacity = new_capacity;

    /*
     * NOTE EDUCATIVE - Inizializzazione nuovi elementi:
     *
     * Se abbiamo cresciuto l'array, i nuovi elementi non inizializzati
     * dovrebbero essere NULL per buona pratica.
     *
     * Esempio: capacity da 4 a 8, size = 4
     *   new elements: data[4], data[5], data[6], data[7]
     */
    for (size_t i = array->size; i < new_capacity; i++) {
        array->data[i] = NULL;
    }

    return 0;
}

void dynamic_array_clear(DynamicArray *array) {
    if (array == NULL) {
        return;
    }

    /*
     * NOTE EDUCATIVE - Clear vs Destroy:
     *
     * clear() rimuove tutti gli elementi ma MANTIENE l'array
     * destroy() rimuove l'array completamente
     *
     * ATTENZIONE: clear() NON libera la memoria degli elementi!
     *
     * Se hai elementi allocati, devi liberarli prima:
     *   for (int i = 0; i < array->size; i++) {
     *       free(array->data[i]);
     *   }
     *   dynamic_array_clear(array);
     *
     * Perché non liberiamo automaticamente?
     * - L'array è generico (void*)
     * - Non sappiamo se i puntatori sono da liberare
     * - Potrebbero essere puntatori a stack, variabili globali, etc.
     */
    array->size = 0;

    // Opzionale: impostiamo tutti a NULL per sicurezza
    // (utile per debugging con valgrind)
    for (size_t i = 0; i < array->capacity; i++) {
        array->data[i] = NULL;
    }
}

void dynamic_array_print_info(DynamicArray *array) {
    if (array == NULL) {
        printf("Array: NULL\n");
        return;
    }

    printf("========== INFO ARRAY DINAMICO ==========\n");
    printf("Indirizzo struttura: %p\n", (void*)array);
    printf("Indirizzo dati:      %p\n", (void*)array->data);
    printf("Dimensione (size):   %zu elementi\n", array->size);
    printf("Capacità (capacity): %zu elementi\n", array->capacity);
    printf("Memoria allocata:    %zu bytes\n",
           array->capacity * sizeof(void*));
    printf("Occupazione:         %.1f%%\n",
           (array->capacity > 0) ? (100.0 * array->size / array->capacity) : 0.0);
    printf("Elementi:\n");

    for (size_t i = 0; i < array->size; i++) {
        printf("  [%zu] → %p", i, array->data[i]);
        if (array->data[i] != NULL) {
            printf(" (dato: %d)", *(int*)array->data[i]);
        }
        printf("\n");
    }

    printf("==========================================\n");
}
