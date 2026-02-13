/**
 * @file bigint.h
 * @brief Definizione della classe BigInt per operazioni su numeri interi arbitrariamente grandi
 * @author Matti
 * @date 2025
 *
 * Questa classe implementa un tipo di dato per gestire numeri interi
 * di dimensione arbitraria, superando i limiti dei tipi primitivi del C++.
 */

#ifndef BIGINT_H
#define BIGINT_H

#include <vector>
#include <string>
#include <iostream>

/**
 * @class BigInt
 * @brief Classe per la gestione di numeri interi arbitrariamente grandi
 *
 * La classe utilizza std::vector<int> per memorizzare le cifre del numero
 * e implementa operator overloading per tutte le operazioni aritmetiche
 * e di confronto standard.
 */
class BigInt {
private:
    std::vector<int> digits;  ///< Cifre del numero (0-9), memorizzate in ordine inverso
    bool negative;            ///< Flag per indicare se il numero è negativo

    // Metodi helper privati
    void removeLeadingZeros();              ///< Rimuove gli zeri in eccesso
    int compareAbsolute(const BigInt& other) const;  ///< Confronta valori assoluti
    BigInt addAbsolute(const BigInt& other) const;    ///< Addizione valori assoluti
    BigInt subtractAbsolute(const BigInt& other) const; ///< Sottrazione valori assoluti

public:
    // ================== COSTRUTTORI ==================

    /**
     * @brief Costruttore di default - inizializza a 0
     */
    BigInt();

    /**
     * @brief Costruttore da long long
     * @param n Numero da convertire in BigInt
     */
    BigInt(long long n);

    /**
     * @brief Costruttore da stringa
     * @param s Stringa rappresentante il numero (opzionalmente con segno + o -)
     * @throws std::invalid_argument se la stringa non è valida
     */
    BigInt(const std::string& s);

    /**
     * @brief Costruttore di copia
     * @param other Oggetto BigInt da copiare
     */
    BigInt(const BigInt& other);

    /**
     * @brief Distruttore
     */
    ~BigInt();

    // ================== ASSEGNAZIONE ==================

    /**
     * @brief Operatore di assegnazione
     * @param other Oggetto BigInt da assegnare
     * @return Riferimento a this
     */
    BigInt& operator=(const BigInt& other);

    // ================== OPERATORI ARITMETICI ==================

    /**
     * @brief Operatore di addizione
     * @param other Operando destro
     * @return Nuovo BigInt risultante dalla somma
     */
    BigInt operator+(const BigInt& other) const;

    /**
     * @brief Operatore di sottrazione
     * @param other Operando destro
     * @return Nuovo BigInt risultante dalla differenza
     */
    BigInt operator-(const BigInt& other) const;

    /**
     * @brief Operatore di moltiplicazione (algoritmo schoolbook)
     * @param other Operando destro
     * @return Nuovo BigInt risultante dal prodotto
     */
    BigInt operator*(const BigInt& other) const;

    /**
     * @brief Operatore di divisione intera
     * @param other Operando destro (divisore)
     * @return Nuovo BigInt risultante dalla divisione
     * @throws std::runtime_error se si tenta la divisione per zero
     */
    BigInt operator/(const BigInt& other) const;

    /**
     * @brief Operatore di modulo (resto della divisione)
     * @param other Operando destro (divisore)
     * @return Nuovo BigInt resto della divisione
     * @throws std::runtime_error se si tenta la divisione per zero
     */
    BigInt operator%(const BigInt& other) const;

    /**
     * @brief Operatore meno unario (cambia segno)
     * @return Nuovo BigInt con segno invertito
     */
    BigInt operator-() const;

    // ================== OPERATORI DI CONFRONTO ==================

    /**
     * @brief Operatore di uguaglianza
     * @param other Operando da confrontare
     * @return true se i numeri sono uguali
     */
    bool operator==(const BigInt& other) const;

    /**
     * @brief Operatore di disuguaglianza
     * @param other Operando da confrontare
     * @return true se i numeri sono diversi
     */
    bool operator!=(const BigInt& other) const;

    /**
     * @brief Operatore minore di
     * @param other Operando da confrontare
     * @return true se this è minore di other
     */
    bool operator<(const BigInt& other) const;

    /**
     * @brief Operatore maggiore di
     * @param other Operando da confrontare
     * @return true se this è maggiore di other
     */
    bool operator>(const BigInt& other) const;

    /**
     * @brief Operatore minore o uguale
     * @param other Operando da confrontare
     * @return true se this è minore o uguale a other
     */
    bool operator<=(const BigInt& other) const;

    /**
     * @brief Operatore maggiore o uguale
     * @param other Operando da confrontare
     * @return true se this è maggiore o uguale a other
     */
    bool operator>=(const BigInt& other) const;

    // ================== OPERATORI DI STREAM ==================

    /**
     * @brief Operatore di output (<<)
     * @param os Stream di output
     * @param num BigInt da stampare
     * @return Stream di output
     */
    friend std::ostream& operator<<(std::ostream& os, const BigInt& num);

    /**
     * @brief Operatore di input (>>)
     * @param is Stream di input
     * @param num BigInt in cui leggere
     * @return Stream di input
     */
    friend std::istream& operator>>(std::istream& is, BigInt& num);

    // ================== METODI DI CONVERSIONE ==================

    /**
     * @brief Conversione a stringa
     * @return Stringa rappresentante il numero
     */
    std::string toString() const;

    /**
     * @brief Conversione a long
     * @return Valore long del numero
     * @throws std::overflow_error se il numero è troppo grande
     */
    long toLong() const;

    /**
     * @brief Conversione a int
     * @return Valore int del numero
     * @throws std::overflow_error se il numero è troppo grande
     */
    int toInt() const;

    // ================== ALTRI METODI UTILI ==================

    /**
     * @brief Restituisce il valore assoluto
     * @return Nuovo BigInt con valore assoluto
     */
    BigInt absolute() const;

    /**
     * @brief Verifica se il numero è negativo
     * @return true se il numero è negativo
     */
    bool isNegative() const;

    /**
     * @brief Verifica se il numero è zero
     * @return true se il numero è zero
     */
    bool isZero() const;

    /**
     * @brief Restituisce il numero di cifre
     * @return Numero di cifre del numero
     */
    size_t numDigits() const;
};

#endif // BIGINT_H
