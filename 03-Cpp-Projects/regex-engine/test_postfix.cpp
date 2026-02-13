#include "nfa.h"
#include <iostream>

using namespace regex_engine;

int main() {
    std::string pattern = "a.b";
    
    // Call the infixToPostfix function (it's private, but we can test via fromPattern)
    try {
        auto nfa = NFA::fromPattern(pattern);
        std::cout << "NFA created for pattern: " << pattern << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}
