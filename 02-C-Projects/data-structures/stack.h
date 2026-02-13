/**
 * @file stack.h
 * @brief Header file per Stack (array-based)
 * @author Matti
 * @date 2026
 */

#ifndef STACK_H
#define STACK_H

#include <stdio.h>
#include <stdlib.h>

#define MAX_STACK_SIZE 100

/**
 * @struct Stack
 * @brief Struttura dello Stack implementato con array
 */
typedef struct Stack {
    int items[MAX_STACK_SIZE];  ///< Array che contiene gli elementi
    int top;                    ///< Indice dell'elemento in cima
} Stack;

/* Funzioni per Stack */

/**
 * @brief Crea uno nuovo stack vuoto
 * @return Puntatore al nuovo stack
 */
Stack* stack_create();

/**
 * @brief Aggiunge un elemento in cima allo stack
 * @param stack Puntatore allo stack
 * @param value Valore da inserire
 * @return 1 se successo, 0 se stack pieno
 */
int stack_push(Stack* stack, int value);

/**
 * @brief Rimuove e restituisce l'elemento in cima allo stack
 * @param stack Puntatore allo stack
 * @return Valore rimosso, -1 se stack vuoto
 */
int stack_pop(Stack* stack);

/**
 * @brief Restituisce l'elemento in cima senza rimuoverlo
 * @param stack Puntatore allo stack
 * @return Valore in cima, -1 se stack vuoto
 */
int stack_peek(Stack* stack);

/**
 * @brief Verifica se lo stack è vuoto
 * @param stack Puntatore allo stack
 * @return 1 se vuoto, 0 altrimenti
 */
int stack_is_empty(Stack* stack);

/**
 * @brief Verifica se lo stack è pieno
 * @param stack Puntatore allo stack
 * @return 1 se pieno, 0 altrimenti
 */
int stack_is_full(Stack* stack);

/**
 * @brief Restituisce il numero di elementi nello stack
 * @param stack Puntatore allo stack
 * @return Numero di elementi
 */
int stack_size(Stack* stack);

/**
 * @brief Stampa tutti gli elementi dello stack
 * @param stack Puntatore allo stack
 */
void stack_print(Stack* stack);

/**
 * @brief Libera la memoria occupata dallo stack
 * @param stack Puntatore allo stack
 */
void stack_destroy(Stack* stack);

#endif // STACK_H
