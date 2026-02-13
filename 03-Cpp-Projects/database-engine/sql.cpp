#include "sql.h"
#include <iostream>
#include <algorithm>
#include <sstream>
#include <cctype>

// SQLTokenizer Implementation
char SQLTokenizer::current_char() {
    if (pos < input.size()) {
        return input[pos];
    }
    return '\0';
}

void SQLTokenizer::advance() {
    ++pos;
}

void SQLTokenizer::skip_whitespace() {
    while (pos < input.size() && std::isspace(input[pos])) {
        ++pos;
    }
}

std::string SQLTokenizer::get_next_token() {
    skip_whitespace();

    if (pos >= input.size()) {
        return "";
    }

    char c = input[pos];

    // Parentesi
    if (c == '(' || c == ')' || c == ',' || c == ';') {
        ++pos;
        return std::string(1, c);
    }

    // Operatori
    if (c == '=' || c == '!' || c == '>' || c == '<') {
        std::string op;
        op += c;
        ++pos;
        if (pos < input.size() && input[pos] == '=') {
            op += '=';
            ++pos;
        }
        return op;
    }

    // Stringhe tra apici
    if (c == '\'' || c == '"') {
        char quote = c;
        ++pos;
        std::string str;
        while (pos < input.size() && input[pos] != quote) {
            str += input[pos];
            ++pos;
        }
        ++pos; // Skip closing quote
        return str;
    }

    * Identificatori o keywords
    if (std::isalpha(c) || c == '_') {
        std::string token;
        while (pos < input.size() && (std::isalnum(input[pos]) || input[pos] == '_')) {
            token += input[pos];
            ++pos;
        }
        return token;
    }

    // Numeri
    if (std::isdigit(c) || c == '-') {
        std::string token;
        while (pos < input.size() && (std::isdigit(input[pos]) || input[pos] == '.')) {
            token += input[pos];
            ++pos;
        }
        return token;
    }

    // Default (carattere singolo)
    ++pos;
    return std::string(1, c);
}

std::vector<std::string> SQLTokenizer::tokenize() {
    std::vector<std::string> tokens;
    std::string token;
    while ((token = get_next_token()) != "") {
        // Converti a uppercase per keywords
        std::string upper_token = token;
        std::transform(upper_token.begin(), upper_token.end(), upper_token.begin(), ::toupper);

        // Mantieni originale se è un valore tra apici, altrimenti usa uppercase
        if (token[0] != '\'' && token[0] != '"') {
            tokens.push_back(upper_token);
        } else {
            tokens.push_back(token);
        }
    }
    return tokens;
}

// SQLParser Implementation
std::string SQLParser::current_token() {
    if (pos < tokens.size()) {
        return tokens[pos];
    }
    return "";
}

void SQLParser::advance() {
    ++pos;
}

bool SQLParser::has_more() {
    return pos < tokens.size();
}

SQLCommand SQLParser::parse_command() {
    std::string cmd = current_token();
    advance();

    if (cmd == "CREATE") {
        // Controlla se c'è "TABLE"
        if (current_token() == "TABLE") {
            advance();
            return SQLCommand::CREATE_TABLE;
        }
    } else if (cmd == "INSERT") {
        // Controlla "INTO"
        if (current_token() == "INTO") {
            advance();
            return SQLCommand::INSERT;
        }
    } else if (cmd == "SELECT") {
        return SQLCommand::SELECT;
    } else if (cmd == "UPDATE") {
        return SQLCommand::UPDATE;
    } else if (cmd == "DELETE") {
        return SQLCommand::DELETE;
    }

    return SQLCommand::UNKNOWN;
}

std::vector<std::string> SQLParser::parse_column_list() {
    std::vector<std::string> columns;

    if (current_token() == "(") {
        advance();
    }

    while (has_more() && current_token() != ")") {
        if (current_token() != ",") {
            columns.push_back(current_token());
        }
        advance();
    }

    if (current_token() == ")") {
        advance();
    }

    return columns;
}

std::vector<std::string> SQLParser::parse_value_list() {
    std::vector<std::string> values;

    if (current_token() == "(") {
        advance();
    }

    while (has_more() && current_token() != ")") {
        if (current_token() != ",") {
            values.push_back(current_token());
        }
        advance();
    }

    if (current_token() == ")") {
        advance();
    }

    return values;
}

WhereCondition SQLParser::parse_where_clause() {
    WhereCondition cond;

    if (current_token() == "WHERE") {
        advance();
        cond.column = current_token();
        advance();
        cond.op = current_token();
        advance();
        cond.value = current_token();
        advance();
    }

    return cond;
}

std::pair<std::vector<std::string>, std::vector<std::string>> SQLParser::parse_set_clause() {
    std::vector<std::string> columns;
    std::vector<std::string> values;

    if (current_token() == "SET") {
        advance();

        while (has_more() && current_token() != "WHERE") {
            if (current_token() != ",") {
                columns.push_back(current_token());
                advance(); // column
                advance(); // =
                values.push_back(current_token());
                advance(); // value
            } else {
                advance();
            }
        }
    }

    return {columns, values};
}

ParsedSQL SQLParser::parse() {
    ParsedSQL result;

    if (!has_more()) {
        return result;
    }

    result.command = parse_command();

    if (result.command == SQLCommand::UNKNOWN) {
        return result;
    }

    // Parse table name
    if (has_more()) {
        result.table_name = current_token();
        advance();
    }

    // Parse based on command type
    switch (result.command) {
        case SQLCommand::CREATE_TABLE:
            result.columns = parse_column_list();
            break;

        case SQLCommand::INSERT:
            if (current_token() == "(") {
                // Opzionale: colonne specificate
                // Ignoriamo per semplicità
                result.columns = parse_column_list();
            }
            if (current_token() == "VALUES") {
                advance();
            }
            result.values = parse_value_list();
            break;

        case SQLCommand::SELECT:
            // Parse SELECT columns
            while (has_more() && current_token() != "FROM") {
                if (current_token() != ",") {
                    result.select_columns.push_back(current_token());
                }
                advance();
            }
            if (current_token() == "FROM") {
                advance();
                result.table_name = current_token();
                advance();
            }
            result.where = parse_where_clause();
            break;

        case SQLCommand::UPDATE:
            result.table_name = current_token();
            advance();
            std::tie(result.update_columns, result.update_values) = parse_set_clause();
            result.where = parse_where_clause();
            break;

        case SQLCommand::DELETE:
            if (current_token() == "FROM") {
                advance();
                result.table_name = current_token();
                advance();
            }
            result.where = parse_where_clause();
            break;

        default:
            break;
    }

    return result;
}

// Funzioni helper
ParsedSQL parse_sql(const std::string& sql) {
    SQLTokenizer tokenizer(sql);
    auto tokens = tokenizer.tokenize();

    SQLParser parser(tokens);
    return parser.parse();
}

std::string sql_command_to_string(SQLCommand cmd) {
    switch (cmd) {
        case SQLCommand::CREATE_TABLE: return "CREATE_TABLE";
        case SQLCommand::INSERT: return "INSERT";
        case SQLCommand::SELECT: return "SELECT";
        case SQLCommand::UPDATE: return "UPDATE";
        case SQLCommand::DELETE: return "DELETE";
        default: return "UNKNOWN";
    }
}
