/**
 * Test Suite per Mini Shell
 * Programma di test per verificare le funzionalità della shell
 */

#include "shell.h"
#include <assert.h>

/* Contatore test */
int tests_passed = 0;
int tests_failed = 0;

/* Macro per test */
#define TEST(name) printf("\n🧪 Test: %s\n", name);
#define ASSERT(condition) \
    do { \
        if (condition) { \
            printf("  ✅ PASS: %s\n", #condition); \
            tests_passed++; \
        } else { \
            printf("  ❌ FAIL: %s\n", #condition); \
            tests_failed++; \
        } \
    } while(0)

/**
 * Test: Parsing input
 */
void test_parse_input(void) {
    TEST("Parsing input");

    char input[] = "ls -la /home";
    int argc;
    char **args = parse_input(input, &argc);

    ASSERT(argc == 3);
    ASSERT(strcmp(args[0], "ls") == 0);
    ASSERT(strcmp(args[1], "-la") == 0);
    ASSERT(strcmp(args[2], "/home") == 0);
    ASSERT(args[3] == NULL);

    free(args);
}

/**
 * Test: Comando vuoto
 */
void test_empty_input(void) {
    TEST("Input vuoto");

    char input[] = "";
    int argc;
    char **args = parse_input(input, &argc);

    ASSERT(argc == 0);
    ASSERT(args[0] == NULL);

    free(args);
}

/**
 * Test: Spazi multipli
 */
void test_multiple_spaces(void) {
    TEST("Spazi multipli");

    char input[] = "echo    hello    world";
    int argc;
    char **args = parse_input(input, &argc);

    ASSERT(argc == 3);
    ASSERT(strcmp(args[0], "echo") == 0);
    ASSERT(strcmp(args[1], "hello") == 0);
    ASSERT(strcmp(args[2], "world") == 0);

    free(args);
}

/**
 * Test: Verifica built-in
 */
void test_is_builtin(void) {
    TEST("Verifica built-in");

    ASSERT(is_builtin("cd") == 1);
    ASSERT(is_builtin("pwd") == 1);
    ASSERT(is_builtin("ls") == 1);
    ASSERT(is_builtin("echo") == 1);
    ASSERT(is_builtin("exit") == 1);
    ASSERT(is_builtin("clear") == 1);
    ASSERT(is_builtin("history") == 1);
    ASSERT(is_builtin("help") == 1);
    ASSERT(is_builtin("gcc") == 0);
    ASSERT(is_builtin("notacommand") == 0);
}

/**
 * Test: History
 */
void test_history(void) {
    TEST("Gestione history");

    History hist;
    init_history(&hist);

    ASSERT(hist.count == 0);
    ASSERT(hist.current == -1);

    add_to_history(&hist, "ls");
    ASSERT(hist.count == 1);
    ASSERT(strcmp(hist.commands[0], "ls") == 0);

    add_to_history(&hist, "pwd");
    ASSERT(hist.count == 2);
    ASSERT(strcmp(hist.commands[1], "pwd") == 0);

    char *cmd = get_history_command(&hist, -1);
    ASSERT(cmd != NULL);
    ASSERT(strcmp(cmd, "ls") == 0);

    cmd = get_history_command(&hist, 0);
    ASSERT(cmd != NULL);
    ASSERT(strcmp(cmd, "pwd") == 0);

    free_history(&hist);
}

/**
 * Test: Built-in echo
 */
void test_builtin_echo(void) {
    TEST("Built-in echo");

    char *args1[] = {"echo", "hello", "world", NULL};
    int result = builtin_echo(args1);
    ASSERT(result == 0);

    char *args2[] = {"echo", NULL};
    result = builtin_echo(args2);
    ASSERT(result == 0);
}

/**
 * Test: Conteggio argomenti
 */
void test_count_args(void) {
    TEST("Conteggio argomenti");

    char *args1[] = {"ls", "-la", "/home", NULL};
    ASSERT(count_args(args1) == 3);

    char *args2[] = {NULL};
    ASSERT(count_args(args2) == 0);
}

/**
 * Test: Rimozione spazi
 */
void test_strip_whitespace(void) {
    TEST("Rimozione spazi bianchi");

    char str1[] = "  hello  ";
    strip_whitespace(str1);
    ASSERT(strcmp(str1, "hello") == 0);

    char str2[] = "\ttab\t";
    strip_whitespace(str2);
    ASSERT(strcmp(str2, "tab") == 0);
}

/**
 * Test: Built-in exit
 */
void test_builtin_exit(void) {
    TEST("Built-in exit");

    g_running = 1;
    g_last_exit_status = 0;

    char *args1[] = {"exit", NULL};
    int result = builtin_exit(args1);
    ASSERT(g_running == 0);

    g_running = 1; /* Reset */
}

/**
 * Test: Built-in clear
 */
void test_builtin_clear(void) {
    TEST("Built-in clear");

    int result = builtin_clear(NULL);
    ASSERT(result == 0);
}

/**
 * Test: Built-in history command
 */
void test_builtin_history_cmd(void) {
    TEST("Built-in history command");

    /* Aggiungi alcuni comandi */
    add_to_history(&g_history, "ls");
    add_to_history(&g_history, "pwd");

    int result = builtin_history(NULL);
    ASSERT(result == 0);
}

/**
 * Test: Built-in help
 */
void test_builtin_help(void) {
    TEST("Built-in help");

    int result = builtin_help(NULL);
    ASSERT(result == 0);
}

/**
 * Funzione principale dei test
 */
int main(void) {
    printf("=================================\n");
    printf("  Mini Shell - Test Suite\n");
    printf("=================================\n");

    /* Esegui tutti i test */
    test_parse_input();
    test_empty_input();
    test_multiple_spaces();
    test_is_builtin();
    test_history();
    test_builtin_echo();
    test_count_args();
    test_strip_whitespace();
    test_builtin_exit();
    test_builtin_clear();
    test_builtin_history_cmd();
    test_builtin_help();

    /* Stampa risultati */
    printf("\n=================================\n");
    printf("  Risultati Test\n");
    printf("=================================\n");
    printf("✅ Passati: %d\n", tests_passed);
    printf("❌ Falliti: %d\n", tests_failed);
    printf("📊 Totale:  %d\n", tests_passed + tests_failed);
    printf("=================================\n");

    if (tests_failed == 0) {
        printf("✨ Tutti i test sono passati!\n");
        return 0;
    } else {
        printf("⚠️  Alcuni test sono falliti!\n");
        return 1;
    }
}
