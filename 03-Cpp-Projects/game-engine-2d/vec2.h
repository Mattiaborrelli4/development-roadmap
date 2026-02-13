/**
 * @file vec2.h
 * @brief Struttura Vec2 per operazioni vettoriali 2D
 */

#ifndef VEC2_H
#define VEC2_H

#include <cmath>

namespace GameEngine {

/**
 * @struct Vec2
 * @brief Vettore 2D con operazioni matematiche base
 */
struct Vec2 {
    float x;
    float y;

    // Costruttori
    Vec2() : x(0.0f), y(0.0f) {}
    Vec2(float x, float y) : x(x), y(y) {}

    // Operatori aritmetici
    Vec2 operator+(const Vec2& other) const {
        return Vec2(x + other.x, y + other.y);
    }

    Vec2 operator-(const Vec2& other) const {
        return Vec2(x - other.x, y - other.y);
    }

    Vec2 operator*(float scalar) const {
        return Vec2(x * scalar, y * scalar);
    }

    Vec2 operator/(float scalar) const {
        return Vec2(x / scalar, y / scalar);
    }

    // Operatori di assegnazione
    Vec2& operator+=(const Vec2& other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    Vec2& operator-=(const Vec2& other) {
        x -= other.x;
        y -= other.y;
        return *this;
    }

    Vec2& operator*=(float scalar) {
        x *= scalar;
        y *= scalar;
        return *this;
    }

    // Confronto
    bool operator==(const Vec2& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Vec2& other) const {
        return !(*this == other);
    }

    // Lunghezza del vettore
    float length() const {
        return std::sqrt(x * x + y * y);
    }

    // Normalizzazione
    Vec2 normalized() const {
        float len = length();
        if (len > 0.0f) {
            return Vec2(x / len, y / len);
        }
        return Vec2(0.0f, 0.0f);
    }

    // Distanza tra due punti
    float distanceTo(const Vec2& other) const {
        return (*this - other).length();
    }

    // Prodotto scalare
    float dot(const Vec2& other) const {
        return x * other.x + y * other.y;
    }
};

} // namespace GameEngine

#endif // VEC2_H
