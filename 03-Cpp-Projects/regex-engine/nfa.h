#ifndef NFA_H
#define NFA_H

#include <vector>
#include <set>
#include <memory>
#include <string>
#include <unordered_map>
#include <unordered_set>

namespace regex_engine {

// ID univoco per ogni stato NFA
using StateID = int;

// Carattere speciale per epsilon transitions
constexpr char EPSILON = '\0';

// Carattere speciale per concatenazione (non visibile in pattern)
constexpr char CONCAT = '\1';

// Rappresenta una transizione NFA
struct Transition {
    StateID from;
    StateID to;
    char symbol;  // EPSILON per epsilon-transitions

    Transition(StateID f, StateID t, char s = EPSILON)
        : from(f), to(t), symbol(s) {}
};

// Rappresenta uno stato NFA
struct State {
    StateID id;
    bool is_accepting;
    std::string name;

    State(StateID i, bool accept = false, const std::string& n = "")
        : id(i), is_accepting(accept), name(n) {}
};

// Non-deterministic Finite Automaton
class NFA {
public:
    NFA();
    NFA(StateID start, StateID accept);

    // Aggiunge uno stato all'NFA
    StateID addState(bool is_accepting = false);

    // Aggiunge una transizione
    void addTransition(StateID from, StateID to, char symbol = EPSILON);

    // Getter methods
    StateID getStartState() const { return start_state_; }
    StateID getAcceptState() const { return accept_state_; }
    const std::vector<State>& getStates() const { return states_; }
    const std::vector<Transition>& getTransitions() const { return transitions_; }

    // Setter methods
    void setStartState(StateID id) { start_state_ = id; }
    void setAcceptState(StateID id) { accept_state_ = id; }

    // Calcola la epsilon-closure di uno stato
    std::set<StateID> epsilonClosure(const std::set<StateID>& states) const;

    // Calcola la epsilon-closure di un singolo stato
    std::set<StateID> epsilonClosure(StateID state) const;

    // Move function per simbolo
    std::set<StateID> move(const std::set<StateID>& states, char symbol) const;

    // Visualizza l'NFA (debug)
    void print() const;

    // Costruisce NFA da un pattern regex
    static std::unique_ptr<NFA> fromPattern(const std::string& pattern);

    // Helper functions per costruzione NFA (public per NFABuilder)
    static std::unique_ptr<NFA> createLiteralNFA(char c);
    static std::unique_ptr<NFA> createDotNFA();
    static std::unique_ptr<NFA> createStarNFA(std::unique_ptr<NFA> nfa);
    static std::unique_ptr<NFA> createPlusNFA(std::unique_ptr<NFA> nfa);
    static std::unique_ptr<NFA> createQuestionNFA(std::unique_ptr<NFA> nfa);
    static std::unique_ptr<NFA> createConcatNFA(std::unique_ptr<NFA> left,
                                                std::unique_ptr<NFA> right);
    static std::unique_ptr<NFA> createOrNFA(std::unique_ptr<NFA> left,
                                            std::unique_ptr<NFA> right);

private:
    std::vector<State> states_;
    std::vector<Transition> transitions_;
    StateID start_state_;
    StateID accept_state_;
    StateID next_id_;

    // Build NFA con Thompson's construction algorithm
    static std::unique_ptr<NFA> buildFromPostfix(const std::string& postfix);
};

// NFA Builder - Costruisce NFA dal pattern regex
class NFABuilder {
public:
    static std::unique_ptr<NFA> build(const std::string& pattern);

private:
    // Converte infix regex in postfix notation
    static std::string infixToPostfix(const std::string& pattern);

    // Build NFA da postfix
    static std::unique_ptr<NFA> buildFromPostfix(const std::string& postfix);

    // Precedenza degli operatori
    static int getPrecedence(char op);

    // Verifica se è un operatore
    static bool isOperator(char c);

    // Verifica se è un operando
    static bool isOperand(char c);
};

} // namespace regex_engine

#endif // NFA_H
