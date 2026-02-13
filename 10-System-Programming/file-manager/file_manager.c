/*
 * =============================================
 * FILE MANAGER - Gestione File in C
 * =============================================
 * Progetto di System Programming
 * Creato per: Portfolio Project Ideas
 * Linguaggio: C
 * =============================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>

#define MAX_PATH 1024
#define MAX_FILENAME 256

/* Colori per il terminale */
#define COLOR_RESET   "\033[0m"
#define COLOR_RED     "\033[31m"
#define COLOR_GREEN   "\033[32m"
#define COLOR_YELLOW  "\033[33m"
#define COLOR_BLUE    "\033[34m"
#define COLOR_CYAN    "\033[36m"

/* =============================================
 * FUNZIONI DI UTILITY
 * ============================================= */

/**
 * Pulisce il buffer di input
 */
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

/**
 * Verifica se un path è una directory
 */
int is_directory(const char *path) {
    struct stat statbuf;
    if (stat(path, &statbuf) != 0)
        return 0;
    return S_ISDIR(statbuf.st_mode);
}

/**
 * Verifica se un file esiste
 */
int file_exists(const char *path) {
    struct stat statbuf;
    return (stat(path, &statbuf) == 0);
}

/* =============================================
 * FUNZIONI DI GESTIONE FILE
 * ============================================= */

/**
 * Lista i file nella directory corrente
 */
void list_files() {
    DIR *d;
    struct dirent *dir;
    struct stat statbuf;
    char path[MAX_PATH];
    int count = 0;

    printf("\n");
    printf(COLOR_CYAN "╔══════════════════════════════════════════════╗\n");
    printf("║          CONTENUTO DIRECTORY CORRENTE         ║\n");
    printf("╚══════════════════════════════════════════════╝\n" COLOR_RESET);

    d = opendir(".");
    if (d) {
        printf("\n%-30s %15s %15s\n", "NOME", "TIPO", "DIMENSIONE");
        printf("────────────────────────────────────────────────────────\n");

        while ((dir = readdir(d)) != NULL) {
            if (strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0)
                continue;

            snprintf(path, sizeof(path), "%s", dir->d_name);

            if (stat(path, &statbuf) == 0) {
                const char *type = S_ISDIR(statbuf.st_mode) ? "DIR" : "FILE";
                long size = statbuf.st_size;

                printf("%-30s %15s", dir->d_name, type);

                if (S_ISDIR(statbuf.st_mode)) {
                    printf("%15s\n", "-");
                } else {
                    if (size < 1024) {
                        printf("%12ld B\n", size);
                    } else if (size < 1024 * 1024) {
                        printf("%12.2f KB\n", size / 1024.0);
                    } else {
                        printf("%12.2f MB\n", size / (1024.0 * 1024.0));
                    }
                }
                count++;
            }
        }
        closedir(d);

        printf("────────────────────────────────────────────────────────\n");
        printf("Totale elementi: %d\n", count);
    } else {
        printf(COLOR_RED "Errore: Impossibile aprire la directory corrente\n" COLOR_RESET);
    }
}

/**
 * Copia un file
 */
int copy_file(const char *source, const char *destination) {
    FILE *src, *dest;
    char buffer[4096];
    size_t bytes_read;

    /* Verifica che il file sorgente esista */
    if (!file_exists(source)) {
        printf(COLOR_RED "Errore: Il file sorgente '%s' non esiste\n" COLOR_RESET, source);
        return 0;
    }

    /* Verifica che non sia una directory */
    if (is_directory(source)) {
        printf(COLOR_RED "Errore: '%s' è una directory, non un file\n" COLOR_RESET, source);
        return 0;
    }

    /* Apre i file */
    src = fopen(source, "rb");
    if (src == NULL) {
        printf(COLOR_RED "Errore: Impossibile aprire il file sorgente\n" COLOR_RESET);
        return 0;
    }

    dest = fopen(destination, "wb");
    if (dest == NULL) {
        printf(COLOR_RED "Errore: Impossibile creare il file destinazione\n" COLOR_RESET);
        fclose(src);
        return 0;
    }

    /* Copia il contenuto */
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        if (fwrite(buffer, 1, bytes_read, dest) != bytes_read) {
            printf(COLOR_RED "Errore durante la scrittura del file\n" COLOR_RESET);
            fclose(src);
            fclose(dest);
            return 0;
        }
    }

    fclose(src);
    fclose(dest);

    printf(COLOR_GREEN "✓ File copiato con successo: '%s' -> '%s'\n" COLOR_RESET, source, destination);
    return 1;
}

/**
 * Sposta o rinomina un file
 */
int move_file(const char *source, const char *destination) {
    /* Verifica che il file sorgente esista */
    if (!file_exists(source)) {
        printf(COLOR_RED "Errore: Il file sorgente '%s' non esiste\n" COLOR_RESET, source);
        return 0;
    }

    /* Tenta di rinominare/spostare il file */
    if (rename(source, destination) == 0) {
        printf(COLOR_GREEN "✓ File spostato/rinominato con successo: '%s' -> '%s'\n" COLOR_RESET,
               source, destination);
        return 1;
    } else {
        printf(COLOR_RED "Errore: Impossibile spostare/rinominare il file (%s)\n" COLOR_RESET,
               strerror(errno));
        return 0;
    }
}

/**
 * Elimina un file
 */
int delete_file(const char *filename) {
    /* Verifica che il file esista */
    if (!file_exists(filename)) {
        printf(COLOR_RED "Errore: Il file '%s' non esiste\n" COLOR_RESET, filename);
        return 0;
    }

    /* Verifica che non sia una directory */
    if (is_directory(filename)) {
        printf(COLOR_RED "Errore: '%s' è una directory (non supportato)\n" COLOR_RESET, filename);
        printf("Nota: L'eliminazione di directory non è supportata in questa versione\n");
        return 0;
    }

    /* Conferma eliminazione */
    printf(COLOR_YELLOW "Sei sicuro di voler eliminare '%s'? (s/n): " COLOR_RESET, filename);
    char confirm;
    scanf(" %c", &confirm);
    clear_input_buffer();

    if (confirm == 's' || confirm == 'S') {
        if (unlink(filename) == 0) {
            printf(COLOR_GREEN "✓ File eliminato con successo: '%s'\n" COLOR_RESET, filename);
            return 1;
        } else {
            printf(COLOR_RED "Errore: Impossibile eliminare il file (%s)\n" COLOR_RESET,
                   strerror(errno));
            return 0;
        }
    } else {
        printf(COLOR_YELLOW "Operazione annullata\n" COLOR_RESET);
        return 0;
    }
}

/* =============================================
 * INTERFACCIA UTENTE
 * ============================================= */

/**
 * Mostra il menu principale
 */
void display_menu() {
    printf("\n");
    printf(COLOR_CYAN "╔══════════════════════════════════════════════════════╗\n");
    printf("║           FILE MANAGER - Menu Principale           ║\n");
    printf("╠══════════════════════════════════════════════════════╣\n");
    printf("║  1. Lista file nella directory corrente              ║\n");
    printf("║  2. Copia file                                       ║\n");
    printf("║  3. Sposta/Rinomina file                             ║\n");
    printf("║  4. Elimina file                                     ║\n");
    printf("║  5. Visualizza informazioni file                     ║\n");
    printf("║  0. Esci                                             ║\n");
    printf("╚══════════════════════════════════════════════════════╝\n" COLOR_RESET);
    printf(COLOR_GREEN "Scelta: " COLOR_RESET);
}

/**
 * Visualizza informazioni dettagliate su un file
 */
void show_file_info(const char *filename) {
    struct stat statbuf;

    if (!file_exists(filename)) {
        printf(COLOR_RED "Errore: Il file '%s' non esiste\n" COLOR_RESET, filename);
        return;
    }

    if (stat(filename, &statbuf) == 0) {
        printf("\n");
        printf(COLOR_CYAN "╔══════════════════════════════════════════════╗\n");
        printf("║        INFORMAZIONI FILE                       ║\n");
        printf("╚══════════════════════════════════════════════╝\n" COLOR_RESET);

        printf("\nNome:              %s\n", filename);
        printf("Tipo:              %s\n",
               S_ISDIR(statbuf.st_mode) ? "Directory" : "File");

        if (!S_ISDIR(statbuf.st_mode)) {
            printf("Dimensione:        %ld bytes\n", statbuf.st_size);

            if (statbuf.st_size < 1024) {
                printf("                   (%.2f B)\n", (double)statbuf.st_size);
            } else if (statbuf.st_size < 1024 * 1024) {
                printf("                   (%.2f KB)\n", statbuf.st_size / 1024.0);
            } else {
                printf("                   (%.2f MB)\n", statbuf.st_size / (1024.0 * 1024.0));
            }
        }

        printf("Permessi:          ");
        printf((statbuf.st_mode & S_IRUSR) ? "r" : "-");
        printf((statbuf.st_mode & S_IWUSR) ? "w" : "-");
        printf((statbuf.st_mode & S_IXUSR) ? "x" : "-");
        printf((statbuf.st_mode & S_IRGRP) ? "r" : "-");
        printf((statbuf.st_mode & S_IWGRP) ? "w" : "-");
        printf((statbuf.st_mode & S_IXGRP) ? "x" : "-");
        printf((statbuf.st_mode & S_IROTH) ? "r" : "-");
        printf((statbuf.st_mode & S_IWOTH) ? "w" : "-");
        printf((statbuf.st_mode & S_IXOTH) ? "x" : "-");
        printf("\n");
    }
}

/**
 * Ottieni la directory corrente
 */
void show_current_directory() {
    char cwd[MAX_PATH];

    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("\n" COLOR_YELLOW "Directory corrente: " COLOR_CYAN "%s\n" COLOR_RESET, cwd);
    } else {
        printf(COLOR_RED "Impossibile ottenere la directory corrente\n" COLOR_RESET);
    }
}

/* =============================================
 * FUNZIONE PRINCIPALE
 * ============================================= */

int main() {
    int choice;
    char source[MAX_FILENAME], dest[MAX_FILENAME];

    printf(COLOR_CYAN "\n");
    printf("╔══════════════════════════════════════════════════════╗\n");
    printf("║                                                      ║\n");
    printf("║              FILE MANAGER v1.0                      ║\n");
    printf("║         Sistema di Gestione File in C               ║\n");
    printf("║                                                      ║\n");
    printf("╚══════════════════════════════════════════════════════╝\n" COLOR_RESET);

    while (1) {
        show_current_directory();
        display_menu();

        if (scanf("%d", &choice) != 1) {
            printf(COLOR_RED "Input non valido. Inserisci un numero.\n" COLOR_RESET);
            clear_input_buffer();
            continue;
        }
        clear_input_buffer();

        switch (choice) {
            case 1:
                list_files();
                break;

            case 2:
                printf("\n--- COPIA FILE ---\n");
                printf("Nome file sorgente: ");
                fgets(source, sizeof(source), stdin);
                source[strcspn(source, "\n")] = 0;

                printf("Nome file destinazione: ");
                fgets(dest, sizeof(dest), stdin);
                dest[strcspn(dest, "\n")] = 0;

                copy_file(source, dest);
                break;

            case 3:
                printf("\n--- SPOSTA/RINOMINA FILE ---\n");
                printf("Nome file sorgente: ");
                fgets(source, sizeof(source), stdin);
                source[strcspn(source, "\n")] = 0;

                printf("Nuovo nome/destinazione: ");
                fgets(dest, sizeof(dest), stdin);
                dest[strcspn(dest, "\n")] = 0;

                move_file(source, dest);
                break;

            case 4:
                printf("\n--- ELIMINA FILE ---\n");
                printf("Nome file da eliminare: ");
                fgets(source, sizeof(source), stdin);
                source[strcspn(source, "\n")] = 0;

                delete_file(source);
                break;

            case 5:
                printf("\n--- INFORMAZIONI FILE ---\n");
                printf("Nome file: ");
                fgets(source, sizeof(source), stdin);
                source[strcspn(source, "\n")] = 0;

                show_file_info(source);
                break;

            case 0:
                printf("\n" COLOR_GREEN "Grazie per aver usato File Manager!\n" COLOR_RESET);
                printf(COLOR_CYAN "Alla prossima! 👋\n\n" COLOR_RESET);
                return 0;

            default:
                printf(COLOR_RED "Scelta non valida. Riprova.\n" COLOR_RESET);
        }

        printf("\nPremi Enter per continuare...");
        getchar();
    }

    return 0;
}
