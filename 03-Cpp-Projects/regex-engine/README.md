# C++ Regex Engine

Un motore di espressioni regolari implementato in C++17 con architettura NFA/DFA.

## 🎯 Panoramica

Questo progetto implementa un engine regex completo che:

1. **Parsa** pattern regex in token
2. **Costruisce** un NFA (Non-deterministic Finite Automaton)
3. **Converte** l'NFA in DFA (Deterministic Finite Automaton)
4. **Matcha** stringhe contro il DFA

## ✨ Caratteristiche

### Pattern Supportati

| Simbolo | Descrizione | Esempio |
|---------|-------------|---------|
| `.` | Qualsiasi carattere | `a.b` → `axb`, `aab`, `a1b` |
| `*` | Zero o più ripetizioni | `a*` → ``, `a`, `aaa` |
| `+` | Uno o più ripetizioni | `a+` → `a`, `aaa` |
| `?` | Zero o una ripetizione | `a?` → ``, `a` |
| `^` | Inizio stringa | `^abc` → stringhe che iniziano con "abc" |
| `$` | Fine stringa | `xyz$` → stringhe che finiscono con "xyz" |
| `[` `]` | Character class | `[abc]` → `a`, `b`, o `c` |
| `\` | Escape | `\.` → letteralmente `.` |

### Algoritmi Implementati

- **Thompson's Construction**: Costruzione NFA da pattern regex
- **Subset Construction**: Conversione NFA → DFA
- **Epsilon-Closure**: Gestione epsilon-transitions
- **Backtracking**: Ricerca pattern in stringa

## 📁 Struttura del Progetto

```
regex-engine/
├── regex.h          # Lexer e Parser per tokenizzazione pattern
├── regex.cpp        # Implementazione del parser
├── nfa.h            # Definizione NFA e Thompson construction
├── nfa.cpp          # Implementazione NFA
├── dfa.h            # Definizione DFA e subset construction
├── dfa.cpp          # Implementazione DFA
├── main.cpp         # Test suite e modalità interattiva
└── README.md        # Questa documentazione
```

## 🏗️ Architettura

### 1. Lexer & Parser (`regex.h/cpp`)

```cpp
// Tokenizza il pattern regex
RegexLexer lexer("a*b");
Token token = lexer.getCurrentToken();

// Valida il pattern
RegexParser parser(lexer);
parser.parse();
```

### 2. NFA Construction (`nfa.h/cpp`)

```cpp
// Costruisce NFA dal pattern
auto nfa = NFA::fromPattern("a*b");

// Calcola epsilon-closure
auto closure = nfa->epsilonClosure(start_state);

// Move function
auto next_states = nfa->move(current_states, 'a');
```

### 3. DFA Construction (`dfa.h/cpp`)

```cpp
// Converte NFA in DFA
auto dfa = DFA::fromNFA(*nfa);

// Match stringa
bool matched = dfa->match("aaab");

// Trova occorrenza
size_t start, end;
bool found = dfa->search("xxaaabyy", start, end);
```

## 🔧 Compilazione

### Requisiti

- C++17 o superiore
- CMake 3.10+ (opzionale)

### Compilazione Manuale

```bash
# Windows (MSVC)
cl /EHsc /std:c++17 regex.cpp nfa.cpp dfa.cpp main.cpp /Fe:regex.exe

# Windows (MinGW)
g++ -std=c++17 regex.cpp nfa.cpp dfa.cpp main.cpp -o regex.exe

# Linux/macOS
g++ -std=c++17 regex.cpp nfa.cpp dfa.cpp main.cpp -o regex
```

### CMake (Opzionale)

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

## 🚀 Utilizzo

### Esecuzione dei Test

```bash
./regex test
```

Output:
```
=== TEST: Match Letterale ===
[PASS] Match letterale 'a'
       Pattern: a, Input: "a", Expected: true, Got: true

=== TEST: Star (*) - Zero o Più ===
[PASS] Star: zero occorrenze
       Pattern: a*, Input: "", Expected: true, Got: true
...
```

### Modalità Interattiva

```bash
./regex interactive
```

Esempio di sessione:
```
Pattern: a*b
Input:   aaab

Risultato Match: TRUE
Risultato Search: TRUE (trovato alle posizioni [0:4])
        "aaab"

Statistiche:
  Stati NFA: 4
  Transizioni NFA: 4
  Stati DFA: 2
  Transizioni DFA: 2
```

### Utilizzo nel Codice

```cpp
#include "regex.h"
#include "nfa.h"
#include "dfa.h"

using namespace regex_engine;

int main() {
    // Costruisci NFA dal pattern
    auto nfa = NFA::fromPattern("a*b");

    // Converti in DFA
    auto dfa = DFA::fromNFA(*nfa);

    // Crea matcher
    DFAMatcher matcher(*dfa);

    // Test
    std::string input = "aaab";
    bool matched = matcher.match(input);

    std::cout << "Match: " << (matched ? "YES" : "NO") << std::endl;

    // Trova occorrenza
    size_t start, end;
    if (dfa->search("xxaaabyy", start, end)) {
        std::cout << "Found at [" << start << ":" << end << ")" << std::endl;
    }

    return 0;
}
```

## 📊 Esempi di Pattern

### Pattern Base

```cpp
"a.c"        // Match: "abc", "a.c", "a1c"
"ab*c"       // Match: "ac", "abc", "abbc", "abbbc"
"ab+c"       // Match: "abc", "abbc", "abbbc" (NON "ac")
"ab?c"       // Match: "ac", "abc"
"^abc"       // Match: "abc..." (inizia con abc)
"xyz$"       // Match: "...xyz" (finisce con xyz)
```

### Pattern Complessi

```cpp
"a.*b"       // Match: "ab", "axxxxxb", "a123b"
"a.+b"       // Match: "axb", "a123b" (NON "ab")
"a*b+c"      // Match: "abc", "aaabbbc", "bbbc"
```

## 🔍 Come Funziona

### 1. Tokenizzazione (Lexer)

Il pattern `a*b` viene tokenizzato in:
```
LITERAL('a') → STAR → LITERAL('b')
```

### 2. Parsing

Conversione in postfix notation:
```
Infix:  a*b
Postfix: ab*
```

### 3. NFA Construction (Thompson)

Per ogni token/parti del pattern, si costruisce un mini-NFA:
```
LITERAL('a'): 0 --'a'--> 1
STAR:         0 --EPSILON--> 1, 1 --EPSILON--> 0
```

### 4. Subset Construction

NFA → DFA calcolando epsilon-closure:
```
DFA State 0 = ε-closure(NFA Start)
DFA State 1 = ε-closure(move(State 0, 'a'))
...
```

### 5. Matching

Il DFA è deterministico, quindi il matching è O(n):
```
current = DFA Start
for char in input:
    current = transition[current][char]
return is_accepting[current]
```

## 🧪 Test Suite

Il progetto include una suite completa di test che copre:

- ✅ Match letterale
- ✅ Dot (qualsiasi carattere)
- ✅ Star (zero o più)
- ✅ Plus (uno o più)
- ✅ Question (zero o uno)
- ✅ Caret (inizio stringa)
- ✅ Dollar (fine stringa)
- ✅ Combinazioni complesse
- ✅ Search (trova occorrenza)
- ✅ Edge cases

## 📈 Complessità

| Operazione | NFA | DFA |
|------------|-----|-----|
| Costruzione | O(m) | O(2ⁿ) |
| Matching | O(nm²) | O(n) |
| Spazio | O(m) | O(2ⁿ) |

Dove:
- m = lunghezza pattern
- n = numero stati NFA
- input = lunghezza stringa input

## 🎓 Concetti Chiave

### Epsilon-Transition

Transizione che non consuma input:
```
State A --EPSILON--> State B
```
Usata per:
- Kleene star (*)
- Concatenazione
- Alternazione (OR)

### Subset Construction

Algoritmo per convertire NFA in DFA:
1. Calcola epsilon-closure dello start state NFA → DFA start state
2. Per ogni simbolo input:
   - Calcola move(current_states, symbol)
   - Calcola epsilon-closure del risultato → nuovo DFA state
3. Ripeti finché non ci sono nuovi stati

## 🐛 Debug

### Abilitare Output Debug

Decommenta le chiamate a `print()` in `nfa.cpp` e `dfa.cpp`:

```cpp
nfa->print();  // Mostra stati e transizioni NFA
dfa->print();  // Mostra stati e transizioni DFA
```

### Traccia Matching

Aggiungi logging in `dfa.cpp`:

```cpp
std::cout << "Current state: " << current << ", Input: " << c << std::endl;
```

## 📚 Risorse

- [Thompson's Construction](https://en.wikipedia.org/wiki/Thompson%27s_construction)
- [Subset Construction Algorithm](https://en.wikipedia.org/wiki/Powerset_construction)
- [Regular Expressions](https://en.wikipedia.org/wiki/Regular_expression)

## 📝 TODO

- [ ] Supporto per character classes `[a-z]`
- [ ] Supporto per groups `(abc)+`
- [ ] Supporto per OR `a|b`
- [ ] Supporto per escape completo `\d`, `\w`, `\s`
- [ ] Ottimizzazione DFA minimization
- [ ] Supporto per backreference
- [ ] Benchmark performance

## 👨‍💻 Autore

Progetto realizzato per portfolio personale.

## 📄 Licenza

Questo progetto è a scopo educativo. Sentiti libero di utilizzarlo e modificarlo.

---

**Divertiti con le regex! 🚀**
