/**
 * @file dynamic_array.h
 * @brief Implementazione di un Array Dinamico Generico in C
 *
 * Questo file contiene la definizione della struttura e i prototipi delle funzioni
 * per gestire un array dinamico che può crescere automaticamente quando necessario.
 *
 * @author Educational Project
 * @date 2025
 * @version 1.0
 */

#ifndef DYNAMIC_ARRAY_H
#define DYNAMIC_ARRAY_H

#include <stddef.h>  // per size_t

/**
 * @struct DynamicArray
 * @brief Struttura che rappresenta un array dinamico generico
 *
 * Questa struttura implementa il pattern "struct of pointers" per gestire
 * un array che può crescere dinamicamente.
 *
 * @var data      Puntatore all'array di puntatori void* (generico)
 * @var size      Numero di elementi attualmente presenti nell'array
 * @var capacity  Capacità totale dell'array (numero di elementi allocati)
 *
 * NOTE EDUCATIVE:
 * - Usiamo void* per rendere l'array generico (può contenere qualsiasi tipo di dato)
 * - size != capacity: size è quello che usi, capacity è quello che è allocato
 * - Manteniamo sempre capacity > size per evitare riallocazioni frequenti
 */
typedef struct {
    void **data;      // Array di puntatori a void (generico)
    size_t size;      // Numero di elementi attualmente presenti
    size_t capacity;  // Capacità totale allocata
} DynamicArray;

/* ============================================================
   FUNZIONI DI GESTIONE BASE
   ============================================================ */

/**
 * @brief Crea un nuovo array dinamico
 * @param initial_capacity Capacità iniziale dell'array
 * @return Puntatore al nuovo array, o NULL se errore di allocazione
 *
 * NOTE EDUCATIVE:
 * - malloc alloca memoria nell'heap
 * - Dobbiamo sempre controllare se malloc ritorna NULL
 * - La memoria allocata persiste finché non viene liberata con free()
 */
DynamicArray* dynamic_array_create(size_t initial_capacity);

/**
 * @brief Distrugge un array dinamico e libera la memoria
 * @param array Puntatore all'array da distruggere
 *
 * IMPORTANTISSIMO:
 * - Questa funzione NON libera la memoria puntata dagli elementi
 * - Libera solo la struttura dell'array e l'array data[]
 * - Se gli elementi contengono puntatori, devi liberarli PRIMA!
 *
 * Esempio di memoria leak:
 *   for (int i = 0; i < array->size; i++) {
 *       free(array->data[i]);  // DA FARE PRIMA!
 *   }
 *   dynamic_array_destroy(array);
 */
void dynamic_array_destroy(DynamicArray *array);

/* ============================================================
   FUNZIONI DI MODIFICA ARRAY
   ============================================================ */

/**
 * @brief Aggiunge un elemento alla fine dell'array
 * @param array Puntatore all'array
 * @param element Puntatore all'elemento da aggiungere
 * @return 0 se successo, -1 se errore
 *
 * NOTE EDUCATIVE:
 * - Se size == capacity, dobbiamo riallocare più memoria
 * - Usiamo realloc() per ridimensionare l'array
 * - realloc() può SPOSTARE l'array in memoria, quindi il puntatore cambia!
 *
 * COMPLEXITÀ: O(1) medio, O(n) nel caso peggiore (riallocazione)
 */
int dynamic_array_push(DynamicArray *array, void *element);

/**
 * @brief Rimuove e restituisce l'ultimo elemento
 * @param array Puntatore all'array
 * @return Puntatore all'elemento rimosso, o NULL se array vuoto
 *
 * NOTE EDUCATIVE:
 * - NON riallochiamo memoria quando rimuoviamo (ottimizzazione)
 * - Decrementiamo solo size
 * - Il vecchio puntatore è ancora in memoria ma non più accessibile
 *
 * COMPLEXITÀ: O(1)
 */
void* dynamic_array_pop(DynamicArray *array);

/**
 * @brief Inserisce un elemento in una posizione specifica
 * @param array Puntatore all'array
 * @param index Indice dove inserire
 * @param element Puntatore all'elemento da inserire
 * @return 0 se successo, -1 se errore
 *
 * NOTE EDUCATIVE:
 * - Dobbiamo SHIFTARE tutti gli elementi dopo index
 * - Questo è O(n) perché dobbiamo copiare n-elementi
 * - Shiftare a destra: for i from size down to index+1
 *
 * COMPLEXITÀ: O(n) - deve spostare elementi
 */
int dynamic_array_insert(DynamicArray *array, size_t index, void *element);

/**
 * @brief Rimuove un elemento da una posizione specifica
 * @param array Puntatore all'array
 * @param index Indice dell'elemento da rimuovere
 * @return Puntatore all'elemento rimosso, o NULL se errore
 *
 * NOTE EDUCATIVE:
 * - Dobbiamo SHIFTARE tutti gli elementi dopo index a SINISTRA
 * - Copiamo gli elementi: data[i] = data[i+1]
 * - NON liberiamo la memoria dell'elemento rimosso!
 *
 * COMPLEXITÀ: O(n) - deve spostare elementi
 */
void* dynamic_array_remove(DynamicArray *array, size_t index);

/* ============================================================
   FUNZIONI DI ACCESSO E UTILITÀ
   ============================================================ */

/**
 * @brief Ottiene un elemento in una posizione specifica
 * @param array Puntatore all'array
 * @param index Indice dell'elemento
 * @return Puntatore all'elemento, o NULL se indice non valido
 *
 * COMPLEXITÀ: O(1)
 */
void* dynamic_array_get(DynamicArray *array, size_t index);

/**
 * @brief Imposta un elemento in una posizione specifica
 * @param array Puntatore all'array
 * @param index Indice dove impostare
 * @param element Nuovo elemento
 * @return 0 se successo, -1 se errore
 *
 * NOTE EDUCATIVE:
 * - Sovrascrive l'elemento esistente
 * - NON libera il vecchio elemento (possibile memory leak!)
 * - Fai free(old_element) PRIMA di chiamare questa funzione se necessario
 *
 * COMPLEXITÀ: O(1)
 */
int dynamic_array_set(DynamicArray *array, size_t index, void *element);

/**
 * @brief Restituisce la dimensione attuale dell'array
 * @param array Puntatore all'array
 * @return Numero di elementi nell'array
 */
size_t dynamic_array_size(DynamicArray *array);

/**
 * @brief Controlla se l'array è vuoto
 * @param array Puntatore all'array
 * @return 1 se vuoto, 0 altrimenti
 */
int dynamic_array_is_empty(DynamicArray *array);

/**
 * @brief Ridimensiona la capacità dell'array
 * @param array Puntatore all'array
 * @param new_capacity Nuova capacità
 * @return 0 se successo, -1 se errore
 *
 * NOTE EDUCATIVE:
 * - realloc() può:
 *   1. Estendere la memoria esistente (se c'è spazio contiguo)
 *   2. Allocare nuova memoria altrove e COPIARE i dati
 *   3. Fallire e ritornare NULL (in questo caso l'array originale rimane!)
 *
 * IMPORTANTE: Bisogna sempre salvare il risultato in una variabile temporanea
 * per non perdere il puntatore originale se realloc fallisce!
 *
 * COMPLEXITÀ: O(n) - può dover copiare tutti gli elementi
 */
int dynamic_array_resize(DynamicArray *array, size_t new_capacity);

/**
 * @brief Pulisce l'array rimuovendo tutti gli elementi
 * @param array Puntatore all'array
 *
 * NOTE EDUCATIVE:
 * - Imposta size a 0 ma MANTIENE la capacità allocata
 * - NON libera gli elementi (possibile memory leak!)
 * - Ottimizzazione per riutilizzare l'array senza riallocazioni
 */
void dynamic_array_clear(DynamicArray *array);

/* ============================================================
   FUNZIONI DI UTILITÀ PER STAMPA
   ============================================================ */

/**
 * @brief Stampa informazioni di debug sull'array
 * @param array Puntatore all'array
 *
 * Utile per capire size vs capacity e verificare la memoria
 */
void dynamic_array_print_info(DynamicArray *array);

#endif // DYNAMIC_ARRAY_H
