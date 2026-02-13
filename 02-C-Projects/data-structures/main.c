/**
 * @file main.c
 * @brief Programma di test per la libreria Data Structures
 * @author Matti
 * @date 2026
 */

#include <stdio.h>
#include "list.h"
#include "stack.h"
#include "queue.h"
#include "hashtable.h"

void print_separator(const char* title) {
    printf("\n");
    printf("========================================\n");
    printf("  %s\n", title);
    printf("========================================\n");
}

void test_linked_list() {
    print_separator("TEST LINKED LIST");

    LinkedList* list = list_create();

    // Test insert
    printf("\n1. Inserimento elementi (insert):\n");
    list_insert(list, 10);
    list_insert(list, 20);
    list_insert(list, 30);
    list_print(list);

    // Test append
    printf("\n2. Aggiunta elementi alla fine (append):\n");
    list_append(list, 40);
    list_append(list, 50);
    list_print(list);

    // Test search
    printf("\n3. Ricerca elementi:\n");
    printf("Cerco 20: %s\n", list_search(list, 20) ? "Trovato" : "Non trovato");
    printf("Cerco 100: %s\n", list_search(list, 100) ? "Trovato" : "Non trovato");

    // Test delete
    printf("\n4. Cancellazione elemento 20:\n");
    list_delete(list, 20);
    list_print(list);

    // Test delete head
    printf("\n5. Cancellazione elemento in testa (30):\n");
    list_delete(list, 30);
    list_print(list);

    list_destroy(list);
}

void test_stack() {
    print_separator("TEST STACK");

    Stack* stack = stack_create();

    // Test push
    printf("\n1. Push elementi:\n");
    stack_push(stack, 10);
    stack_push(stack, 20);
    stack_push(stack, 30);
    stack_print(stack);

    // Test peek
    printf("\n2. Peek (elemento in cima): %d\n", stack_peek(stack));

    // Test pop
    printf("\n3. Pop elemento: %d\n", stack_pop(stack));
    stack_print(stack);

    // Test is_empty
    printf("\n4. Stack vuoto? %s\n", stack_is_empty(stack) ? "Si" : "No");

    // Test pop all
    printf("\n5. Pop di tutti gli elementi:\n");
    while (!stack_is_empty(stack)) {
        printf("Pop: %d\n", stack_pop(stack));
    }

    // Test empty stack
    printf("\n6. Stack vuoto dopo aver rimosso tutto:\n");
    stack_print(stack);

    stack_destroy(stack);
}

void test_queue() {
    print_separator("TEST QUEUE");

    Queue* queue = queue_create();

    // Test enqueue
    printf("\n1. Enqueue elementi:\n");
    queue_enqueue(queue, 10);
    queue_enqueue(queue, 20);
    queue_enqueue(queue, 30);
    queue_print(queue);

    // Test front
    printf("\n2. Front (elemento frontale): %d\n", queue_front(queue));

    // Test dequeue
    printf("\n3. Dequeue elemento: %d\n", queue_dequeue(queue));
    queue_print(queue);

    // Test is_empty
    printf("\n4. Queue vuota? %s\n", queue_is_empty(queue) ? "Si" : "No");

    // Test dequeue all
    printf("\n5. Dequeue di tutti gli elementi:\n");
    while (!queue_is_empty(queue)) {
        printf("Dequeue: %d\n", queue_dequeue(queue));
    }

    // Test empty queue
    printf("\n6. Queue vuota dopo aver rimosso tutto:\n");
    queue_print(queue);

    // Test circular behavior
    printf("\n7. Test comportamento circolare:\n");
    for (int i = 1; i <= 5; i++) {
        queue_enqueue(queue, i * 10);
    }
    queue_print(queue);

    printf("Dequeue 2 elementi...\n");
    queue_dequeue(queue);
    queue_dequeue(queue);

    printf("Enqueue 2 nuovi elementi...\n");
    queue_enqueue(queue, 60);
    queue_enqueue(queue, 70);
    queue_print(queue);

    queue_destroy(queue);
}

void test_hashtable() {
    print_separator("TEST HASH TABLE");

    HashTable* table = hashtable_create();

    // Test insert
    printf("\n1. Inserimento elementi:\n");
    hashtable_insert(table, 10, 10);
    hashtable_insert(table, 20, 20);
    hashtable_insert(table, 30, 30);
    hashtable_insert(table, 15, 15);
    hashtable_insert(table, 25, 25);
    hashtable_insert(table, 35, 35);
    hashtable_print(table);

    // Test contains
    printf("\n2. Ricerca elementi:\n");
    printf("Contiene 20? %s\n", hashtable_contains(table, 20) ? "Si" : "No");
    printf("Contiene 100? %s\n", hashtable_contains(table, 100) ? "Si" : "No");

    // Test get
    printf("\n3. Get elemento 15: %d\n", hashtable_get(table, 15));

    // Test remove
    printf("\n4. Rimozione elemento 20:\n");
    hashtable_remove(table, 20);
    hashtable_print(table);

    // Test collision handling
    printf("\n5. Test gestione collisioni (hash collision):\n");
    hashtable_insert(table, 40, 40);  // Possibile collisione
    hashtable_insert(table, 50, 50);  // Possibile collisione
    hashtable_print(table);

    hashtable_destroy(table);
}

int main() {
    printf("\n");
    printf("╔════════════════════════════════════════╗\n");
    printf("║   DATA STRUCTURES LIBRARY - TEST       ║\n");
    printf("║   Author: Matti                        ║\n");
    printf("║   Date: 2026                            ║\n");
    printf("╚════════════════════════════════════════╝\n");

    test_linked_list();
    test_stack();
    test_queue();
    test_hashtable();

    print_separator("TUTTI I TEST COMPLETATI");
    printf("\n");

    return 0;
}
