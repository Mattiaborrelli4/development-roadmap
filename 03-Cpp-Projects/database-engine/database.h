#ifndef DATABASE_H
#define DATABASE_H

#include "btree.h"
#include "sql.h"
#include <string>
#include <map>
#include <memory>
#include <fstream>

// Struct per rappresentare una riga
struct Row {
    std::map<std::string, std::string> data; // column -> value

    void serialize(std::ofstream& out) const;
    void deserialize(std::ifstream& in);
};

// Struct per rappresentare una tabella
struct Table {
    std::string name;
    std::vector<std::string> columns;
    BTree index;  // B-tree per indicizzazione (usiamo la prima colonna come chiave)
    std::map<int, Row> rows; // Cache delle righe (key -> row)

    Table() = default;
    explicit Table(const std::string& n) : name(n) {}

    // Serializzazione
    void serialize(std::ofstream& out) const;
    void deserialize(std::ifstream& in);
};

// Classe principale del Database
class Database {
private:
    std::string name;
    std::map<std::string, std::shared_ptr<Table>> tables;

    std::string get_filename() const;

public:
    explicit Database(const std::string& db_name);

    // Operazioni DDL
    bool create_table(const std::string& name, const std::vector<std::string>& columns);
    bool table_exists(const std::string& name) const;
    std::shared_ptr<Table> get_table(const std::string& name);

    // Operazioni DML
    bool insert_into(const std::string& table_name, const std::vector<std::string>& values);
    std::vector<Row> select_from(const std::string& table_name,
                                const std::vector<std::string>& columns = {},
                                const WhereCondition& where = WhereCondition());
    bool update(const std::string& table_name,
               const std::vector<std::string>& update_columns,
               const std::vector<std::string>& update_values,
               const WhereCondition& where);
    bool delete_from(const std::string& table_name, const WhereCondition& where);

    // Esecuzione di comandi SQL
    std::string execute(const std::string& sql);
    std::string execute(const ParsedSQL& parsed);

    // Persistence
    bool save();
    bool load();

    // Debug
    void print_schema() const;
};

#endif // DATABASE_H
