/**
 * Mini Vim - Buffer Implementation
 * Implementazione della gestione del buffer
 */

#include "buffer.h"
#include <string.h>
#include <stdlib.h>

Buffer *buffer_create(void) {
    Buffer *buf = (Buffer *)malloc(sizeof(Buffer));
    if (!buf) return NULL;

    buf->lines = (char **)malloc(sizeof(char *) * INITIAL_LINE_CAPACITY);
    if (!buf->lines) {
        free(buf);
        return NULL;
    }

    /* Crea la prima riga vuota */
    buf->lines[0] = (char *)malloc(INITIAL_BUFFER_SIZE);
    if (!buf->lines[0]) {
        free(buf->lines);
        free(buf);
        return NULL;
    }
    buf->lines[0][0] = '\0';

    buf->line_count = 1;
    buf->line_capacity = INITIAL_LINE_CAPACITY;
    buf->cursor_x = 0;
    buf->cursor_y = 0;
    buf->modified = 0;
    buf->filename = NULL;

    return buf;
}

void buffer_destroy(Buffer *buf) {
    if (!buf) return;

    for (size_t i = 0; i < buf->line_count; i++) {
        free(buf->lines[i]);
    }
    free(buf->lines);
    free(buf->filename);
    free(buf);
}

void buffer_insert_char(Buffer *buf, char c) {
    if (!buf) return;

    char *current_line = buf->lines[buf->cursor_y];
    size_t len = strlen(current_line);

    /* Sposta il carattere successivo e quelli dopo per fare spazio */
    memmove(&current_line[buf->cursor_x + 1],
            &current_line[buf->cursor_x],
            len - buf->cursor_x + 1);

    /* Inserisce il nuovo carattere */
    current_line[buf->cursor_x] = c;

    /* Muove il cursore a destra */
    buf->cursor_x++;

    buf->modified = 1;
}

void buffer_delete_char(Buffer *buf) {
    if (!buf) return;

    if (buf->cursor_x == 0) {
        /* Se siamo all'inizio della riga e non è la prima riga,
         * uniamo con la riga precedente */
        if (buf->cursor_y > 0) {
            size_t prev_len = strlen(buf->lines[buf->cursor_y - 1]);
            size_t curr_len = strlen(buf->lines[buf->cursor_y]);

            /* Ridimensiona la riga precedente */
            char *prev_line = buf->lines[buf->cursor_y - 1];
            char *curr_line = buf->lines[buf->cursor_y];

            /* Concatena le righe */
            memcpy(&prev_line[prev_len], curr_line, curr_len + 1);

            /* Libera la riga corrente */
            free(buf->lines[buf->cursor_y]);

            /* Sposta le righe successive */
            for (size_t i = buf->cursor_y; i < buf->line_count - 1; i++) {
                buf->lines[i] = buf->lines[i + 1];
            }

            buf->line_count--;
            buf->cursor_y--;
            buf->cursor_x = prev_len;
        }
    } else {
        /* Elimina il carattere precedente */
        char *current_line = buf->lines[buf->cursor_y];
        size_t len = strlen(current_line);

        memmove(&current_line[buf->cursor_x - 1],
                &current_line[buf->cursor_x],
                len - buf->cursor_x + 1);

        buf->cursor_x--;
    }

    buf->modified = 1;
}

void buffer_insert_newline(Buffer *buf) {
    if (!buf) return;

    char *current_line = buf->lines[buf->cursor_y];

    /* Assicuriamoci di avere abbastanza spazio per nuove righe */
    if (buf->line_count >= buf->line_capacity) {
        buf->line_capacity *= 2;
        buf->lines = (char **)realloc(buf->lines,
                                      sizeof(char *) * buf->line_capacity);
        if (!buf->lines) return;
    }

    /* Crea una nuova riga con il testo dopo il cursore */
    char *new_line = (char *)malloc(INITIAL_BUFFER_SIZE);
    if (!new_line) return;

    strcpy(new_line, &current_line[buf->cursor_x]);
    current_line[buf->cursor_x] = '\0';

    /* Sposta le righe successive */
    for (size_t i = buf->line_count; i > buf->cursor_y + 1; i--) {
        buf->lines[i] = buf->lines[i - 1];
    }

    buf->lines[buf->cursor_y + 1] = new_line;
    buf->line_count++;

    /* Muove il cursore all'inizio della nuova riga */
    buf->cursor_y++;
    buf->cursor_x = 0;

    buf->modified = 1;
}

int buffer_load_file(Buffer *buf, const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        return -1;
    }

    /* Libera le righe esistenti */
    for (size_t i = 0; i < buf->line_count; i++) {
        free(buf->lines[i]);
    }

    buf->line_count = 0;

    char line[INITIAL_BUFFER_SIZE];
    while (fgets(line, sizeof(line), file)) {
        /* Rimuove il newline se presente */
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
            len--;
        }

        /* Assicuriamoci di avere abbastanza spazio */
        if (buf->line_count >= buf->line_capacity) {
            buf->line_capacity *= 2;
            buf->lines = (char **)realloc(buf->lines,
                                          sizeof(char *) * buf->line_capacity);
        }

        /* Alloca e copia la riga */
        buf->lines[buf->line_count] = (char *)malloc(INITIAL_BUFFER_SIZE);
        if (!buf->lines[buf->line_count]) {
            fclose(file);
            return -1;
        }

        strcpy(buf->lines[buf->line_count], line);
        buf->line_count++;
    }

    fclose(file);

    /* Se il file è vuoto, crea almeno una riga vuota */
    if (buf->line_count == 0) {
        buf->lines[0] = (char *)malloc(INITIAL_BUFFER_SIZE);
        if (!buf->lines[0]) return -1;
        buf->lines[0][0] = '\0';
        buf->line_count = 1;
    }

    /* Reset del cursore */
    buf->cursor_x = 0;
    buf->cursor_y = 0;
    buf->modified = 0;

    /* Imposta il nome del file */
    buffer_set_filename(buf, filename);

    return 0;
}

int buffer_save_file(Buffer *buf, const char *filename) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        return -1;
    }

    for (size_t i = 0; i < buf->line_count; i++) {
        fputs(buf->lines[i], file);
        if (i < buf->line_count - 1) {
            fputs("\n", file);
        }
    }

    fclose(file);

    buf->modified = 0;
    buffer_set_filename(buf, filename);

    return 0;
}

void buffer_move_left(Buffer *buf) {
    if (buf->cursor_x > 0) {
        buf->cursor_x--;
    }
}

void buffer_move_right(Buffer *buf) {
    size_t len = strlen(buf->lines[buf->cursor_y]);
    if (buf->cursor_x < len) {
        buf->cursor_x++;
    }
}

void buffer_move_up(Buffer *buf) {
    if (buf->cursor_y > 0) {
        buf->cursor_y--;
        /* Adjust cursor_x se la riga precedente è più corta */
        size_t len = strlen(buf->lines[buf->cursor_y]);
        if (buf->cursor_x > len) {
            buf->cursor_x = len;
        }
    }
}

void buffer_move_down(Buffer *buf) {
    if (buf->cursor_y < buf->line_count - 1) {
        buf->cursor_y++;
        /* Adjust cursor_x se la riga successiva è più corta */
        size_t len = strlen(buf->lines[buf->cursor_y]);
        if (buf->cursor_x > len) {
            buf->cursor_x = len;
        }
    }
}

void buffer_set_filename(Buffer *buf, const char *filename) {
    if (buf->filename) {
        free(buf->filename);
    }
    if (filename) {
        buf->filename = (char *)malloc(strlen(filename) + 1);
        if (buf->filename) {
            strcpy(buf->filename, filename);
        }
    } else {
        buf->filename = NULL;
    }
}

char *buffer_get_current_line(Buffer *buf) {
    if (!buf || buf->cursor_y >= buf->line_count) return NULL;
    return buf->lines[buf->cursor_y];
}

size_t buffer_get_current_line_length(Buffer *buf) {
    if (!buf || buf->cursor_y >= buf->line_count) return 0;
    return strlen(buf->lines[buf->cursor_y]);
}
