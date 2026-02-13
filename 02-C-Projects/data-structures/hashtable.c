/**
 * @file hashtable.c
 * @brief Implementazione della Hash Table con chaining
 */

#include "hashtable.h"
#include <stdio.h>
#include <stdlib.h>

HashTable* hashtable_create() {
    HashTable* table = (HashTable*)malloc(sizeof(HashTable));
    if (table == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per la hash table\n");
        exit(1);
    }

    // Inizializza ogni bucket come una linked list vuota
    for (int i = 0; i < TABLE_SIZE; i++) {
        table->buckets[i] = list_create();
    }

    table->size = 0;
    return table;
}

int hashtable_hash(int key) {
    // Funzione di hash semplice: modulo della grandezza della tabella
    // Gestisce chiavi negative con abs()
    return (abs(key) % TABLE_SIZE);
}

void hashtable_insert(HashTable* table, int key, int value) {
    int index = hashtable_hash(key);
    LinkedList* bucket = table->buckets[index];

    // Controlla se la chiave esiste già
    Node* current = bucket->head;
    while (current != NULL) {
        if (current->data == key) {
            printf("Chiave %d già presente. Aggiornamento non supportato in questa implementazione.\n", key);
            return;
        }
        current = current->next;
    }

    // Inserisce la nuova chiave nel bucket appropriato
    // Nota: In questa implementazione semplificata, usiamo lo stesso valore per chiave e dato
    list_insert(table->buckets[index], value);
    table->size++;
}

int hashtable_get(HashTable* table, int key) {
    int index = hashtable_hash(key);
    LinkedList* bucket = table->buckets[index];

    if (list_search(bucket, key)) {
        return key;
    }
    return -1;
}

int hashtable_remove(HashTable* table, int key) {
    int index = hashtable_hash(key);

    if (list_delete(table->buckets[index], key)) {
        table->size--;
        return 1;
    }
    return 0;
}

int hashtable_contains(HashTable* table, int key) {
    int index = hashtable_hash(key);
    return list_search(table->buckets[index], key);
}

void hashtable_print(HashTable* table) {
    printf("\n=== Hash Table ===\n");
    printf("Dimensione totale: %d\n", table->size);
    printf("Bucket size: %d\n\n", TABLE_SIZE);

    for (int i = 0; i < TABLE_SIZE; i++) {
        printf("Bucket[%d]: ", i);
        if (table->buckets[i]->head == NULL) {
            printf("vuoto");
        } else {
            Node* current = table->buckets[i]->head;
            while (current != NULL) {
                printf("%d", current->data);
                if (current->next != NULL) {
                    printf(" -> ");
                }
                current = current->next;
            }
        }
        printf("\n");
    }
    printf("==================\n\n");
}

void hashtable_destroy(HashTable* table) {
    for (int i = 0; i < TABLE_SIZE; i++) {
        list_destroy(table->buckets[i]);
    }
    free(table);
}
