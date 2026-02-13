/**
 * Mini Shell - Implementazione Principale
 * Un semplice interprete di comandi Unix-like con history e gestione segnali
 */

#include "shell.h"
#include <errno.h>

#ifndef _WIN32
#include <termios.h>
#endif

/* Variabili globali */
History g_history;
int g_running = 1;
int g_last_exit_status = 0;

/* Struttura termios per salvare/ripristinare le impostazioni del terminale */
#ifdef __linux__
static struct termios orig_termios;
#endif

/**
 * Inizializza la shell
 */
void initialize_shell(void) {
    /* Inizializza la history */
    init_history(&g_history);

    /* Carica history dal file */
    load_history_from_file(&g_history);

    /* Configura i gestori di segnale */
    #ifndef _WIN32
        setup_signal_handlers();
    #endif

    /* Pulisci lo schermo all'avvio */
    builtin_clear(NULL);

    printf("=================================\n");
    printf("  Mini Shell v1.0\n");
    printf("  Digita 'help' per i comandi\n");
    printf("=================================\n\n");
}

/**
 * Pulisce le risorse della shell
 */
void cleanup_shell(void) {
    /* Salva la history su file */
    save_history_to_file(&g_history);

    /* Libera la memoria della history */
    free_history(&g_history);

    printf("\nGrazie per aver usato Mini Shell!\n");
}

/**
 * Stampa il prompt della shell
 */
void print_prompt(void) {
    char cwd[PATH_MAX];

    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        #ifdef _WIN32
            printf("mini-shell:%s$ ", cwd);
        #else
            printf("\033[1;32mmini-shell\033[0m:\033[1;34m%s\033[0m$ ", cwd);
        #endif
    } else {
        printf(PROMPT);
    }

    fflush(stdout);
}

/**
 * Legge l'input dall'utente
 */
char* read_input(void) {
    char *input = malloc(MAX_INPUT_LEN);

    if (input == NULL) {
        perror("malloc");
        return NULL;
    }

    if (fgets(input, MAX_INPUT_LEN, stdin) == NULL) {
        /* EOF o errore */
        free(input);
        return NULL;
    }

    /* Rimuovi il newline finale */
    size_t len = strlen(input);
    if (len > 0 && input[len - 1] == '\n') {
        input[len - 1] = '\0';
    }

    return input;
}

/**
 * Tokenizza l'input in argomenti
 */
char** parse_input(char *input, int *argc) {
    char **args = malloc(MAX_ARGS * sizeof(char*));
    char *token;
    int i = 0;

    if (args == NULL) {
        perror("malloc");
        return NULL;
    }

    token = strtok(input, " \t\n");
    while (token != NULL && i < MAX_ARGS - 1) {
        args[i++] = token;
        token = strtok(NULL, " \t\n");
    }

    args[i] = NULL;
    *argc = i;

    return args;
}

/**
 * Inizializza la history
 */
void init_history(History *hist) {
    hist->count = 0;
    hist->current = -1;

    for (int i = 0; i < MAX_HISTORY; i++) {
        hist->commands[i] = NULL;
    }
}

/**
 * Aggiunge un comando alla history
 */
void add_to_history(History *hist, const char *command) {
    if (command == NULL || strlen(command) == 0) {
        return;
    }

    /* Libera il comando più vecchio se la history è piena */
    if (hist->count >= MAX_HISTORY) {
        free(hist->commands[0]);

        /* Sposta tutti i comandi */
        for (int i = 1; i < MAX_HISTORY; i++) {
            hist->commands[i - 1] = hist->commands[i];
        }

        hist->count = MAX_HISTORY - 1;
    }

    /* Aggiungi il nuovo comando */
    hist->commands[hist->count] = strdup(command);
    hist->count++;
    hist->current = hist->count;
}

/**
 * Ottiene un comando dalla history
 */
char* get_history_command(History *hist, int offset) {
    int index = hist->current + offset;

    if (index < 0 || index >= hist->count) {
        return NULL;
    }

    return hist->commands[index];
}

/**
 * Libera la memoria della history
 */
void free_history(History *hist) {
    for (int i = 0; i < hist->count; i++) {
        if (hist->commands[i] != NULL) {
            free(hist->commands[i]);
        }
    }
}

/**
 * Salva la history su file
 */
void save_history_to_file(History *hist) {
    FILE *file = fopen(".mini_shell_history", "w");

    if (file == NULL) {
        return;
    }

    for (int i = 0; i < hist->count; i++) {
        if (hist->commands[i] != NULL) {
            fprintf(file, "%s\n", hist->commands[i]);
        }
    }

    fclose(file);
}

/**
 * Carica la history da file
 */
void load_history_from_file(History *hist) {
    FILE *file = fopen(".mini_shell_history", "r");
    char line[MAX_INPUT_LEN];

    if (file == NULL) {
        return;
    }

    while (fgets(line, sizeof(line), file) != NULL && hist->count < MAX_HISTORY) {
        /* Rimuovi il newline */
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
        }

        if (strlen(line) > 0) {
            hist->commands[hist->count] = strdup(line);
            hist->count++;
        }
    }

    hist->current = hist->count;
    fclose(file);
}

/**
 * Verifica se un comando è built-in
 */
int is_builtin(char *cmd) {
    if (cmd == NULL) return 0;

    return (strcmp(cmd, "cd") == 0 ||
            strcmp(cmd, "pwd") == 0 ||
            strcmp(cmd, "ls") == 0 ||
            strcmp(cmd, "echo") == 0 ||
            strcmp(cmd, "exit") == 0 ||
            strcmp(cmd, "clear") == 0 ||
            strcmp(cmd, "history") == 0 ||
            strcmp(cmd, "help") == 0);
}

/**
 * Esegue un comando built-in
 */
int execute_builtin(char **args) {
    if (args[0] == NULL) {
        return 0;
    }

    if (strcmp(args[0], "cd") == 0) {
        return builtin_cd(args);
    } else if (strcmp(args[0], "pwd") == 0) {
        return builtin_pwd(args);
    } else if (strcmp(args[0], "ls") == 0) {
        return builtin_ls(args);
    } else if (strcmp(args[0], "echo") == 0) {
        return builtin_echo(args);
    } else if (strcmp(args[0], "exit") == 0) {
        return builtin_exit(args);
    } else if (strcmp(args[0], "clear") == 0) {
        return builtin_clear(args);
    } else if (strcmp(args[0], "history") == 0) {
        return builtin_history(args);
    } else if (strcmp(args[0], "help") == 0) {
        return builtin_help(args);
    }

    return -1;
}

/**
 * Built-in: cd - Cambia directory
 */
int builtin_cd(char **args) {
    const char *path;

    if (args[1] == NULL) {
        /* Vai alla home directory */
        #ifdef _WIN32
            path = getenv("USERPROFILE");
        #else
            struct passwd *pw = getpwuid(getuid());
            path = pw->pw_dir;
        #endif
    } else {
        path = args[1];
    }

    if (chdir(path) != 0) {
        perror("cd");
        return 1;
    }

    return 0;
}

/**
 * Built-in: pwd - Stampa la directory corrente
 */
int builtin_pwd(char **args) {
    (void)args;  /* Suppress unused parameter warning */
    char cwd[PATH_MAX];

    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("%s\n", cwd);
        return 0;
    } else {
        perror("pwd");
        return 1;
    }
}

/**
 * Built-in: ls - Lista i file (versione semplificata)
 */
int builtin_ls(char **args) {
    const char *path = args[1] ? args[1] : ".";

    #ifdef _WIN32
        char command[MAX_INPUT_LEN];
        snprintf(command, sizeof(command), "dir /B \"%s\"", path);
        return system(command);
    #else
        char command[MAX_INPUT_LEN];
        snprintf(command, sizeof(command), "ls -F --color=auto %s", path);
        return system(command);
    #endif
}

/**
 * Built-in: echo - Stampa argomenti
 */
int builtin_echo(char **args) {
    for (int i = 1; args[i] != NULL; i++) {
        printf("%s", args[i]);
        if (args[i + 1] != NULL) {
            printf(" ");
        }
    }
    printf("\n");
    return 0;
}

/**
 * Built-in: exit - Esci dalla shell
 */
int builtin_exit(char **args) {
    int status = g_last_exit_status;

    if (args[1] != NULL) {
        status = atoi(args[1]);
    }

    g_running = 0;
    return status;
}

/**
 * Built-in: clear - Pulisci lo schermo
 */
int builtin_clear(char **args) {
    (void)args;  /* Suppress unused parameter warning */
    #ifdef _WIN32
        system("cls");
    #else
        printf("\033[2J\033[H");
    #endif
    fflush(stdout);
    return 0;
}

/**
 * Built-in: history - Mostra la history
 */
int builtin_history(char **args) {
    (void)args;  /* Suppress unused parameter warning */
    for (int i = 0; i < g_history.count; i++) {
        if (g_history.commands[i] != NULL) {
            printf("%4d  %s\n", i + 1, g_history.commands[i]);
        }
    }
    return 0;
}

/**
 * Built-in: help - Mostra l'aiuto
 */
int builtin_help(char **args) {
    (void)args;  /* Suppress unused parameter warning */
    printf("Mini Shell - Comandi disponibili:\n\n");
    printf("Comandi Built-in:\n");
    printf("  cd [dir]      Cambia la directory corrente\n");
    printf("  pwd           Mostra la directory corrente\n");
    printf("  ls [dir]      Lista i file nella directory\n");
    printf("  echo [args]   Stampa gli argomenti\n");
    printf("  clear         Pulisce lo schermo\n");
    printf("  history       Mostra la cronologia comandi\n");
    printf("  help          Mostra questo messaggio\n");
    printf("  exit [n]      Esce dalla shell\n\n");
    printf("Comandi Esterni:\n");
    printf("  Qualsiasi comando disponibile nel sistema\n");
    printf("  (es. gcc, python, vim, etc.)\n\n");
    #ifndef _WIN32
    printf("Ctrl+C non terminerà la shell\n");
    #endif

    return 0;
}

/**
 * Esegue un comando esterno usando fork/exec
 */
int execute_external(char **args) {
    #ifdef _WIN32
        /* Windows: usa _spawnvp */
        int result = _spawnvp(_P_WAIT, args[0], (const char *const *)args);
        if (result == -1) {
            fprintf(stderr, "mini-shell: comando non trovato: %s\n", args[0]);
            return 1;
        }
        return result;
    #else
        /* Unix/POSIX: usa fork/exec */
        pid_t pid = fork();

        if (pid == 0) {
            /* Processo figlio */
            execvp(args[0], args);

            /* Se execvp ritorna, c'è stato un errore */
            fprintf(stderr, "mini-shell: comando non trovato: %s\n", args[0]);
            exit(1);
        } else if (pid < 0) {
            /* Errore nella fork */
            perror("fork");
            return 1;
        } else {
            /* Processo padre */
            int status;
            waitpid(pid, &status, 0);

            if (WIFEXITED(status)) {
                return WEXITSTATUS(status);
            } else {
                return 1;
            }
        }
    #endif
}

/**
 * Configura i gestori di segnale
 */
void setup_signal_handlers(void) {
    #ifndef _WIN32
        struct sigaction sa_int, sa_chld;

        /* Gestore per SIGINT (Ctrl+C) */
        sa_int.sa_handler = handle_sigint;
        sigemptyset(&sa_int.sa_mask);
        sa_int.sa_flags = SA_RESTART;
        sigaction(SIGINT, &sa_int, NULL);

        /* Gestore per SIGCHLD (figlio terminato) */
        sa_chld.sa_handler = handle_sigchld;
        sigemptyset(&sa_chld.sa_mask);
        sa_chld.sa_flags = SA_RESTART | SA_NOCLDSTOP;
        sigaction(SIGCHLD, &sa_chld, NULL);
    #endif
}

/**
 * Gestore per SIGINT - Non fa nulla (prevede la chiusura della shell)
 */
void handle_sigint(int sig) {
    (void)sig;  /* Suppress unused parameter warning */
    printf("\nUsa 'exit' per uscire dalla shell.\n");
    print_prompt();
    fflush(stdout);
}

/**
 * Gestore per SIGCHLD - Pulisce i processi figli zombie
 */
void handle_sigchld(int sig) {
    (void)sig;  /* Suppress unused parameter warning */
    #ifndef _WIN32
        while (waitpid(-1, NULL, WNOHANG) > 0);
    #endif
}

/**
 * Rimuove gli spazi bianchi da una stringa
 */
void strip_whitespace(char *str) {
    if (str == NULL) return;

    char *start = str;
    char *end = str + strlen(str) - 1;

    /* Rimuovi spazi iniziali */
    while (*start && (*start == ' ' || *start == '\t')) {
        start++;
    }

    /* Rimuovi spazi finali */
    while (end > start && (*end == ' ' || *end == '\t' || *end == '\n')) {
        end--;
    }

    /* Sposta la stringa */
    memmove(str, start, end - start + 1);
    str[end - start + 1] = '\0';
}

/**
 * Conta gli argomenti
 */
int count_args(char **args) {
    int count = 0;
    while (args != NULL && args[count] != NULL) {
        count++;
    }
    return count;
}

/**
 * Funzione principale - Loop della shell
 */
int main(int argc, char **argv) {
    char *input;
    char **parsed_args;
    int arg_count;

    (void)argc;  /* Suppress unused parameter warning */
    (void)argv;  /* Suppress unused parameter warning */

    /* Inizializza la shell */
    initialize_shell();

    /* Loop principale */
    while (g_running) {
        /* Mostra il prompt */
        print_prompt();

        /* Leggi l'input */
        input = read_input();

        if (input == NULL) {
            /* EOF o errore */
            printf("\n");
            break;
        }

        /* Salta linee vuote */
        if (strlen(input) == 0) {
            free(input);
            continue;
        }

        /* Aggiungi alla history */
        add_to_history(&g_history, input);

        /* Parso l'input */
        parsed_args = parse_input(input, &arg_count);

        if (parsed_args == NULL) {
            free(input);
            continue;
        }

        /* Esegui il comando */
        if (parsed_args[0] != NULL) {
            int result;

            if (is_builtin(parsed_args[0])) {
                result = execute_builtin(parsed_args);
            } else {
                result = execute_external(parsed_args);
            }

            g_last_exit_status = result;
        }

        /* Pulisci */
        free(input);
        free(parsed_args);
    }

    /* Pulisci e esci */
    cleanup_shell();

    return g_last_exit_status;
}
