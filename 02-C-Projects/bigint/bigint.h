/**
 * @file bigint.h
 * @brief Libreria per numeri interi arbitrariamente grandi
 *
 * Questa libreria implementa operazioni aritmetiche su interi di dimensione arbitraria
 * utilizzando un array di cifre decimali.
 */

#ifndef BIGINT_H
#define BIGINT_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/**
 * @struct BigInt
 * @brief Rappresenta un numero intero arbitrariamente grande
 *
 * @var BigInt::digits Array di cifre decimali (0-9), memorizzate little-endian
 * @var BigInt::length Numero di cifre nel numero
 * @var BigInt::sign Segno del numero (1 = positivo, -1 = negativo)
 */
typedef struct {
    char *digits;    // Array di cifre decimali
    size_t length;   // Numero di cifre
    int sign;        // 1 per positivo, -1 per negativo
} BigInt;

/**
 * @brief Crea un BigInt da un long intero
 * @param n Il numero intero da convertire
 * @return Puntatore al nuovo BigInt creato
 */
BigInt* bigint_create(long n);

/**
 * @brief Crea un BigInt da una stringa
 * @param str La stringa che rappresenta il numero (può includere segno +/-)
 * @return Puntatore al nuovo BigInt creato, NULL se errore di parsing
 */
BigInt* bigint_from_string(const char *str);

/**
 * @brief Libera la memoria allocata per un BigInt
 * @param bi Il BigInt da liberare
 */
void bigint_free(BigInt *bi);

/**
 * @brief Crea una copia di un BigInt
 * @param bi Il BigInt da copiare
 * @return Puntatore al nuovo BigInt copia
 */
BigInt* bigint_copy(const BigInt *bi);

/**
 * @brief Somma due BigInt
 * @param a Primo operando
 * @param b Secondo operando
 * @return Nuovo BigInt risultante dalla somma a + b
 */
BigInt* bigint_add(const BigInt *a, const BigInt *b);

/**
 * @brief Sottrae due BigInt
 * @param a Primo operando
 * @param b Secondo operando
 * @return Nuovo BigInt risultante dalla sottrazione a - b
 */
BigInt* bigint_subtract(const BigInt *a, const BigInt *b);

/**
 * @brief Moltiplica due BigInt (algoritmo schoolbook)
 * @param a Primo operando
 * @param b Secondo operando
 * @return Nuovo BigInt risultante dalla moltiplicazione a * b
 */
BigInt* bigint_multiply(const BigInt *a, const BigInt *b);

/**
 * @brief Divide due BigInt (divisione intera)
 * @param a Numeratore
 * @param b Denominatore
 * @return Nuovo BigInt risultante dalla divisione a / b
 */
BigInt* bigint_divide(const BigInt *a, const BigInt *b);

/**
 * @brief Calcola il modulo di due BigInt
 * @param a Numeratore
 * @param b Denominatore
 * @return Nuovo BigInt risultante da a % b
 */
BigInt* bigint_mod(const BigInt *a, const BigInt *b);

/**
 * @brief Converte un BigInt in una stringa
 * @param bi Il BigInt da convertire
 * @return Stringa allocata dinamicamente (deve essere liberata dal chiamante)
 */
char* bigint_to_string(const BigInt *bi);

/**
 * @brief Compara due BigInt
 * @param a Primo BigInt
 * @param b Secondo BigInt
 * @return -1 se a < b, 0 se a == b, 1 se a > b
 */
int bigint_compare(const BigInt *a, const BigInt *b);

/**
 * @brief Stampa un BigInt su stdout
 * @param bi Il BigInt da stampare
 */
void bigint_print(const BigInt *bi);

/**
 * @brief Verifica se un BigInt è zero
 * @param bi Il BigInt da verificare
 * @return 1 se è zero, 0 altrimenti
 */
int bigint_is_zero(const BigInt *bi);

#endif // BIGINT_H
