#include <iostream>
#include <string>

bool isOperator(char c) {
    return c == '|' || c == '*' || c == '+' || c == '?';
}

bool isOperand(char c) {
    return !isOperator(c) && c != '(' && c != ')' && c != '[' && c != ']' &&
           c != '^' && c != '$' && c != '\';
}

int main() {
    const char CONCAT = '\1';
    std::string pattern = "abc";
    std::string expanded;
    
    std::cout << "Original pattern: " << pattern << std::endl;
    
    for (size_t i = 0; i < pattern.length(); i++) {
        char c = pattern[i];
        std::cout << "Processing '" << c << "' (ASCII " << (int)c << ")" << std::endl;

        if (c == '\') {
            expanded += c;
            if (i + 1 < pattern.length()) {
                expanded += pattern[++i];
            }
            continue;
        }

        expanded += c;
        std::cout << "  Added to expanded, length now: " << expanded.length() << std::endl;

        // Aggiungi operatore di concatenazione
        if (i + 1 < pattern.length()) {
            char next = pattern[i + 1];
            std::cout << "  Next char: '" << next << "' (ASCII " << (int)next << ")" << std::endl;

            bool curr_is_operand = isOperand(c) || c == '.' || c == ')' || c == '*' ||
                                   c == '+' || c == '?' || c == ']' || c == '$';
            bool next_is_operand = isOperand(next) || next == '.' || next == '(' ||
                                   next == '[' || next == '^' || next == '\';
                                   
            std::cout << "  curr_is_operand: " << curr_is_operand << ", next_is_operand: " << next_is_operand << std::endl;

            if (curr_is_operand && next_is_operand) {
                expanded += CONCAT;
                std::cout << "  Added CONCAT, length now: " << expanded.length() << std::endl;
            }
        }
    }
    
    std::cout << "\nExpanded string (length " << expanded.length() << "): ";
    for (char c : expanded) {
        if (c == CONCAT) {
            std::cout << "CONCAT ";
        } else {
            std::cout << "'" << c << "' ";
        }
    }
    std::cout << std::endl;
    
    return 0;
}
