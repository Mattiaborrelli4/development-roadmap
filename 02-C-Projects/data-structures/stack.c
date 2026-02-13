/**
 * @file stack.c
 * @brief Implementazione dello Stack (array-based)
 */

#include "stack.h"
#include <stdio.h>
#include <stdlib.h>

Stack* stack_create() {
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    if (stack == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per lo stack\n");
        exit(1);
    }
    stack->top = -1;
    return stack;
}

int stack_push(Stack* stack, int value) {
    if (stack_is_full(stack)) {
        fprintf(stderr, "Errore: Stack pieno - impossibile inserire %d\n", value);
        return 0;
    }
    stack->top++;
    stack->items[stack->top] = value;
    return 1;
}

int stack_pop(Stack* stack) {
    if (stack_is_empty(stack)) {
        fprintf(stderr, "Errore: Stack vuoto - impossibile rimuovere elementi\n");
        return -1;
    }
    int value = stack->items[stack->top];
    stack->top--;
    return value;
}

int stack_peek(Stack* stack) {
    if (stack_is_empty(stack)) {
        fprintf(stderr, "Errore: Stack vuoto - nessun elemento in cima\n");
        return -1;
    }
    return stack->items[stack->top];
}

int stack_is_empty(Stack* stack) {
    return stack->top == -1;
}

int stack_is_full(Stack* stack) {
    return stack->top == MAX_STACK_SIZE - 1;
}

int stack_size(Stack* stack) {
    return stack->top + 1;
}

void stack_print(Stack* stack) {
    if (stack_is_empty(stack)) {
        printf("Stack vuoto\n");
        return;
    }

    printf("Stack (dalla cima alla base): ");
    for (int i = stack->top; i >= 0; i--) {
        printf("%d", stack->items[i]);
        if (i > 0) {
            printf(" <- ");
        }
    }
    printf("\nDimensione: %d\n", stack_size(stack));
}

void stack_destroy(Stack* stack) {
    free(stack);
}
