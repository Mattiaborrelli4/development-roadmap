/**
 * @file list.h
 * @brief Header file per Linked List Singly
 * @author Matti
 * @date 2026
 */

#ifndef LIST_H
#define LIST_H

#include <stdio.h>
#include <stdlib.h>

/**
 * @struct Node
 * @brief Nodo della linked list
 */
typedef struct Node {
    int data;           ///< Dato memorizzato nel nodo
    struct Node* next;  ///< Puntatore al prossimo nodo
} Node;

/**
 * @struct LinkedList
 * @brief Struttura della linked list
 */
typedef struct LinkedList {
    Node* head;  ///< Puntatore al primo nodo della lista
    int size;    ///< Numero di elementi nella lista
} LinkedList;

/* Funzioni per Linked List */

/**
 * @brief Crea una nuova linked list vuota
 * @return Puntatore alla nuova lista
 */
LinkedList* list_create();

/**
 * @brief Inserisce un elemento all'inizio della lista
 * @param list Puntatore alla lista
 * @param data Dato da inserire
 */
void list_insert(LinkedList* list, int data);

/**
 * @brief Inserisce un elemento alla fine della lista
 * @param list Puntatore alla lista
 * @param data Dato da inserire
 */
void list_append(LinkedList* list, int data);

/**
 * @brief Cancella un elemento con il valore specificato
 * @param list Puntatore alla lista
 * @param data Valore da cancellare
 * @return 1 se cancellato con successo, 0 altrimenti
 */
int list_delete(LinkedList* list, int data);

/**
 * @brief Cerca un elemento nella lista
 * @param list Puntatore alla lista
 * @param data Valore da cercare
 * @return 1 se trovato, 0 altrimenti
 */
int list_search(LinkedList* list, int data);

/**
 * @brief Stampa tutti gli elementi della lista
 * @param list Puntatore alla lista
 */
void list_print(LinkedList* list);

/**
 * @brief Libera la memoria occupata dalla lista
 * @param list Puntatore alla lista
 */
void list_destroy(LinkedList* list);

#endif // LIST_H
