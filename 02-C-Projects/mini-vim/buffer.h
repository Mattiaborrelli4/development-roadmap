/**
 * Mini Vim - Buffer Management
 * Gestione del buffer di testo per l'editor
 */

#ifndef BUFFER_H
#define BUFFER_H

#include <stdlib.h>
#include <stdio.h>

#define INITIAL_BUFFER_SIZE 1024
#define INITIAL_LINE_CAPACITY 100

typedef struct {
    char **lines;           /* Array di linee */
    size_t line_count;      /* Numero di linee */
    size_t line_capacity;   /* Capacità delle linee */
    size_t cursor_x;        /* Posizione cursore colonna */
    size_t cursor_y;        /* Posizione cursore riga */
    int modified;           /* Flag: buffer modificato */
    char *filename;         /* Nome del file corrente */
} Buffer;

/**
 * Crea un nuovo buffer vuoto
 */
Buffer *buffer_create(void);

/**
 * Distrugge un buffer e libera la memoria
 */
void buffer_destroy(Buffer *buf);

/**
 * Inserisce un carattere nella posizione corrente del cursore
 */
void buffer_insert_char(Buffer *buf, char c);

/**
 * Elimina il carattere alla posizione corrente del cursore
 * (backspace)
 */
void buffer_delete_char(Buffer *buf);

/**
 * Inserisce una nuova riga (invio)
 */
void buffer_insert_newline(Buffer *buf);

/**
 * Carica un file nel buffer
 * Restituisce 0 in caso di successo, -1 in caso di errore
 */
int buffer_load_file(Buffer *buf, const char *filename);

/**
 * Salva il buffer su file
 * Restituisce 0 in caso di successo, -1 in caso di errore
 */
int buffer_save_file(Buffer *buf, const char *filename);

/**
 * Muove il cursore su/giù/sinistra/destra
 */
void buffer_move_left(Buffer *buf);
void buffer_move_right(Buffer *buf);
void buffer_move_up(Buffer *buf);
void buffer_move_down(Buffer *buf);

/**
 * Imposta il nome del file
 */
void buffer_set_filename(Buffer *buf, const char *filename);

/**
 * Ottiene la riga corrente
 */
char *buffer_get_current_line(Buffer *buf);

/**
 * Ottiene la lunghezza della riga corrente
 */
size_t buffer_get_current_line_length(Buffer *buf);

#endif /* BUFFER_H */
