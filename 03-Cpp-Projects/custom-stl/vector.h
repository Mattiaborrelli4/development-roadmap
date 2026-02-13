#ifndef MY_VECTOR_H
#define MY_VECTOR_H

#include <cstddef>
#include <initializer_list>
#include <stdexcept>

namespace mystl {

template <typename T>
class MyVector {
public:
    // Costruttore di default
    MyVector() noexcept;

    // Costruttore con size
    explicit MyVector(size_t count);

    // Costruttore con initializer list
    MyVector(std::initializer_list<T> init);

    // Copy constructor
    MyVector(const MyVector& other);

    // Move constructor
    MyVector(MyVector&& other) noexcept;

    // Destructor
    ~MyVector();

    // Copy assignment
    MyVector& operator=(const MyVector& other);

    // Move assignment
    MyVector& operator=(MyVector&& other) noexcept;

    // Element access
    T& operator[](size_t index);
    const T& operator[](size_t index) const;

    T& at(size_t index);
    const T& at(size_t index) const;

    T& front();
    const T& front() const;

    T& back();
    const T& back() const;

    T* data() noexcept;
    const T* data() const noexcept;

    // Iterators
    T* begin() noexcept;
    const T* begin() const noexcept;
    const T* cbegin() const noexcept;

    T* end() noexcept;
    const T* end() const noexcept;
    const T* cend() const noexcept;

    // Capacity
    size_t size() const noexcept;
    size_t capacity() const noexcept;
    bool empty() const noexcept;

    void reserve(size_t new_cap);
    void shrink_to_fit();

    // Modifiers
    void clear() noexcept;

    void push_back(const T& value);
    void push_back(T&& value);

    void pop_back();

    template <typename... Args>
    void emplace_back(Args&&... args);

    void resize(size_t count);

    void swap(MyVector& other) noexcept;

private:
    T* m_data;
    size_t m_size;
    size_t m_capacity;

    void reallocate(size_t new_capacity);
};

} // namespace mystl

#include "vector.tpp"

#endif // MY_VECTOR_H
