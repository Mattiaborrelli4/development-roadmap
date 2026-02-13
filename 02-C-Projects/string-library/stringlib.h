/**
 * ================================================
 * STRINGLIB.H - Libreria di Manipolazione Stringhe
 * ================================================
 *
 * Questa libreria implementa le funzioni fondamentali per
 * la manipolazione delle stringhe in C, con focus sulla
 * sicurezza della memoria e sull'uso dei puntatori.
 *
 * Autore: Progetto Didattico
 * Target: Studenti Universitari
 * Linguaggio: C (ASCII)
 */

#ifndef STRINGLIB_H
#define STRINGLIB_H

#include <stddef.h>  /* per size_t */

/**
 * ============================================
 * SEZIONE 1: Funtionalità Base della Libreria
 * ============================================
 */

/**
 * Calcola la lunghezza di una stringa
 *
 * IMPORTANTE: Questa funzione dimostra l'uso di puntatori
 * per traversare un array di caratteri.
 *
 * @param str Puntatore alla stringa da misurare
 * @return Lunghezza della stringa (escluso il terminatore '\0')
 *
 * Esempio:
 *   char *s = "Hello";
 *   int len = stringlib_strlen(s);  // Ritorna 5
 *
 * CONCETTI CHIAVE:
 * - I puntatori possono essere incrementati per attraversare array
 * - Le stringhe C terminano sempre con '\0'
 * - Non conosciamo la lunghezza a priori, dobbiamo cercare il terminatore
 */
size_t stringlib_strlen(const char *str);

/**
 * Copia una stringa da source a destination
 *
 * IMPORTANTE: Questa funzione dimostra:
 * - Copia memoria byte per byte
 * - Gestione del terminatore '\0'
 * - Verifica di sicurezza NULL
 *
 * @param dest Puntatore alla stringa di destinazione
 * @param src Puntatore alla stringa sorgente
 * @return Puntatore alla stringa di destinazione
 *
 * NOTE DI SICUREZZA:
 * - DEVI assicurarti che dest abbia abbastanza spazio!
 * - Spazio necessario: strlen(src) + 1 caratteri
 * - La funzione NON verifica la dimensione del buffer
 *
 * Esempio:
 *   char buffer[20];
 *   char *text = "Hello";
 *   stringlib_strcpy(buffer, text);  // buffer ora contiene "Hello"
 *
 * CONCETTI CHIAVE:
 * - I puntatori permettono la modifica diretta della memoria
 * - *dest = *src copia un carattere
 * - dest++, src++ avanzano i puntatori al carattere successivo
 */
char *stringlib_strcpy(char *dest, const char *src);

/**
 * Concatena (aggiunge) una stringa alla fine di un'altra
 *
 * IMPORTANTE: Questa funzione combina:
 * - Ricerca del terminatore della prima stringa
 * - Copia della seconda stringa
 * - Gestione della memoria contigua
 *
 * @param dest Puntatore alla stringa di destinazione
 * @param src Puntatore alla stringa da aggiungere
 * @return Puntatore alla stringa di destinazione
 *
 * NOTE DI SICUREZZA:
 * - DEVI assicurarti che dest abbia abbastanza spazio!
 * - Spazio necessario: strlen(dest) + strlen(src) + 1 caratteri
 * - Overflow del buffer = vulnerabilità di sicurezza grave!
 *
 * Esempio:
 *   char buffer[50] = "Hello ";
 *   char *name = "World";
 *   stringlib_strcat(buffer, name);  // buffer ora contiene "Hello World"
 *
 * CONCETTI CHIAVE:
 * - Le stringhe sono memorizzate come array contigui in memoria
 * - Concatenare significa scrivere dopo il '\0' della prima stringa
 * - Due stringhe diventano una sola in memoria
 */
char *stringlib_strcat(char *dest, const char *src);

/**
 * ============================================
 * SEZIONE 2: Funzioni Aggiuntive di Sicurezza
 * ============================================
 */

/**
 * Copia sicura con limite di caratteri
 *
 * @param dest Puntatore alla stringa di destinazione
 * @param src Puntatore alla stringa sorgente
 * @param n Numero massimo di caratteri da copiare
 * @return Puntatore alla stringa di destinazione
 *
 * VANTAGGI: Previene buffer overflow specificando un limite
 */
size_t stringlib_strlcpy(char *dest, const char *src, size_t n);

/**
 * Concatenazione sicura con limite di caratteri
 *
 * @param dest Puntatore alla stringa di destinazione
 * @param src Puntatore alla stringa da aggiungere
 * @param n Dimensione totale del buffer di destinazione
 * @return Lunghezza totale della stringa risultante
 *
 * VANTAGGI: Previene overflow durante la concatenazione
 */
size_t stringlib_strlcat(char *dest, const char *src, size_t n);

/**
 * Confronta due stringhe lessicograficamente
 *
 * @param s1 Prima stringa
 * @param s2 Seconda stringa
 * @return 0 se uguali, <0 se s1 < s2, >0 se s1 > s2
 */
int stringlib_strcmp(const char *s1, const char *s2);

/**
 * Cerca un carattere in una stringa
 *
 * @param str Stringa in cui cercare
 * @param c Carattere da trovare
 * @return Puntatore al carattere trovato, NULL se non presente
 */
char *stringlib_strchr(const char *str, int c);

/**
 * Cerca una sottostringa in una stringa
 *
 * @param haystack Stringa in cui cercare
 * @param needle Stringa da trovare
 * @return Puntatore all'inizio della sottostringa, NULL se non presente
 */
char *stringlib_strstr(const char *haystack, const char *needle);

/**
 * Duplica una stringa (alloca nuova memoria)
 *
 * @param str Stringa da duplicare
 * @return Puntatore alla nuova stringa, NULL se errore allocazione
 *
 * IMPORTANTE: Devi chiamare free() sul risultato quando finito!
 */
char *stringlib_strdup(const char *str);

#endif /* STRINGLIB_H */
