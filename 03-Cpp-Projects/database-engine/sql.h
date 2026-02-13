#ifndef SQL_H
#define SQL_H

#include <string>
#include <vector>
#include <memory>

// Enum per i tipi di comandi SQL
enum class SQLCommand {
    CREATE_TABLE,
    INSERT,
    SELECT,
    UPDATE,
    DELETE,
    UNKNOWN
};

// Struct per rappresentare una condizione WHERE
struct WhereCondition {
    std::string column;
    std::string op;  // "==", "!=", ">", "<", ">=", "<="
    std::string value;

    WhereCondition() = default;
    WhereCondition(const std::string& col, const std::string& o, const std::string& v)
        : column(col), op(o), value(v) {}
};

// Struct per rappresentare un comando SQL parsato
struct ParsedSQL {
    SQLCommand command;
    std::string table_name;
    std::vector<std::string> columns;
    std::vector<std::string> values;
    std::vector<std::string> select_columns;
    WhereCondition where;
    std::vector<std::string> update_columns;
    std::vector<std::string> update_values;

    ParsedSQL() : command(SQLCommand::UNKNOWN) {}
};

// Tokenizer per SQL
class SQLTokenizer {
private:
    std::string input;
    size_t pos;

    char current_char();
    void advance();
    void skip_whitespace();

public:
    explicit SQLTokenizer(const std::string& sql) : input(sql), pos(0) {}

    std::string get_next_token();
    std::vector<std::string> tokenize();
};

// Parser SQL
class SQLParser {
private:
    std::vector<std::string> tokens;
    size_t pos;

    std::string current_token();
    void advance();
    bool has_more();
    void skip_whitespace();

    // Parsing helper functions
    SQLCommand parse_command();
    std::vector<std::string> parse_column_list();
    std::vector<std::string> parse_value_list();
    WhereCondition parse_where_clause();
    std::pair<std::vector<std::string>, std::vector<std::string>> parse_set_clause();

public:
    explicit SQLParser(const std::vector<std::string>& t) : tokens(t), pos(0) {}

    ParsedSQL parse();
};

// Funzioni helper per il parsing
ParsedSQL parse_sql(const std::string& sql);
std::string sql_command_to_string(SQLCommand cmd);

#endif // SQL_H
