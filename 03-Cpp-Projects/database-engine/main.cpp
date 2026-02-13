#include "database.h"
#include <iostream>
#include <string>
#include <sstream>

void print_menu() {
    std::cout << "\n===========================================\n";
    std::cout << "        DATABASE ENGINE - Menu Principale\n";
    std::cout << "===========================================\n";
    std::cout << "1. Esegui comando SQL\n";
    std::cout << "2. Esegui test automatici\n";
    std::cout << "3. Salva database su file\n";
    std::cout << "4. Carica database da file\n";
    std::cout << "5. Visualizza schema\n";
    std::cout << "6. Visualizza B-tree\n";
    std::cout << "0. Esci\n";
    std::cout << "===========================================\n";
    std::cout << "Scelta: ";
}

void run_tests(Database& db) {
    std::cout << "\n=== ESECUZIONE TEST AUTOMATICI ===\n\n";

    // Test 1: CREATE TABLE
    std::cout << "Test 1: CREATE TABLE\n";
    std::string result = db.execute("CREATE TABLE users (id, nome, eta)");
    std::cout << db.execute("CREATE TABLE users (id, nome, eta)") << "\n";

    // Test 2: INSERT
    std::cout << "\nTest 2: INSERT\n";
    db.execute("INSERT INTO users (1, Mario, 25)");
    std::cout << db.execute("INSERT INTO users (1, Mario, 25)") << "\n";
    db.execute("INSERT INTO users (2, Luigi, 30)");
    std::cout << db.execute("INSERT INTO users (2, Luigi, 30)") << "\n";
    db.execute("INSERT INTO users (3, Anna, 28)");
    std::cout << db.execute("INSERT INTO users (3, Anna, 28)") << "\n";
    db.execute("INSERT INTO users (4, Paolo, 35)");
    std::cout << db.execute("INSERT INTO users (4, Paolo, 35)") << "\n";
    db.execute("INSERT INTO users (5, Laura, 22)");
    std::cout << db.execute("INSERT INTO users (5, Laura, 22)") << "\n";

    // Test 3: SELECT *
    std::cout << "\nTest 3: SELECT * FROM users\n";
    std::cout << db.execute("SELECT * FROM users") << "\n";

    // Test 4: SELECT con WHERE
    std::cout << "\nTest 4: SELECT con WHERE\n";
    std::cout << db.execute("SELECT * FROM users WHERE eta == 30") << "\n";

    // Test 5: UPDATE
    std::cout << "\nTest 5: UPDATE\n";
    std::cout << db.execute("UPDATE users SET eta = 26 WHERE id == 1") << "\n";

    // Verifica UPDATE
    std::cout << "\nVerifica UPDATE:\n";
    std::cout << db.execute("SELECT * FROM users WHERE id == 1") << "\n";

    // Test 6: DELETE
    std::cout << "\nTest 6: DELETE\n";
    std::cout << db.execute("DELETE FROM users WHERE id == 3") << "\n";

    // Verifica DELETE
    std::cout << "\nVerifica DELETE:\n";
    std::cout << db.execute("SELECT * FROM users") << "\n";

    // Test 7: B-tree structure
    std::cout << "\nTest 7: Struttura B-tree\n";
    auto table = db.get_table("users");
    if (table) {
        table->index.print();
    }

    // Test 8: Salvataggio
    std::cout << "\nTest 8: Salvataggio su file\n";
    if (db.save()) {
        std::cout << "Database salvato con successo!\n";
    } else {
        std::cout << "Errore nel salvataggio del database.\n";
    }

    std::cout << "\n=== TEST COMPLETATI ===\n";
}

void interactive_mode(Database& db) {
    while (true) {
        print_menu();

        std::string choice_str;
        std::getline(std::cin, choice_str);

        int choice = 0;
        try {
            choice = std::stoi(choice_str);
        } catch (...) {
            std::cout << "Scelta non valida. Riprova.\n";
            continue;
        }

        switch (choice) {
            case 1: {
                std::cout << "\nInserisci comando SQL (o 'back' per tornare al menu):\n";
                std::string sql;
                std::cout << "SQL> ";
                std::getline(std::cin, sql);

                if (sql == "back") {
                    continue;
                }

                std::cout << "\n" << db.execute(sql) << "\n";
                break;
            }

            case 2:
                run_tests(db);
                break;

            case 3:
                if (db.save()) {
                    std::cout << "\nDatabase salvato con successo!\n";
                } else {
                    std::cout << "\nErrore nel salvataggio del database.\n";
                }
                break;

            case 4:
                if (db.load()) {
                    std::cout << "\nDatabase caricato con successo!\n";
                    db.print_schema();
                } else {
                    std::cout << "\nErrore nel caricamento del database.\n";
                }
                break;

            case 5:
                db.print_schema();
                break;

            case 6: {
                std::cout << "\nNome della tabella: ";
                std::string table_name;
                std::getline(std::cin, table_name);

                auto table = db.get_table(table_name);
                if (table) {
                    std::cout << "\nStruttura B-tree della tabella '" << table_name << "':\n";
                    table->index.print();
                } else {
                    std::cout << "\nTabella non trovata.\n";
                }
                break;
            }

            case 0:
                std::cout << "\nArrivederci!\n";
                return;

            default:
                std::cout << "\nScelta non valida. Riprova.\n";
                break;
        }
    }
}

int main() {
    std::cout << "===========================================\n";
    std::cout << "       C++ DATABASE ENGINE v1.0\n";
    std::cout << "===========================================\n";
    std::cout << "\nQuesto database engine implementa:\n";
    std::cout << "- B-tree per indicizzazione (ordine 4)\n";
    std::cout << "- SQL parser semplice\n";
    std::cout << "- Persistence su file binario\n";
    std::cout << "\nSQL Supportato:\n";
    std::cout << "  CREATE TABLE name (col1, col2, ...)\n";
    std::cout << "  INSERT INTO name (val1, val2, ...)\n";
    std::cout << "  SELECT * FROM name [WHERE col == value]\n";
    std::cout << "  UPDATE name SET col = value WHERE id == 1\n";
    std::cout << "  DELETE FROM name WHERE id == 1\n";
    std::cout << "\nNota: La prima colonna deve essere un intero usato come chiave.\n";

    // Crea il database
    Database db("test_db");

    // Modalità interattiva
    interactive_mode(db);

    return 0;
}
