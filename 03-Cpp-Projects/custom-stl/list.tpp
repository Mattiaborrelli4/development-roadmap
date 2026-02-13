#ifndef LIST_TPP
#define LIST_TPP

#include <utility>

namespace mystl {

// ==================== Costruttori ====================

template <typename T>
MyLinkedList<T>::MyLinkedList()
    : m_head(nullptr), m_tail(nullptr), m_size(0) {
    m_head = new Node;
    m_tail = new Node;
    m_head->next = m_tail;
    m_tail->prev = m_head;
}

template <typename T>
MyLinkedList<T>::MyLinkedList(std::initializer_list<T> init)
    : MyLinkedList() {
    for (const auto& item : init) {
        push_back(item);
    }
}

template <typename T>
MyLinkedList<T>::MyLinkedList(const MyLinkedList& other)
    : MyLinkedList() {
    for (const auto& item : other) {
        push_back(item);
    }
}

template <typename T>
MyLinkedList<T>::MyLinkedList(MyLinkedList&& other) noexcept
    : m_head(other.m_head), m_tail(other.m_tail), m_size(other.m_size) {
    other.m_head = new Node;
    other.m_tail = new Node;
    other.m_head->next = other.m_tail;
    other.m_tail->prev = other.m_head;
    other.m_size = 0;
}

template <typename T>
MyLinkedList<T>::~MyLinkedList() {
    destroy_list();
    delete m_head;
    delete m_tail;
}

// ==================== Assignment Operators ====================

template <typename T>
MyLinkedList<T>& MyLinkedList<T>::operator=(const MyLinkedList& other) {
    if (this != &other) {
        MyLinkedList temp(other);
        swap(temp);
    }
    return *this;
}

template <typename T>
MyLinkedList<T>& MyLinkedList<T>::operator=(MyLinkedList&& other) noexcept {
    if (this != &other) {
        destroy_list();
        delete m_head;
        delete m_tail;

        m_head = other.m_head;
        m_tail = other.m_tail;
        m_size = other.m_size;

        other.m_head = new Node;
        other.m_tail = new Node;
        other.m_head->next = other.m_tail;
        other.m_tail->prev = other.m_head;
        other.m_size = 0;
    }
    return *this;
}

// ==================== Element Access ====================

template <typename T>
T& MyLinkedList<T>::front() {
    return m_head->next->data;
}

template <typename T>
const T& MyLinkedList<T>::front() const {
    return m_head->next->data;
}

template <typename T>
T& MyLinkedList<T>::back() {
    return m_tail->prev->data;
}

template <typename T>
const T& MyLinkedList<T>::back() const {
    return m_tail->prev->data;
}

// ==================== Iterators ====================

template <typename T>
typename MyLinkedList<T>::iterator MyLinkedList<T>::begin() noexcept {
    return iterator(m_head->next);
}

template <typename T>
typename MyLinkedList<T>::const_iterator MyLinkedList<T>::begin() const noexcept {
    return const_iterator(m_head->next);
}

template <typename T>
typename MyLinkedList<T>::const_iterator MyLinkedList<T>::cbegin() const noexcept {
    return const_iterator(m_head->next);
}

template <typename T>
typename MyLinkedList<T>::iterator MyLinkedList<T>::end() noexcept {
    return iterator(m_tail);
}

template <typename T>
typename MyLinkedList<T>::const_iterator MyLinkedList<T>::end() const noexcept {
    return const_iterator(m_tail);
}

template <typename T>
typename MyLinkedList<T>::const_iterator MyLinkedList<T>::cend() const noexcept {
    return const_iterator(m_tail);
}

// ==================== Capacity ====================

template <typename T>
size_t MyLinkedList<T>::size() const noexcept {
    return m_size;
}

template <typename T>
bool MyLinkedList<T>::empty() const noexcept {
    return m_size == 0;
}

// ==================== Modifiers ====================

template <typename T>
void MyLinkedList<T>::clear() noexcept {
    destroy_list();
    m_head->next = m_tail;
    m_tail->prev = m_head;
    m_size = 0;
}

template <typename T>
void MyLinkedList<T>::push_front(const T& value) {
    Node* new_node = new Node(value);
    new_node->prev = m_head;
    new_node->next = m_head->next;
    m_head->next->prev = new_node;
    m_head->next = new_node;
    ++m_size;
}

template <typename T>
void MyLinkedList<T>::push_front(T&& value) {
    Node* new_node = new Node(std::move(value));
    new_node->prev = m_head;
    new_node->next = m_head->next;
    m_head->next->prev = new_node;
    m_head->next = new_node;
    ++m_size;
}

template <typename T>
void MyLinkedList<T>::push_back(const T& value) {
    Node* new_node = new Node(value);
    new_node->next = m_tail;
    new_node->prev = m_tail->prev;
    m_tail->prev->next = new_node;
    m_tail->prev = new_node;
    ++m_size;
}

template <typename T>
void MyLinkedList<T>::push_back(T&& value) {
    Node* new_node = new Node(std::move(value));
    new_node->next = m_tail;
    new_node->prev = m_tail->prev;
    m_tail->prev->next = new_node;
    m_tail->prev = new_node;
    ++m_size;
}

template <typename T>
void MyLinkedList<T>::pop_front() {
    if (m_size > 0) {
        Node* to_delete = m_head->next;
        m_head->next = to_delete->next;
        to_delete->next->prev = m_head;
        delete to_delete;
        --m_size;
    }
}

template <typename T>
void MyLinkedList<T>::pop_back() {
    if (m_size > 0) {
        Node* to_delete = m_tail->prev;
        m_tail->prev = to_delete->prev;
        to_delete->prev->next = m_tail;
        delete to_delete;
        --m_size;
    }
}

template <typename T>
typename MyLinkedList<T>::iterator MyLinkedList<T>::insert(iterator pos, const T& value) {
    Node* new_node = new Node(value);
    Node* current = pos.get_node();

    new_node->prev = current->prev;
    new_node->next = current;
    current->prev->next = new_node;
    current->prev = new_node;
    ++m_size;

    return iterator(new_node);
}

template <typename T>
typename MyLinkedList<T>::iterator MyLinkedList<T>::insert(iterator pos, T&& value) {
    Node* new_node = new Node(std::move(value));
    Node* current = pos.get_node();

    new_node->prev = current->prev;
    new_node->next = current;
    current->prev->next = new_node;
    current->prev = new_node;
    ++m_size;

    return iterator(new_node);
}

template <typename T>
typename MyLinkedList<T>::iterator MyLinkedList<T>::erase(iterator pos) {
    Node* to_delete = pos.get_node();
    iterator result(to_delete->next);

    to_delete->prev->next = to_delete->next;
    to_delete->next->prev = to_delete->prev;
    delete to_delete;
    --m_size;

    return result;
}

template <typename T>
typename MyLinkedList<T>::iterator MyLinkedList<T>::erase(iterator first, iterator last) {
    while (first != last) {
        first = erase(first);
    }
    return last;
}

template <typename T>
void MyLinkedList<T>::swap(MyLinkedList& other) noexcept {
    std::swap(m_head, other.m_head);
    std::swap(m_tail, other.m_tail);
    std::swap(m_size, other.m_size);
}

// ==================== Private Methods ====================

template <typename T>
void MyLinkedList<T>::destroy_list() {
    Node* current = m_head->next;
    while (current != m_tail) {
        Node* to_delete = current;
        current = current->next;
        delete to_delete;
    }
}

} // namespace mystl

#endif // LIST_TPP
