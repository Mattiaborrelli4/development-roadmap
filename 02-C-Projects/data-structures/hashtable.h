/**
 * @file hashtable.h
 * @brief Header file per Hash Table con chaining
 * @author Matti
 * @date 2026
 */

#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <stdio.h>
#include <stdlib.h>
#include "list.h"

#define TABLE_SIZE 10

/**
 * @struct HashTable
 * @brief Struttura della Hash Table implementata con array di linked lists
 */
typedef struct HashTable {
    LinkedList* buckets[TABLE_SIZE];  ///< Array di linked lists per chaining
    int size;                         ///< Numero di elementi nella tabella
} HashTable;

/* Funzioni per Hash Table */

/**
 * @brief Crea una nuova hash table vuota
 * @return Puntatore alla nuova hash table
 */
HashTable* hashtable_create();

/**
 * @brief Funzione di hash
 * @param key Chiave da hashare
 * @return Indice del bucket
 */
int hashtable_hash(int key);

/**
 * @brief Inserisce una coppia key-value nella hash table
 * @param table Puntatore alla hash table
 * @param key Chiave
 * @param value Valore
 */
void hashtable_insert(HashTable* table, int key, int value);

/**
 * @brief Ottiene il valore associato a una chiave
 * @param table Puntatore alla hash table
 * @param key Chiave da cercare
 * @return Valore associato, -1 se non trovato
 */
int hashtable_get(HashTable* table, int key);

/**
 * @brief Rimuove una coppia key-value dalla hash table
 * @param table Puntatore alla hash table
 * @param key Chiave da rimuovere
 * @return 1 se rimosso con successo, 0 altrimenti
 */
int hashtable_remove(HashTable* table, int key);

/**
 * @brief Verifica se una chiave esiste nella hash table
 * @param table Puntatore alla hash table
 * @param key Chiave da cercare
 * @return 1 se trovata, 0 altrimenti
 */
int hashtable_contains(HashTable* table, int key);

/**
 * @brief Stampa tutti gli elementi della hash table
 * @param table Puntatore alla hash table
 */
void hashtable_print(HashTable* table);

/**
 * @brief Libera la memoria occupata dalla hash table
 * @param table Puntatore alla hash table
 */
void hashtable_destroy(HashTable* table);

#endif // HASHTABLE_H
