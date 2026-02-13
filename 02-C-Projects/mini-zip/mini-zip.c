/*
 * Mini-Zip - Utility di Compressione File RLE
 * Implementazione di Run-Length Encoding per compressione dati
 *
 * Autore: Matti
 * Data: 2026-02-12
 * Linguaggio: C (C99)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAX_COUNT 255
#define BUFFER_SIZE 4096

/* Struttura per l'header del file compresso */
typedef struct {
    uint8_t magic[4];      /* Signature: "RLE\0" */
    uint32_t original_size; /* Dimensione file originale */
} RLEHeader;

/* Funzione per mostrare l'uso del programma */
void print_usage(const char *program_name) {
    printf("Mini-Zip - Utility di Compressione RLE\n");
    printf("======================================\n\n");
    printf("Uso: %s <comando> <file_input> [file_output]\n\n", program_name);
    printf("Comandi:\n");
    printf("  c, compress    Comprimi un file\n");
    printf("  d, decompress  Decomprimi un file\n");
    printf("  h, help        Mostra questo aiuto\n\n");
    printf("Esempi:\n");
    printf("  %s compress documento.txt documento.rle\n", program_name);
    printf("  %s d documento.rle documento.txt\n", program_name);
}

/* Funzione per comprimere un file usando RLE */
int compress_file(const char *input_path, const char *output_path) {
    FILE *input_file = NULL;
    FILE *output_file = NULL;
    unsigned char *buffer = NULL;
    unsigned char *compressed = NULL;
    size_t bytes_read;
    size_t compressed_size = 0;
    size_t original_size = 0;

    /* Apri il file di input */
    input_file = fopen(input_path, "rb");
    if (input_file == NULL) {
        fprintf(stderr, "Errore: Impossibile aprire il file '%s'\n", input_path);
        return 1;
    }

    /* Ottieni la dimensione del file */
    fseek(input_file, 0, SEEK_END);
    original_size = ftell(input_file);
    fseek(input_file, 0, SEEK_SET);

    if (original_size == 0) {
        fprintf(stderr, "Errore: Il file '%s' e' vuoto\n", input_path);
        fclose(input_file);
        return 1;
    }

    /* Alloca buffer per lettura e scrittura */
    buffer = (unsigned char *)malloc(BUFFER_SIZE);
    compressed = (unsigned char *)malloc(BUFFER_SIZE * 2);

    if (buffer == NULL || compressed == NULL) {
        fprintf(stderr, "Errore: Memoria insufficiente\n");
        if (buffer) free(buffer);
        if (compressed) free(compressed);
        fclose(input_file);
        return 1;
    }

    /* Apri il file di output */
    output_file = fopen(output_path, "wb");
    if (output_file == NULL) {
        fprintf(stderr, "Errore: Impossibile creare il file '%s'\n", output_path);
        free(buffer);
        free(compressed);
        fclose(input_file);
        return 1;
    }

    /* Scrivi l'header del file compresso */
    RLEHeader header;
    header.magic[0] = 'R';
    header.magic[1] = 'L';
    header.magic[2] = 'E';
    header.magic[3] = '\0';
    header.original_size = (uint32_t)original_size;

    if (fwrite(&header, sizeof(RLEHeader), 1, output_file) != 1) {
        fprintf(stderr, "Errore: Impossibile scrivere l'header\n");
        free(buffer);
        free(compressed);
        fclose(input_file);
        fclose(output_file);
        return 1;
    }

    printf("Compressione in corso...\n");

    /* Leggi e comprimi il file */
    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, input_file)) > 0) {
        size_t i = 0;
        size_t comp_idx = 0;

        while (i < bytes_read) {
            unsigned char current_byte = buffer[i];
            unsigned char count = 1;

            /* Conta byte consecutivi uguali */
            while (i + count < bytes_read &&
                   buffer[i + count] == current_byte &&
                   count < MAX_COUNT) {
                count++;
            }

            /* Scrivi count e byte */
            compressed[comp_idx++] = count;
            compressed[comp_idx++] = current_byte;

            i += count;
        }

        /* Scrivi i dati compressi */
        if (fwrite(compressed, 1, comp_idx, output_file) != comp_idx) {
            fprintf(stderr, "Errore: Impossibile scrivere i dati compressi\n");
            free(buffer);
            free(compressed);
            fclose(input_file);
            fclose(output_file);
            return 1;
        }

        compressed_size += comp_idx;
    }

    /* Cleanup */
    free(buffer);
    free(compressed);
    fclose(input_file);
    fclose(output_file);

    /* Calcola e mostra il compression ratio */
    double ratio = ((double)compressed_size / original_size) * 100.0;
    printf("\nCompressione completata!\n");
    printf("Dimensione originale:      %lu bytes\n", (unsigned long)original_size);
    printf("Dimensione compressa:      %lu bytes\n", (unsigned long)compressed_size);
    printf("Compression ratio:         %.2f%%\n", ratio);
    printf("Spazio risparmiato:        %lu bytes\n", (unsigned long)(original_size - compressed_size));

    return 0;
}

/* Funzione per decomprimere un file RLE */
int decompress_file(const char *input_path, const char *output_path) {
    FILE *input_file = NULL;
    FILE *output_file = NULL;
    unsigned char *buffer = NULL;
    RLEHeader header;

    /* Apri il file di input */
    input_file = fopen(input_path, "rb");
    if (input_file == NULL) {
        fprintf(stderr, "Errore: Impossibile aprire il file '%s'\n", input_path);
        return 1;
    }

    /* Leggi l'header */
    if (fread(&header, sizeof(RLEHeader), 1, input_file) != 1) {
        fprintf(stderr, "Errore: Impossibile leggere l'header\n");
        fclose(input_file);
        return 1;
    }

    /* Verifica la signature */
    if (header.magic[0] != 'R' || header.magic[1] != 'L' ||
        header.magic[2] != 'E' || header.magic[3] != '\0') {
        fprintf(stderr, "Errore: Formato file non valido (non e' un file RLE)\n");
        fclose(input_file);
        return 1;
    }

    /* Alloca buffer */
    buffer = (unsigned char *)malloc(BUFFER_SIZE * 2);
    if (buffer == NULL) {
        fprintf(stderr, "Errore: Memoria insufficiente\n");
        fclose(input_file);
        return 1;
    }

    /* Apri il file di output */
    output_file = fopen(output_path, "wb");
    if (output_file == NULL) {
        fprintf(stderr, "Errore: Impossibile creare il file '%s'\n", output_path);
        free(buffer);
        fclose(input_file);
        return 1;
    }

    printf("Decompressione in corso...\n");

    /* Leggi e decomprimi il file */
    size_t decompressed_size = 0;
    size_t bytes_read;

    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE * 2, input_file)) > 0) {
        size_t i = 0;

        while (i < bytes_read) {
            if (i + 1 >= bytes_read) {
                fprintf(stderr, "Errore: File corrotto\n");
                free(buffer);
                fclose(input_file);
                fclose(output_file);
                return 1;
            }

            unsigned char count = buffer[i];
            unsigned char byte = buffer[i + 1];

            /* Scrivi il byte 'count' volte */
            for (unsigned char j = 0; j < count; j++) {
                if (fwrite(&byte, 1, 1, output_file) != 1) {
                    fprintf(stderr, "Errore: Impossibile scrivere i dati decompressi\n");
                    free(buffer);
                    fclose(input_file);
                    fclose(output_file);
                    return 1;
                }
                decompressed_size++;
            }

            i += 2;
        }
    }

    /* Cleanup */
    free(buffer);
    fclose(input_file);
    fclose(output_file);

    printf("\nDecompressione completata!\n");
    printf("Dimensione decompressa:    %lu bytes\n", (unsigned long)decompressed_size);
    printf("Dimensione originale:      %u bytes\n", header.original_size);

    if (decompressed_size != header.original_size) {
        fprintf(stderr, "Attenzione: La dimensione decompressa non corrisponde a quella originale!\n");
    }

    return 0;
}

/* Funzione principale */
int main(int argc, char *argv[]) {
    if (argc < 3) {
        print_usage(argv[0]);
        return 1;
    }

    const char *command = argv[1];
    const char *input_path = argv[2];
    char output_path[512];

    /* Genera automaticamente il nome del file di output se non specificato */
    if (argc < 4) {
        if (strcmp(command, "c") == 0 || strcmp(command, "compress") == 0) {
            snprintf(output_path, sizeof(output_path), "%s.rle", input_path);
        } else if (strcmp(command, "d") == 0 || strcmp(command, "decompress") == 0) {
            /* Rimuovi l'estensione .rle se presente */
            strncpy(output_path, input_path, sizeof(output_path) - 1);
            char *ext = strstr(output_path, ".rle");
            if (ext != NULL) {
                *ext = '\0';
            } else {
                strncat(output_path, ".dec", sizeof(output_path) - strlen(output_path) - 1);
            }
        } else {
            print_usage(argv[0]);
            return 1;
        }
    } else {
        strncpy(output_path, argv[3], sizeof(output_path) - 1);
        output_path[sizeof(output_path) - 1] = '\0';
    }

    /* Esegui il comando appropriato */
    if (strcmp(command, "h") == 0 || strcmp(command, "help") == 0) {
        print_usage(argv[0]);
        return 0;
    } else if (strcmp(command, "c") == 0 || strcmp(command, "compress") == 0) {
        return compress_file(input_path, output_path);
    } else if (strcmp(command, "d") == 0 || strcmp(command, "decompress") == 0) {
        return decompress_file(input_path, output_path);
    } else {
        fprintf(stderr, "Errore: Comando non riconosciuto '%s'\n\n", command);
        print_usage(argv[0]);
        return 1;
    }

    return 0;
}
