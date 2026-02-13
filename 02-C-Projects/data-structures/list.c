/**
 * @file list.c
 * @brief Implementazione della Linked List Singly
 */

#include "list.h"
#include <stdio.h>
#include <stdlib.h>

LinkedList* list_create() {
    LinkedList* list = (LinkedList*)malloc(sizeof(LinkedList));
    if (list == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per la lista\n");
        exit(1);
    }
    list->head = NULL;
    list->size = 0;
    return list;
}

void list_insert(LinkedList* list, int data) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per il nodo\n");
        exit(1);
    }

    new_node->data = data;
    new_node->next = list->head;
    list->head = new_node;
    list->size++;
}

void list_append(LinkedList* list, int data) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per il nodo\n");
        exit(1);
    }

    new_node->data = data;
    new_node->next = NULL;

    if (list->head == NULL) {
        list->head = new_node;
    } else {
        Node* current = list->head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_node;
    }
    list->size++;
}

int list_delete(LinkedList* list, int data) {
    if (list->head == NULL) {
        return 0;
    }

    Node* current = list->head;
    Node* prev = NULL;

    // Cerca il nodo da cancellare
    while (current != NULL && current->data != data) {
        prev = current;
        current = current->next;
    }

    // Elemento non trovato
    if (current == NULL) {
        return 0;
    }

    // Se il nodo da cancellare è la testa
    if (prev == NULL) {
        list->head = current->next;
    } else {
        prev->next = current->next;
    }

    free(current);
    list->size--;
    return 1;
}

int list_search(LinkedList* list, int data) {
    Node* current = list->head;
    while (current != NULL) {
        if (current->data == data) {
            return 1;
        }
        current = current->next;
    }
    return 0;
}

void list_print(LinkedList* list) {
    if (list->head == NULL) {
        printf("Lista vuota\n");
        return;
    }

    Node* current = list->head;
    printf("Lista: ");
    while (current != NULL) {
        printf("%d", current->data);
        if (current->next != NULL) {
            printf(" -> ");
        }
        current = current->next;
    }
    printf("\nDimensione: %d\n", list->size);
}

void list_destroy(LinkedList* list) {
    Node* current = list->head;
    while (current != NULL) {
        Node* temp = current;
        current = current->next;
        free(temp);
    }
    free(list);
}
