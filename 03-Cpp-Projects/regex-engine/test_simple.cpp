#include "nfa.h"
#include "dfa.h"
#include <iostream>

using namespace regex_engine;

int main() {
    std::string pattern = "a.b";
    std::string input = "ab";
    
    std::cout << "Pattern: " << pattern << std::endl;
    std::cout << "Input: " << input << std::endl;
    
    try {
        auto nfa = NFA::fromPattern(pattern);
        std::cout << "NFA created successfully" << std::endl;
        nfa->print();
        
        auto dfa = DFA::fromNFA(*nfa);
        std::cout << "DFA created successfully" << std::endl;
        dfa->print();
        
        bool result = dfa->match(input);
        std::cout << "Match result: " << (result ? "TRUE" : "FALSE") << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}
