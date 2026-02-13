/**
 * Mini Shell - Header File
 * Un semplice interprete di comandi Unix-like
 */

#ifndef SHELL_H
#define SHELL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Definizioni per la compatibilità Windows */
#ifdef _WIN32
    #include <windows.h>
    #include <direct.h>
    #include <io.h>
    #include <process.h>
    #define chdir _chdir
    #define getcwd _getcwd
    #define popen _popen
    #define pclose _pclose
    #ifndef PATH_MAX
        #define PATH_MAX MAX_PATH
    #endif
    #ifndef strdup
        #define strdup _strdup
    #endif
#else
    #include <unistd.h>
    #include <sys/wait.h>
    #include <sys/types.h>
    #include <pwd.h>
    #include <limits.h>
    #include <signal.h>
    #include <fcntl.h>
#endif

/* Costanti */
#define MAX_INPUT_LEN 1024
#define MAX_ARGS 64
#define MAX_HISTORY 100
#define PROMPT "mini-shell> "

/* Struttura per la history */
typedef struct {
    char *commands[MAX_HISTORY];
    int count;
    int current;
} History;

/* Funzioni di utilità */
void initialize_shell(void);
void cleanup_shell(void);
void print_prompt(void);
char* read_input(void);
char** parse_input(char *input, int *argc);

/* Gestione history */
void init_history(History *hist);
void add_to_history(History *hist, const char *command);
char* get_history_command(History *hist, int offset);
void free_history(History *hist);
void save_history_to_file(History *hist);
void load_history_from_file(History *hist);

/* Built-in commands */
int is_builtin(char *cmd);
int execute_builtin(char **args);

int builtin_cd(char **args);
int builtin_pwd(char **args);
int builtin_ls(char **args);
int builtin_echo(char **args);
int builtin_exit(char **args);
int builtin_clear(char **args);
int builtin_history(char **args);
int builtin_help(char **args);

/* Esecuzione comandi esterni */
int execute_external(char **args);

/* Variabili globali (definite in shell.c) */
extern int g_running;
extern int g_last_exit_status;

/* Gestione segnali */
void setup_signal_handlers(void);
void handle_sigint(int sig);
void handle_sigchld(int sig);

/* Funzioni di supporto */
void strip_whitespace(char *str);
int count_args(char **args);

#endif /* SHELL_H */
