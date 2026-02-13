/**
 * @file bigint.cpp
 * @brief Implementazione della classe BigInt
 */

#include "bigint.h"
#include <stdexcept>
#include <algorithm>
#include <sstream>
#include <climits>

// ================== METODI HELPER PRIVATI ==================

void BigInt::removeLeadingZeros() {
    while (digits.size() > 1 && digits.back() == 0) {
        digits.pop_back();
    }

    // Se il numero è 0, assicuriamoci che non sia negativo
    if (digits.size() == 1 && digits[0] == 0) {
        negative = false;
    }
}

int BigInt::compareAbsolute(const BigInt& other) const {
    // Confronta prima il numero di cifre
    if (digits.size() != other.digits.size()) {
        return digits.size() < other.digits.size() ? -1 : 1;
    }

    // Stesso numero di cifre: confronta cifra per cifra dall'alto
    for (int i = digits.size() - 1; i >= 0; --i) {
        if (digits[i] != other.digits[i]) {
            return digits[i] < other.digits[i] ? -1 : 1;
        }
    }

    return 0; // Uguali
}

BigInt BigInt::addAbsolute(const BigInt& other) const {
    BigInt result;
    result.digits.clear();
    result.negative = false;

    int carry = 0;
    size_t maxSize = std::max(digits.size(), other.digits.size());

    for (size_t i = 0; i < maxSize || carry > 0; ++i) {
        int sum = carry;

        if (i < digits.size()) {
            sum += digits[i];
        }

        if (i < other.digits.size()) {
            sum += other.digits[i];
        }

        result.digits.push_back(sum % 10);
        carry = sum / 10;
    }

    return result;
}

BigInt BigInt::subtractAbsolute(const BigInt& other) const {
    // Assumiamo che *this >= other in valore assoluto
    BigInt result;
    result.digits.clear();
    result.negative = false;

    int borrow = 0;

    for (size_t i = 0; i < digits.size(); ++i) {
        int diff = digits[i] - borrow;

        if (i < other.digits.size()) {
            diff -= other.digits[i];
        }

        if (diff < 0) {
            diff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }

        result.digits.push_back(diff);
    }

    result.removeLeadingZeros();
    return result;
}

// ================== COSTRUTTORI ==================

BigInt::BigInt() : digits(1, 0), negative(false) {
}

BigInt::BigInt(long long n) {
    if (n < 0) {
        negative = true;
        n = -n;
    } else {
        negative = false;
    }

    // Gestisci il caso di LLONG_MIN
    if (n == LLONG_MIN) {
        digits.push_back(8);
        n = 922337203685477580; // LLONG_MAX / 10
    }

    if (n == 0) {
        digits.push_back(0);
    } else {
        while (n > 0) {
            digits.push_back(n % 10);
            n /= 10;
        }
    }
}

BigInt::BigInt(const std::string& s) {
    if (s.empty()) {
        throw std::invalid_argument("Stringa vuota non valida per BigInt");
    }

    size_t start = 0;
    negative = false;

    // Gestisci segno
    if (s[0] == '-') {
        negative = true;
        start = 1;
    } else if (s[0] == '+') {
        start = 1;
    }

    // Verifica che ci siano cifre dopo il segno
    if (start >= s.length()) {
        throw std::invalid_argument("Stringa non valida: solo segno senza cifre");
    }

    // Verifica caratteri validi
    for (size_t i = start; i < s.length(); ++i) {
        if (s[i] < '0' || s[i] > '9') {
            throw std::invalid_argument("Stringa contiene caratteri non validi");
        }
    }

    // Converti stringa (dalla fine all'inizio)
    digits.clear();
    for (int i = s.length() - 1; i >= static_cast<int>(start); --i) {
        digits.push_back(s[i] - '0');
    }

    removeLeadingZeros();
}

BigInt::BigInt(const BigInt& other) : digits(other.digits), negative(other.negative) {
}

BigInt::~BigInt() {
    // Vector gestisce la memoria automaticamente
}

// ================== ASSEGNAZIONE ==================

BigInt& BigInt::operator=(const BigInt& other) {
    if (this != &other) {
        digits = other.digits;
        negative = other.negative;
    }
    return *this;
}

// ================== OPERATORI ARITMETICI ==================

BigInt BigInt::operator+(const BigInt& other) const {
    BigInt result;

    if (negative == other.negative) {
        // Stesso segno: somma i valori assoluti e mantieni il segno
        result = addAbsolute(other);
        result.negative = negative;
    } else {
        // Segni opposti: sottrai il più piccolo dal più grande
        int cmp = compareAbsolute(other);

        if (cmp == 0) {
            // Valori assoluti uguali: risultato è 0
            result = BigInt();
        } else if (cmp > 0) {
            // |this| > |other|
            result = subtractAbsolute(other);
            result.negative = negative;
        } else {
            // |other| > |this|
            result = other.subtractAbsolute(*this);
            result.negative = other.negative;
        }
    }

    return result;
}

BigInt BigInt::operator-(const BigInt& other) const {
    BigInt tempOther = other;
    tempOther.negative = !other.negative; // Inverti il segno
    return *this + tempOther;
}

BigInt BigInt::operator*(const BigInt& other) const {
    BigInt result;
    result.digits.assign(digits.size() + other.digits.size(), 0);
    result.negative = negative != other.negative;

    // Moltiplicazione schoolbook O(n*m)
    for (size_t i = 0; i < digits.size(); ++i) {
        int carry = 0;

        for (size_t j = 0; j < other.digits.size() || carry > 0; ++j) {
            long long product = result.digits[i + j] + carry;

            if (j < other.digits.size()) {
                product += static_cast<long long>(digits[i]) * other.digits[j];
            }

            result.digits[i + j] = product % 10;
            carry = product / 10;
        }
    }

    result.removeLeadingZeros();
    return result;
}

BigInt BigInt::operator/(const BigInt& other) const {
    if (other.isZero()) {
        throw std::runtime_error("Divisione per zero");
    }

    BigInt dividend = this->absolute();
    BigInt divisor = other.absolute();

    // Caso speciale: dividendo più piccolo del divisore
    if (dividend.compareAbsolute(divisor) < 0) {
        return BigInt();
    }

    // Caso speciale: divisore uguale a 1
    if (divisor == BigInt(1)) {
        BigInt result = dividend;
        result.negative = negative != other.negative;
        return result;
    }

    BigInt remainder;
    BigInt quotient;
    quotient.digits.clear();

    // Long division: processa ogni cifra del dividendo (dalla più significativa)
    for (int i = dividend.digits.size() - 1; i >= 0; --i) {
        // remainder = remainder * 10 + cifra corrente
        if (remainder.isZero()) {
            remainder.digits = {dividend.digits[i]};
        } else {
            // Moltiplica remainder per 10
            remainder.digits.insert(remainder.digits.begin(), 0);
            // Aggiungi la nuova cifra (in fondo poiché digits è in ordine inverso)
            remainder.digits[0] = dividend.digits[i];
        }

        // Calcola quante volte divisor sta in remainder
        int count = 0;
        while (remainder.compareAbsolute(divisor) >= 0) {
            remainder = remainder.subtractAbsolute(divisor);
            ++count;
        }

        // Inserisci count all'inizio delle cifre del quoziente
        quotient.digits.insert(quotient.digits.begin(), count);
    }

    quotient.removeLeadingZeros();
    quotient.negative = negative != other.negative;

    return quotient;
}

BigInt BigInt::operator%(const BigInt& other) const {
    if (other.isZero()) {
        throw std::runtime_error("Modulo con divisore zero");
    }

    BigInt quotient = *this / other;
    BigInt product = quotient * other;
    BigInt remainder = *this - product;

    return remainder;
}

BigInt BigInt::operator-() const {
    BigInt result(*this);
    if (!isZero()) {
        result.negative = !negative;
    }
    return result;
}

// ================== OPERATORI DI CONFRONTO ==================

bool BigInt::operator==(const BigInt& other) const {
    if (negative != other.negative) {
        return false;
    }
    return compareAbsolute(other) == 0;
}

bool BigInt::operator!=(const BigInt& other) const {
    return !(*this == other);
}

bool BigInt::operator<(const BigInt& other) const {
    if (negative != other.negative) {
        return negative; // I negativi sono minori dei positivi
    }

    int cmp = compareAbsolute(other);

    if (negative) {
        // Entrambi negativi: confronto invertito
        return cmp > 0;
    } else {
        // Entrambi positivi: confronto normale
        return cmp < 0;
    }
}

bool BigInt::operator>(const BigInt& other) const {
    return other < *this;
}

bool BigInt::operator<=(const BigInt& other) const {
    return !(other < *this);
}

bool BigInt::operator>=(const BigInt& other) const {
    return !(*this < other);
}

// ================== OPERATORI DI STREAM ==================

std::ostream& operator<<(std::ostream& os, const BigInt& num) {
    os << num.toString();
    return os;
}

std::istream& operator>>(std::istream& is, BigInt& num) {
    std::string s;
    is >> s;

    try {
        num = BigInt(s);
    } catch (const std::invalid_argument&) {
        is.setstate(std::ios::failbit);
    }

    return is;
}

// ================== METODI DI CONVERSIONE ==================

std::string BigInt::toString() const {
    if (isZero()) {
        return "0";
    }

    std::ostringstream oss;

    if (negative) {
        oss << '-';
    }

    for (int i = digits.size() - 1; i >= 0; --i) {
        oss << digits[i];
    }

    return oss.str();
}

long BigInt::toLong() const {
    // Verifica overflow
    const long LONG_MAX_DIV_10 = LONG_MAX / 10;

    if (digits.size() > 19) { // 19 cifre in LONG_MAX
        throw std::overflow_error("Numero troppo grande per long");
    }

    long result = 0;
    for (int i = digits.size() - 1; i >= 0; --i) {
        if (result > LONG_MAX_DIV_10) {
            throw std::overflow_error("Numero troppo grande per long");
        }
        result = result * 10 + digits[i];
    }

    if (negative) {
        result = -result;
    }

    return result;
}

int BigInt::toInt() const {
    long l = toLong();

    if (l < INT_MIN || l > INT_MAX) {
        throw std::overflow_error("Numero troppo grande per int");
    }

    return static_cast<int>(l);
}

// ================== ALTRI METODI UTILI ==================

BigInt BigInt::absolute() const {
    BigInt result(*this);
    result.negative = false;
    return result;
}

bool BigInt::isNegative() const {
    return negative && !isZero();
}

bool BigInt::isZero() const {
    return digits.size() == 1 && digits[0] == 0;
}

size_t BigInt::numDigits() const {
    if (isZero()) {
        return 1;
    }
    return digits.size();
}
