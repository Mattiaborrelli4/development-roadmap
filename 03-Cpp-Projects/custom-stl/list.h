#ifndef MY_LIST_H
#define MY_LIST_H

#include <cstddef>
#include <initializer_list>

namespace mystl {

template <typename T>
class MyLinkedList {
private:
    struct Node {
        T data;
        Node* next;
        Node* prev;

        Node() : next(nullptr), prev(nullptr) {}
        explicit Node(const T& value) : data(value), next(nullptr), prev(nullptr) {}
        explicit Node(T&& value) : data(std::move(value)), next(nullptr), prev(nullptr) {}
    };

public:
    // Iterator class
    class iterator {
    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;

        iterator() : current(nullptr) {}
        explicit iterator(Node* node) : current(node) {}

        reference operator*() const {
            return current->data;
        }

        pointer operator->() const {
            return &current->data;
        }

        iterator& operator++() {
            current = current->next;
            return *this;
        }

        iterator operator++(int) {
            iterator temp = *this;
            current = current->next;
            return temp;
        }

        iterator& operator--() {
            current = current->prev;
            return *this;
        }

        iterator operator--(int) {
            iterator temp = *this;
            current = current->prev;
            return temp;
        }

        bool operator==(const iterator& other) const {
            return current == other.current;
        }

        bool operator!=(const iterator& other) const {
            return current != other.current;
        }

        Node* get_node() const {
            return current;
        }

    private:
        Node* current;
    };

    // Const iterator class
    class const_iterator {
    public:
        using iterator_category = std::bidirectional_iterator_tag;
        using value_type = const T;
        using difference_type = std::ptrdiff_t;
        using pointer = const T*;
        using reference = const T&;

        const_iterator() : current(nullptr) {}
        explicit const_iterator(const Node* node) : current(node) {}
        const_iterator(const iterator& it) : current(it.get_node()) {}

        reference operator*() const {
            return current->data;
        }

        pointer operator->() const {
            return &current->data;
        }

        const_iterator& operator++() {
            current = current->next;
            return *this;
        }

        const_iterator operator++(int) {
            const_iterator temp = *this;
            current = current->next;
            return temp;
        }

        const_iterator& operator--() {
            current = current->prev;
            return *this;
        }

        const_iterator operator--(int) {
            const_iterator temp = *this;
            current = current->prev;
            return temp;
        }

        bool operator==(const const_iterator& other) const {
            return current == other.current;
        }

        bool operator!=(const const_iterator& other) const {
            return current != other.current;
        }

    private:
        const Node* current;
    };

    // Costruttore di default
    MyLinkedList();

    // Costruttore con initializer list
    MyLinkedList(std::initializer_list<T> init);

    // Copy constructor
    MyLinkedList(const MyLinkedList& other);

    // Move constructor
    MyLinkedList(MyLinkedList&& other) noexcept;

    // Destructor
    ~MyLinkedList();

    // Copy assignment
    MyLinkedList& operator=(const MyLinkedList& other);

    // Move assignment
    MyLinkedList& operator=(MyLinkedList&& other) noexcept;

    // Element access
    T& front();
    const T& front() const;

    T& back();
    const T& back() const;

    // Iterators
    iterator begin() noexcept;
    const_iterator begin() const noexcept;
    const_iterator cbegin() const noexcept;

    iterator end() noexcept;
    const_iterator end() const noexcept;
    const_iterator cend() const noexcept;

    // Capacity
    size_t size() const noexcept;
    bool empty() const noexcept;

    // Modifiers
    void clear() noexcept;

    void push_front(const T& value);
    void push_front(T&& value);

    void push_back(const T& value);
    void push_back(T&& value);

    void pop_front();
    void pop_back();

    iterator insert(iterator pos, const T& value);
    iterator insert(iterator pos, T&& value);

    iterator erase(iterator pos);
    iterator erase(iterator first, iterator last);

    void swap(MyLinkedList& other) noexcept;

private:
    Node* m_head;
    Node* m_tail;
    size_t m_size;

    void destroy_list();
};

} // namespace mystl

#include "list.tpp"

#endif // MY_LIST_H
