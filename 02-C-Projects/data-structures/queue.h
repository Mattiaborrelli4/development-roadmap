/**
 * @file queue.h
 * @brief Header file per Queue (array-based circular)
 * @author Matti
 * @date 2026
 */

#ifndef QUEUE_H
#define QUEUE_H

#include <stdio.h>
#include <stdlib.h>

#define MAX_QUEUE_SIZE 100

/**
 * @struct Queue
 * @brief Struttura della Queue implementata con array circolare
 */
typedef struct Queue {
    int items[MAX_QUEUE_SIZE];  ///< Array circolare per gli elementi
    int front;                  ///< Indice dell'elemento frontale
    int rear;                   ///< Indice dell'elemento posteriore
    int size;                   ///< Numero corrente di elementi
} Queue;

/* Funzioni per Queue */

/**
 * @brief Crea una nuova queue vuota
 * @return Puntatore alla nuova queue
 */
Queue* queue_create();

/**
 * @brief Aggiunge un elemento alla fine della queue
 * @param queue Puntatore alla queue
 * @param value Valore da inserire
 * @return 1 se successo, 0 se queue piena
 */
int queue_enqueue(Queue* queue, int value);

/**
 * @brief Rimuove e restituisce l'elemento frontale della queue
 * @param queue Puntatore alla queue
 * @return Valore rimosso, -1 se queue vuota
 */
int queue_dequeue(Queue* queue);

/**
 * @brief Restituisce l'elemento frontale senza rimuoverlo
 * @param queue Puntatore alla queue
 * @return Valore frontale, -1 se queue vuota
 */
int queue_front(Queue* queue);

/**
 * @brief Verifica se la queue è vuota
 * @param queue Puntatore alla queue
 * @return 1 se vuota, 0 altrimenti
 */
int queue_is_empty(Queue* queue);

/**
 * @brief Verifica se la queue è piena
 * @param queue Puntatore alla queue
 * @return 1 se piena, 0 altrimenti
 */
int queue_is_full(Queue* queue);

/**
 * @brief Restituisce il numero di elementi nella queue
 * @param queue Puntatore alla queue
 * @return Numero di elementi
 */
int queue_size(Queue* queue);

/**
 * @brief Stampa tutti gli elementi della queue
 * @param queue Puntatore alla queue
 */
void queue_print(Queue* queue);

/**
 * @brief Libera la memoria occupata dalla queue
 * @param queue Puntatore alla queue
 */
void queue_destroy(Queue* queue);

#endif // QUEUE_H
