# Architettura Custom STL Containers

## Overview del Progetto

```
┌─────────────────────────────────────────────────────────────┐
│                    Custom STL Containers                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ MyVector<T> │  │MyLinkedList<T>│  │  Algorithms     │    │
│  │             │  │              │  │                 │    │
│  │ • Dynamic   │  │ • Doubly     │  │ • my_sort       │    │
│  │   Array     │  │   Linked     │  │ • my_find       │    │
│  │ • Random    │  │   List       │  │ • my_copy       │    │
│  │   Access    │  │ • Sequential │  │ • my_move       │    │
│  │ • O(1)      │  │   Access     │  │ • my_fill       │    │
│  │   []        │  │ • O(1)       │  │ • my_equal      │    │
│  │             │  │   insert/    │  │ • my_count      │    │
│  │             │  │   erase      │  │ • my_accumulate │    │
│  └─────────────┘  └──────────────┘  └─────────────────┘    │
│         │                  │                    │           │
│         └──────────────────┴────────────────────┘           │
│                          │                                  │
│                 ┌────────▼────────┐                         │
│                 │   C++17 Core    │                         │
│                 │                 │                         │
│                 │ • Templates     │                         │
│                 │ • Move Semantics│                         │
│                 │ • RAII          │                         │
│                 │ • Iterators     │                         │
│                 └─────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## MyVector Internals

```
┌────────────────────────────────────────────────────────┐
│                    MyVector<int>                        │
├────────────────────────────────────────────────────────┤
│  m_data ───► [10][20][30][40][50][  ][  ][  ]            │
│                  ↑                                      │
│  m_size ────────┘ (5 elementi)                          │
│                                                         │
│  m_capacity ─────────► 8 (spazio allocato)              │
└────────────────────────────────────────────────────────┘

Memoria (Heap):
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│  10  │  20  │  30  │  40  │  50  │  ?   │  ?   │  ?   │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
   0      1      2      3      4      5      6      7
   └───────────────────────────────────────┘
                m_size (5)
   └───────────────────────────────────────────────────────┘
                        m_capacity (8)

Iteratori:
begin() ──► m_data
end()   ──► m_data + m_size
```

## MyLinkedList Internals

```
┌────────────────────────────────────────────────────────────┐
│                 MyLinkedList<int>                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  m_head  m_tail                                             │
│    │       │                                                │
│    ▼       ▼                                                │
│  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐            │
│  │dummy│◄─►│ 10  │◄─►│ 20  │◄─►│ 30  │◄─►│dummy│            │
│  │node │   │node │   │node │   │node │   │node │           │
│  └─────┘   └─────┘   └─────┘   └─────┘   └─────┘           │
│    ▲                                                   ▲    │
│    │ begin()                                          │    │
│    └──────────────────────────────────────────────────┘    │
│                            end()                            │
│                                                             │
│  m_size = 3                                                 │
└────────────────────────────────────────────────────────────┘

Struttura Node:
┌─────────────────────────┐
│  struct Node {           │
│    T data;               │
│    Node* next;           │
│    Node* prev;           │
│  };                      │
└─────────────────────────┘

Esempio nodo con valore 20:
┌────────────────┐
│    prev       │ ─────► nodo precedente
├────────────────┤
│    data = 20  │
├────────────────┤
│    next       │ ─────► nodo successivo
└────────────────┘
```

## Iterator Hierarchy

```
                 std::iterator_traits
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    Input        Forward          Bidirectional
   Iterator       Iterator            Iterator
        │               │                   │
        │               │                   │
   MyVector:      MyVector:        MyLinkedList:
   Random Access Random Access    Bidirectional
   Iterator       Iterator         Iterator

MyVector Iterator Operations:
• operator*()        → T& (dereference)
• operator++()       → Pre-increment
• operator++(int)    → Post-increment
• operator+(n)       → Random access
• operator-(n)       → Random access
• operator[](n)      → Random access
• operator<, >, etc. → Comparison

MyLinkedList Iterator Operations:
• operator*()        → T& (dereference)
• operator->()       → T* (member access)
• operator++()       → Pre-increment
• operator++(int)    → Post-increment
• operator--()       → Pre-decrement
• operator--(int)    → Post-decrement
• operator==, !=     → Equality
```

## MyVector - Memory Allocation Strategy

```
Growth Strategy: raddoppio capacity quando pieno

Initial:
┌────────┐
│ m_size │ 0
├────────┤
│m_cap   │ 0
└────────┘
m_data = nullptr

push_back(10):
┌───┐
│ 10│
└───┘
m_size=1, m_cap=1

push_back(20), push_back(30):
┌───┬───┬───┐
│ 10│ 20│ 30│
└───┴───┴───┘
m_size=3, m_cap=4  (doppio di prima)

push_back(40), push_back(50):
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 10│ 20│ 30│ 40│ 50│   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┘
m_size=5, m_cap=8  (doppio di prima)

Reallocation Process:
1. Allocare nuovo array più grande
2. Move costruire elementi in nuova memoria
3. Distruggere elementi vecchi
4. Deallocare vecchia memoria
5. Aggiornare puntatore m_data
```

## Move Semantics Visualization

```
Copy Semantics (Costoso):
┌─────────────┐                 ┌─────────────┐
│  source     │                 │  dest       │
│             │    copy         │             │
│  data ──────┼────────────────►│  data       │
│             │                 │             │
└─────────────┘                 └─────────────┘
     ▲                               ▲
     │                               │
   [10,20,30]                     [10,20,30]
                                     (duplicato)

Move Semantics (Efficiente):
┌─────────────┐                 ┌─────────────┐
│  source     │                 │  dest       │
│             │    move         │             │
│  data ──────┼────────────────►│  data       │
│             │                 │             │
└─────────────┘                 └─────────────┘
     ▲                               ▲
     │                               │
   nullptr                        [10,20,30]
                               (rubato, non duplicato)
```

## Algorithms - QuickSort Visualization

```
my_sort([5, 2, 8, 1, 9, 3])

Passo 1: Partition
Pivot = 8 (middle)

[5, 2, 8, 1, 9, 3]
  ▼           ▼
 i=0         j=5

Swap 5<8, 3<8? No
    i++     j--
Swap 2<8, 9<8? Si → swap
[5, 2, 8, 1, 9, 3]
        ▼ ▼
        i j

Swap 8<8? No
         i++
         j--
i > j → done

Result: [5, 2, 8, 1, 9, 3]
              ┬
              └─ pivot position

Passo 2: Recurse
my_sort([5, 2, 8, 1])    my_sort([9, 3])
                          │
                    [3, 9] (sorted)

Passo 3: Merge
[1, 2, 5, 8] + [3, 9] = [1, 2, 3, 5, 8, 9]
```

## Class Relationships

```
┌───────────────────────────────────────────────────────────┐
│                      namespace mystl                       │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────┐         ┌─────────────────────┐      │
│  │   template<T>   │         │   template<T>       │      │
│  │                 │         │                     │      │
│  │   MyVector      │         │   MyLinkedList      │      │
│  │                 │         │                     │      │
│  │ - m_data: T*    │         │ - m_head: Node*     │      │
│  │ - m_size: size_t│         │ - m_tail: Node*     │      │
│  │ - m_capacity:   │         │ - m_size: size_t    │      │
│  │   size_t        │         │                     │      │
│  │                 │         │ + iterator class    │      │
│  │ + begin()       │         │ + const_iterator    │      │
│  │ + end()         │         │                     │      │
│  │ + push_back()   │         │ + begin()           │      │
│  │ + pop_back()    │         │ + end()             │      │
│  │ + operator[]    │         │ + push_back()       │      │
│  │ + front()/back()│         │ + push_front()      │      │
│  └──────────────────┘         │ + insert()          │      │
│                              │ + erase()           │      │
│                              └─────────────────────┘      │
│                                    │                      │
└────────────────────────────────────┼──────────────────────┘
                                       │
                   ┌───────────────────┴──────────────────┐
                   │                                      │
         ┌─────────▼─────────┐              ┌──────────────▼───────┐
         │  template<It, T>   │              │  template<It, Comp>  │
         │                   │              │                      │
         │  my_find()        │              │  my_sort()          │
         │  my_copy()        │              │                      │
         │  my_move()        │              └──────────────────────┘
         │  my_fill()        │
         │  my_equal()       │
         │  my_count()       │
         │  my_accumulate()  │
         └───────────────────┘
```

## Memory Safety Features

```
1. Rule of Five Implementation:
   ┌────────────────────────────────────┐
   │ ~MyVector()     // Destructor      │
   │ MyVector(const MyVector&)          │
   │ operator=(const MyVector&)         │
   │ MyVector(MyVector&&)               │
   │ operator=(MyVector&&)              │
   └────────────────────────────────────┘

2. Exception Safety:
   - Strong exception guarantee in copy operations
   - Copy-and-swap idiom per assignment
   - nothrow per move operations

3. Const Correctness:
   const T& operator[](size_t) const;  // Read-only
   T& operator[](size_t);              // Read-write

4. Iterator Validation:
   - begin() ≰ end() solo se container non vuoto
   - Iterator invalidati dopo modifica
```

## Compilation Pipeline

```
Source Files:
┌──────────┐  ┌──────────┐  ┌─────────────┐
│vector.h  │  │list.h    │  │algorithms.h│
└────┬─────┘  └────┬─────┘  └──────┬──────┘
     │             │               │
     ▼             ▼               ▼
┌────────────────────────────────────────┐
│           main.cpp                     │
│  #include "vector.h"                  │
│  #include "list.h"                    │
│  #include "algorithms.h"              │
│                                       │
│  int main() {                         │
│    MyVector<int> v;                   │
│    ...                               │
│  }                                   │
└───────────────────┬──────────────────┘
                    │
                    ▼
        ┌──────────────────────┐
        │  g++ -std=c++17      │
        │  -Wall -Wextra       │
        │  -O2                │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  custom_stl.exe       │
        └──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Test Execution      │
        │  ✓ All Pass          │
        └──────────────────────┘
```

## Usage Examples by Feature

```
VECTOR:
Basic Usage      → push_back, [], size, empty
Capacity         → reserve, resize, shrink_to_fit
Access           → at, front, back, data
Modifiers        → pop_back, clear, emplace_back
Iterators        → begin, end, cbegin, cend
Copy/Move        → Copy ctor/assign, Move ctor/assign

LINKED LIST:
Basic Usage      → push_front, push_back, front, back
Modifiers        → pop_front, pop_back, insert, erase
Iterators        → bidirectional ++, --, *, ->
Copy/Move        → Same as vector

ALGORITHMS:
Search           → my_find, my_find_if
Modification     → my_copy, my_move, my_fill
Sorting          → my_sort (with/without comparator)
Comparison       → my_equal
Reduction        → my_count, my_accumulate
```

---

Questa architettura dimostra una profonda comprensione di:
- Template metaprogramming
- Memory management a basso livello
- Iterator design patterns
- Move semantics e perfrect forwarding
- STL principles e best practices
- Exception safety
- C++17 modern idioms
