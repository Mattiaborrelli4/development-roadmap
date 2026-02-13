/**
 * @file examples.c
 * @brief Esempi di utilizzo della libreria BigInt
 *
 * Per compilare:
 * gcc -Wall -Wextra -O2 -o examples examples.c bigint.c
 */

#include "bigint.h"
#include <stdio.h>
#include <stdlib.h>

// Esempio 1: Calcolo del fattoriale
void example_factorial(int n) {
    printf("\n=== Esempio 1: Fattoriale di %d ===\n", n);

    BigInt *result = bigint_create(1);
    BigInt *temp, *factor;

    for (int i = 2; i <= n; i++) {
        factor = bigint_create(i);
        temp = bigint_multiply(result, factor);
        bigint_free(result);
        bigint_free(factor);
        result = temp;
    }

    char *str = bigint_to_string(result);
    printf("%d! = %s\n", n, str);
    printf("Numero di cifre: %zu\n", strlen(str));
    free(str);

    bigint_free(result);
}

// Esempio 2: Successione di Fibonacci
void example_fibonacci(int n) {
    printf("\n=== Esempio 2: Fibonacci(%d) ===\n", n);

    if (n <= 0) {
        printf("Fibonacci(0) = 0\n");
        return;
    }
    if (n == 1) {
        printf("Fibonacci(1) = 1\n");
        return;
    }

    BigInt *a = bigint_create(0);  // F(0)
    BigInt *b = bigint_create(1);  // F(1)
    BigInt *temp, *next;

    for (int i = 2; i <= n; i++) {
        next = bigint_add(a, b);   // F(i) = F(i-1) + F(i-2)
        temp = b;
        b = next;
        a = temp;
    }

    char *str = bigint_to_string(b);
    printf("Fibonacci(%d) = %s\n", n, str);
    printf("Numero di cifre: %zu\n", strlen(str));
    free(str);

    bigint_free(a);
    bigint_free(b);
}

// Esempio 3: Potenza
BigInt* bigint_power(BigInt *base, int exponent) {
    if (exponent < 0) {
        // Per semplicità, non supportiamo esponenti negativi
        return NULL;
    }

    BigInt *result = bigint_create(1);
    BigInt *temp = bigint_copy(base);
    int exp = exponent;

    while (exp > 0) {
        if (exp % 2 == 1) {
            BigInt *new_result = bigint_multiply(result, temp);
            bigint_free(result);
            result = new_result;
        }
        exp /= 2;
        if (exp > 0) {
            BigInt *new_temp = bigint_multiply(temp, temp);
            bigint_free(temp);
            temp = new_temp;
        }
    }

    bigint_free(temp);
    return result;
}

void example_power(int base, int exp) {
    printf("\n=== Esempio 3: %d^%d ===\n", base, exp);

    BigInt *b = bigint_create(base);
    BigInt *result = bigint_power(b, exp);

    if (result) {
        char *str = bigint_to_string(result);
        printf("%d^%d = %s\n", base, exp, str);
        printf("Numero di cifre: %zu\n", strlen(str));
        free(str);
        bigint_free(result);
    }

    bigint_free(b);
}

// Esempio 4: Massimo Comun Divisore (Euclide)
BigInt* bigint_gcd(BigInt *a, BigInt *b) {
    BigInt *temp_a = bigint_copy(a);
    BigInt *temp_b = bigint_copy(b);
    BigInt *remainder;

    while (!bigint_is_zero(temp_b)) {
        remainder = bigint_mod(temp_a, temp_b);
        bigint_free(temp_a);
        temp_a = temp_b;
        temp_b = remainder;
    }

    bigint_free(temp_b);
    return temp_a;
}

void example_gcd(const char *a_str, const char *b_str) {
    printf("\n=== Esempio 4: MCD ===\n");

    BigInt *a = bigint_from_string(a_str);
    BigInt *b = bigint_from_string(b_str);

    printf("Calcolo MCD di: %s e %s\n", a_str, b_str);

    BigInt *gcd = bigint_gcd(a, b);

    char *gcd_str = bigint_to_string(gcd);
    printf("Risultato: %s\n", gcd_str);
    free(gcd_str);

    bigint_free(a);
    bigint_free(b);
    bigint_free(gcd);
}

// Esempio 5: Serie geometrica
void example_geometric_series(const char *a_str, const char *r_str, int n) {
    printf("\n=== Esempio 5: Serie geometrica (n=%d) ===\n", n);

    BigInt *a = bigint_from_string(a_str);  // Primo termine
    BigInt *r = bigint_from_string(r_str);  // Ragione
    BigInt *sum = bigint_create(0);
    BigInt *term = bigint_copy(a);
    BigInt *temp;

    printf("Serie: ");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf(" + ");
        bigint_print(term);

        // Aggiungi il termine alla somma
        temp = bigint_add(sum, term);
        bigint_free(sum);
        sum = temp;

        // Calcola il prossimo termine
        if (i < n - 1) {
            BigInt *next_term = bigint_multiply(term, r);
            bigint_free(term);
            term = next_term;
        }
    }

    printf("\nSomma: ");
    bigint_print(sum);
    printf("\n");

    bigint_free(a);
    bigint_free(r);
    bigint_free(sum);
    bigint_free(term);
}

// Esempio 6: Verifica numero primo (semplice)
int bigint_is_prime_naive(BigInt *n) {
    if (bigint_compare(n, bigint_create(2)) < 0) return 0;
    if (bigint_compare(n, bigint_create(2)) == 0) return 1;

    BigInt *zero = bigint_create(0);
    BigInt *one = bigint_create(1);
    BigInt *two = bigint_create(2);
    BigInt *i = bigint_create(2);
    BigInt *quotient = bigint_divide(n, two);
    BigInt *remainder, *temp;

    int is_prime = 1;

    while (bigint_compare(i, quotient) <= 0) {
        remainder = bigint_mod(n, i);
        if (bigint_is_zero(remainder)) {
            is_prime = 0;
            bigint_free(remainder);
            break;
        }
        bigint_free(remainder);

        temp = bigint_add(i, one);
        bigint_free(i);
        i = temp;
    }

    bigint_free(zero);
    bigint_free(one);
    bigint_free(two);
    bigint_free(i);
    bigint_free(quotient);

    return is_prime;
}

void example_prime(const char *n_str) {
    printf("\n=== Esempio 6: Verifica primalità di %s ===\n", n_str);

    BigInt *n = bigint_from_string(n_str);
    int is_prime = bigint_is_prime_naive(n);

    printf("%s %s un numero primo\n", n_str, is_prime ? "è" : "non è");

    bigint_free(n);
}

int main(void) {
    printf("╔════════════════════════════════════════════════╗\n");
    printf("║  BigInt Library - Esempi di Utilizzo          ║\n");
    printf("╚════════════════════════════════════════════════╝\n");

    // Esempio 1: Fattoriale
    example_factorial(50);
    example_factorial(100);

    // Esempio 2: Fibonacci
    example_fibonacci(100);
    example_fibonacci(200);

    // Esempio 3: Potenza
    example_power(2, 64);
    example_power(3, 40);

    // Esempio 4: MCD
    example_gcd("123456789", "987654321");

    // Esempio 5: Serie geometrica
    example_geometric_series("2", "3", 5);  // 2 + 6 + 18 + 54 + 162 = 242

    // Esempio 6: Verifica primalità (solo numeri piccoli per velocità)
    example_prime("104729");  // Primo
    example_prime("104730");  // Non primo

    printf("\n╔════════════════════════════════════════════════╗\n");
    printf("║  Tutti gli esempi completati con successo!     ║\n");
    printf("╚════════════════════════════════════════════════╝\n");

    return 0;
}
