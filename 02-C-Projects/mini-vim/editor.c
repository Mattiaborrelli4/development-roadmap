/**
 * Mini Vim - Un Editor di Testo Modal
 * Editor di testo in stile Vim con modalità NORMAL e INSERT
 *
 * Comandi in modalità NORMAL:
 *   h, j, k, l - movimento cursore
 *   i - entra in modalità INSERT
 *   :w - salva file
 *   :q - esci
 *   :wq - salva e esci
 *   :e filename - carica file
 *
 * Comandi in modalità INSERT:
 *   caratteri - inserisce testo
 *   BACKSPACE - elimina carattere
 *   ENTER - nuova riga
 *   ESC - torna a modalità NORMAL
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "buffer.h"

/* Definizione piattaforma */
#if defined(_WIN32) || defined(_WIN64)
    #define PLATFORM_WINDOWS
    #include <conio.h>
    #include <windows.h>
#else
    #define PLATFORM_UNIX
    #include <termios.h>
    #include <unistd.h>
    #include <sys/ioctl.h>
#endif

/* Modalità dell'editor */
typedef enum {
    MODE_NORMAL,
    MODE_INSERT,
    MODE_COMMAND
} EditorMode;

/* Struttura editor */
typedef struct {
    Buffer *buffer;
    EditorMode mode;
    int running;
    char command[256];      /* Buffer per comandi */
    size_t command_len;
} Editor;

/* Funzioni di I/O dipendenti dalla piattaforma */
void enable_raw_mode(void) {
#ifdef PLATFORM_UNIX
    struct termios term;
    tcgetattr(STDIN_FILENO, &term);
    term.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &term);
#endif
}

void disable_raw_mode(void) {
#ifdef PLATFORM_UNIX
    struct termios term;
    tcgetattr(STDIN_FILENO, &term);
    term.c_lflag |= (ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &term);
#endif
}

int kbhit(void) {
#ifdef PLATFORM_WINDOWS
    return _kbhit();
#else
    struct timeval tv = {0L, 0L};
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(STDIN_FILENO, &fds);
    return select(STDIN_FILENO + 1, &fds, NULL, NULL, &tv);
#endif
}

int getch(void) {
#ifdef PLATFORM_WINDOWS
    return _getch();
#else
    struct termios oldt, newt;
    int ch;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return ch;
#endif
}

void clear_screen(void) {
#ifdef PLATFORM_WINDOWS
    system("cls");
#else
    system("clear");
#endif
}

/* Funzioni dell'editor */
void editor_init(Editor *editor) {
    editor->buffer = buffer_create();
    editor->mode = MODE_NORMAL;
    editor->running = 1;
    editor->command[0] = '\0';
    editor->command_len = 0;

    enable_raw_mode();
}

void editor_cleanup(Editor *editor) {
    if (editor->buffer) {
        buffer_destroy(editor->buffer);
    }
    disable_raw_mode();
}

void editor_draw(Editor *editor) {
    clear_screen();

    printf("=== MINI VIM ===\n");
    printf("File: %s\n", editor->buffer->filename ?
           editor->buffer->filename : "(senza nome)");
    printf("Modalità: %s %s\n",
           editor->mode == MODE_NORMAL ? "NORMAL" :
           editor->mode == MODE_INSERT ? "INSERT" : "COMMAND",
           editor->buffer->modified ? "[MODIFICATO]" : "");
    printf("==================================\n\n");

    /* Mostra le righe del buffer */
    for (size_t i = 0; i < editor->buffer->line_count; i++) {
        if (i == editor->buffer->cursor_y) {
            /* Mostra il cursore sulla riga corrente */
            printf("%.*s", (int)editor->buffer->cursor_x,
                   editor->buffer->lines[i]);
            printf("|");  /* Indicatore cursore */
            printf("%s\n", &editor->buffer->lines[i][editor->buffer->cursor_x]);
        } else {
            printf("%s\n", editor->buffer->lines[i]);
        }
    }

    printf("\n==================================\n");
    printf("Comandi NORMAL: h,j,k,l=move i=insert :=command ESC=normal\n");
    printf("Comandi: :w=save :q=quit :wq=save&quit :e file=load\n");

    if (editor->mode == MODE_COMMAND) {
        printf("\n:%s", editor->command);
    }
}

void editor_handle_normal(Editor *editor, int ch) {
    switch (ch) {
        case 'h':
            buffer_move_left(editor->buffer);
            break;
        case 'l':
            buffer_move_right(editor->buffer);
            break;
        case 'k':
            buffer_move_up(editor->buffer);
            break;
        case 'j':
            buffer_move_down(editor->buffer);
            break;
        case 'i':
            editor->mode = MODE_INSERT;
            break;
        case ':':
            editor->mode = MODE_COMMAND;
            editor->command[0] = '\0';
            editor->command_len = 0;
            break;
        case 27: /* ESC */
            /* Già in NORMAL, non fare nulla */
            break;
    }
}

void editor_handle_insert(Editor *editor, int ch) {
    switch (ch) {
        case 27: /* ESC */
            editor->mode = MODE_NORMAL;
            break;
        case 8:   /* BACKSPACE */
        case 127: /* BACKSPACE su Unix */
            buffer_delete_char(editor->buffer);
            break;
        case 13:  /* ENTER */
            buffer_insert_newline(editor->buffer);
            break;
        case 3:   /* CTRL+C - Ignora */
            break;
        default:
            if (ch >= 32 && ch <= 126) { /* Caratteri stampabili */
                buffer_insert_char(editor->buffer, (char)ch);
            }
            break;
    }
}

void editor_handle_command(Editor *editor, int ch) {
    switch (ch) {
        case 27: /* ESC */
            editor->mode = MODE_NORMAL;
            editor->command[0] = '\0';
            editor->command_len = 0;
            break;
        case 13: /* ENTER - Esegui comando */
            editor->command[editor->command_len] = '\0';

            /* Analizza il comando */
            if (strcmp(editor->command, "w") == 0) {
                /* Salva */
                if (editor->buffer->filename) {
                    if (buffer_save_file(editor->buffer,
                                        editor->buffer->filename) == 0) {
                        printf("\nFile salvato con successo!");
                        getchar();
                    } else {
                        printf("\nErrore nel salvataggio!");
                        getchar();
                    }
                } else {
                    printf("\nNessun nome file specificato. Usa :w filename");
                    getchar();
                }
            } else if (strcmp(editor->command, "q") == 0) {
                /* Esci */
                if (editor->buffer->modified) {
                    printf("\nFile modificato. Usa :wq per salvare e uscire.");
                    getchar();
                } else {
                    editor->running = 0;
                }
            } else if (strcmp(editor->command, "wq") == 0) {
                /* Salva e esci */
                if (editor->buffer->filename) {
                    buffer_save_file(editor->buffer,
                                    editor->buffer->filename);
                    editor->running = 0;
                } else {
                    printf("\nNessun nome file specificato.");
                    getchar();
                }
            } else if (strncmp(editor->command, "w ", 2) == 0) {
                /* Salva con nome */
                const char *filename = &editor->command[2];
                if (buffer_save_file(editor->buffer, filename) == 0) {
                    printf("\nFile salvato con successo!");
                    getchar();
                } else {
                    printf("\nErrore nel salvataggio!");
                    getchar();
                }
            } else if (strncmp(editor->command, "e ", 2) == 0) {
                /* Carica file */
                const char *filename = &editor->command[2];
                if (buffer_load_file(editor->buffer, filename) == 0) {
                    printf("\nFile caricato con successo!");
                    getchar();
                } else {
                    printf("\nErrore nel caricamento del file!");
                    getchar();
                }
            } else if (strncmp(editor->command, "wq ", 3) == 0) {
                /* Salva con nome e esci */
                const char *filename = &editor->command[3];
                if (buffer_save_file(editor->buffer, filename) == 0) {
                    editor->running = 0;
                } else {
                    printf("\nErrore nel salvataggio!");
                    getchar();
                }
            } else {
                printf("\nComando sconosciuto: %s", editor->command);
                getchar();
            }

            editor->mode = MODE_NORMAL;
            editor->command[0] = '\0';
            editor->command_len = 0;
            break;
        case 8:   /* BACKSPACE */
        case 127: /* BACKSPACE su Unix */
            if (editor->command_len > 0) {
                editor->command_len--;
                editor->command[editor->command_len] = '\0';
            }
            break;
        default:
            if (ch >= 32 && ch <= 126 && editor->command_len < 255) {
                editor->command[editor->command_len++] = (char)ch;
                editor->command[editor->command_len] = '\0';
            }
            break;
    }
}

void editor_run(Editor *editor) {
    while (editor->running) {
        editor_draw(editor);

        /* Attende input */
        if (kbhit()) {
            int ch = getch();

            switch (editor->mode) {
                case MODE_NORMAL:
                    editor_handle_normal(editor, ch);
                    break;
                case MODE_INSERT:
                    editor_handle_insert(editor, ch);
                    break;
                case MODE_COMMAND:
                    editor_handle_command(editor, ch);
                    break;
            }
        }

        /* Piccola pausa per non consumare CPU */
#ifdef PLATFORM_WINDOWS
        Sleep(10);
#else
        usleep(10000);
#endif
    }
}

void print_usage(const char *progname) {
    printf("Mini Vim - Editor di Testo Modal\n\n");
    printf("Uso: %s [filename]\n", progname);
    printf("\nComandi in modalità NORMAL:\n");
    printf("  h, j, k, l - movimento cursore (sinistra, giù, su, destra)\n");
    printf("  i - entra in modalità INSERT\n");
    printf("  : - entra in modalità COMMAND\n\n");
    printf("Comandi in modalità INSERT:\n");
    printf("  caratteri - inserisce testo\n");
    printf("  BACKSPACE - elimina carattere\n");
    printf("  ENTER - nuova riga\n");
    printf("  ESC - torna a modalità NORMAL\n\n");
    printf("Comandi:\n");
    printf("  :w - salva file\n");
    printf("  :w filename - salva con nome\n");
    printf("  :q - esci (se non modificato)\n");
    printf("  :wq - salva e esci\n");
    printf("  :wq filename - salva con nome e esci\n");
    printf("  :e filename - carica file\n");
}

int main(int argc, char *argv[]) {
    Editor editor;

    printf("\nMini Vim v1.0\n");
    printf("Premi ENTER per iniziare...\n");
    getchar();

    editor_init(&editor);

    /* Carica file se specificato */
    if (argc > 1) {
        if (buffer_load_file(editor.buffer, argv[1]) != 0) {
            printf("Nuovo file: %s\n", argv[1]);
            buffer_set_filename(editor.buffer, argv[1]);
        } else {
            printf("File caricato: %s\n", argv[1]);
        }
    }

    /* Loop principale */
    editor_run(&editor);

    /* Cleanup */
    editor_cleanup(&editor);

    printf("\nGrazie per aver usato Mini Vim!\n");

    return 0;
}
