#include "dfa.h"
#include <iostream>
#include <queue>
#include <algorithm>

namespace regex_engine {

// ==================== DFA Implementation ====================

DFA::DFA()
    : start_state_(-1), next_id_(0) {
}

DFAStateID DFA::addState(const std::set<StateID>& nfa_states, bool is_accepting) {
    DFAStateID id = next_id_++;
    states_.emplace_back(id, nfa_states, is_accepting);
    return id;
}

void DFA::addTransition(DFAStateID from, DFAStateID to, char symbol) {
    transitions_.emplace_back(from, to, symbol);
}

bool DFA::hasState(const std::set<StateID>& nfa_states) const {
    return findState(nfa_states) != -1;
}

DFAStateID DFA::findState(const std::set<StateID>& nfa_states) const {
    for (const auto& state : states_) {
        if (state.nfa_states == nfa_states) {
            return state.id;
        }
    }
    return -1;
}

std::vector<DFAStateID> DFA::getTransitionsFrom(DFAStateID state, char symbol) const {
    std::vector<DFAStateID> result;
    for (const auto& trans : transitions_) {
        if (trans.from == state && trans.symbol == symbol) {
            result.push_back(trans.to);
        }
    }
    return result;
}

void DFA::print() const {
    std::cout << "=== DFA ===" << std::endl;
    std::cout << "Start: " << start_state_ << std::endl;
    std::cout << "States: ";
    for (const auto& state : states_) {
        std::cout << state.id << (state.is_accepting ? "(A) " : " ");
    }
    std::cout << std::endl;
    std::cout << "Transitions:" << std::endl;
    for (const auto& trans : transitions_) {
        std::cout << "  " << trans.from << " --'" << trans.symbol << "'--> " << trans.to << std::endl;
    }
    std::cout << "==========" << std::endl;
}

bool DFA::match(const std::string& input) const {
    if (start_state_ == -1) {
        return false;
    }

    DFAStateID current = start_state_;

    for (char c : input) {
        auto transitions = getTransitionsFrom(current, c);
        if (transitions.empty()) {
            return false;
        }
        current = transitions[0];  // DFA ha al massimo una transizione per simbolo
    }

    // Verifica se lo stato finale è accepting
    auto it = std::find_if(states_.begin(), states_.end(),
                          [current](const DFAState& s) { return s.id == current; });
    return it != states_.end() && it->is_accepting;
}

bool DFA::search(const std::string& input, size_t& start, size_t& end) const {
    if (start_state_ == -1 || input.empty()) {
        return false;
    }

    // Prova a matchare da ogni posizione
    for (size_t i = 0; i < input.length(); i++) {
        DFAStateID current = start_state_;

        for (size_t j = i; j < input.length(); j++) {
            auto transitions = getTransitionsFrom(current, input[j]);
            if (transitions.empty()) {
                break;
            }
            current = transitions[0];

            // Verifica se siamo in uno stato accepting
            auto it = std::find_if(states_.begin(), states_.end(),
                                  [current](const DFAState& s) { return s.id == current; });
            if (it != states_.end() && it->is_accepting) {
                start = i;
                end = j + 1;
                return true;
            }
        }
    }

    return false;
}

std::unordered_set<char> DFA::getInputSymbols(const NFA& nfa) {
    std::unordered_set<char> symbols;

    for (const auto& trans : nfa.getTransitions()) {
        if (trans.symbol != EPSILON) {
            symbols.insert(trans.symbol);
        }
    }

    return symbols;
}

// ==================== DFABuilder Implementation ====================

std::unique_ptr<DFA> DFABuilder::build(const NFA& nfa) {
    auto dfa = std::make_unique<DFA>();

    // Calcola epsilon-closure dello stato iniziale NFA
    std::set<StateID> start_closure = nfa.epsilonClosure(nfa.getStartState());

    // Crea stato iniziale DFA
    DFAStateID dfa_start = dfa->addState(start_closure, false);
    dfa->setStartState(dfa_start);

    // Marca come accepting se contiene accepting state NFA
    for (StateID nfa_state : start_closure) {
        auto it = std::find_if(nfa.getStates().begin(), nfa.getStates().end(),
                             [nfa_state](const State& s) { return s.id == nfa_state; });
        if (it != nfa.getStates().end() && it->is_accepting) {
            // Aggiorna stato DFA come accepting
            for (auto& dfa_state : dfa->getStates()) {
                if (dfa_state.id == dfa_start) {
                    dfa_state.is_accepting = true;
                    break;
                }
            }
            break;
        }
    }

    // Queue per BFS di stati DFA
    std::queue<DFAStateID> unmarked;
    unmarked.push(dfa_start);

    // Set di stati già processati
    std::set<DFAStateID> marked;

    // Ottieni tutti i simboli input possibili
    std::unordered_set<char> input_symbols = dfa->getInputSymbols(nfa);

    // Subset construction
    while (!unmarked.empty()) {
        DFAStateID current_dfa_state = unmarked.front();
        unmarked.pop();

        if (marked.find(current_dfa_state) != marked.end()) {
            continue;
        }
        marked.insert(current_dfa_state);

        // Trova il set di stati NFA corrispondenti
        std::set<StateID> current_nfa_states;
        for (const auto& state : dfa->getStates()) {
            if (state.id == current_dfa_state) {
                current_nfa_states = state.nfa_states;
                break;
            }
        }

        // Per ogni simbolo input
        for (char symbol : input_symbols) {
            // Calcola move
            std::set<StateID> move_result = nfa.move(current_nfa_states, symbol);

            // Calcola epsilon-closure
            std::set<StateID> new_nfa_states = nfa.epsilonClosure(move_result);

            if (new_nfa_states.empty()) {
                continue;
            }

            // Verifica se questo stato DFA già esiste
            DFAStateID next_dfa_state = dfa->findState(new_nfa_states);

            if (next_dfa_state == -1) {
                // Crea nuovo stato DFA
                bool is_accepting = false;

                // Verifica se contiene accepting state NFA
                for (StateID nfa_state : new_nfa_states) {
                    auto it = std::find_if(nfa.getStates().begin(), nfa.getStates().end(),
                                         [nfa_state](const State& s) { return s.id == nfa_state; });
                    if (it != nfa.getStates().end() && it->is_accepting) {
                        is_accepting = true;
                        break;
                    }
                }

                next_dfa_state = dfa->addState(new_nfa_states, is_accepting);
                unmarked.push(next_dfa_state);
            }

            // Aggiungi transizione DFA
            dfa->addTransition(current_dfa_state, next_dfa_state, symbol);
        }
    }

    return dfa;
}

std::unique_ptr<DFA> DFA::fromNFA(const NFA& nfa) {
    return DFABuilder::build(nfa);
}

// ==================== DFAMatcher Implementation ====================

DFAMatcher::DFAMatcher(const DFA& dfa) : dfa_(dfa) {
}

bool DFAMatcher::match(const std::string& input) const {
    return dfa_.match(input);
}

bool DFAMatcher::search(const std::string& input, size_t& start, size_t& end) const {
    return dfa_.search(input, start, end);
}

std::vector<std::pair<size_t, size_t>> DFAMatcher::findAll(const std::string& input) const {
    std::vector<std::pair<size_t, size_t>> results;
    size_t pos = 0;

    while (pos < input.length()) {
        size_t start, end;
        if (dfa_.search(input.substr(pos), start, end)) {
            start += pos;
            end += pos;
            results.push_back({start, end});
            pos = end;
        } else {
            break;
        }
    }

    return results;
}

} // namespace regex_engine
