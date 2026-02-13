#ifndef DATABASE_H
#define DATABASE_H

#include <time.h>

#define MAX_KEY_LENGTH 64
#define MAX_VALUE_LENGTH 256
#define TABLE_SIZE 1024
#define DEFAULT_FILENAME "database.db"

// Struttura per un record
typedef struct {
    char key[MAX_KEY_LENGTH];
    char value[MAX_VALUE_LENGTH];
    time_t timestamp;
} Record;

// Struttura per la tabella hash
typedef struct {
    Record* records[TABLE_SIZE];
    int count;
} HashTable;

// Funzioni principali
HashTable* db_create();
void db_destroy(HashTable* table);

// Operazioni CRUD
int db_set(HashTable* table, const char* key, const char* value);
char* db_get(HashTable* table, const char* key);
int db_delete(HashTable* table, const char* key);
void db_list(HashTable* table);

// Persistenza su file
int db_save(HashTable* table, const char* filename);
int db_load(HashTable* table, const char* filename);

// Funzioni di utilità
unsigned int hash_function(const char* key);
void db_print_info(HashTable* table);

#endif // DATABASE_H
