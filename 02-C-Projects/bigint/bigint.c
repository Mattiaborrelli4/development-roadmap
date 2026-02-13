/**
 * @file bigint.c
 * @brief Implementazione della libreria BigInt
 */

#include "bigint.h"
#include <limits.h>
#include <ctype.h>

// ========== FUNZIONI DI UTILITÀ INTERNE ==========

/**
 * @brief Alloca e inizializza un BigInt
 */
static BigInt* bigint_alloc(size_t length) {
    BigInt *bi = (BigInt*)malloc(sizeof(BigInt));
    if (!bi) return NULL;

    bi->digits = (char*)calloc(length, sizeof(char));
    if (!bi->digits) {
        free(bi);
        return NULL;
    }

    bi->length = length;
    bi->sign = 1;
    return bi;
}

/**
 * @brief Rimuove gli zeri leading dal BigInt
 */
static void bigint_trim(BigInt *bi) {
    if (!bi || !bi->digits) return;

    size_t new_length = bi->length;
    while (new_length > 1 && bi->digits[new_length - 1] == 0) {
        new_length--;
    }

    if (new_length < bi->length) {
        char *new_digits = (char*)realloc(bi->digits, new_length * sizeof(char));
        if (new_digits || new_length == 0) {
            bi->digits = new_digits;
            bi->length = new_length;
        }
    }

    // Se il numero è zero, assicura che il segno sia positivo
    if (bi->length == 1 && bi->digits[0] == 0) {
        bi->sign = 1;
    }
}

/**
 * @brief Somma assoluta di due BigInt (ignora il segno)
 * Assume che a e b siano entrambi positivi
 */
static BigInt* bigint_add_absolute(const BigInt *a, const BigInt *b) {
    size_t max_len = (a->length > b->length) ? a->length : b->length;
    BigInt *result = bigint_alloc(max_len + 1);
    if (!result) return NULL;

    int carry = 0;

    for (size_t i = 0; i < max_len || carry; i++) {
        int sum = carry;
        if (i < a->length) sum += a->digits[i];
        if (i < b->length) sum += b->digits[i];

        result->digits[i] = sum % 10;
        carry = sum / 10;
    }

    bigint_trim(result);
    return result;
}

/**
 * @brief Sottrazione assoluta di due BigInt (a - b, assume a >= b)
 * Assume che a e b siano entrambi positivi e che a >= b
 */
static BigInt* bigint_subtract_absolute(const BigInt *a, const BigInt *b) {
    BigInt *result = bigint_alloc(a->length);
    if (!result) return NULL;

    int borrow = 0;

    for (size_t i = 0; i < a->length; i++) {
        int diff = a->digits[i] - borrow;
        if (i < b->length) diff -= b->digits[i];

        if (diff < 0) {
            diff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }

        result->digits[i] = diff;
    }

    bigint_trim(result);
    return result;
}

/**
 * @brief Compara i valori assoluti di due BigInt
 * @return -1 se |a| < |b|, 0 se |a| == |b|, 1 se |a| > |b|
 */
static int bigint_compare_absolute(const BigInt *a, const BigInt *b) {
    if (a->length != b->length) {
        return a->length > b->length ? 1 : -1;
    }

    for (int i = (int)a->length - 1; i >= 0; i--) {
        if (a->digits[i] != b->digits[i]) {
            return a->digits[i] > b->digits[i] ? 1 : -1;
        }
    }

    return 0;
}

/**
 * @brief Moltiplicazione schoolbook
 */
static BigInt* bigint_multiply_schoolbook(const BigInt *a, const BigInt *b) {
    if (bigint_is_zero(a) || bigint_is_zero(b)) {
        return bigint_create(0);
    }

    BigInt *result = bigint_alloc(a->length + b->length);
    if (!result) return NULL;

    for (size_t i = 0; i < a->length; i++) {
        int carry = 0;
        for (size_t j = 0; j < b->length || carry; j++) {
            int product = result->digits[i + j] + carry;
            if (j < b->length) {
                product += a->digits[i] * b->digits[j];
            }
            result->digits[i + j] = product % 10;
            carry = product / 10;
        }
    }

    bigint_trim(result);
    return result;
}

// ========== FUNZIONI PUBBLICHE ==========

BigInt* bigint_create(long n) {
    int sign = 1;
    unsigned long absolute;

    if (n == LONG_MIN) {
        // Caso speciale per LONG_MIN
        absolute = (unsigned long)LONG_MAX + 1;
        sign = -1;
    } else if (n < 0) {
        absolute = (unsigned long)(-n);
        sign = -1;
    } else {
        absolute = (unsigned long)n;
    }

    // Calcola il numero di cifre
    size_t length = 0;
    unsigned long temp = absolute;
    do {
        length++;
        temp /= 10;
    } while (temp > 0);

    if (length == 0) length = 1;

    BigInt *bi = bigint_alloc(length);
    if (!bi) return NULL;

    bi->sign = sign;

    if (absolute == 0) {
        bi->digits[0] = 0;
    } else {
        for (size_t i = 0; i < length && absolute > 0; i++) {
            bi->digits[i] = absolute % 10;
            absolute /= 10;
        }
    }

    return bi;
}

BigInt* bigint_from_string(const char *str) {
    if (!str || !*str) return NULL;

    // Salta gli spazi iniziali
    while (isspace((unsigned char)*str)) str++;

    // Determina il segno
    int sign = 1;
    if (*str == '-') {
        sign = -1;
        str++;
    } else if (*str == '+') {
        str++;
    }

    // Salta gli zeri leading
    while (*str == '0') str++;

    // Se solo zeri, ritorna zero
    int all_zeros = 1;
    const char *check = str;
    while (*check) {
        if (*check != '0' && !isdigit((unsigned char)*check)) {
            return NULL; // Carattere non valido
        }
        if (*check != '0') all_zeros = 0;
        check++;
    }

    if (all_zeros) {
        BigInt *zero = bigint_create(0);
        return zero;
    }

    // Calcola la lunghezza
    size_t len = strlen(str);

    BigInt *bi = bigint_alloc(len);
    if (!bi) return NULL;

    bi->sign = sign;

    // Copia le cifre in ordine inverso (little-endian)
    for (size_t i = 0; i < len; i++) {
        bi->digits[len - 1 - i] = str[i] - '0';
    }

    bigint_trim(bi);
    return bi;
}

void bigint_free(BigInt *bi) {
    if (bi) {
        if (bi->digits) {
            free(bi->digits);
        }
        free(bi);
    }
}

BigInt* bigint_copy(const BigInt *bi) {
    if (!bi) return NULL;

    BigInt *copy = bigint_alloc(bi->length);
    if (!copy) return NULL;

    copy->sign = bi->sign;
    memcpy(copy->digits, bi->digits, bi->length * sizeof(char));

    return copy;
}

BigInt* bigint_add(const BigInt *a, const BigInt *b) {
    if (!a || !b) return NULL;

    // Caso speciale: uno dei due è zero
    if (bigint_is_zero(a)) return bigint_copy(b);
    if (bigint_is_zero(b)) return bigint_copy(a);

    // Stesso segno: somma assoluta
    if (a->sign == b->sign) {
        BigInt *result = bigint_add_absolute(a, b);
        if (result) result->sign = a->sign;
        return result;
    }

    // Segni opposti: sottrai il più piccolo dal più grande
    int cmp_abs = bigint_compare_absolute(a, b);
    if (cmp_abs == 0) {
        return bigint_create(0); // a + (-a) = 0
    }

    BigInt *result;
    BigInt *abs_a, *abs_b;

    // Crea copie positive per la sottrazione
    abs_a = bigint_copy(a);
    abs_b = bigint_copy(b);
    if (!abs_a || !abs_b) {
        bigint_free(abs_a);
        bigint_free(abs_b);
        return NULL;
    }
    abs_a->sign = 1;
    abs_b->sign = 1;

    if (cmp_abs > 0) {
        // |a| > |b|
        result = bigint_subtract_absolute(abs_a, abs_b);
        if (result) result->sign = a->sign;
    } else {
        // |b| > |a|
        result = bigint_subtract_absolute(abs_b, abs_a);
        if (result) result->sign = b->sign;
    }

    bigint_free(abs_a);
    bigint_free(abs_b);
    return result;
}

BigInt* bigint_subtract(const BigInt *a, const BigInt *b) {
    if (!a || !b) return NULL;

    // Caso speciale: b è zero
    if (bigint_is_zero(b)) return bigint_copy(a);

    // Calcola a - b come a + (-b)
    BigInt *neg_b = bigint_copy(b);
    if (!neg_b) return NULL;
    neg_b->sign = -neg_b->sign;

    BigInt *result = bigint_add(a, neg_b);
    bigint_free(neg_b);

    return result;
}

BigInt* bigint_multiply(const BigInt *a, const BigInt *b) {
    if (!a || !b) return NULL;

    // Caso speciale: uno dei due è zero
    if (bigint_is_zero(a) || bigint_is_zero(b)) {
        return bigint_create(0);
    }

    BigInt *result = bigint_multiply_schoolbook(a, b);
    if (result) {
        result->sign = a->sign * b->sign;
    }

    return result;
}

BigInt* bigint_divide(const BigInt *a, const BigInt *b) {
    if (!a || !b) return NULL;

    // Divisione per zero
    if (bigint_is_zero(b)) {
        fprintf(stderr, "Errore: divisione per zero\n");
        return NULL;
    }

    // Implementazione divisione per sottrazione successiva sui valori assoluti
    BigInt *abs_a = bigint_copy(a);
    BigInt *abs_b = bigint_copy(b);
    if (!abs_a || !abs_b) {
        bigint_free(abs_a);
        bigint_free(abs_b);
        return NULL;
    }

    abs_a->sign = 1;
    abs_b->sign = 1;

    // Se |a| < |b|, il risultato è 0
    int cmp_abs = bigint_compare_absolute(abs_a, abs_b);
    if (cmp_abs < 0) {
        bigint_free(abs_a);
        bigint_free(abs_b);
        return bigint_create(0);
    }

    BigInt *quotient = bigint_create(0);
    BigInt *one = bigint_create(1);

    while (bigint_compare_absolute(abs_a, abs_b) >= 0) {
        BigInt *temp = bigint_subtract_absolute(abs_a, abs_b);
        bigint_free(abs_a);
        abs_a = temp;

        BigInt *new_quotient = bigint_add(quotient, one);
        bigint_free(quotient);
        quotient = new_quotient;
    }

    bigint_free(abs_a);
    bigint_free(abs_b);
    bigint_free(one);

    if (quotient) {
        quotient->sign = a->sign * b->sign;
    }

    return quotient;
}

BigInt* bigint_mod(const BigInt *a, const BigInt *b) {
    if (!a || !b) return NULL;

    // Modulo per zero
    if (bigint_is_zero(b)) {
        fprintf(stderr, "Errore: divisione per zero\n");
        return NULL;
    }

    // Calcola a % b come a - (a / b) * b
    BigInt *quotient = bigint_divide(a, b);
    if (!quotient) return NULL;

    BigInt *product = bigint_multiply(quotient, b);
    bigint_free(quotient);

    if (!product) return NULL;

    BigInt *remainder = bigint_subtract(a, product);
    bigint_free(product);

    return remainder;
}

char* bigint_to_string(const BigInt *bi) {
    if (!bi) return NULL;

    // Calcola la lunghezza della stringa
    size_t len = bi->length;
    if (bi->sign < 0) len++;

    char *str = (char*)malloc(len + 1);
    if (!str) return NULL;

    size_t pos = 0;

    // Aggiungi il segno
    if (bi->sign < 0) {
        str[pos++] = '-';
    }

    // Copia le cifre in ordine inverso
    for (size_t i = 0; i < bi->length; i++) {
        str[pos++] = bi->digits[bi->length - 1 - i] + '0';
    }

    str[pos] = '\0';
    return str;
}

int bigint_compare(const BigInt *a, const BigInt *b) {
    if (!a || !b) return 0;

    // Confronta i segni
    if (a->sign != b->sign) {
        return a->sign > b->sign ? 1 : -1;
    }

    // Confronta le lunghezze (valori assoluti)
    if (a->length != b->length) {
        if (a->sign > 0) {
            return a->length > b->length ? 1 : -1;
        } else {
            return a->length < b->length ? 1 : -1;
        }
    }

    // Confronta cifra per cifra
    for (int i = (int)a->length - 1; i >= 0; i--) {
        if (a->digits[i] != b->digits[i]) {
            if (a->sign > 0) {
                return a->digits[i] > b->digits[i] ? 1 : -1;
            } else {
                return a->digits[i] < b->digits[i] ? 1 : -1;
            }
        }
    }

    return 0; // Uguali
}

void bigint_print(const BigInt *bi) {
    if (!bi) {
        printf("NULL");
        return;
    }

    char *str = bigint_to_string(bi);
    if (str) {
        printf("%s", str);
        free(str);
    } else {
        printf("(errore conversione)");
    }
}

int bigint_is_zero(const BigInt *bi) {
    if (!bi) return 0;
    return bi->length == 1 && bi->digits[0] == 0;
}
