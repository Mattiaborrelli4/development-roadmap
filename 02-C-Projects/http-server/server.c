/*
 * HTTP Server in C
 * Server HTTP multi-threaded con supporto per file statici
 * Compatibile con Windows (Winsock2) e Linux (BSD sockets)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* Cross-platform socket headers */
#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #ifndef _MSC_VER
        #pragma comment(lib, "ws2_32.lib")
    #endif
    #define close closesocket
    typedef int socklen_t;
#else
    #include <sys/socket.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <arpa/inet.h>
    #include <netinet/in.h>
    #include <unistd.h>
    #include <pthread.h>
    #define INVALID_SOCKET -1
    #define SOCKET_ERROR -1
    typedef int SOCKET;
#endif

/* Configurazioni */
#define PORT 8080
#define BUFFER_SIZE 8192
#ifndef MAX_PATH
    #define MAX_PATH 256
#endif
#define PUBLIC_DIR "./public"

/* Struttura per passare dati ai thread */
typedef struct {
    SOCKET client_socket;
    struct sockaddr_in client_addr;
} client_data_t;

/* Funzioni di utilità */
const char* get_content_type(const char* path);
void send_response(SOCKET socket, int status_code, const char* status_text,
                   const char* content_type, const char* body, size_t body_length);
void handle_client(SOCKET client_socket);
void serve_file(SOCKET client_socket, const char* filepath);
void* client_thread(void* arg);

/*
 * Ottieni il Content-Type appropriato basato sull'estensione del file
 */
const char* get_content_type(const char* path) {
    const char* ext = strrchr(path, '.');
    if (ext == NULL) {
        return "application/octet-stream";
    }

    if (strcmp(ext, ".html") == 0 || strcmp(ext, ".htm") == 0) {
        return "text/html";
    } else if (strcmp(ext, ".css") == 0) {
        return "text/css";
    } else if (strcmp(ext, ".js") == 0) {
        return "application/javascript";
    } else if (strcmp(ext, ".jpg") == 0 || strcmp(ext, ".jpeg") == 0) {
        return "image/jpeg";
    } else if (strcmp(ext, ".png") == 0) {
        return "image/png";
    } else if (strcmp(ext, ".gif") == 0) {
        return "image/gif";
    } else if (strcmp(ext, ".svg") == 0) {
        return "image/svg+xml";
    } else if (strcmp(ext, ".json") == 0) {
        return "application/json";
    } else if (strcmp(ext, ".txt") == 0) {
        return "text/plain";
    } else if (strcmp(ext, ".pdf") == 0) {
        return "application/pdf";
    } else if (strcmp(ext, ".ico") == 0) {
        return "image/x-icon";
    } else if (strcmp(ext, ".woff") == 0) {
        return "font/woff";
    } else if (strcmp(ext, ".woff2") == 0) {
        return "font/woff2";
    } else if (strcmp(ext, ".ttf") == 0) {
        return "font/ttf";
    }

    return "application/octet-stream";
}

/*
 * Invia una risposta HTTP completa
 */
void send_response(SOCKET socket, int status_code, const char* status_text,
                   const char* content_type, const char* body, size_t body_length) {
    char header[BUFFER_SIZE];
    int header_len;

    /* Costruisci l'header HTTP */
    header_len = snprintf(header, sizeof(header),
        "HTTP/1.1 %d %s\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %llu\r\n"
        "Connection: close\r\n"
        "Server: C-HTTP-Server/1.0\r\n"
        "\r\n",
        status_code, status_text, content_type, (unsigned long long)body_length);

    /* Invia l'header */
    if (send(socket, header, header_len, 0) == SOCKET_ERROR) {
        fprintf(stderr, "Errore nell'invio dell'header\n");
        return;
    }

    /* Invia il body se presente */
    if (body != NULL && body_length > 0) {
        if (send(socket, body, body_length, 0) == SOCKET_ERROR) {
            fprintf(stderr, "Errore nell'invio del body\n");
        }
    }
}

/*
 * Leggi e servi un file statico
 */
void serve_file(SOCKET client_socket, const char* filepath) {
    FILE* file;
    char* content;
    long file_size;
    size_t bytes_read;
    const char* content_type;
    size_t file_size_t;

    /* Apri il file in modalità binaria */
    file = fopen(filepath, "rb");
    if (file == NULL) {
        /* File non trovato - 404 */
        char* not_found_body = "<!DOCTYPE html>\n"
            "<html>\n<head><title>404 Non Trovato</title></head>\n"
            "<body>\n"
            "<h1>404 - File Non Trovato</h1>\n"
            "<p>Il file richiesto non esiste su questo server.</p>\n"
            "</body>\n</html>";
        send_response(client_socket, 404, "Not Found", "text/html",
                     not_found_body, strlen(not_found_body));
        return;
    }

    /* Ottieni la dimensione del file */
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    /* Converti a size_t per il confronto */
    file_size_t = (size_t)file_size;

    /* Alloca memoria per il contenuto */
    content = (char*)malloc(file_size_t + 1);
    if (content == NULL) {
        fclose(file);
        char* error_body = "<!DOCTYPE html>\n"
            "<html>\n<head><title>500 Errore Interno</title></head>\n"
            "<body>\n"
            "<h1>500 - Errore Interno del Server</h1>\n"
            "<p>Errore di allocazione memoria.</p>\n"
            "</body>\n</html>";
        send_response(client_socket, 500, "Internal Server Error", "text/html",
                     error_body, strlen(error_body));
        return;
    }

    /* Leggi il file */
    bytes_read = fread(content, 1, file_size_t, file);
    fclose(file);

    if (bytes_read != file_size_t) {
        free(content);
        char* error_body = "<!DOCTYPE html>\n"
            "<html>\n<head><title>500 Errore di Lettura</title></head>\n"
            "<body>\n"
            "<h1>500 - Errore di Lettura</h1>\n"
            "<p>Impossibile leggere il file completamente.</p>\n"
            "</body>\n</html>";
        send_response(client_socket, 500, "Internal Server Error", "text/html",
                     error_body, strlen(error_body));
        return;
    }

    /* Ottieni il Content-Type */
    content_type = get_content_type(filepath);

    /* Invia il file */
    send_response(client_socket, 200, "OK", content_type, content, file_size_t);

    free(content);
}

/*
 * Gestisci una richiesta client
 */
void handle_client(SOCKET client_socket) {
    char buffer[BUFFER_SIZE];
    char method[16] = {0};
    char path[MAX_PATH] = {0};
    char version[16] = {0};
    char filepath[MAX_PATH + 64];
    int bytes_received;
    char* token;

    /* Ricevi la richiesta */
    bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received <= 0) {
        close(client_socket);
        return;
    }

    buffer[bytes_received] = '\0';

    /* Log della richiesta */
    printf("Richiesta ricevuta:\n%s\n", buffer);

    /* Parsifica la request line: METHOD PATH VERSION */
    token = strtok(buffer, " \r\n");
    if (token == NULL) {
        close(client_socket);
        return;
    }
    strncpy(method, token, sizeof(method) - 1);

    token = strtok(NULL, " \r\n");
    if (token == NULL) {
        close(client_socket);
        return;
    }
    strncpy(path, token, sizeof(path) - 1);

    token = strtok(NULL, " \r\n");
    if (token != NULL) {
        strncpy(version, token, sizeof(version) - 1);
    }

    /* Gestisci solo GET */
    if (strcmp(method, "GET") != 0) {
        char* not_allowed_body = "<!DOCTYPE html>\n"
            "<html>\n<head><title>405 Metodo Non Consentito</title></head>\n"
            "<body>\n"
            "<h1>405 - Metodo Non Consentito</h1>\n"
            "<p>Solo il metodo GET è supportato.</p>\n"
            "</body>\n</html>";
        send_response(client_socket, 405, "Method Not Allowed", "text/html",
                     not_allowed_body, strlen(not_allowed_body));
        close(client_socket);
        return;
    }

    /* Convertisci il path URL in un path filesystem */
    /* Se è la root, servi index.html */
    if (strcmp(path, "/") == 0) {
        snprintf(filepath, sizeof(filepath), "%s/index.html", PUBLIC_DIR);
    } else {
        /* Rimuovi eventuali query parameters */
        char* query = strchr(path, '?');
        if (query != NULL) {
            *query = '\0';
        }

        /* Sanitizza il path per evitare directory traversal */
        /* Rimuovi eventuali ../ */
        char* sanitized = path;
        while ((sanitized = strstr(sanitized, "..")) != NULL) {
            *sanitized = '_';
            *(sanitized + 1) = '_';
        }

        snprintf(filepath, sizeof(filepath), "%s%s", PUBLIC_DIR, path);
    }

    /* Servi il file */
    serve_file(client_socket, filepath);

    /* Chiudi la connessione */
    close(client_socket);
}

/*
 * Thread wrapper per gestire i client (Linux/Unix)
 */
#ifdef __linux__
void* client_thread(void* arg) {
    client_data_t* data = (client_data_t*)arg;
    SOCKET client_socket = data->client_socket;
    struct sockaddr_in client_addr = data->client_addr;

    printf("Nuova connessione da %s:%d\n",
           inet_ntoa(client_addr.sin_addr),
           ntohs(client_addr.sin_port));

    free(data);

    handle_client(client_socket);

    printf("Connessione chiusa\n");

    return NULL;
}
#endif

/*
 * Wrapper Windows per i thread
 */
#ifdef _WIN32
DWORD WINAPI client_thread_win(LPVOID arg) {
    client_data_t* data = (client_data_t*)arg;
    SOCKET client_socket = data->client_socket;
    struct sockaddr_in client_addr = data->client_addr;

    printf("Nuova connessione da %s:%d\n",
           inet_ntoa(client_addr.sin_addr),
           ntohs(client_addr.sin_port));

    free(data);

    handle_client(client_socket);

    printf("Connessione chiusa\n");

    return 0;
}
#endif

/*
 * Funzione principale
 */
int main(int argc, char* argv[]) {
    SOCKET server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    int port = PORT;
    int opt = 1;

#ifdef _WIN32
    WSADATA wsa_data;
#endif

    /* Parse opzionale della porta da riga di comando */
    if (argc > 1) {
        port = atoi(argv[1]);
        if (port <= 0 || port > 65535) {
            fprintf(stderr, "Porta non valida. Uso porta 8080.\n");
            port = PORT;
        }
    }

#ifdef _WIN32
    /* Inizializza Winsock */
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        fprintf(stderr, "Errore nell'inizializzazione di Winsock\n");
        return 1;
    }
#endif

    /* Crea il socket */
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == INVALID_SOCKET) {
        fprintf(stderr, "Errore nella creazione del socket\n");
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    /* Imposta opzioni socket (riuso indirizzo) */
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR,
                   (const char*)&opt, sizeof(opt)) == SOCKET_ERROR) {
        fprintf(stderr, "Errore in setsockopt\n");
        close(server_socket);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    /* Configura l'indirizzo del server */
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    /* Bind */
    if (bind(server_socket, (struct sockaddr*)&server_addr,
             sizeof(server_addr)) == SOCKET_ERROR) {
        fprintf(stderr, "Errore nel bind. La porta %d potrebbe essere in uso.\n", port);
        close(server_socket);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    /* Listen */
    if (listen(server_socket, 10) == SOCKET_ERROR) {
        fprintf(stderr, "Errore in listen\n");
        close(server_socket);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    printf("========================================\n");
    printf("  Server HTTP in C\n");
    printf("========================================\n");
    printf("Porta: %d\n", port);
    printf("Directory: %s\n", PUBLIC_DIR);
    printf("Server URL: http://localhost:%d\n", port);
    printf("========================================\n");
    printf("Premi Ctrl+C per terminare\n\n");

    /* Loop principale di accettazione */
    while (1) {
        /* Accetta una nuova connessione */
        client_socket = accept(server_socket, (struct sockaddr*)&client_addr,
                              &client_len);
        if (client_socket == INVALID_SOCKET) {
            fprintf(stderr, "Errore in accept\n");
            continue;
        }

        /* Alloca dati per il thread */
        client_data_t* data = (client_data_t*)malloc(sizeof(client_data_t));
        if (data == NULL) {
            fprintf(stderr, "Errore di allocazione memoria\n");
            close(client_socket);
            continue;
        }

        data->client_socket = client_socket;
        data->client_addr = client_addr;

        /* Crea un thread per gestire il client */
#ifdef _WIN32
        HANDLE thread = CreateThread(NULL, 0, client_thread_win, data, 0, NULL);
        if (thread == NULL) {
            fprintf(stderr, "Errore nella creazione del thread\n");
            free(data);
            close(client_socket);
        } else {
            CloseHandle(thread);
        }
#else
        pthread_t thread_id;
        if (pthread_create(&thread_id, NULL, client_thread, data) != 0) {
            fprintf(stderr, "Errore nella creazione del thread\n");
            free(data);
            close(client_socket);
        } else {
            pthread_detach(thread_id);
        }
#endif
    }

    /* Cleanup */
    close(server_socket);
#ifdef _WIN32
    WSACleanup();
#endif

    return 0;
}
