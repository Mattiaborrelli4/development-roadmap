/**
 * @file queue.c
 * @brief Implementazione della Queue (array-based circular)
 */

#include "queue.h"
#include <stdio.h>
#include <stdlib.h>

Queue* queue_create() {
    Queue* queue = (Queue*)malloc(sizeof(Queue));
    if (queue == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per la queue\n");
        exit(1);
    }
    queue->front = 0;
    queue->rear = -1;
    queue->size = 0;
    return queue;
}

int queue_enqueue(Queue* queue, int value) {
    if (queue_is_full(queue)) {
        fprintf(stderr, "Errore: Queue piena - impossibile inserire %d\n", value);
        return 0;
    }

    // Circolare: torna all'inizio se raggiunge la fine
    queue->rear = (queue->rear + 1) % MAX_QUEUE_SIZE;
    queue->items[queue->rear] = value;
    queue->size++;
    return 1;
}

int queue_dequeue(Queue* queue) {
    if (queue_is_empty(queue)) {
        fprintf(stderr, "Errore: Queue vuota - impossibile rimuovere elementi\n");
        return -1;
    }

    int value = queue->items[queue->front];
    queue->front = (queue->front + 1) % MAX_QUEUE_SIZE;
    queue->size--;
    return value;
}

int queue_front(Queue* queue) {
    if (queue_is_empty(queue)) {
        fprintf(stderr, "Errore: Queue vuota - nessun elemento frontale\n");
        return -1;
    }
    return queue->items[queue->front];
}

int queue_is_empty(Queue* queue) {
    return queue->size == 0;
}

int queue_is_full(Queue* queue) {
    return queue->size == MAX_QUEUE_SIZE;
}

int queue_size(Queue* queue) {
    return queue->size;
}

void queue_print(Queue* queue) {
    if (queue_is_empty(queue)) {
        printf("Queue vuota\n");
        return;
    }

    printf("Queue (dal front al rear): ");
    int i = queue->front;
    int count = 0;

    while (count < queue->size) {
        printf("%d", queue->items[i]);
        if (count < queue->size - 1) {
            printf(" <- ");
        }
        i = (i + 1) % MAX_QUEUE_SIZE;
        count++;
    }
    printf("\nDimensione: %d\n", queue_size(queue));
}

void queue_destroy(Queue* queue) {
    free(queue);
}
