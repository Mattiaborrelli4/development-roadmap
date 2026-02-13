#ifndef MY_ALGORITHMS_H
#define MY_ALGORITHMS_H

#include <cstddef>
#include <iterator>
#include <utility>

namespace mystl {

// ==================== my_find ====================
// Cerca un valore in un range [first, last)
// Restituisce un iteratore al primo elemento trovato, o last se non trovato
template <typename InputIt, typename T>
InputIt my_find(InputIt first, InputIt last, const T& value) {
    for (; first != last; ++first) {
        if (*first == value) {
            return first;
        }
    }
    return last;
}

// ==================== my_find_if ====================
// Cerca un elemento che soddisfa un predicato
template <typename InputIt, typename Predicate>
InputIt my_find_if(InputIt first, InputIt last, Predicate pred) {
    for (; first != last; ++first) {
        if (pred(*first)) {
            return first;
        }
    }
    return last;
}

// ==================== my_copy ====================
// Copia elementi da [first, last) a [d_first, d_first + (last - first))
// Restituisce un iteratore alla fine dell'intervallo di destinazione
template <typename InputIt, typename OutputIt>
OutputIt my_copy(InputIt first, InputIt last, OutputIt d_first) {
    while (first != last) {
        *d_first++ = *first++;
    }
    return d_first;
}

// ==================== my_move ====================
// Sposta elementi da [first, last) a [d_first, ...)
template <typename InputIt, typename OutputIt>
OutputIt my_move(InputIt first, InputIt last, OutputIt d_first) {
    while (first != last) {
        *d_first++ = std::move(*first++);
    }
    return d_first;
}

// ==================== my_sort ====================
// Implementazione di QuickSort per iteratori random access
template <typename RandomIt>
void my_sort(RandomIt first, RandomIt last) {
    using diff_t = typename std::iterator_traits<RandomIt>::difference_type;

    diff_t count = last - first;
    if (count <= 1) {
        return;
    }

    // Partition
    RandomIt pivot = first + count / 2;
    auto pivot_value = *pivot;

    RandomIt i = first;
    RandomIt j = last - 1;

    while (i <= j) {
        while (*i < pivot_value) {
            ++i;
        }
        while (*j > pivot_value) {
            --j;
        }
        if (i <= j) {
            std::swap(*i, *j);
            ++i;
            --j;
        }
    }

    // Ricorsione
    if (first < j) {
        my_sort(first, j + 1);
    }
    if (i < last) {
        my_sort(i, last);
    }
}

// ==================== my_sort con comparatore ====================
template <typename RandomIt, typename Compare>
void my_sort(RandomIt first, RandomIt last, Compare comp) {
    using diff_t = typename std::iterator_traits<RandomIt>::difference_type;

    diff_t count = last - first;
    if (count <= 1) {
        return;
    }

    // Partition
    RandomIt pivot = first + count / 2;
    auto pivot_value = *pivot;

    RandomIt i = first;
    RandomIt j = last - 1;

    while (i <= j) {
        while (comp(*i, pivot_value)) {
            ++i;
        }
        while (comp(pivot_value, *j)) {
            --j;
        }
        if (i <= j) {
            std::swap(*i, *j);
            ++i;
            --j;
        }
    }

    // Ricorsione
    if (first < j) {
        my_sort(first, j + 1, comp);
    }
    if (i < last) {
        my_sort(i, last, comp);
    }
}

// ==================== my_fill ====================
// Riempie [first, last) con value
template <typename ForwardIt, typename T>
void my_fill(ForwardIt first, ForwardIt last, const T& value) {
    for (; first != last; ++first) {
        *first = value;
    }
}

// ==================== my_equal ====================
// Verifica se due range sono uguali
template <typename InputIt1, typename InputIt2>
bool my_equal(InputIt1 first1, InputIt1 last1, InputIt2 first2) {
    for (; first1 != last1; ++first1, ++first2) {
        if (!(*first1 == *first2)) {
            return false;
        }
    }
    return true;
}

// ==================== my_count ====================
// Conta gli elementi uguali a value
template <typename InputIt, typename T>
typename std::iterator_traits<InputIt>::difference_type
my_count(InputIt first, InputIt last, const T& value) {
    typename std::iterator_traits<InputIt>::difference_type result = 0;
    for (; first != last; ++first) {
        if (*first == value) {
            ++result;
        }
    }
    return result;
}

// ==================== my_accumulate ====================
// Somma tutti gli elementi nel range
template <typename InputIt, typename T>
T my_accumulate(InputIt first, InputIt last, T init) {
    for (; first != last; ++first) {
        init = init + *first;
    }
    return init;
}

} // namespace mystl

#endif // MY_ALGORITHMS_H
