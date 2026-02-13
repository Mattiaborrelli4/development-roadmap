#include "nfa.h"
#include <iostream>
#include <stack>
#include <sstream>
#include <algorithm>
#include <cctype>

namespace regex_engine {

// ==================== NFA Implementation ====================

NFA::NFA()
    : start_state_(-1), accept_state_(-1), next_id_(0) {
}

NFA::NFA(StateID start, StateID accept)
    : start_state_(start), accept_state_(accept), next_id_(0) {
    // Aggiungi stati start e accept
    states_.emplace_back(start, false, "start");
    states_.emplace_back(accept, true, "accept");
    next_id_ = accept + 1;
}

StateID NFA::addState(bool is_accepting) {
    StateID id = next_id_++;
    states_.emplace_back(id, is_accepting);
    return id;
}

void NFA::addTransition(StateID from, StateID to, char symbol) {
    transitions_.emplace_back(from, to, symbol);
}

std::set<StateID> NFA::epsilonClosure(const std::set<StateID>& states) const {
    std::set<StateID> closure = states;
    std::vector<StateID> stack(states.begin(), states.end());

    while (!stack.empty()) {
        StateID current = stack.back();
        stack.pop_back();

        // Trova tutte le epsilon-transitions da questo stato
        for (const auto& trans : transitions_) {
            if (trans.from == current && trans.symbol == EPSILON) {
                if (closure.find(trans.to) == closure.end()) {
                    closure.insert(trans.to);
                    stack.push_back(trans.to);
                }
            }
        }
    }

    return closure;
}

std::set<StateID> NFA::epsilonClosure(StateID state) const {
    std::set<StateID> states = {state};
    return epsilonClosure(states);
}

std::set<StateID> NFA::move(const std::set<StateID>& states, char symbol) const {
    std::set<StateID> result;

    for (StateID state : states) {
        for (const auto& trans : transitions_) {
            if (trans.from == state && trans.symbol == symbol) {
                result.insert(trans.to);
            }
        }
    }

    return result;
}

void NFA::print() const {
    std::cout << "=== NFA ===" << std::endl;
    std::cout << "Start: " << start_state_ << std::endl;
    std::cout << "Accept: " << accept_state_ << std::endl;
    std::cout << "States: ";
    for (const auto& state : states_) {
        std::cout << state.id << (state.is_accepting ? "(A) " : " ");
    }
    std::cout << std::endl;
    std::cout << "Transitions:" << std::endl;
    for (const auto& trans : transitions_) {
        if (trans.symbol == EPSILON) {
            std::cout << "  " << trans.from << " --EPSILON--> " << trans.to << std::endl;
        } else {
            std::cout << "  " << trans.from << " --'" << trans.symbol << "'--> " << trans.to << std::endl;
        }
    }
    std::cout << "==========" << std::endl;
}

// ==================== NFA Factory Methods ====================

std::unique_ptr<NFA> NFA::createLiteralNFA(char c) {
    auto nfa = std::make_unique<NFA>();
    StateID start = nfa->addState();
    StateID accept = nfa->addState(true);

    nfa->setStartState(start);
    nfa->setAcceptState(accept);
    nfa->addTransition(start, accept, c);

    return nfa;
}

std::unique_ptr<NFA> NFA::createDotNFA() {
    auto nfa = std::make_unique<NFA>();
    StateID start = nfa->addState();
    StateID accept = nfa->addState(true);

    nfa->setStartState(start);
    nfa->setAcceptState(accept);

    // Aggiungi transizioni per tutti i caratteri possibili (tranne newline)
    for (int c = 1; c < 128; c++) {
        if (c != '\n') {
            nfa->addTransition(start, accept, static_cast<char>(c));
        }
    }

    return nfa;
}

std::unique_ptr<NFA> NFA::createStarNFA(std::unique_ptr<NFA> nfa) {
    auto result = std::make_unique<NFA>();
    StateID new_start = result->addState();
    StateID new_accept = result->addState(true);

    // Copia stati e transizioni dall'NFA originale
    std::unordered_map<StateID, StateID> state_map;
    state_map[nfa->getStartState()] = new_start;
    state_map[nfa->getAcceptState()] = new_accept;

    for (const auto& state : nfa->getStates()) {
        if (state.id != nfa->getStartState() && state.id != nfa->getAcceptState()) {
            StateID new_id = result->addState();
            state_map[state.id] = new_id;
        }
    }

    for (const auto& trans : nfa->getTransitions()) {
        result->addTransition(state_map[trans.from], state_map[trans.to], trans.symbol);
    }

    // Aggiungi transizioni per Kleene star
    result->addTransition(new_start, new_accept);  // Skip (zero ripetizioni)
    result->addTransition(new_accept, new_start);  // Loop (più ripetizioni)

    result->setStartState(new_start);
    result->setAcceptState(new_accept);

    return result;
}

std::unique_ptr<NFA> NFA::createPlusNFA(std::unique_ptr<NFA> nfa) {
    // a+ = aa*
    auto star_nfa = createStarNFA(std::move(nfa));
    return createConcatNFA(createLiteralNFA(star_nfa->getStartState()), std::move(star_nfa));
}

std::unique_ptr<NFA> NFA::createQuestionNFA(std::unique_ptr<NFA> nfa) {
    auto result = std::make_unique<NFA>();
    StateID new_start = result->addState();
    StateID new_accept = result->addState(true);

    // Copia stati e transizioni
    std::unordered_map<StateID, StateID> state_map;
    state_map[nfa->getStartState()] = new_start;
    state_map[nfa->getAcceptState()] = new_accept;

    for (const auto& state : nfa->getStates()) {
        if (state.id != nfa->getStartState() && state.id != nfa->getAcceptState()) {
            StateID new_id = result->addState();
            state_map[state.id] = new_id;
        }
    }

    for (const auto& trans : nfa->getTransitions()) {
        result->addTransition(state_map[trans.from], state_map[trans.to], trans.symbol);
    }

    // Aggiungi epsilon transition per skip
    result->addTransition(new_start, new_accept);

    result->setStartState(new_start);
    result->setAcceptState(new_accept);

    return result;
}

std::unique_ptr<NFA> NFA::createConcatNFA(std::unique_ptr<NFA> left, std::unique_ptr<NFA> right) {
    auto result = std::make_unique<NFA>();

    // Copia stati dal primo NFA (NON accepting perché dobbiamo continuare)
    std::unordered_map<StateID, StateID> state_map;
    for (const auto& state : left->getStates()) {
        // Non mantenere gli accepting states del left NFA
        StateID new_id = result->addState(false);  // Tutti non-accepting inizialmente
        state_map[state.id] = new_id;
    }

    // Copia stati dal secondo NFA (tranne lo start che verrà fuso)
    StateID right_start = right->getStartState();
    for (const auto& state : right->getStates()) {
        if (state.id != right_start) {
            StateID new_id = result->addState(state.is_accepting);
            state_map[state.id] = new_id;
        }
    }

    // Fusione: accept state di left diventa start state di right
    StateID merge_point = state_map[left->getAcceptState()];
    // Il right_start deve essere mappato al merge_point
    state_map[right_start] = merge_point;

    // Copia transizioni dal primo NFA
    for (const auto& trans : left->getTransitions()) {
        result->addTransition(state_map[trans.from], state_map[trans.to], trans.symbol);
    }

    // Copia transizioni dal secondo NFA
    for (const auto& trans : right->getTransitions()) {
        // Se la transizione parte da right_start, deve partire da merge_point
        StateID from = (trans.from == right_start) ? merge_point : state_map[trans.from];
        StateID to = (trans.to == right_start) ? merge_point : state_map[trans.to];
        result->addTransition(from, to, trans.symbol);
    }

    // Aggiungi epsilon transition per fusione
    result->addTransition(merge_point, merge_point);

    result->setStartState(state_map[left->getStartState()]);
    result->setAcceptState(state_map[right->getAcceptState()]);

    return result;
}

std::unique_ptr<NFA> NFA::createOrNFA(std::unique_ptr<NFA> left, std::unique_ptr<NFA> right) {
    auto result = std::make_unique<NFA>();
    StateID new_start = result->addState();
    StateID new_accept = result->addState(true);

    // Copia stati da entrambi gli NFA
    std::unordered_map<StateID, StateID> state_map;

    for (const auto& state : left->getStates()) {
        StateID new_id = result->addState();
        state_map[state.id] = new_id;
    }

    for (const auto& state : right->getStates()) {
        StateID new_id = result->addState();
        state_map[state.id] = new_id;
    }

    // Copia transizioni
    for (const auto& trans : left->getTransitions()) {
        result->addTransition(state_map[trans.from], state_map[trans.to], trans.symbol);
    }

    for (const auto& trans : right->getTransitions()) {
        result->addTransition(state_map[trans.from], state_map[trans.to], trans.symbol);
    }

    // Branching: epsilon transitions dal nuovo start
    result->addTransition(new_start, state_map[left->getStartState()]);
    result->addTransition(new_start, state_map[right->getStartState()]);

    // Epsilon transitions verso il nuovo accept
    result->addTransition(state_map[left->getAcceptState()], new_accept);
    result->addTransition(state_map[right->getAcceptState()], new_accept);

    result->setStartState(new_start);
    result->setAcceptState(new_accept);

    return result;
}

// ==================== NFABuilder Implementation ====================

bool NFABuilder::isOperator(char c) {
    return c == '|' || c == '*' || c == '+' || c == '?';
}

bool NFABuilder::isOperand(char c) {
    return !isOperator(c) && c != '(' && c != ')' && c != '[' && c != ']' &&
           c != '^' && c != '$' && c != '\\';
}

int NFABuilder::getPrecedence(char op) {
    switch (op) {
        case '|': return 1;
        case '\1': return 2;  // CONCAT (concatenazione implicita)
        case '+': return 3;
        case '?': return 3;
        case '*': return 3;
        default: return 0;
    }
}

std::string NFABuilder::infixToPostfix(const std::string& pattern) {
    std::string postfix;
    std::stack<char> op_stack;

    // Aggiungi concatenazione esplicita
    std::string expanded;
    for (size_t i = 0; i < pattern.length(); i++) {
        char c = pattern[i];

        // Skip escape sequences
        if (c == '\\') {
            expanded += c;
            if (i + 1 < pattern.length()) {
                expanded += pattern[++i];
            }
            continue;
        }

        expanded += c;

        // Aggiungi operatore di concatenazione
        if (i + 1 < pattern.length()) {
            char next = pattern[i + 1];

            bool curr_is_operand = isOperand(c) || c == '.' || c == ')' || c == '*' ||
                                   c == '+' || c == '?' || c == ']' || c == '$';
            bool next_is_operand = isOperand(next) || next == '.' || next == '(' ||
                                   next == '[' || next == '^' || next == '\\';

            if (curr_is_operand && next_is_operand) {
                expanded += CONCAT;  // Usa CONCAT invece di '.'
            }
        }
    }

    // Shunting-yard algorithm
    for (char c : expanded) {
        if (c == CONCAT) {
            // CONCAT è un operatore con precedenza
            while (!op_stack.empty() && op_stack.top() != '(' && op_stack.top() != '[' &&
                   getPrecedence(op_stack.top()) >= getPrecedence(CONCAT)) {
                postfix += op_stack.top();
                op_stack.pop();
            }
            op_stack.push(CONCAT);
        } else if (c == '\\') {
            // Escape sequence - skip backslash, next char already added to expanded
            continue;
        } else if (isOperand(c) || c == '.') {
            postfix += c;
        } else if (c == '(' || c == '[') {
            op_stack.push(c);
        } else if (c == ')' || c == ']') {
            char open = (c == ')') ? '(' : '[';
            while (!op_stack.empty() && op_stack.top() != open) {
                postfix += op_stack.top();
                op_stack.pop();
            }
            if (!op_stack.empty()) {
                op_stack.pop();
            }
        } else {
            while (!op_stack.empty() && op_stack.top() != '(' && op_stack.top() != '[' &&
                   getPrecedence(op_stack.top()) >= getPrecedence(c)) {
                postfix += op_stack.top();
                op_stack.pop();
            }
            op_stack.push(c);
        }
    }

    while (!op_stack.empty()) {
        postfix += op_stack.top();
        op_stack.pop();
    }

    return postfix;
}

std::unique_ptr<NFA> NFABuilder::buildFromPostfix(const std::string& postfix) {
    std::stack<std::unique_ptr<NFA>> nfa_stack;

    for (char c : postfix) {
        if (c == CONCAT) {
            // Concatenazione
            if (nfa_stack.size() < 2) {
                throw std::runtime_error("Invalid pattern: not enough operands for concatenation");
            }
            auto right = std::move(nfa_stack.top()); nfa_stack.pop();
            auto left = std::move(nfa_stack.top()); nfa_stack.pop();
            nfa_stack.push(NFA::createConcatNFA(std::move(left), std::move(right)));
        } else if (c == '|') {
            // OR
            if (nfa_stack.size() < 2) {
                throw std::runtime_error("Invalid pattern: not enough operands for OR");
            }
            auto right = std::move(nfa_stack.top()); nfa_stack.pop();
            auto left = std::move(nfa_stack.top()); nfa_stack.pop();
            nfa_stack.push(NFA::createOrNFA(std::move(left), std::move(right)));
        } else if (c == '*') {
            // Kleene star
            if (nfa_stack.empty()) {
                throw std::runtime_error("Invalid pattern: no operand for *");
            }
            auto nfa = std::move(nfa_stack.top()); nfa_stack.pop();
            nfa_stack.push(NFA::createStarNFA(std::move(nfa)));
        } else if (c == '+') {
            // Plus
            if (nfa_stack.empty()) {
                throw std::runtime_error("Invalid pattern: no operand for +");
            }
            auto nfa = std::move(nfa_stack.top()); nfa_stack.pop();
            nfa_stack.push(NFA::createPlusNFA(std::move(nfa)));
        } else if (c == '?') {
            // Question mark
            if (nfa_stack.empty()) {
                throw std::runtime_error("Invalid pattern: no operand for ?");
            }
            auto nfa = std::move(nfa_stack.top()); nfa_stack.pop();
            nfa_stack.push(NFA::createQuestionNFA(std::move(nfa)));
        } else if (c == '.') {
            // Dot - qualsiasi carattere
            nfa_stack.push(NFA::createDotNFA());
        } else {
            // Operando letterale
            nfa_stack.push(NFA::createLiteralNFA(c));
        }
    }

    if (nfa_stack.size() != 1) {
        throw std::runtime_error("Invalid pattern: malformed NFA stack");
    }

    return std::move(nfa_stack.top());
}

std::unique_ptr<NFA> NFABuilder::build(const std::string& pattern) {
    // Gestisci ^ (inizio stringa) e $ (fine stringa)
    bool anchor_start = !pattern.empty() && pattern[0] == '^';
    bool anchor_end = !pattern.empty() && pattern.back() == '$';

    std::string processed_pattern = pattern;
    size_t start_offset = 0;

    if (anchor_start) {
        start_offset = 1;
    }

    if (anchor_end && !processed_pattern.empty()) {
        processed_pattern.pop_back();
    }

    std::string core_pattern = processed_pattern.substr(start_offset);

    // Converti in postfix e costruisci NFA
    std::string postfix = infixToPostfix(core_pattern);
    // Debug: print postfix
    std::cout << "Pattern: " << pattern << std::endl;
    std::cout << "Postfix: ";
    for (char c : postfix) {
        if (c == CONCAT) std::cout << "CONCAT ";
        else if (c == EPSILON) std::cout << "EPS ";
        else std::cout << c << " ";
    }
    std::cout << std::endl;
    auto nfa = buildFromPostfix(postfix);

    return nfa;
}

std::unique_ptr<NFA> NFA::fromPattern(const std::string& pattern) {
    return NFABuilder::build(pattern);
}

} // namespace regex_engine
