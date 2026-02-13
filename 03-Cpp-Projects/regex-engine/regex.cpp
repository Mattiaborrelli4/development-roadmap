#include "regex.h"
#include <cctype>
#include <stdexcept>

namespace regex_engine {

// ==================== RegexLexer Implementation ====================

RegexLexer::RegexLexer(const std::string& pattern)
    : pattern_(pattern), pos_(0), current_token_(TokenType::END) {
    scanToken();
}

void RegexLexer::advance() {
    if (pos_ < pattern_.length()) {
        pos_++;
    }
    scanToken();
}

void RegexLexer::retreat() {
    if (pos_ > 0) {
        pos_--;
    }
    scanToken();
}

void RegexLexer::scanToken() {
    if (pos_ >= pattern_.length()) {
        current_token_ = Token(TokenType::END);
        return;
    }

    char c = pattern_[pos_];

    switch (c) {
        case '.':
            current_token_ = Token(TokenType::DOT);
            pos_++;
            break;
        case '*':
            current_token_ = Token(TokenType::STAR);
            pos_++;
            break;
        case '+':
            current_token_ = Token(TokenType::PLUS);
            pos_++;
            break;
        case '?':
            current_token_ = Token(TokenType::QUESTION);
            pos_++;
            break;
        case '^':
            current_token_ = Token(TokenType::CARET);
            pos_++;
            break;
        case '$':
            current_token_ = Token(TokenType::DOLLAR);
            pos_++;
            break;
        case '(':
            current_token_ = Token(TokenType::LPAREN);
            pos_++;
            break;
        case ')':
            current_token_ = Token(TokenType::RPAREN);
            pos_++;
            break;
        case '[':
            current_token_ = Token(TokenType::LBRACKET);
            pos_++;
            break;
        case ']':
            current_token_ = Token(TokenType::RBRACKET);
            pos_++;
            break;
        case '|':
            current_token_ = Token(TokenType::OR);
            pos_++;
            break;
        case '\\':
            // Escape sequence
            if (pos_ + 1 < pattern_.length()) {
                current_token_ = Token(TokenType::LITERAL, pattern_[pos_ + 1]);
                pos_ += 2;
            } else {
                current_token_ = Token(TokenType::LITERAL, '\\');
                pos_++;
            }
            break;
        default:
            // Carattere letterale
            current_token_ = Token(TokenType::LITERAL, c);
            pos_++;
            break;
    }
}

// ==================== RegexParser Implementation ====================

RegexParser::RegexParser(RegexLexer& lexer)
    : lexer_(lexer), pattern_(), is_valid_(false) {
    // Initialize pattern from lexer if needed
    (void)lexer_;  // Suppress unused warning
}

void RegexParser::parse() {
    try {
        parseExpression();
        is_valid_ = lexer_.getCurrentToken().type == TokenType::END;
    } catch (...) {
        is_valid_ = false;
    }
}

void RegexParser::parseExpression() {
    parseTerm();

    // Gestisci operatori OR (|)
    while (lexer_.getCurrentToken().type == TokenType::OR) {
        lexer_.advance();
        parseTerm();
    }
}

void RegexParser::parseTerm() {
    parseFactor();

    // Concatenazione implicita - continua a parsare factors
    while (lexer_.getCurrentToken().type == TokenType::LITERAL ||
           lexer_.getCurrentToken().type == TokenType::DOT ||
           lexer_.getCurrentToken().type == TokenType::LPAREN ||
           lexer_.getCurrentToken().type == TokenType::LBRACKET ||
           lexer_.getCurrentToken().type == TokenType::CARET) {
        parseFactor();
    }
}

void RegexParser::parseFactor() {
    parsePrimary();

    // Gestisci operatori di ripetizione (*, +, ?)
    Token token = lexer_.getCurrentToken();
    if (token.type == TokenType::STAR ||
        token.type == TokenType::PLUS ||
        token.type == TokenType::QUESTION) {
        lexer_.advance();
    }
}

void RegexParser::parsePrimary() {
    Token token = lexer_.getCurrentToken();

    if (token.type == TokenType::LITERAL) {
        lexer_.advance();
    } else if (token.type == TokenType::DOT) {
        lexer_.advance();
    } else if (token.type == TokenType::CARET) {
        lexer_.advance();
    } else if (token.type == TokenType::DOLLAR) {
        lexer_.advance();
    } else if (token.type == TokenType::LPAREN) {
        lexer_.advance();
        parseExpression();
        if (lexer_.getCurrentToken().type != TokenType::RPAREN) {
            throw std::runtime_error("Missing closing parenthesis");
        }
        lexer_.advance();
    } else if (token.type == TokenType::LBRACKET) {
        lexer_.advance();
        // Parse character class
        while (lexer_.getCurrentToken().type != TokenType::RBRACKET &&
               !lexer_.isAtEnd()) {
            lexer_.advance();
        }
        if (lexer_.getCurrentToken().type != TokenType::RBRACKET) {
            throw std::runtime_error("Missing closing bracket");
        }
        lexer_.advance();
    } else {
        throw std::runtime_error("Unexpected token in pattern");
    }
}

} // namespace regex_engine
