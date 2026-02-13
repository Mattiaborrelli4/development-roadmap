#ifndef REGEX_H
#define REGEX_H

#include <string>
#include <vector>
#include <memory>

namespace regex_engine {

// Token types per il parsing delle regex
enum class TokenType {
    LITERAL,      // Carattere letterale
    DOT,          // . - qualsiasi carattere
    STAR,         // * - zero o più ripetizioni
    PLUS,         // + - uno o più ripetizioni
    QUESTION,     // ? - zero o uno
    CARET,        // ^ - inizio stringa
    DOLLAR,       // $ - fine stringa
    LPAREN,       // ( - parentesi aperta
    RPAREN,       // ) - parentesi chiusa
    LBRACKET,     // [ - parentesi quadra aperta
    RBRACKET,     // ] - parentesi quadra chiusa
    OR,           // | - OR logico
    ESCAPE,       // \ - carattere di escape
    END           // Fine del pattern
};

// Rappresenta un token nel pattern regex
struct Token {
    TokenType type;
    char value;  // Carattere effettivo (per literali)

    Token(TokenType t, char v = '\0') : type(t), value(v) {}
};

// Lexer per tokenizzare il pattern regex
class RegexLexer {
public:
    explicit RegexLexer(const std::string& pattern);

    // Restituisce il token corrente
    Token getCurrentToken() const { return current_token_; }

    // Avanza al prossimo token
    void advance();

    // Ritorna alla posizione precedente
    void retreat();

    // Controlla se siamo alla fine del pattern
    bool isAtEnd() const { return pos_ >= pattern_.length(); }

private:
    std::string pattern_;
    size_t pos_;
    Token current_token_;

    void scanToken();
};

// Parser per costruire l'albero sintattico dal pattern
class RegexParser {
public:
    explicit RegexParser(RegexLexer& lexer);

    // Parsa il pattern completo
    void parse();

    // Restituisce il pattern parsato per NFA construction
    std::string getPattern() const { return pattern_; }

    // Verifica se il pattern è valido
    bool isValid() const { return is_valid_; }

private:
    RegexLexer& lexer_;
    std::string pattern_;
    bool is_valid_;

    void parseExpression();
    void parseTerm();
    void parseFactor();
    void parsePrimary();
};

} // namespace regex_engine

#endif // REGEX_H
