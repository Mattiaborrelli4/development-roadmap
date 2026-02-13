#ifndef VECTOR_TPP
#define VECTOR_TPP

#include <algorithm>
#include <memory>
#include <utility>

namespace mystl {

// ==================== Costruttori ====================

template <typename T>
MyVector<T>::MyVector() noexcept
    : m_data(nullptr), m_size(0), m_capacity(0) {}

template <typename T>
MyVector<T>::MyVector(size_t count)
    : m_data(nullptr), m_size(0), m_capacity(0) {
    resize(count);
}

template <typename T>
MyVector<T>::MyVector(std::initializer_list<T> init)
    : m_data(nullptr), m_size(0), m_capacity(0) {
    reserve(init.size());
    for (const auto& item : init) {
        push_back(item);
    }
}

template <typename T>
MyVector<T>::MyVector(const MyVector& other)
    : m_data(nullptr), m_size(0), m_capacity(0) {
    reserve(other.m_size);
    for (size_t i = 0; i < other.m_size; ++i) {
        push_back(other.m_data[i]);
    }
}

template <typename T>
MyVector<T>::MyVector(MyVector&& other) noexcept
    : m_data(other.m_data), m_size(other.m_size), m_capacity(other.m_capacity) {
    other.m_data = nullptr;
    other.m_size = 0;
    other.m_capacity = 0;
}

template <typename T>
MyVector<T>::~MyVector() {
    clear();
    ::operator delete(m_data, m_capacity * sizeof(T));
}

// ==================== Assignment Operators ====================

template <typename T>
MyVector<T>& MyVector<T>::operator=(const MyVector& other) {
    if (this != &other) {
        MyVector temp(other);
        swap(temp);
    }
    return *this;
}

template <typename T>
MyVector<T>& MyVector<T>::operator=(MyVector&& other) noexcept {
    if (this != &other) {
        clear();
        ::operator delete(m_data, m_capacity * sizeof(T));

        m_data = other.m_data;
        m_size = other.m_size;
        m_capacity = other.m_capacity;

        other.m_data = nullptr;
        other.m_size = 0;
        other.m_capacity = 0;
    }
    return *this;
}

// ==================== Element Access ====================

template <typename T>
T& MyVector<T>::operator[](size_t index) {
    return m_data[index];
}

template <typename T>
const T& MyVector<T>::operator[](size_t index) const {
    return m_data[index];
}

template <typename T>
T& MyVector<T>::at(size_t index) {
    if (index >= m_size) {
        throw std::out_of_range("MyVector::at: index out of range");
    }
    return m_data[index];
}

template <typename T>
const T& MyVector<T>::at(size_t index) const {
    if (index >= m_size) {
        throw std::out_of_range("MyVector::at: index out of range");
    }
    return m_data[index];
}

template <typename T>
T& MyVector<T>::front() {
    return m_data[0];
}

template <typename T>
const T& MyVector<T>::front() const {
    return m_data[0];
}

template <typename T>
T& MyVector<T>::back() {
    return m_data[m_size - 1];
}

template <typename T>
const T& MyVector<T>::back() const {
    return m_data[m_size - 1];
}

template <typename T>
T* MyVector<T>::data() noexcept {
    return m_data;
}

template <typename T>
const T* MyVector<T>::data() const noexcept {
    return m_data;
}

// ==================== Iterators ====================

template <typename T>
T* MyVector<T>::begin() noexcept {
    return m_data;
}

template <typename T>
const T* MyVector<T>::begin() const noexcept {
    return m_data;
}

template <typename T>
const T* MyVector<T>::cbegin() const noexcept {
    return m_data;
}

template <typename T>
T* MyVector<T>::end() noexcept {
    return m_data + m_size;
}

template <typename T>
const T* MyVector<T>::end() const noexcept {
    return m_data + m_size;
}

template <typename T>
const T* MyVector<T>::cend() const noexcept {
    return m_data + m_size;
}

// ==================== Capacity ====================

template <typename T>
size_t MyVector<T>::size() const noexcept {
    return m_size;
}

template <typename T>
size_t MyVector<T>::capacity() const noexcept {
    return m_capacity;
}

template <typename T>
bool MyVector<T>::empty() const noexcept {
    return m_size == 0;
}

template <typename T>
void MyVector<T>::reserve(size_t new_cap) {
    if (new_cap > m_capacity) {
        reallocate(new_cap);
    }
}

template <typename T>
void MyVector<T>::shrink_to_fit() {
    if (m_size < m_capacity) {
        reallocate(m_size);
    }
}

// ==================== Modifiers ====================

template <typename T>
void MyVector<T>::clear() noexcept {
    for (size_t i = 0; i < m_size; ++i) {
        m_data[i].~T();
    }
    m_size = 0;
}

template <typename T>
void MyVector<T>::push_back(const T& value) {
    if (m_size >= m_capacity) {
        reserve(m_capacity == 0 ? 1 : m_capacity * 2);
    }
    new (&m_data[m_size]) T(value);
    ++m_size;
}

template <typename T>
void MyVector<T>::push_back(T&& value) {
    if (m_size >= m_capacity) {
        reserve(m_capacity == 0 ? 1 : m_capacity * 2);
    }
    new (&m_data[m_size]) T(std::move(value));
    ++m_size;
}

template <typename T>
void MyVector<T>::pop_back() {
    if (m_size > 0) {
        --m_size;
        m_data[m_size].~T();
    }
}

template <typename T>
template <typename... Args>
void MyVector<T>::emplace_back(Args&&... args) {
    if (m_size >= m_capacity) {
        reserve(m_capacity == 0 ? 1 : m_capacity * 2);
    }
    new (&m_data[m_size]) T(std::forward<Args>(args)...);
    ++m_size;
}

template <typename T>
void MyVector<T>::resize(size_t count) {
    if (count < m_size) {
        for (size_t i = count; i < m_size; ++i) {
            m_data[i].~T();
        }
    } else if (count > m_size) {
        reserve(count);
        for (size_t i = m_size; i < count; ++i) {
            new (&m_data[i]) T();
        }
    }
    m_size = count;
}

template <typename T>
void MyVector<T>::swap(MyVector& other) noexcept {
    std::swap(m_data, other.m_data);
    std::swap(m_size, other.m_size);
    std::swap(m_capacity, other.m_capacity);
}

// ==================== Private Methods ====================

template <typename T>
void MyVector<T>::reallocate(size_t new_capacity) {
    // Alloca nuova memoria
    T* new_data = static_cast<T*>(::operator new(new_capacity * sizeof(T)));

    // Move costruisce gli elementi esistenti
    for (size_t i = 0; i < m_size; ++i) {
        new (&new_data[i]) T(std::move(m_data[i]));
        m_data[i].~T();
    }

    // Dealloca vecchia memoria
    ::operator delete(m_data, m_capacity * sizeof(T));

    m_data = new_data;
    m_capacity = new_capacity;
}

} // namespace mystl

#endif // VECTOR_TPP
