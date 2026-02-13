#include "database.h"
#include <iostream>
#include <sstream>
#include <iomanip>

// Row Implementation
void Row::serialize(std::ofstream& out) const {
    size_t num_cols = data.size();
    out.write(reinterpret_cast<const char*>(&num_cols), sizeof(num_cols));

    for (const auto& [col, val] : data) {
        size_t col_size = col.size();
        out.write(reinterpret_cast<const char*>(&col_size), sizeof(col_size));
        out.write(col.c_str(), col_size);

        size_t val_size = val.size();
        out.write(reinterpret_cast<const char*>(&val_size), sizeof(val_size));
        out.write(val.c_str(), val_size);
    }
}

void Row::deserialize(std::ifstream& in) {
    size_t num_cols = 0;
    in.read(reinterpret_cast<char*>(&num_cols), sizeof(num_cols));

    for (size_t i = 0; i < num_cols; ++i) {
        std::string col, val;
        size_t size = 0;

        in.read(reinterpret_cast<char*>(&size), sizeof(size));
        col.resize(size);
        in.read(&col[0], size);

        in.read(reinterpret_cast<char*>(&size), sizeof(size));
        val.resize(size);
        in.read(&val[0], size);

        data[col] = val;
    }
}

// Table Implementation
void Table::serialize(std::ofstream& out) const {
    // Scrivi nome tabella
    size_t name_size = name.size();
    out.write(reinterpret_cast<const char*>(&name_size), sizeof(name_size));
    out.write(name.c_str(), name_size);

    // Scrivi colonne
    size_t num_cols = columns.size();
    out.write(reinterpret_cast<const char*>(&num_cols), sizeof(num_cols));
    for (const auto& col : columns) {
        size_t col_size = col.size();
        out.write(reinterpret_cast<const char*>(&col_size), sizeof(col_size));
        out.write(col.c_str(), col_size);
    }

    // Scrivi righe
    size_t num_rows = rows.size();
    out.write(reinterpret_cast<const char*>(&num_rows), sizeof(num_rows));
    for (const auto& [key, row] : rows) {
        out.write(reinterpret_cast<const char*>(&key), sizeof(key));
        row.serialize(out);
    }

    // Scrivi B-tree
    index.serialize(out);
}

void Table::deserialize(std::ifstream& in) {
    // Leggi nome tabella
    size_t name_size = 0;
    in.read(reinterpret_cast<char*>(&name_size), sizeof(name_size));
    name.resize(name_size);
    in.read(&name[0], name_size);

    // Leggi colonne
    size_t num_cols = 0;
    in.read(reinterpret_cast<char*>(&num_cols), sizeof(num_cols));
    columns.resize(num_cols);
    for (size_t i = 0; i < num_cols; ++i) {
        size_t col_size = 0;
        in.read(reinterpret_cast<char*>(&col_size), sizeof(col_size));
        columns[i].resize(col_size);
        in.read(&columns[i][0], col_size);
    }

    // Leggi righe
    size_t num_rows = 0;
    in.read(reinterpret_cast<char*>(&num_rows), sizeof(num_rows));
    for (size_t i = 0; i < num_rows; ++i) {
        int key = 0;
        in.read(reinterpret_cast<char*>(&key), sizeof(key));

        Row row;
        row.deserialize(in);
        rows[key] = row;
    }

    // Leggi B-tree
    index.deserialize(in);
}

// Database Implementation
Database::Database(const std::string& db_name) : name(db_name) {}

std::string Database::get_filename() const {
    return name + ".db";
}

bool Database::create_table(const std::string& table_name, const std::vector<std::string>& columns) {
    if (table_exists(table_name)) {
        return false;
    }

    auto table = std::make_shared<Table>(table_name);
    table->columns = columns;
    tables[table_name] = table;

    return true;
}

bool Database::table_exists(const std::string& table_name) const {
    return tables.find(table_name) != tables.end();
}

std::shared_ptr<Table> Database::get_table(const std::string& table_name) {
    auto it = tables.find(table_name);
    if (it != tables.end()) {
        return it->second;
    }
    return nullptr;
}

bool Database::insert_into(const std::string& table_name, const std::vector<std::string>& values) {
    auto table = get_table(table_name);
    if (!table) {
        return false;
    }

    if (values.size() != table->columns.size()) {
        std::cerr << "Errore: Numero di valori non corrisponde al numero di colonne\n";
        return false;
    }

    Row row;
    int key = 0; // Usiamo la prima colonna come chiave intera

    for (size_t i = 0; i < table->columns.size() && i < values.size(); ++i) {
        row.data[table->columns[i]] = values[i];

        if (i == 0) {
            try {
                key = std::stoi(values[i]);
            } catch (...) {
                std::cerr << "Errore: La prima colonna deve essere un intero per essere usata come chiave\n";
                return false;
            }
        }
    }

    // Inserisci nel B-tree
    std::string row_data;
    for (size_t i = 1; i < table->columns.size(); ++i) {
        if (!row_data.empty()) row_data += ",";
        row_data += values[i];
    }
    table->index.insert(key, row_data);

    // Inserisci nella cache
    table->rows[key] = row;

    return true;
}

std::vector<Row> Database::select_from(const std::string& table_name,
                                       const std::vector<std::string>& columns,
                                       const WhereCondition& where) {
    std::vector<Row> result;
    auto table = get_table(table_name);
    if (!table) {
        return result;
    }

    // Se non c'è WHERE, ritorna tutte le righe
    if (where.column.empty()) {
        for (const auto& [key, row] : table->rows) {
            result.push_back(row);
        }
    } else {
        // Filtra basandosi sulla condizione WHERE
        for (const auto& [key, row] : table->rows) {
            bool match = true;

            auto it = row.data.find(where.column);
            if (it != row.data.end()) {
                std::string row_val = it->second;

                if (where.op == "==") {
                    match = (row_val == where.value);
                } else if (where.op == "!=") {
                    match = (row_val != where.value);
                } else if (where.op == ">") {
                    try {
                        match = (std::stoi(row_val) > std::stoi(where.value));
                    } catch (...) { match = false; }
                } else if (where.op == "<") {
                    try {
                        match = (std::stoi(row_val) < std::stoi(where.value));
                    } catch (...) { match = false; }
                } else if (where.op == ">=") {
                    try {
                        match = (std::stoi(row_val) >= std::stoi(where.value));
                    } catch (...) { match = false; }
                } else if (where.op == "<=") {
                    try {
                        match = (std::stoi(row_val) <= std::stoi(where.value));
                    } catch (...) { match = false; }
                }
            } else {
                match = false;
            }

            if (match) {
                result.push_back(row);
            }
        }
    }

    return result;
}

bool Database::update(const std::string& table_name,
                     const std::vector<std::string>& update_columns,
                     const std::vector<std::string>& update_values,
                     const WhereCondition& where) {
    auto table = get_table(table_name);
    if (!table) {
        return false;
    }

    if (update_columns.size() != update_values.size()) {
        return false;
    }

    auto rows = select_from(table_name, {}, where);

    for (auto& row : rows) {
        for (size_t i = 0; i < update_columns.size(); ++i) {
            row.data[update_columns[i]] = update_values[i];
        }

        // Aggiorna anche il B-tree
        int key = std::stoi(row.data[table->columns[0]]);
        std::string row_data;
        for (size_t i = 1; i < table->columns.size(); ++i) {
            if (!row_data.empty()) row_data += ",";
            row_data += row.data[table->columns[i]];
        }
        table->index.update(key, row_data);
    }

    return true;
}

bool Database::delete_from(const std::string& table_name, const WhereCondition& where) {
    auto table = get_table(table_name);
    if (!table) {
        return false;
    }

    auto rows = select_from(table_name, {}, where);

    for (const auto& row : rows) {
        int key = std::stoi(row.data[table->columns[0]]);
        table->rows.erase(key);
        table->index.remove(key);
    }

    return true;
}

std::string Database::execute(const std::string& sql) {
    auto parsed = parse_sql(sql);
    return execute(parsed);
}

std::string Database::execute(const ParsedSQL& parsed) {
    std::ostringstream result;

    switch (parsed.command) {
        case SQLCommand::CREATE_TABLE: {
            bool success = create_table(parsed.table_name, parsed.columns);
            if (success) {
                result << "Tabella '" << parsed.table_name << "' creata con successo.";
            } else {
                result << "Errore: Impossibile creare la tabella (potrebbe esistere già).";
            }
            break;
        }

        case SQLCommand::INSERT: {
            bool success = insert_into(parsed.table_name, parsed.values);
            if (success) {
                result << "Inserito con successo nella tabella '" << parsed.table_name << "'.";
            } else {
                result << "Errore nell'inserimento.";
            }
            break;
        }

        case SQLCommand::SELECT: {
            auto rows = select_from(parsed.table_name, parsed.select_columns, parsed.where);

            if (rows.empty()) {
                result << "Nessuna riga trovata.";
            } else {
                // Stampa header
                auto table = get_table(parsed.table_name);
                if (table) {
                    for (size_t i = 0; i < table->columns.size(); ++i) {
                        if (i > 0) result << " | ";
                        result << std::setw(15) << table->columns[i];
                    }
                    result << "\n";
                    for (size_t i = 0; i < table->columns.size(); ++i) {
                        result << std::string(16, '-');
                    }
                    result << "\n";

                    // Stampa righe
                    for (const auto& row : rows) {
                        for (size_t i = 0; i < table->columns.size(); ++i) {
                            if (i > 0) result << " | ";
                            result << std::setw(15) << row.data.at(table->columns[i]);
                        }
                        result << "\n";
                    }
                }

                result << "\nTotale: " << rows.size() << " riga/e.";
            }
            break;
        }

        case SQLCommand::UPDATE: {
            bool success = update(parsed.table_name, parsed.update_columns,
                                 parsed.update_values, parsed.where);
            if (success) {
                result << "Aggiornamento completato.";
            } else {
                result << "Errore nell'aggiornamento.";
            }
            break;
        }

        case SQLCommand::DELETE: {
            bool success = delete_from(parsed.table_name, parsed.where);
            if (success) {
                result << "Eliminazione completata.";
            } else {
                result << "Errore nell'eliminazione.";
            }
            break;
        }

        default:
            result << "Comando SQL non riconosciuto.";
            break;
    }

    return result.str();
}

bool Database::save() {
    std::string filename = get_filename();
    std::ofstream out(filename, std::ios::binary);

    if (!out.is_open()) {
        std::cerr << "Errore: Impossibile aprire il file per il salvataggio\n";
        return false;
    }

    // Scrivi numero di tabelle
    size_t num_tables = tables.size();
    out.write(reinterpret_cast<const char*>(&num_tables), sizeof(num_tables));

    // Scrivi ogni tabella
    for (const auto& [name, table] : tables) {
        table->serialize(out);
    }

    out.close();
    return true;
}

bool Database::load() {
    std::string filename = get_filename();
    std::ifstream in(filename, std::ios::binary);

    if (!in.is_open()) {
        std::cerr << "Errore: Impossibile aprire il file per il caricamento\n";
        return false;
    }

    // Leggi numero di tabelle
    size_t num_tables = 0;
    in.read(reinterpret_cast<char*>(&num_tables), sizeof(num_tables));

    // Leggi ogni tabella
    for (size_t i = 0; i < num_tables; ++i) {
        auto table = std::make_shared<Table>();
        table->deserialize(in);
        tables[table->name] = table;
    }

    in.close();
    return true;
}

void Database::print_schema() const {
    std::cout << "\n=== Database Schema: " << name << " ===\n";
    for (const auto& [name, table] : tables) {
        std::cout << "\nTabella: " << name << "\n";
        std::cout << "  Colonne: ";
        for (size_t i = 0; i < table->columns.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << table->columns[i];
        }
        std::cout << "\n";
        std::cout << "  Righe: " << table->rows.size() << "\n";
    }
    std::cout << "\n";
}
