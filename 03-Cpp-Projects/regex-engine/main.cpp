#include "regex.h"
#include "nfa.h"
#include "dfa.h"
#include <iostream>
#include <string>
#include <vector>
#include <cassert>

using namespace regex_engine;

// Colore per output console
namespace colors {
    const char* RESET = "\033[0m";
    const char* RED = "\033[31m";
    const char* GREEN = "\033[32m";
    const char* YELLOW = "\033[33m";
    const char* BLUE = "\033[34m";
    const char* CYAN = "\033[36m";
}

// Funzione di test
void runTest(const std::string& pattern, const std::string& input, bool expected, const std::string& description) {
    try {
        auto nfa = NFA::fromPattern(pattern);
        auto dfa = DFA::fromNFA(*nfa);
        DFAMatcher matcher(*dfa);

        bool result = matcher.match(input);

        if (result == expected) {
            std::cout << colors::GREEN << "[PASS]" << colors::RESET;
        } else {
            std::cout << colors::RED << "[FAIL]" << colors::RESET;
        }

        std::cout << " " << description << std::endl;
        std::cout << "       Pattern: " << colors::CYAN << pattern << colors::RESET;
        std::cout << ", Input: \"" << colors::YELLOW << input << colors::RESET << "\"";
        std::cout << ", Expected: " << (expected ? "true" : "false");
        std::cout << ", Got: " << (result ? "true" : "false") << std::endl;
    } catch (const std::exception& e) {
        std::cout << colors::RED << "[ERROR]" << colors::RESET << " " << description << std::endl;
        std::cout << "       Exception: " << e.what() << std::endl;
    }
}

void runSearchTest(const std::string& pattern, const std::string& input,
                   bool expected_found, size_t expected_start, size_t expected_end,
                   const std::string& description) {
    try {
        auto nfa = NFA::fromPattern(pattern);
        auto dfa = DFA::fromNFA(*nfa);

        size_t start, end;
        bool found = dfa->search(input, start, end);

        if (found == expected_found && (!found || (start == expected_start && end == expected_end))) {
            std::cout << colors::GREEN << "[PASS]" << colors::RESET;
        } else {
            std::cout << colors::RED << "[FAIL]" << colors::RESET;
        }

        std::cout << " " << description << std::endl;
        std::cout << "       Pattern: " << colors::CYAN << pattern << colors::RESET;
        std::cout << ", Input: \"" << colors::YELLOW << input << colors::RESET << "\"";

        if (found) {
            std::cout << ", Found at: [" << start << "," << end << ")";
        } else {
            std::cout << ", Not found";
        }

        std::cout << std::endl;
    } catch (const std::exception& e) {
        std::cout << colors::RED << "[ERROR]" << colors::RESET << " " << description << std::endl;
        std::cout << "       Exception: " << e.what() << std::endl;
    }
}

// Suite di test
void runTests() {
    std::cout << "\n" << colors::BLUE << "========================================" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "   REGEX ENGINE - SUITE DI TEST" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "========================================" << colors::RESET << "\n" << std::endl;

    std::cout << colors::CYAN << "=== TEST: Match Letterale ===" << colors::RESET << std::endl;
    runTest("a", "a", true, "Match letterale 'a'");
    runTest("a", "b", false, "No match per letterale diverso");
    runTest("abc", "abc", true, "Match multipli caratteri");
    runTest("abc", "abd", false, "No match per stringa diversa");

    std::cout << "\n" << colors::CYAN << "=== TEST: Dot (.) - Qualsiasi Carattere ===" << colors::RESET << std::endl;
    runTest("a.b", "aab", true, "Dot matcha qualsiasi carattere");
    runTest("a.b", "abb", true, "Dot matcha qualsiasi carattere");
    runTest("a.b", "acb", true, "Dot matcha qualsiasi carattere");
    runTest("a.b", "ab", false, "Dot richiede un carattere");

    std::cout << "\n" << colors::CYAN << "=== TEST: Star (*) - Zero o Più ===" << colors::RESET << std::endl;
    runTest("a*", "", true, "Star: zero occorrenze");
    runTest("a*", "a", true, "Star: una occorrenza");
    runTest("a*", "aaa", true, "Star: multiple occorrenze");
    runTest("a*", "b", false, "Star: non matcha caratteri diversi");  // Corretto: a* non matcha 'b'
    runTest("aa*", "a", true, "Star: una 'a' seguita da zero 'a'");
    runTest("aa*", "aaa", true, "Star: una 'a' seguita da multiple 'a'");

    std::cout << "\n" << colors::CYAN << "=== TEST: Plus (+) - Uno o Più ===" << colors::RESET << std::endl;
    runTest("a+", "a", true, "Plus: una occorrenza");
    runTest("a+", "aaa", true, "Plus: multiple occorrenze");
    runTest("a+", "", false, "Plus: richiede almeno una occorrenza");
    runTest("a+", "b", false, "Plus: no match con carattere diverso");

    std::cout << "\n" << colors::CYAN << "=== TEST: Question (?) - Zero o Uno ===" << colors::RESET << std::endl;
    runTest("a?", "", true, "Question: zero occorrenze");
    runTest("a?", "a", true, "Question: una occorrenza");
    runTest("a?", "aa", true, "Question: una occorrenza matchata");
    runTest("ab?", "a", true, "Question: 'b' opzionale assente");
    runTest("ab?", "ab", true, "Question: 'b' opzionale presente");

    std::cout << "\n" << colors::CYAN << "=== TEST: Caret (^) - Inizio Stringa ===" << colors::RESET << std::endl;
    runTest("^abc", "abc", true, "Caret: matcha inizio");
    runTest("^abc", "xabc", false, "Caret: no match se non all'inizio");

    std::cout << "\n" << colors::CYAN << "=== TEST: Dollar ($) - Fine Stringa ===" << colors::RESET << std::endl;
    runTest("xyz$", "xyz", true, "Dollar: matcha fine");
    runTest("xyz$", "xyzu", false, "Dollar: no match se non alla fine");

    std::cout << "\n" << colors::CYAN << "=== TEST: Combinazioni Complesse ===" << colors::RESET << std::endl;
    runTest("a*b", "b", true, "Star seguito da letterale: zero 'a'");
    runTest("a*b", "ab", true, "Star seguito da letterale: una 'a'");
    runTest("a*b", "aaab", true, "Star seguito da letterale: multiple 'a'");
    runTest("a*b", "ba", false, "Star seguito da letterale: ordine sbagliato");
    runTest("a+b", "ab", true, "Plus seguito da letterale");
    runTest("a+b", "aaab", true, "Plus seguito da letterale: multiple 'a'");
    runTest("a+b", "b", false, "Plus: richiede almeno una 'a'");

    std::cout << "\n" << colors::CYAN << "=== TEST: Concatenazione ===" << colors::RESET << std::endl;
    runTest("abc", "abc", true, "Concatenazione semplice");
    runTest("a.b.c", "axbyc", true, "Concatenazione con dot");
    runTest("a*b", "aaab", true, "Concatenazione con star");

    std::cout << "\n" << colors::CYAN << "=== TEST: Search (Trova Occorrenza) ===" << colors::RESET << std::endl;
    runSearchTest("abc", "xyzabcuvw", true, 3, 6, "Search: pattern nel mezzo");
    runSearchTest("abc", "abc", true, 0, 3, "Search: pattern all'inizio");
    runSearchTest("abc", "xyzabc", true, 3, 6, "Search: pattern alla fine");
    runSearchTest("abc", "xyzab", false, 0, 0, "Search: pattern non trovato");
    runSearchTest("a.b", "xaayb", false, 0, 0, "Search: dot non matcha con caratteri multipli");
    runSearchTest("a.b", "xayb", true, 1, 4, "Search: dot matcha un carattere");

    std::cout << "\n" << colors::CYAN << "=== TEST: Pattern Complessi ===" << colors::RESET << std::endl;
    runTest("a.*b", "ab", true, "Dot star: match minimo");
    runTest("a.*b", "axxxxxb", true, "Dot star: match con caratteri intermedi");
    runTest("a.*b", "axb", true, "Dot star: match con un carattere intermedio");
    runTest("a.+b", "ab", false, "Dot plus: richiede almeno un carattere");
    runTest("a.+b", "axb", true, "Dot plus: match con un carattere");
    runTest("a.+b", "axxxxxb", true, "Dot plus: match con caratteri intermedi");

    std::cout << "\n" << colors::CYAN << "=== TEST: Edge Cases ===" << colors::RESET << std::endl;
    runTest("", "", true, "Pattern vuoto matcha stringa vuota");
    runTest("a", "", false, "Pattern non vuoto non matcha stringa vuota");
    runTest("a*", "aaaaa", true, "Star con molte ripetizioni");
    runTest("aaaaaaaaaa", "aaaaaaaaaa", true, "Pattern lungo esatto");

    std::cout << "\n" << colors::BLUE << "========================================" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "   TEST COMPLETATI" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "========================================" << colors::RESET << "\n" << std::endl;
}

// Modalità interattiva
void interactiveMode() {
    std::cout << "\n" << colors::BLUE << "========================================" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "   MODALITÀ INTERATTIVA" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "========================================" << colors::RESET << "\n" << std::endl;

    std::cout << "Inserisci " << colors::CYAN << "pattern" << colors::RESET << " e " << colors::YELLOW << "stringa" << colors::RESET;
    std::cout << " da testare (o " << colors::RED << "quit" << colors::RESET << " per uscire)\n" << std::endl;

    while (true) {
        std::string pattern, input;

        std::cout << colors::CYAN << "Pattern: " << colors::RESET;
        std::getline(std::cin, pattern);

        if (pattern == "quit" || pattern == "exit" || pattern == "q") {
            break;
        }

        if (pattern.empty()) {
            std::cout << colors::YELLOW << "Pattern vuoto non valido. Riprova." << colors::RESET << "\n" << std::endl;
            continue;
        }

        std::cout << colors::YELLOW << "Input:   " << colors::RESET;
        std::getline(std::cin, input);

        try {
            auto nfa = NFA::fromPattern(pattern);
            auto dfa = DFA::fromNFA(*nfa);
            DFAMatcher matcher(*dfa);

            // Test match completo
            bool match = matcher.match(input);
            std::cout << "\nRisultato " << colors::GREEN << "Match: " << colors::RESET;
            if (match) {
                std::cout << colors::GREEN << "TRUE" << colors::RESET;
            } else {
                std::cout << colors::RED << "FALSE" << colors::RESET;
            }
            std::cout << std::endl;

            // Test search
            size_t start, end;
            bool found = dfa->search(input, start, end);
            std::cout << "Risultato " << colors::GREEN << "Search: " << colors::RESET;
            if (found) {
                std::cout << colors::GREEN << "TRUE" << colors::RESET << " (trovato alle posizioni [" << start << ":" << end << ")" << std::endl;
                std::cout << "        \"" << input.substr(0, start) << colors::GREEN << input.substr(start, end - start) << colors::RESET << input.substr(end) << "\"" << std::endl;
            } else {
                std::cout << colors::RED << "FALSE" << colors::RESET << " (non trovato)" << std::endl;
            }

            // Mostra statistiche
            std::cout << "\nStatistiche:" << std::endl;
            std::cout << "  Stati NFA: " << nfa->getStates().size() << std::endl;
            std::cout << "  Transizioni NFA: " << nfa->getTransitions().size() << std::endl;
            std::cout << "  Stati DFA: " << dfa->getStates().size() << std::endl;
            std::cout << "  Transizioni DFA: " << dfa->getTransitions().size() << std::endl;

        } catch (const std::exception& e) {
            std::cout << colors::RED << "\nErrore: " << colors::RESET << e.what() << std::endl;
        }

        std::cout << std::endl;
    }
}

// Stampa usage
void printUsage(const char* program_name) {
    std::cout << "Uso: " << program_name << " [opzioni]" << std::endl;
    std::cout << "\nOpzioni:" << std::endl;
    std::cout << "  " << colors::CYAN << "test" << colors::RESET << "       Esegue la suite di test" << std::endl;
    std::cout << "  " << colors::CYAN << "interactive" << colors::RESET << " Modalità interattiva" << std::endl;
    std::cout << "  " << colors::CYAN << "help" << colors::RESET << "      Mostra questo help" << std::endl;
    std::cout << "\nPattern supportati:" << std::endl;
    std::cout << "  " << colors::YELLOW << "." << colors::RESET << "    - Qualsiasi carattere" << std::endl;
    std::cout << "  " << colors::YELLOW << "*" << colors::RESET << "    - Zero o più ripetizioni" << std::endl;
    std::cout << "  " << colors::YELLOW << "+" << colors::RESET << "    - Uno o più ripetizioni" << std::endl;
    std::cout << "  " << colors::YELLOW << "?" << colors::RESET << "    - Zero o una ripetizione" << std::endl;
    std::cout << "  " << colors::YELLOW << "^" << colors::RESET << "    - Inizio stringa" << std::endl;
    std::cout << "  " << colors::YELLOW << "$" << colors::RESET << "    - Fine stringa" << std::endl;
    std::cout << "\nEsempi:" << std::endl;
    std::cout << "  a.b    - Match 'a' seguito da qualsiasi carattere poi 'b'" << std::endl;
    std::cout << "  a*     - Zero o più 'a'" << std::endl;
    std::cout << "  a+     - Uno o più 'a'" << std::endl;
    std::cout << "  ^abc   - Stringa che inizia con 'abc'" << std::endl;
    std::cout << "  xyz$   - Stringa che finisce con 'xyz'" << std::endl;
}

int main(int argc, char* argv[]) {
    std::cout << "\n" << colors::BLUE << "╔══════════════════════════════════════╗" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "║" << colors::RESET << "      C++ REGEX ENGINE v1.0        " << colors::BLUE << "║" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "║   NFA/DFA Implementation             ║" << colors::RESET << std::endl;
    std::cout << colors::BLUE << "╚══════════════════════════════════════╝" << colors::RESET << "\n" << std::endl;

    if (argc > 1) {
        std::string arg = argv[1];

        if (arg == "test" || arg == "t") {
            runTests();
        } else if (arg == "interactive" || arg == "i") {
            interactiveMode();
        } else if (arg == "help" || arg == "h" || arg == "--help") {
            printUsage(argv[0]);
        } else {
            std::cout << colors::RED << "Opzione non riconosciuta: " << colors::RESET << arg << std::endl;
            printUsage(argv[0]);
            return 1;
        }
    } else {
        // Default: mostra menu
        std::cout << "Seleziona modalità:" << std::endl;
        std::cout << "  1. Esegui test" << std::endl;
        std::cout << "  2. Modalità interattiva" << std::endl;
        std::cout << "  3. Help" << std::endl;
        std::cout << "\nScelta: ";

        std::string choice;
        std::getline(std::cin, choice);

        if (choice == "1") {
            runTests();
        } else if (choice == "2") {
            interactiveMode();
        } else {
            printUsage(argv[0]);
        }
    }

    return 0;
}
