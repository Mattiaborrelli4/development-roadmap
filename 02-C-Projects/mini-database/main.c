#include "database.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_COMMAND_LENGTH 512
#define PROMPT "db> "

// Stampa il messaggio di aiuto
void print_help() {
    printf("\n=== Mini Database Engine - Comandi ===\n");
    printf("  SET <chiave> <valore>    - Salva o aggiorna un valore\n");
    printf("  GET <chiave>              - Recupera un valore\n");
    printf("  DELETE <chiave>           - Rimuove una chiave\n");
    printf("  LIST                      - Mostra tutti i record\n");
    printf("  SAVE [filename]           - Salva su file (default: database.db)\n");
    printf("  LOAD [filename]           - Carica da file (default: database.db)\n");
    printf("  INFO                      - Mostra informazioni sul database\n");
    printf("  HELP                      - Mostra questo messaggio\n");
    printf("  CLEAR                     - Pulisce lo schermo\n");
    printf("  EXIT / QUIT               - Esce dal programma\n");
    printf("====================================\n\n");
}

// Trim degli spazi
void trim(char* str) {
    char* start = str;
    char* end;

    while (isspace((unsigned char)*start)) {
        start++;
    }

    if (*start == 0) {
        *str = 0;
        return;
    }

    end = start + strlen(start) - 1;
    while (end > start && isspace((unsigned char)*end)) {
        end--;
    }

    end[1] = '\0';
    memmove(str, start, end - start + 2);
}

// Parser e esecuzione dei comandi
int execute_command(HashTable* db, const char* command) {
    char cmd[MAX_COMMAND_LENGTH];
    char arg1[MAX_COMMAND_LENGTH];
    char rest[MAX_COMMAND_LENGTH];

    (void)arg1; // Mark as intentionally unused when needed
    int num_args = sscanf(command, "%s %s %[^\n]", cmd, arg1, rest);

    // Converti il comando in maiuscolo
    for (char* p = cmd; *p; p++) {
        *p = toupper((unsigned char)*p);
    }

    // Comando SET
    if (strcmp(cmd, "SET") == 0) {
        if (num_args < 3) {
            printf("Uso: SET <chiave> <valore>\n");
            return 0;
        }
        if (db_set(db, arg1, rest) == 0) {
            printf("OK: Chiave '%s' impostata\n", arg1);
        }
        return 0;
    }

    // Comando GET
    if (strcmp(cmd, "GET") == 0) {
        if (num_args < 2) {
            printf("Uso: GET <chiave>\n");
            return 0;
        }
        char* value = db_get(db, arg1);
        if (value != NULL) {
            printf("Valore: %s\n", value);
        } else {
            printf("Chiave '%s' non trovata\n", arg1);
        }
        return 0;
    }

    // Comando DELETE
    if (strcmp(cmd, "DELETE") == 0) {
        if (num_args < 2) {
            printf("Uso: DELETE <chiave>\n");
            return 0;
        }
        if (db_delete(db, arg1) == 0) {
            printf("OK: Chiave '%s' eliminata\n", arg1);
        }
        return 0;
    }

    // Comando LIST
    if (strcmp(cmd, "LIST") == 0) {
        db_list(db);
        return 0;
    }

    // Comando SAVE
    if (strcmp(cmd, "SAVE") == 0) {
        char* filename = (num_args >= 2) ? arg1 : (char*)DEFAULT_FILENAME;
        db_save(db, filename);
        return 0;
    }

    // Comando LOAD
    if (strcmp(cmd, "LOAD") == 0) {
        char* filename = (num_args >= 2) ? arg1 : (char*)DEFAULT_FILENAME;
        db_load(db, filename);
        return 0;
    }

    // Comando INFO
    if (strcmp(cmd, "INFO") == 0) {
        db_print_info(db);
        return 0;
    }

    // Comando HELP
    if (strcmp(cmd, "HELP") == 0 || strcmp(cmd, "?") == 0) {
        print_help();
        return 0;
    }

    // Comando CLEAR
    if (strcmp(cmd, "CLEAR") == 0 || strcmp(cmd, "CLS") == 0) {
        system("cls || clear");
        return 0;
    }

    // Comando sconosciuto
    printf("Comando sconosciuto: %s\n", cmd);
    printf("Digita 'HELP' per la lista dei comandi\n");

    return 0;
}

int main(int argc, char* argv[]) {
    printf("╔════════════════════════════════════════╗\n");
    printf("║     Mini Database Engine v1.0          ║\n");
    printf("║     Database Key-Value in C            ║\n");
    printf("╚════════════════════════════════════════╝\n\n");

    // Crea il database
    HashTable* db = db_create();
    if (db == NULL) {
        fprintf(stderr, "Errore fatale: Impossibile creare il database\n");
        return 1;
    }

    // Carica automaticamente il database se esiste
    if (argc > 1) {
        printf("Caricamento database da: %s\n", argv[1]);
        db_load(db, argv[1]);
    } else {
        // Tenta di caricare il file di default
        FILE* test = fopen(DEFAULT_FILENAME, "rb");
        if (test != NULL) {
            fclose(test);
            printf("Caricamento database da: %s\n", DEFAULT_FILENAME);
            db_load(db, DEFAULT_FILENAME);
        }
    }

    print_help();

    // Loop principale
    char command[MAX_COMMAND_LENGTH];
    while (1) {
        printf("%s", PROMPT);
        fflush(stdout);

        if (fgets(command, sizeof(command), stdin) == NULL) {
            break;
        }

        // Rimuovi il newline
        command[strcspn(command, "\n")] = 0;
        command[strcspn(command, "\r")] = 0;

        // Trim
        trim(command);

        // Salta linee vuote
        if (strlen(command) == 0) {
            continue;
        }

        // Converti in maiuscolo per il controllo
        char cmd_upper[MAX_COMMAND_LENGTH];
        strcpy(cmd_upper, command);
        for (char* p = cmd_upper; *p; p++) {
            *p = toupper((unsigned char)*p);
        }

        // Comandi di uscita
        if (strcmp(cmd_upper, "EXIT") == 0 || strcmp(cmd_upper, "QUIT") == 0) {
            break;
        }

        // Esegui il comando
        execute_command(db, command);
    }

    // Salva automaticamente prima di uscire
    printf("\nSalvataggio automatico in corso...\n");
    db_save(db, DEFAULT_FILENAME);

    // Pulisci
    db_destroy(db);
    printf("Arrivederci!\n");

    return 0;
}
