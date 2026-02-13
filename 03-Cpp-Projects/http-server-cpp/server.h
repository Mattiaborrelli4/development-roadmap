#ifndef SERVER_H
#define SERVER_H

#include <string>
#include <map>

#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    typedef int socklen_t;
    typedef SOCKET socket_t;
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <sys/types.h>
    #define INVALID_SOCKET -1
    #define SOCKET_ERROR -1
    typedef int socket_t;
#endif

#include "thread_pool.h"

class HTTPServer {
public:
    HTTPServer(int port, const std::string& webRoot, size_t numThreads = 4);
    ~HTTPServer();

    bool start();
    void stop();

private:
    int port;
    std::string webRoot;
    socket_t serverSocket;
    ThreadPool threadPool;
    bool running;

    // Inizializza Winsock per Windows
    bool initWinsock();

    // Crea il server socket
    bool createSocket();

    // Bind del socket alla porta
    bool bindSocket();

    // Metti il socket in ascolto
    bool listenSocket();

    // Accetta connessioni
    void acceptConnections();

    // Gestisce una singola connessione client
    void handleClient(socket_t clientSocket);

    // Parse HTTP request
    struct HttpRequest {
        std::string method;
        std::string path;
        std::string version;
    };
    HttpRequest parseRequest(const std::string& request);

    // Genera HTTP response
    std::string buildResponse(int statusCode, const std::string& statusText,
                             const std::string& contentType, const std::string& content);

    // Ottieni Content-Type basato sull'estensione del file
    std::string getContentType(const std::string& path);

    // Leggi file dal disco
    std::string readFile(const std::string& filePath);

    // URL decode
    std::string urlDecode(const std::string& encoded);
};

#endif // SERVER_H
