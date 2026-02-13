#include "database.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Funzione hash semplice ma efficace
unsigned int hash_function(const char* key) {
    unsigned int hash = 5381;
    int c;
    while ((c = *key++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return hash % TABLE_SIZE;
}

// Crea una nuova tabella hash
HashTable* db_create() {
    HashTable* table = (HashTable*)malloc(sizeof(HashTable));
    if (table == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per la tabella\n");
        return NULL;
    }

    for (int i = 0; i < TABLE_SIZE; i++) {
        table->records[i] = NULL;
    }
    table->count = 0;

    return table;
}

// Distrugge la tabella e libera la memoria
void db_destroy(HashTable* table) {
    if (table == NULL) return;

    for (int i = 0; i < TABLE_SIZE; i++) {
        if (table->records[i] != NULL) {
            free(table->records[i]);
        }
    }
    free(table);
}

// Inserisci o aggiorna un record
int db_set(HashTable* table, const char* key, const char* value) {
    if (table == NULL || key == NULL || value == NULL) {
        fprintf(stderr, "Errore: Parametri non validi\n");
        return -1;
    }

    if (strlen(key) >= MAX_KEY_LENGTH) {
        fprintf(stderr, "Errore: Chiave troppo lunga (max %d caratteri)\n", MAX_KEY_LENGTH - 1);
        return -1;
    }

    if (strlen(value) >= MAX_VALUE_LENGTH) {
        fprintf(stderr, "Errore: Valore troppo lungo (max %d caratteri)\n", MAX_VALUE_LENGTH - 1);
        return -1;
    }

    unsigned int index = hash_function(key);

    // Cerca se la chiave esiste già
    Record* current = table->records[index];
    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            // Aggiorna il record esistente
            strncpy(current->value, value, MAX_VALUE_LENGTH - 1);
            current->value[MAX_VALUE_LENGTH - 1] = '\0';
            current->timestamp = time(NULL);
            return 0;
        }
        // Collision handling con linear probing
        index = (index + 1) % TABLE_SIZE;
        current = table->records[index];
    }

    // Crea un nuovo record
    Record* new_record = (Record*)malloc(sizeof(Record));
    if (new_record == NULL) {
        fprintf(stderr, "Errore: Impossibile allocare memoria per il record\n");
        return -1;
    }

    strncpy(new_record->key, key, MAX_KEY_LENGTH - 1);
    new_record->key[MAX_KEY_LENGTH - 1] = '\0';
    strncpy(new_record->value, value, MAX_VALUE_LENGTH - 1);
    new_record->value[MAX_VALUE_LENGTH - 1] = '\0';
    new_record->timestamp = time(NULL);

    table->records[index] = new_record;
    table->count++;

    return 0;
}

// Recupera un valore dato una chiave
char* db_get(HashTable* table, const char* key) {
    if (table == NULL || key == NULL) {
        fprintf(stderr, "Errore: Parametri non validi\n");
        return NULL;
    }

    unsigned int index = hash_function(key);
    unsigned int start_index = index;

    do {
        Record* record = table->records[index];
        if (record != NULL && strcmp(record->key, key) == 0) {
            return record->value;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    return NULL; // Chiave non trovata
}

// Cancella un record
int db_delete(HashTable* table, const char* key) {
    if (table == NULL || key == NULL) {
        fprintf(stderr, "Errore: Parametri non validi\n");
        return -1;
    }

    unsigned int index = hash_function(key);
    unsigned int start_index = index;

    do {
        Record* record = table->records[index];
        if (record != NULL && strcmp(record->key, key) == 0) {
            free(record);
            table->records[index] = NULL;
            table->count--;
            return 0;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    fprintf(stderr, "Errore: Chiave '%s' non trovata\n", key);
    return -1;
}

// Lista tutti i record
void db_list(HashTable* table) {
    if (table == NULL) return;

    if (table->count == 0) {
        printf("Database vuoto.\n");
        return;
    }

    printf("\n=== Database (%d record) ===\n", table->count);
    printf("%-20s %-30s %s\n", "Chiave", "Valore", "Timestamp");
    printf("%-20s %-30s %s\n", "-----", "-----", "---------");

    for (int i = 0; i < TABLE_SIZE; i++) {
        Record* record = table->records[i];
        if (record != NULL) {
            char time_str[64];
            struct tm* tm_info = localtime(&record->timestamp);
            strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", tm_info);

            printf("%-20s %-30s %s\n", record->key, record->value, time_str);
        }
    }
    printf("===========================\n\n");
}

// Salva il database su file
int db_save(HashTable* table, const char* filename) {
    if (table == NULL || filename == NULL) {
        fprintf(stderr, "Errore: Parametri non validi\n");
        return -1;
    }

    FILE* file = fopen(filename, "wb");
    if (file == NULL) {
        fprintf(stderr, "Errore: Impossibile aprire il file '%s' in scrittura\n", filename);
        return -1;
    }

    // Scrivi il numero di record
    if (fwrite(&table->count, sizeof(int), 1, file) != 1) {
        fprintf(stderr, "Errore: Scrittura fallita\n");
        fclose(file);
        return -1;
    }

    // Scrivi ogni record
    int written = 0;
    for (int i = 0; i < TABLE_SIZE; i++) {
        Record* record = table->records[i];
        if (record != NULL) {
            if (fwrite(record, sizeof(Record), 1, file) != 1) {
                fprintf(stderr, "Errore: Scrittura record fallita\n");
                fclose(file);
                return -1;
            }
            written++;
        }
    }

    fclose(file);
    printf("Database salvato con successo: %d record in '%s'\n", written, filename);
    return 0;
}

// Carica il database da file
int db_load(HashTable* table, const char* filename) {
    if (table == NULL || filename == NULL) {
        fprintf(stderr, "Errore: Parametri non validi\n");
        return -1;
    }

    FILE* file = fopen(filename, "rb");
    if (file == NULL) {
        fprintf(stderr, "Errore: Impossibile aprire il file '%s' in lettura\n", filename);
        return -1;
    }

    // Pulisci la tabella corrente
    for (int i = 0; i < TABLE_SIZE; i++) {
        if (table->records[i] != NULL) {
            free(table->records[i]);
            table->records[i] = NULL;
        }
    }
    table->count = 0;

    // Leggi il numero di record
    int num_records;
    if (fread(&num_records, sizeof(int), 1, file) != 1) {
        fprintf(stderr, "Errore: Lettura fallita\n");
        fclose(file);
        return -1;
    }

    // Leggi ogni record
    Record temp;
    for (int i = 0; i < num_records; i++) {
        if (fread(&temp, sizeof(Record), 1, file) != 1) {
            fprintf(stderr, "Errore: Lettura record fallita\n");
            fclose(file);
            return -1;
        }

        if (db_set(table, temp.key, temp.value) != 0) {
            fprintf(stderr, "Errore: Caricamento record fallito\n");
            fclose(file);
            return -1;
        }

        // Ripristina il timestamp originale
        unsigned int index = hash_function(temp.key);
        unsigned int start_index = index;
        do {
            Record* record = table->records[index];
            if (record != NULL && strcmp(record->key, temp.key) == 0) {
                record->timestamp = temp.timestamp;
                break;
            }
            index = (index + 1) % TABLE_SIZE;
        } while (index != start_index);
    }

    fclose(file);
    printf("Database caricato con successo: %d record da '%s'\n", num_records, filename);
    return 0;
}

// Stampa informazioni sul database
void db_print_info(HashTable* table) {
    if (table == NULL) {
        printf("Database non inizializzato\n");
        return;
    }

    printf("\n=== Info Database ===\n");
    printf("Record totali: %d\n", table->count);
    printf("Dimensione tabella: %d\n", TABLE_SIZE);
    printf("Carico: %.2f%%\n", (float)table->count / TABLE_SIZE * 100);
    printf("======================\n\n");
}
