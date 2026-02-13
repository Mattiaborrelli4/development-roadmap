#ifndef DFA_H
#define DFA_H

#include "nfa.h"
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <string>

namespace regex_engine {

// DFA State ID
using DFAStateID = int;

// Rappresenta uno stato DFA
struct DFAState {
    DFAStateID id;
    bool is_accepting;
    std::set<StateID> nfa_states;  // Set di stati NFA che compongono questo stato DFA

    DFAState(DFAStateID i, const std::set<StateID>& states, bool accept = false)
        : id(i), is_accepting(accept), nfa_states(states) {}

    // Operator per unordered_set
    bool operator==(const DFAState& other) const {
        return nfa_states == other.nfa_states;
    }
};

// Hash function per DFAState
struct DFAStateHash {
    size_t operator()(const DFAState& state) const {
        size_t hash = 0;
        for (StateID id : state.nfa_states) {
            hash ^= std::hash<StateID>{}(id) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
        }
        return hash;
    }
};

// Rappresenta una transizione DFA
struct DFATransition {
    DFAStateID from;
    DFAStateID to;
    char symbol;

    DFATransition(DFAStateID f, DFAStateID t, char s)
        : from(f), to(t), symbol(s) {}
};

// Deterministic Finite Automaton
class DFA {
public:
    DFA();

    // Aggiunge uno stato DFA
    DFAStateID addState(const std::set<StateID>& nfa_states, bool is_accepting);

    // Aggiunge una transizione DFA
    void addTransition(DFAStateID from, DFAStateID to, char symbol);

    // Getter methods
    DFAStateID getStartState() const { return start_state_; }
    const std::vector<DFAState>& getStates() const { return states_; }
    std::vector<DFAState>& getStates() { return states_; }
    const std::vector<DFATransition>& getTransitions() const { return transitions_; }

    // Setter methods
    void setStartState(DFAStateID id) { start_state_ = id; }

    // Verifica se uno stato esiste
    bool hasState(const std::set<StateID>& nfa_states) const;

    // Trova uno stato DFA by NFA states set
    DFAStateID findState(const std::set<StateID>& nfa_states) const;

    // Trova transizione da uno stato per un simbolo
    std::vector<DFAStateID> getTransitionsFrom(DFAStateID state, char symbol) const;

    // Visualizza il DFA (debug)
    void print() const;

    // Match stringa contro il DFA
    bool match(const std::string& input) const;

    // Trova prima occorrenza del pattern
    bool search(const std::string& input, size_t& start, size_t& end) const;

    // Costruisce DFA da NFA usando subset construction
    static std::unique_ptr<DFA> fromNFA(const NFA& nfa);

    // Ottieni tutti i simboli input possibili dalle transizioni NFA (public per DFABuilder)
    static std::unordered_set<char> getInputSymbols(const NFA& nfa);

private:
    std::vector<DFAState> states_;
    std::vector<DFATransition> transitions_;
    DFAStateID start_state_;
    DFAStateID next_id_;
};

// DFA Matcher - Gestisce il matching di stringhe
class DFAMatcher {
public:
    explicit DFAMatcher(const DFA& dfa);

    // Match completo
    bool match(const std::string& input) const;

    // Trova prima occorrenza
    bool search(const std::string& input, size_t& start, size_t& end) const;

    // Trova tutte le occorrenze
    std::vector<std::pair<size_t, size_t>> findAll(const std::string& input) const;

private:
    const DFA& dfa_;
};

// DFA Builder - Costruisce DFA da NFA
class DFABuilder {
public:
    // Subset construction algorithm
    static std::unique_ptr<DFA> build(const NFA& nfa);

private:
    // Crea stato DFA da set di stati NFA
    static DFAStateID createDFAState(DFA& dfa, const std::set<StateID>& nfa_states,
                                     const NFA& nfa);
};

} // namespace regex_engine

#endif // DFA_H
