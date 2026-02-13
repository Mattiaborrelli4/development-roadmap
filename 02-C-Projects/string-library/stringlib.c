/**
 * ================================================
 * STRINGLIB.C - Implementazione Libreria Stringhe
 * ================================================
 *
 * File di implementazione che contiene tutto il codice
 * delle funzioni dichiarate in stringlib.h
 *
 * Ogni funzione include commenti educativi dettagliati
 * per comprendere il funzionamento interno e l'uso dei
 * puntatori in C.
 */

#include "stringlib.h"
#include <stdlib.h>  /* per malloc, free */

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strlen
 * ============================================
 *
 * Calcola la lunghezza di una stringa contando i caratteri
 * finché non trova il terminatore '\0'.
 *
 * COMPLESSITÀ: O(n) dove n è la lunghezza della stringa
 */
size_t stringlib_strlen(const char *str) {
    size_t len;

    /*
     * VERIFICA DI SICUREZZA:
     * Controlliamo se il puntatore e NULL prima di accedere alla memoria.
     * Questo previene crash (segmentation fault).
     */
    if (str == NULL) {
        return 0;
    }

    /*
     * VARIABILE LOCALE:
     * 'len' tiene traccia del conteggio dei caratteri
     * Inizializzata a 0 perche non abbiamo ancora contato nulla
     */
    len = 0;

    /*
     * CICLO WHILE: Il cuore della funzione
     *
     * Condizione: *str != '\0'
     * - *str dereferenzia il puntatore: ottiene il carattere puntato
     * - '\0' è il carattere null che termina le stringhe C
     * - Il ciclo continua finché NON troviamo il terminatore
     *
     * Incremento: str++
     * - Sposta il puntatore al carattere successivo in memoria
     * - I char occupano 1 byte, quindi incrementa di 1 l'indirizzo
     *
     * ESEMPIO VISUALE:
     * Stringa "HI" in memoria:
     * Indirizzo:  1000   1001   1002
     * Valore:     'H'    'I'    '\0'
     *              ↑
     *             str
     *
     * Dopo str++ (1 iterazione):
     *              ↑      ↑
     *             str    (punta ora qui)
     *
     * CONCETTO CHIAVE:
     * I puntatori sono come frecce che puntano a posizioni di memoria.
     * Possiamo "spostare" la freccia avanti (o indietro) nell'array.
     */
    while (*str != '\0') {
        len++;  /* Conta questo carattere */
        str++;  /* Sposta il puntatore al carattere successivo */
    }

    /*
     * RETURN:
     * Restituisce il conteggio finale
     * NOTA: Non conta il '\0', solo i caratteri "utili"
     */
    return len;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strcpy
 * ============================================
 *
 * Copia una stringa da src a dest, carattere per carattere.
 *
 * COMPLESSITÀ: O(n) dove n è la lunghezza della stringa sorgente
 */
char *stringlib_strcpy(char *dest, const char *src) {
    /*
     * VERIFICHE DI SICUREZZA:
     * 1. dest non deve essere NULL (dove scriviamo)
     * 2. src non deve essere NULL (cosa leggiamo)
     *
     * Se una condizione fallisce, ritorniamo dest senza fare nulla.
     * Questo previene crash ma potrebbe causare comportamenti imprevisti.
     */
    if (dest == NULL || src == NULL) {
        return dest;
    }

    /*
     * PUNTATORE DI LAVORO:
     * Salviamo l'indirizzo originale di dest per poterlo ritornare.
     * Questo segue la convenzione della funzione standard strcpy().
     *
     * CONCETTO CHIAVE:
     * Possiamo avere più puntatori che puntano alla stessa memoria.
     * 'original' punta all'inizio del buffer dest.
     * 'dest' verrà spostato durante la copia.
     */
    char *original = dest;

    /*
     * CICLO DO-WHILE: Copia caratteri
     *
     * Questo pattern è elegante ma richiede spiegazione:
     *
     * 1. *dest = *src
     *    - Copia il carattere puntato da src nella posizione puntata da dest
     *    - Esempio: se src punta a 'H', dopo questo *dest contiene 'H'
     *
     * 2. Il valore assegnato (*dest) viene valutato come condizione
     *    - '\0' (valore 0) = falso, ciclo termina
     *    - Qualsiasi altro carattere = vero, ciclo continua
     *
     * 3. src++, dest++
     *    - Spostano entrambi i puntatori al carattere successivo
     *
     * ESEMPIO VISUALE:
     * src = "HI", dest = buffer vuoto
     *
     * Iterazione 1:
     * src: ['H']['I']['\0']  →  Copia 'H'
     *      ↑
     * dest: ['H'][ ? ][ ? ]  →  'H' copiato
     *       ↑
     *
     * Iterazione 2:
     * src: ['H']['I']['\0']  →  Copia 'I'
     *           ↑
     * dest: ['H']['I'][ ? ]  →  'I' copiato
     *            ↑
     *
     * Iterazione 3:
     * src: ['H']['I']['\0']  →  Copia '\0'
     *                ↑
     * dest: ['H']['I']['\0']  →  '\0' copiato, ciclo finisce
     *             ↑
     *
     * CONCETTO CHIAVE:
     * Il terminatore '\0' VIENE COPIATO! Questo è essenziale perché
     * senza di esso, la stringa non è valida e funzioni come strlen
     * continuerebbero a leggere memoria oltre la fine della stringa.
     */
    do {
        *dest = *src;
        dest++;
        src++;
    } while (*src != '\0');

    /*
     * COPIA DEL TERMINATORE:
     * Il ciclo do-while si ferma quando *src == '\0'
     * ma non l'ha ancora copiato in dest. Dobbiamo farlo ora.
     *
     * ALTERNATIVA: Usare un do-while che copia poi controlla.
     */
    *dest = '\0';

    /*
     * RETURN:
     * Ritorniamo il puntatore originale alla destinazione.
     * Questo permette concatenazioni: strcpy(strcpy(dest, a), b);
     */
    return original;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strcat
 * ============================================
 *
 * Concatena due stringhe scrivendo la seconda alla fine della prima.
 *
 * COMPLESSITÀ: O(n + m) dove n e m sono le lunghezze delle stringhe
 */
char *stringlib_strcat(char *dest, const char *src) {
    /*
     * VERIFICHE DI SICUREZZA:
     * Stesso controllo di strcpy per prevenire NULL pointer dereference
     */
    if (dest == NULL || src == NULL) {
        return dest;
    }

    /*
     * SALVATAGGIO PUNTATORE ORIGINALE:
     * Come in strcpy, salviamo l'indirizzo iniziale per il return
     */
    char *original = dest;

    /*
     * FASE 1: Trovare la fine di dest
     *
     * Dobbiamo trovare il '\0' di dest per sapere dove iniziare
     * a scrivere i caratteri di src.
     *
     * CONCETTO CHIAVE:
     * Questo è IDENTICO a strlen! Spostiamo il puntatore finché
     * non troviamo il terminatore.
     *
     * VISUALMENTE:
     * dest = "Hello", src = "World"
     * Memoria di dest: ['H']['e']['l']['l']['o']['\0'][ ? ][ ? ]
     *                                  ↑
     * Dopo questo ciclo, dest punta qui
     */
    while (*dest != '\0') {
        dest++;
    }

    /*
     * FASE 2: Copiare src alla fine di dest
     *
     * Ora che dest punta al '\0' della prima stringa, possiamo
     * copiare src esattamente come fa strcpy.
     *
     * VISUALMENTE (continuazione):
     * dest ora punta qui → ['H']['e']['l']['l']['o']['\0'][ ? ][ ? ]
     *
     * Durante la copia di "World":
     * ['H']['e']['l']['l']['o']['W']['o']['r']['l']['d']['\0']
     *
     * CONCETTO CHIAVE:
     * Le due stringhe diventano UNA SOLA stringa in memoria!
     * Il '\0' originale di "Hello" viene sovrascritto da 'W'.
     * Il nuovo '\0' alla fine completa la stringa concatenata.
     */
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }

    /*
     * TERMINATORE FINALE:
     * Chiudiamo la stringa concatenata con '\0'
     */
    *dest = '\0';

    /*
     * RETURN:
     * Ritorniamo il puntatore originale, non quello spostato!
     * Questo permette di mantenere l'indirizzo originale del buffer.
     */
    return original;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strlcpy
 * ============================================
 *
 * Versione SICURA di strcpy con limite di caratteri.
 *
 * COMPLESSITÀ: O(min(n, strlen(src)))
 */
size_t stringlib_strlcpy(char *dest, const char *src, size_t n) {
    /*
     * CASI PARTICOLARI:
     * 1. Se n == 0, non possiamo copiare nulla (ritorniamo solo lunghezza)
     * 2. Se src è NULL, consideriamo stringa vuota
     * 3. Se dest è NULL ma n > 0, comportamento indefinito (evitato)
     */
    if (n == 0) {
        return (src == NULL) ? 0 : stringlib_strlen(src);
    }

    if (src == NULL) {
        *dest = '\0';
        return 0;
    }

    /*
     * CALCOLO LUNGHEZZA SOURCES:
     * Dobbiamo sapere quanto è lunga src per decidere quanto copiare
     */
    size_t src_len = stringlib_strlen(src);

    /*
     * COPIA CON LIMITE:
     * Copiamo al più n-1 caratteri (lasciamo spazio per '\0')
     */
    size_t copy_len = (src_len < n - 1) ? src_len : n - 1;

    for (size_t i = 0; i < copy_len; i++) {
        dest[i] = src[i];
    }

    /*
     * TERMINATORE:
     * Garantiamo sempre che dest sia terminata correttamente
     */
    dest[copy_len] = '\0';

    /*
     * RETURN:
     * Ritorniamo la lunghezza totale che avremmo copiato senza limite
     * Questo permette di detectare se c'è stato troncamento
     */
    return src_len;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strlcat
 * ============================================
 *
 * Versione SICURA di strcat con limite del buffer.
 *
 * COMPLESSITÀ: O(n + m) dove n, m sono le lunghezze
 */
size_t stringlib_strlcat(char *dest, const char *src, size_t n) {
    /*
     * CASO LIMITE:
     * Se n == 0, non possiamo fare nulla
     */
    if (n == 0) {
        return 0;
    }

    /*
     * CALCOLO LUNGHEZZA DEST ATTUALE:
     * Dobbiamo sapere dove finisce dest
     */
    size_t dest_len = 0;
    const char *p = dest;

    while (*p != '\0' && dest_len < n) {
        dest_len++;
        p++;
    }

    /*
     * Se dest è già piena fino a n, non possiamo aggiungere nulla
     */
    if (dest_len >= n) {
        return n + stringlib_strlen(src);
    }

    /*
     * SPAZIO DISPONIBILE:
     * Calcoliamo quanti caratteri possiamo ancora copiare
     * (n - dest_len - 1 per il terminatore)
     */
    size_t available = n - dest_len - 1;
    size_t src_len = stringlib_strlen(src);
    size_t copy_len = (src_len < available) ? src_len : available;

    /*
     * COPIA:
     * Copiamo i caratteri di src alla fine di dest
     */
    for (size_t i = 0; i < copy_len; i++) {
        dest[dest_len + i] = src[i];
    }

    /*
     * TERMINATORE:
     * Assicuriamo la terminazione corretta
     */
    dest[dest_len + copy_len] = '\0';

    /*
     * RETURN:
     * Ritorniamo la lunghezza totale della stringa risultante
     * (come se non ci fosse limite)
     */
    return dest_len + src_len;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strcmp
 * ============================================
 *
 * Confronta due stringhe lessicograficamente (alfabeticamente).
 *
 * COMPLESSITÀ: O(min(n, m)) dove n, m sono le lunghezze
 */
int stringlib_strcmp(const char *s1, const char *s2) {
    /*
     * VERIFICHE DI SICUREZZA:
     */
    if (s1 == NULL && s2 == NULL) return 0;
    if (s1 == NULL) return -1;
    if (s2 == NULL) return 1;

    /*
     * CICLO DI CONFRONTO:
     * Confrontiamo carattere per carattere finché:
     * - Troviamo differenza
     * - Arriviamo alla fine di una delle stringhe
     */
    while (*s1 != '\0' && *s2 != '\0') {
        if (*s1 != *s2) {
            /*
             * TROVATA DIFFERENZA:
             * Ritorniamo la differenza tra i codici ASCII
             * - Se s1 < s2, risultato negativo
             * - Se s1 > s2, risultato positivo
             *
             * ESEMPIO:
             * "Hello" vs "World"
             * 'H' (72) vs 'W' (87)
             * Ritorna 72 - 87 = -15 (negativo = s1 < s2)
             */
            return (unsigned char)*s1 - (unsigned char)*s2;
        }
        s1++;
        s2++;
    }

    /*
     * CASO LIMITE:
     * Se arriviamo qui, almeno una stringa è finita
     * Confrontiamo i caratteri rimanenti (uno sarà '\0')
     */
    return (unsigned char)*s1 - (unsigned char)*s2;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strchr
 * ============================================
 *
 * Cerca un carattere in una stringa e ritorna il puntatore.
 *
 * COMPLESSITÀ: O(n)
 */
char *stringlib_strchr(const char *str, int c) {
    if (str == NULL) {
        return NULL;
    }

    /*
     * CICLO DI RICERCA:
     * Cerchiamo il carattere c (convertito a char)
     *
     * NOTA: Controlliamo anche *str == '\0' prima di confrontare
     * per permettere di cercare il terminatore stesso!
     */
    while (*str != '\0') {
        if (*str == (char)c) {
            /*
             * TROVATO!
             * Castiamo a char* perché la funzione ritorna un
             * puntatore non-const (possiamo modificare il risultato)
             */
            return (char *)str;
        }
        str++;
    }

    /*
     * CASO SPECIALE:
     * Se cerchiamo '\0', ritorniamo il puntatore al terminatore
     */
    if ((char)c == '\0') {
        return (char *)str;
    }

    /*
     * NON TROVATO:
     * Ritorniamo NULL per indicare che il carattere non esiste
     */
    return NULL;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strstr
 * ============================================
 *
 * Cerca una sottostringa in una stringa.
 *
 * COMPLESSITÀ: O(n * m) nel caso peggiore
 */
char *stringlib_strstr(const char *haystack, const char *needle) {
    /*
     * PARAMETRI:
     * - haystack: pagliaio (dove cerchiamo)
     * - needle: ago (cosa cerchiamo)
     */

    if (haystack == NULL || needle == NULL) {
        return NULL;
    }

    /*
     * CASO PARTICOLARE:
     * Se needle è vuota, ritorniamo haystack (convenzione standard)
     */
    if (*needle == '\0') {
        return (char *)haystack;
    }

    /*
     * ALGORITMO DI RICERCA:
     * Per ogni posizione in haystack, controlliamo se needle inizia lì
     */
    while (*haystack != '\0') {
        /*
         * PUNTATORI TEMPORANEI:
         * Usiamo puntatori locali per non perdere la posizione
         */
        const char *h = haystack;
        const char *n = needle;

        /*
         * VERIFICA MATCH:
         * Confrontiamo carattere per carattere
         */
        while (*n != '\0' && *h == *n) {
            h++;
            n++;
        }

        /*
         * CONTROLLO SUCCESSO:
         * Se *n == '\0', abbiamo trovato tutta la sottostringa!
         */
        if (*n == '\0') {
            return (char *)haystack;
        }

        /*
         * PROSSIMA POSIZIONE:
         * Spostiamoci al carattere successivo in haystack
         */
        haystack++;
    }

    /*
     * NON TROVATO:
     */
    return NULL;
}

/**
 * ============================================
 * IMPLEMENTAZIONE: stringlib_strdup
 * ============================================
 *
 * Duplica una stringa allocando nuova memoria.
 *
 * COMPLESSITÀ: O(n)
 *
 * IMPORTANTE: Chiama questa funzione DEVE chiamare free()
 * sul risultato quando ha finito di usare la stringa!
 */
char *stringlib_strdup(const char *str) {
    if (str == NULL) {
        return NULL;
    }

    /*
     * CALCOLO DIMENSIONE:
     * +1 per il terminatore '\0'
     */
    size_t len = stringlib_strlen(str);
    char *new_str = (char *)malloc(len + 1);

    /*
     * VERIFICA ALLOCAZIONE:
     * malloc può fallire se la memoria è esaurita
     * In quel caso ritorna NULL
     */
    if (new_str == NULL) {
        return NULL;
    }

    /*
     * COPIA:
     * Usiamo la nostra strcpy per copiare il contenuto
     */
    stringlib_strcpy(new_str, str);

    /*
     * RETURN:
     * Ritorniamo il puntatore alla nuova memoria allocata
     *
     * CONCETTO CHIAVE:
     * Questa nuova memoria è DINAMICA, deve essere liberata!
     * Il chiamante deve fare: free(stringlib_strdup("test"));
     */
    return new_str;
}
