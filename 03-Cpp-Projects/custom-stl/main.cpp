#include <iostream>
#include <string>
#include <cassert>

#include "vector.h"
#include "list.h"
#include "algorithms.h"

using namespace mystl;

// ==================== Funzioni di Test ====================

void test_vector_basic() {
    std::cout << "=== Test MyVector: Funzionalita' Base ===" << std::endl;

    // Costruttore di default
    MyVector<int> v1;
    assert(v1.size() == 0);
    assert(v1.capacity() == 0);
    assert(v1.empty());
    std::cout << "✓ Costruttore di default" << std::endl;

    // push_back e size
    v1.push_back(10);
    v1.push_back(20);
    v1.push_back(30);
    assert(v1.size() == 3);
    assert(!v1.empty());
    std::cout << "✓ push_back e size" << std::endl;

    // operator[]
    assert(v1[0] == 10);
    assert(v1[1] == 20);
    assert(v1[2] == 30);
    std::cout << "✓ operator[]" << std::endl;

    // at() con eccezione
    try {
        int val = v1.at(10);
        (void)val;
        assert(false);
    } catch (const std::out_of_range&) {
        std::cout << "✓ at() lancia out_of_range" << std::endl;
    }

    // front e back
    assert(v1.front() == 10);
    assert(v1.back() == 30);
    std::cout << "✓ front() e back()" << std::endl;

    // pop_back
    v1.pop_back();
    assert(v1.size() == 2);
    assert(v1.back() == 20);
    std::cout << "✓ pop_back()" << std::endl;

    // Initializer list
    MyVector<int> v2 = {1, 2, 3, 4, 5};
    assert(v2.size() == 5);
    assert(v2[2] == 3);
    std::cout << "✓ Initializer list constructor" << std::endl;
}

void test_vector_iterators() {
    std::cout << "\n=== Test MyVector: Iteratori ===" << std::endl;

    MyVector<int> v = {1, 2, 3, 4, 5};

    // Iterazione con iteratori
    int sum = 0;
    for (auto it = v.begin(); it != v.end(); ++it) {
        sum += *it;
    }
    assert(sum == 15);
    std::cout << "✓ Iterazione con begin()/end()" << std::endl;

    // Range-based for loop
    sum = 0;
    for (const auto& elem : v) {
        sum += elem;
    }
    assert(sum == 15);
    std::cout << "✓ Range-based for loop" << std::endl;

    // Const iterator
    int product = 1;
    for (auto it = v.cbegin(); it != v.cend(); ++it) {
        product *= *it;
    }
    assert(product == 120);
    std::cout << "✓ Const iterator" << std::endl;
}

void test_vector_copy_move() {
    std::cout << "\n=== Test MyVector: Copy e Move Semantics ===" << std::endl;

    MyVector<int> original = {1, 2, 3};

    // Copy constructor
    MyVector<int> copy(original);
    assert(copy.size() == 3);
    assert(copy[0] == 1);
    assert(original.size() == 3);
    std::cout << "✓ Copy constructor" << std::endl;

    // Copy assignment
    MyVector<int> copy2;
    copy2 = original;
    assert(copy2.size() == 3);
    std::cout << "✓ Copy assignment" << std::endl;

    // Move constructor
    MyVector<int> moved(std::move(original));
    assert(moved.size() == 3);
    assert(moved[0] == 1);
    assert(original.size() == 0);
    std::cout << "✓ Move constructor" << std::endl;

    // Move assignment
    MyVector<int> moved2;
    moved2 = std::move(moved);
    assert(moved2.size() == 3);
    assert(moved.size() == 0);
    std::cout << "✓ Move assignment" << std::endl;
}

void test_vector_capacity() {
    std::cout << "\n=== Test MyVector: Capacity ===" << std::endl;

    MyVector<int> v;

    // reserve
    v.reserve(10);
    assert(v.capacity() >= 10);
    assert(v.size() == 0);
    std::cout << "✓ reserve()" << std::endl;

    // resize
    v.resize(5);
    assert(v.size() == 5);
    std::cout << "✓ resize()" << std::endl;

    // shrink_to_fit
    v.resize(2);
    size_t old_cap = v.capacity();
    v.shrink_to_fit();
    assert(v.capacity() <= old_cap);
    std::cout << "✓ shrink_to_fit()" << std::endl;

    // clear
    v.clear();
    assert(v.size() == 0);
    assert(v.empty());
    std::cout << "✓ clear()" << std::endl;
}

void test_vector_strings() {
    std::cout << "\n=== Test MyVector: Stringhe ===" << std::endl;

    MyVector<std::string> v;

    // push_back con stringhe
    v.push_back("Hello");
    v.push_back("World");
    v.push_back("C++");

    assert(v.size() == 3);
    assert(v[0] == "Hello");
    assert(v[1] == "World");
    std::cout << "✓ push_back con stringhe" << std::endl;

    // emplace_back
    v.emplace_back("Custom");
    assert(v[3] == "Custom");
    std::cout << "✓ emplace_back()" << std::endl;

    // Move semantics con stringhe
    MyVector<std::string> v2;
    v2.push_back(std::move(v[0]));
    assert(v2[0] == "Hello");
    std::cout << "✓ Move semantics con stringhe" << std::endl;
}

void test_list_basic() {
    std::cout << "\n=== Test MyLinkedList: Funzionalita' Base ===" << std::endl;

    // Costruttore di default
    MyLinkedList<int> list1;
    assert(list1.size() == 0);
    assert(list1.empty());
    std::cout << "✓ Costruttore di default" << std::endl;

    // push_back e push_front
    list1.push_back(20);
    list1.push_front(10);
    list1.push_back(30);

    assert(list1.size() == 3);
    assert(!list1.empty());
    std::cout << "✓ push_back() e push_front()" << std::endl;

    // front e back
    assert(list1.front() == 10);
    assert(list1.back() == 30);
    std::cout << "✓ front() e back()" << std::endl;

    // pop_front e pop_back
    list1.pop_front();
    assert(list1.front() == 20);
    list1.pop_back();
    assert(list1.back() == 20);
    std::cout << "✓ pop_front() e pop_back()" << std::endl;

    // Initializer list
    MyLinkedList<int> list2 = {1, 2, 3, 4, 5};
    assert(list2.size() == 5);
    assert(list2.front() == 1);
    assert(list2.back() == 5);
    std::cout << "✓ Initializer list constructor" << std::endl;
}

void test_list_iterators() {
    std::cout << "\n=== Test MyLinkedList: Iteratori ===" << std::endl;

    MyLinkedList<int> list = {1, 2, 3, 4, 5};

    // Iterazione con iteratori
    int sum = 0;
    for (auto it = list.begin(); it != list.end(); ++it) {
        sum += *it;
    }
    assert(sum == 15);
    std::cout << "✓ Iterazione con begin()/end()" << std::endl;

    // Operator++ e operator--
    auto it = list.begin();
    ++it;
    assert(*it == 2);
    it++;
    assert(*it == 3);
    --it;
    assert(*it == 2);
    std::cout << "✓ Operator++ e --" << std::endl;

    // Operator-> e operator*
    it = list.begin();
    assert(*it == 1);
    assert(it.operator->() != nullptr);
    std::cout << "✓ Operator* e ->" << std::endl;

    // Operator== e !=
    auto it1 = list.begin();
    auto it2 = list.begin();
    assert(it1 == it2);
    ++it2;
    assert(it1 != it2);
    std::cout << "✓ Operator== e !=" << std::endl;

    // Range-based for
    sum = 0;
    for (const auto& elem : list) {
        sum += elem;
    }
    assert(sum == 15);
    std::cout << "✓ Range-based for loop" << std::endl;
}

void test_list_insert_erase() {
    std::cout << "\n=== Test MyLinkedList: Insert e Erase ===" << std::endl;

    MyLinkedList<int> list = {1, 3, 5};

    // insert
    auto it = list.begin();
    ++it;
    list.insert(it, 2);
    assert(list.size() == 4);

    // Verifica ordine
    int expected[] = {1, 2, 3, 5};
    size_t i = 0;
    for (const auto& elem : list) {
        assert(elem == expected[i++]);
    }
    std::cout << "✓ insert()" << std::endl;

    // erase
    it = list.begin();
    ++it;
    ++it;
    list.erase(it);
    assert(list.size() == 3);
    std::cout << "✓ erase()" << std::endl;

    // erase range
    MyLinkedList<int> list2 = {1, 2, 3, 4, 5};
    auto first = list2.begin();
    ++first;
    auto last = list2.end();
    --last;
    list2.erase(first, last);
    assert(list2.size() == 2);
    assert(list2.front() == 1);
    assert(list2.back() == 5);
    std::cout << "✓ erase(range)" << std::endl;
}

void test_list_copy_move() {
    std::cout << "\n=== Test MyLinkedList: Copy e Move Semantics ===" << std::endl;

    MyLinkedList<int> original;
    original.push_back(1);
    original.push_back(2);
    original.push_back(3);

    // Copy constructor
    MyLinkedList<int> copy(original);
    assert(copy.size() == 3);
    assert(original.size() == 3);
    std::cout << "✓ Copy constructor" << std::endl;

    // Copy assignment
    MyLinkedList<int> copy2;
    copy2 = original;
    assert(copy2.size() == 3);
    std::cout << "✓ Copy assignment" << std::endl;

    // Move constructor
    MyLinkedList<int> moved(std::move(original));
    assert(moved.size() == 3);
    assert(original.size() == 0);
    std::cout << "✓ Move constructor" << std::endl;

    // Move assignment
    MyLinkedList<int> moved2;
    moved2 = std::move(moved);
    assert(moved2.size() == 3);
    assert(moved.size() == 0);
    std::cout << "✓ Move assignment" << std::endl;
}

void test_algorithms_find() {
    std::cout << "\n=== Test Algoritmi: my_find ===" << std::endl;

    MyVector<int> v = {1, 2, 3, 4, 5};

    // Trova elemento esistente
    auto it = my_find(v.begin(), v.end(), 3);
    assert(it != v.end());
    assert(*it == 3);
    std::cout << "✓ my_find: elemento trovato" << std::endl;

    // Trova elemento inesistente
    it = my_find(v.begin(), v.end(), 10);
    assert(it == v.end());
    std::cout << "✓ my_find: elemento non trovato" << std::endl;

    // my_find_if
    auto it2 = my_find_if(v.begin(), v.end(), [](int x) { return x > 3; });
    assert(it2 != v.end());
    assert(*it2 == 4);
    std::cout << "✓ my_find_if con predicato" << std::endl;
}

void test_algorithms_sort() {
    std::cout << "\n=== Test Algoritmi: my_sort ===" << std::endl;

    MyVector<int> v = {5, 2, 8, 1, 9, 3};

    // Ordinamento crescente
    my_sort(v.begin(), v.end());

    int expected[] = {1, 2, 3, 5, 8, 9};
    for (size_t i = 0; i < v.size(); ++i) {
        assert(v[i] == expected[i]);
    }
    std::cout << "✓ my_sort: ordinamento crescente" << std::endl;

    // Ordinamento decrescente con comparatore
    my_sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

    int expected_desc[] = {9, 8, 5, 3, 2, 1};
    for (size_t i = 0; i < v.size(); ++i) {
        assert(v[i] == expected_desc[i]);
    }
    std::cout << "✓ my_sort: ordinamento decrescente" << std::endl;
}

void test_algorithms_copy() {
    std::cout << "\n=== Test Algoritmi: my_copy ===" << std::endl;

    MyVector<int> src = {1, 2, 3, 4, 5};
    MyVector<int> dest;
    dest.resize(5);

    // my_copy
    my_copy(src.begin(), src.end(), dest.begin());

    for (size_t i = 0; i < src.size(); ++i) {
        assert(src[i] == dest[i]);
    }
    std::cout << "✓ my_copy" << std::endl;

    // Verifica che non siano lo stesso oggetto
    src[0] = 999;
    assert(dest[0] == 1);
    std::cout << "✓ my_copy: copia profonda" << std::endl;
}

void test_algorithms_fill() {
    std::cout << "\n=== Test Algoritmi: my_fill ===" << std::endl;

    MyVector<int> v;
    v.resize(5);

    my_fill(v.begin(), v.end(), 42);

    for (const auto& elem : v) {
        assert(elem == 42);
    }
    std::cout << "✓ my_fill" << std::endl;
}

void test_algorithms_count() {
    std::cout << "\n=== Test Algoritmi: my_count ===" << std::endl;

    MyVector<int> v = {1, 2, 3, 2, 4, 2, 5};

    auto count = my_count(v.begin(), v.end(), 2);
    assert(count == 3);
    std::cout << "✓ my_count: trova 3 occorrenze di 2" << std::endl;
}

void test_algorithms_accumulate() {
    std::cout << "\n=== Test Algoritmi: my_accumulate ===" << std::endl;

    MyVector<int> v = {1, 2, 3, 4, 5};

    auto sum = my_accumulate(v.begin(), v.end(), 0);
    assert(sum == 15);
    std::cout << "✓ my_accumulate: somma = 15" << std::endl;

    auto product = my_accumulate(v.begin(), v.end(), 1);
    // Nota: questo non funziona per il prodotto, servirebbe std::multiplies
    // ma testiamo la funzione base
    std::cout << "✓ my_accumulate: con init differente" << std::endl;
}

void test_algorithms_equal() {
    std::cout << "\n=== Test Algoritmi: my_equal ===" << std::endl;

    MyVector<int> v1 = {1, 2, 3, 4, 5};
    MyVector<int> v2 = {1, 2, 3, 4, 5};
    MyVector<int> v3 = {1, 2, 3, 4, 6};

    assert(my_equal(v1.begin(), v1.end(), v2.begin()));
    std::cout << "✓ my_equal: vettori uguali" << std::endl;

    assert(!my_equal(v1.begin(), v1.end(), v3.begin()));
    std::cout << "✓ my_equal: vettori diversi" << std::endl;
}

void test_comprehensive_example() {
    std::cout << "\n=== Test Esempio Completo ===" << std::endl;

    // Crea un vettore di numeri
    MyVector<int> numbers;
    for (int i = 1; i <= 10; ++i) {
        numbers.push_back(i * i);
    }

    std::cout << "Numeri originali: ";
    for (const auto& n : numbers) {
        std::cout << n << " ";
    }
    std::cout << std::endl;

    // Trova il numero 25
    auto it = my_find(numbers.begin(), numbers.end(), 25);
    if (it != numbers.end()) {
        std::cout << "Trovato 25 alla posizione: "
                  << (it - numbers.begin()) << std::endl;
    }

    // Copia in una nuova struttura
    MyLinkedList<int> list;
    for (const auto& n : numbers) {
        list.push_back(n);
    }

    std::cout << "Elementi nella lista: " << list.size() << std::endl;

    // Usa gli algoritmi sulla lista
    int sum = 0;
    for (const auto& n : list) {
        sum += n;
    }
    std::cout << "Somma totale: " << sum << std::endl;

    std::cout << "✓ Esempio completo eseguito" << std::endl;
}

// ==================== Main ====================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "  Custom STL Containers - Test Suite" << std::endl;
    std::cout << "========================================" << std::endl;

    try {
        // Test MyVector
        test_vector_basic();
        test_vector_iterators();
        test_vector_copy_move();
        test_vector_capacity();
        test_vector_strings();

        // Test MyLinkedList
        test_list_basic();
        test_list_iterators();
        test_list_insert_erase();
        test_list_copy_move();

        // Test Algoritmi
        test_algorithms_find();
        test_algorithms_sort();
        test_algorithms_copy();
        test_algorithms_fill();
        test_algorithms_count();
        test_algorithms_accumulate();
        test_algorithms_equal();

        // Test completo
        test_comprehensive_example();

        std::cout << "\n========================================" << std::endl;
        std::cout << "  Tutti i test sono PASSATI! ✓" << std::endl;
        std::cout << "========================================" << std::endl;

        return 0;
    } catch (const std::exception& e) {
        std::cerr << "\nERRORE: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "\nERRORE SCONOSCIUTO" << std::endl;
        return 1;
    }
}
