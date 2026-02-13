/**
 * @file main.c
 * @brief Programma di test per la libreria BigInt
 */

#include "bigint.h"
#include <stdio.h>
#include <stdlib.h>

// Colori per l'output
#define COLOR_GREEN "\033[0;32m"
#define COLOR_RED "\033[0;31m"
#define COLOR_BLUE "\033[0;34m"
#define COLOR_YELLOW "\033[0;33m"
#define COLOR_RESET "\033[0m"

// Macro per i test
#define TEST_START(name) \
    printf("\n" COLOR_BLUE "=== TEST: %s ===" COLOR_RESET "\n", name);

#define TEST_ASSERT(condition, message) \
    do { \
        if (condition) { \
            printf(COLOR_GREEN "✓ PASS" COLOR_RESET ": %s\n", message); \
            tests_passed++; \
        } else { \
            printf(COLOR_RED "✗ FAIL" COLOR_RESET ": %s\n", message); \
            tests_failed++; \
        } \
        tests_total++; \
    } while(0)

static int tests_total = 0;
static int tests_passed = 0;
static int tests_failed = 0;

// Funzione di utilità per confrontare stringhe BigInt
int bigint_equals_string(BigInt *bi, const char *expected) {
    char *actual = bigint_to_string(bi);
    int result = (actual != NULL) && (strcmp(actual, expected) == 0);
    free(actual);
    return result;
}

// ========== TEST SU CREAZIONE E CONVERSIONE ==========

void test_creation(void) {
    TEST_START("Creazione e Conversione");

    // Test creazione da long
    BigInt *zero = bigint_create(0);
    TEST_ASSERT(bigint_equals_string(zero, "0"), "Creazione di zero");

    BigInt *positive = bigint_create(12345);
    TEST_ASSERT(bigint_equals_string(positive, "12345"), "Creazione di positivo");

    BigInt *negative = bigint_create(-6789);
    TEST_ASSERT(bigint_equals_string(negative, "-6789"), "Creazione di negativo");

    BigInt *large = bigint_create(999999999);
    TEST_ASSERT(bigint_equals_string(large, "999999999"), "Creazione di numero grande");

    // Test creazione da stringa
    BigInt *from_str = bigint_from_string("123456789");
    TEST_ASSERT(bigint_equals_string(from_str, "123456789"), "Parsing da stringa positiva");

    BigInt *from_str_neg = bigint_from_string("-987654321");
    TEST_ASSERT(bigint_equals_string(from_str_neg, "-987654321"), "Parsing da stringa negativa");

    BigInt *from_str_zero = bigint_from_string("00000");
    TEST_ASSERT(bigint_equals_string(from_str_zero, "0"), "Parsing di stringa con zeri");

    BigInt *from_str_plus = bigint_from_string("+42");
    TEST_ASSERT(bigint_equals_string(from_str_plus, "42"), "Parsing di stringa con +");

    // Test conversione to_string
    char *str = bigint_to_string(positive);
    TEST_ASSERT(str != NULL && strcmp(str, "12345") == 0, "Conversione to_string");

    // Pulizia
    free(str);
    bigint_free(zero);
    bigint_free(positive);
    bigint_free(negative);
    bigint_free(large);
    bigint_free(from_str);
    bigint_free(from_str_neg);
    bigint_free(from_str_zero);
    bigint_free(from_str_plus);
}

// ========== TEST SU CONFRONTO ==========

void test_comparison(void) {
    TEST_START("Confronto");

    BigInt *a = bigint_create(100);
    BigInt *b = bigint_create(50);
    BigInt *c = bigint_create(100);
    BigInt *neg_a = bigint_create(-100);

    TEST_ASSERT(bigint_compare(a, b) > 0, "100 > 50");
    TEST_ASSERT(bigint_compare(b, a) < 0, "50 < 100");
    TEST_ASSERT(bigint_compare(a, c) == 0, "100 == 100");
    TEST_ASSERT(bigint_compare(a, neg_a) > 0, "100 > -100");
    TEST_ASSERT(bigint_compare(neg_a, b) < 0, "-100 < 50");

    BigInt *zero = bigint_create(0);
    TEST_ASSERT(bigint_is_zero(zero), "is_zero su zero");
    TEST_ASSERT(!bigint_is_zero(a), "!is_zero su non-zero");

    bigint_free(a);
    bigint_free(b);
    bigint_free(c);
    bigint_free(neg_a);
    bigint_free(zero);
}

// ========== TEST SU ADDIZIONE ==========

void test_addition(void) {
    TEST_START("Addizione");

    BigInt *a = bigint_create(123);
    BigInt *b = bigint_create(456);
    BigInt *result = bigint_add(a, b);
    TEST_ASSERT(bigint_equals_string(result, "579"), "123 + 456 = 579");
    bigint_free(result);

    BigInt *c = bigint_create(999);
    BigInt *d = bigint_create(1);
    BigInt *result2 = bigint_add(c, d);
    TEST_ASSERT(bigint_equals_string(result2, "1000"), "999 + 1 = 1000 (carry)");
    bigint_free(result2);

    BigInt *e = bigint_create(100);
    BigInt *f = bigint_create(-50);
    BigInt *result3 = bigint_add(e, f);
    TEST_ASSERT(bigint_equals_string(result3, "50"), "100 + (-50) = 50");
    bigint_free(result3);

    BigInt *g = bigint_create(-100);
    BigInt *h = bigint_create(-50);
    BigInt *result4 = bigint_add(g, h);
    TEST_ASSERT(bigint_equals_string(result4, "-150"), "-100 + (-50) = -150");
    bigint_free(result4);

    BigInt *i = bigint_create(50);
    BigInt *j = bigint_create(-50);
    BigInt *result5 = bigint_add(i, j);
    TEST_ASSERT(bigint_equals_string(result5, "0"), "50 + (-50) = 0");
    bigint_free(result5);

    BigInt *zero = bigint_create(0);
    BigInt *k = bigint_create(123);
    BigInt *result6 = bigint_add(zero, k);
    TEST_ASSERT(bigint_equals_string(result6, "123"), "0 + 123 = 123");
    bigint_free(result6);

    bigint_free(a);
    bigint_free(b);
    bigint_free(c);
    bigint_free(d);
    bigint_free(e);
    bigint_free(f);
    bigint_free(g);
    bigint_free(h);
    bigint_free(i);
    bigint_free(j);
    bigint_free(k);
    bigint_free(zero);
}

// ========== TEST SU SOTTRAZIONE ==========

void test_subtraction(void) {
    TEST_START("Sottrazione");

    BigInt *a = bigint_create(500);
    BigInt *b = bigint_create(123);
    BigInt *result = bigint_subtract(a, b);
    TEST_ASSERT(bigint_equals_string(result, "377"), "500 - 123 = 377");
    bigint_free(result);

    BigInt *c = bigint_create(100);
    BigInt *d = bigint_create(200);
    BigInt *result2 = bigint_subtract(c, d);
    TEST_ASSERT(bigint_equals_string(result2, "-100"), "100 - 200 = -100");
    bigint_free(result2);

    BigInt *e = bigint_create(-50);
    BigInt *f = bigint_create(30);
    BigInt *result3 = bigint_subtract(e, f);
    TEST_ASSERT(bigint_equals_string(result3, "-80"), "-50 - 30 = -80");
    bigint_free(result3);

    BigInt *g = bigint_create(100);
    BigInt *h = bigint_create(-50);
    BigInt *result4 = bigint_subtract(g, h);
    TEST_ASSERT(bigint_equals_string(result4, "150"), "100 - (-50) = 150");
    bigint_free(result4);

    BigInt *i = bigint_create(50);
    BigInt *j = bigint_create(50);
    BigInt *result5 = bigint_subtract(i, j);
    TEST_ASSERT(bigint_equals_string(result5, "0"), "50 - 50 = 0");
    bigint_free(result5);

    bigint_free(a);
    bigint_free(b);
    bigint_free(c);
    bigint_free(d);
    bigint_free(e);
    bigint_free(f);
    bigint_free(g);
    bigint_free(h);
    bigint_free(i);
    bigint_free(j);
}

// ========== TEST SU MOLTIPLICAZIONE ==========

void test_multiplication(void) {
    TEST_START("Moltiplicazione");

    BigInt *a = bigint_create(12);
    BigInt *b = bigint_create(34);
    BigInt *result = bigint_multiply(a, b);
    TEST_ASSERT(bigint_equals_string(result, "408"), "12 * 34 = 408");
    bigint_free(result);

    BigInt *c = bigint_create(123);
    BigInt *d = bigint_create(456);
    BigInt *result2 = bigint_multiply(c, d);
    TEST_ASSERT(bigint_equals_string(result2, "56088"), "123 * 456 = 56088");
    bigint_free(result2);

    BigInt *e = bigint_create(-12);
    BigInt *f = bigint_create(34);
    BigInt *result3 = bigint_multiply(e, f);
    TEST_ASSERT(bigint_equals_string(result3, "-408"), "-12 * 34 = -408");
    bigint_free(result3);

    BigInt *g = bigint_create(-12);
    BigInt *h = bigint_create(-34);
    BigInt *result4 = bigint_multiply(g, h);
    TEST_ASSERT(bigint_equals_string(result4, "408"), "-12 * -34 = 408");
    bigint_free(result4);

    BigInt *zero = bigint_create(0);
    BigInt *i = bigint_create(123);
    BigInt *result5 = bigint_multiply(zero, i);
    TEST_ASSERT(bigint_equals_string(result5, "0"), "0 * 123 = 0");
    bigint_free(result5);

    BigInt *j = bigint_create(99999);
    BigInt *k = bigint_create(99999);
    BigInt *result6 = bigint_multiply(j, k);
    TEST_ASSERT(bigint_equals_string(result6, "9999800001"), "99999 * 99999 = 9999800001");
    bigint_free(result6);

    bigint_free(a);
    bigint_free(b);
    bigint_free(c);
    bigint_free(d);
    bigint_free(e);
    bigint_free(f);
    bigint_free(g);
    bigint_free(h);
    bigint_free(i);
    bigint_free(j);
    bigint_free(k);
    bigint_free(zero);
}

// ========== TEST SU DIVISIONE ==========

void test_division(void) {
    TEST_START("Divisione");

    BigInt *a = bigint_create(100);
    BigInt *b = bigint_create(5);
    BigInt *result = bigint_divide(a, b);
    TEST_ASSERT(bigint_equals_string(result, "20"), "100 / 5 = 20");
    bigint_free(result);

    BigInt *c = bigint_create(17);
    BigInt *d = bigint_create(5);
    BigInt *result2 = bigint_divide(c, d);
    TEST_ASSERT(bigint_equals_string(result2, "3"), "17 / 5 = 3 (divisione intera)");
    bigint_free(result2);

    BigInt *e = bigint_create(-20);
    BigInt *f = bigint_create(4);
    BigInt *result3 = bigint_divide(e, f);
    TEST_ASSERT(bigint_equals_string(result3, "-5"), "-20 / 4 = -5");
    bigint_free(result3);

    BigInt *g = bigint_create(5);
    BigInt *h = bigint_create(10);
    BigInt *result4 = bigint_divide(g, h);
    TEST_ASSERT(bigint_equals_string(result4, "0"), "5 / 10 = 0");
    bigint_free(result4);

    BigInt *zero = bigint_create(0);
    BigInt *i = bigint_create(5);
    BigInt *result5 = bigint_divide(zero, i);
    TEST_ASSERT(bigint_equals_string(result5, "0"), "0 / 5 = 0");
    bigint_free(result5);

    bigint_free(a);
    bigint_free(b);
    bigint_free(c);
    bigint_free(d);
    bigint_free(e);
    bigint_free(f);
    bigint_free(g);
    bigint_free(h);
    bigint_free(i);
    bigint_free(zero);
}

// ========== TEST SU MODULO ==========

void test_modulo(void) {
    TEST_START("Modulo");

    BigInt *a = bigint_create(17);
    BigInt *b = bigint_create(5);
    BigInt *result = bigint_mod(a, b);
    TEST_ASSERT(bigint_equals_string(result, "2"), "17 % 5 = 2");
    bigint_free(result);

    BigInt *c = bigint_create(100);
    BigInt *d = bigint_create(7);
    BigInt *result2 = bigint_mod(c, d);
    TEST_ASSERT(bigint_equals_string(result2, "2"), "100 % 7 = 2");
    bigint_free(result2);

    BigInt *e = bigint_create(20);
    BigInt *f = bigint_create(4);
    BigInt *result3 = bigint_mod(e, f);
    TEST_ASSERT(bigint_equals_string(result3, "0"), "20 % 4 = 0");
    bigint_free(result3);

    bigint_free(a);
    bigint_free(b);
    bigint_free(c);
    bigint_free(d);
    bigint_free(e);
    bigint_free(f);
}

// ========== TEST SU NUMERI GRANDI ==========

void test_large_numbers(void) {
    TEST_START("Numeri Grandi");

    // Test con numeri molto grandi (oltre LONG_MAX)
    BigInt *a = bigint_from_string("123456789012345678901234567890");
    BigInt *b = bigint_from_string("987654321098765432109876543210");

    BigInt *sum = bigint_add(a, b);
    TEST_ASSERT(bigint_equals_string(sum, "1111111110111111111011111111100"), "Somma numeri grandi");
    bigint_free(sum);

    BigInt *prod = bigint_multiply(a, b);
    TEST_ASSERT(bigint_equals_string(prod, "121932631137021795226185032733622923332237463801111263526900"), "Prodotto numeri grandi");
    bigint_free(prod);

    BigInt *diff = bigint_subtract(b, a);
    TEST_ASSERT(bigint_equals_string(diff, "864197532086419753208641975320"), "Differenza numeri grandi");
    bigint_free(diff);

    bigint_free(a);
    bigint_free(b);

    // Test con numero negativo grande
    BigInt *c = bigint_from_string("-999999999999999999999");
    BigInt *d = bigint_from_string("1");
    BigInt *sum2 = bigint_add(c, d);
    TEST_ASSERT(bigint_equals_string(sum2, "-999999999999999999998"), "-999...999 + 1 = -999...998");
    bigint_free(sum2);

    bigint_free(c);
    bigint_free(d);
}

// ========== TEST INTERATTIVO ==========

void interactive_demo(void) {
    printf("\n" COLOR_YELLOW "=== DEMO INTERATTIVA ===" COLOR_RESET "\n");
    printf("Prova la libreria BigInt!\n");
    printf("Formato: <operando1> <operazione> <operando2>\n");
    printf("Operazioni: +, -, *, /, %%\n");
    printf("Esempio: 12345678901234567890 * 98765432109876543210\n");
    printf("Digita 'quit' per uscire\n\n");

    char line[256];
    while (1) {
        printf(COLOR_BLUE ">>> " COLOR_RESET);

        if (!fgets(line, sizeof(line), stdin)) break;

        // Rimuovi newline
        line[strcspn(line, "\n")] = 0;

        // Esci
        if (strcmp(line, "quit") == 0 || strcmp(line, "exit") == 0) {
            break;
        }

        // Parsing
        char op1_str[128], op2_str[128];
        char op;

        if (sscanf(line, "%127s %c %127s", op1_str, &op, op2_str) != 3) {
            printf(COLOR_RED "Errore: formato non valido. Usa: <num1> <op> <num2>" COLOR_RESET "\n");
            continue;
        }

        BigInt *op1 = bigint_from_string(op1_str);
        BigInt *op2 = bigint_from_string(op2_str);

        if (!op1 || !op2) {
            printf(COLOR_RED "Errore: numeri non validi" COLOR_RESET "\n");
            bigint_free(op1);
            bigint_free(op2);
            continue;
        }

        BigInt *result = NULL;
        switch (op) {
            case '+':
                result = bigint_add(op1, op2);
                break;
            case '-':
                result = bigint_subtract(op1, op2);
                break;
            case '*':
                result = bigint_multiply(op1, op2);
                break;
            case '/':
                result = bigint_divide(op1, op2);
                break;
            case '%':
                result = bigint_mod(op1, op2);
                break;
            default:
                printf(COLOR_RED "Errore: operazione '%c' non supportata" COLOR_RESET "\n", op);
                bigint_free(op1);
                bigint_free(op2);
                continue;
        }

        if (result) {
            printf(COLOR_GREEN "Risultato: " COLOR_RESET);
            bigint_print(result);
            printf("\n");
            bigint_free(result);
        } else {
            printf(COLOR_RED "Errore nel calcolo" COLOR_RESET "\n");
        }

        bigint_free(op1);
        bigint_free(op2);
    }
}

// ========== MAIN ==========

int main(int argc, char *argv[]) {
    printf(COLOR_YELLOW "╔════════════════════════════════════════╗\n");
    printf("║   BigInt Library - Test Suite      ║\n");
    printf("║   Numeri interi arbitrariamente grandi ║\n");
    printf("╚════════════════════════════════════════╝" COLOR_RESET "\n");

    // Esegui tutti i test
    test_creation();
    test_comparison();
    test_addition();
    test_subtraction();
    test_multiplication();
    test_division();
    test_modulo();
    test_large_numbers();

    // Riepilogo
    printf("\n" COLOR_YELLOW "=== RIEPILOGO TEST ===" COLOR_RESET "\n");
    printf("Totale:  %d\n", tests_total);
    printf(COLOR_GREEN "Passati: %d" COLOR_RESET "\n", tests_passed);
    printf(COLOR_RED "Falliti: %d" COLOR_RESET "\n", tests_failed);

    if (tests_failed == 0) {
        printf("\n" COLOR_GREEN "✓ Tutti i test sono passati!" COLOR_RESET "\n");
    } else {
        printf("\n" COLOR_RED "✗ Alcuni test sono falliti" COLOR_RESET "\n");
    }

    // Modalità interattiva
    if (argc > 1 && strcmp(argv[1], "-i") == 0) {
        interactive_demo();
    } else {
        printf("\nPer la modalità interattiva, esegui: %s -i\n", argv[0]);
    }

    return tests_failed > 0 ? 1 : 0;
}
