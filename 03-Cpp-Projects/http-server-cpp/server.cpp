#include "server.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include <algorithm>

#ifdef _WIN32
    #pragma comment(lib, "ws2_32.lib")
#endif

HTTPServer::HTTPServer(int port, const std::string& webRoot, size_t numThreads)
    : port(port), webRoot(webRoot), serverSocket(INVALID_SOCKET),
      threadPool(numThreads), running(false) {
}

HTTPServer::~HTTPServer() {
    stop();
}

bool HTTPServer::initWinsock() {
#ifdef _WIN32
    WSADATA wsaData;
    if(WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Errore WSAStartup: " << WSAGetLastError() << std::endl;
        return false;
    }
#endif
    return true;
}

bool HTTPServer::createSocket() {
    serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if(serverSocket == INVALID_SOCKET) {
        std::cerr << "Errore creazione socket" << std::endl;
        return false;
    }

    // Setta SO_REUSEADDR per evitare "Address already in use"
    int opt = 1;
#ifdef _WIN32
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif

    return true;
}

bool HTTPServer::bindSocket() {
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(port);

    if(bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Errore bind socket" << std::endl;
        return false;
    }

    return true;
}

bool HTTPServer::listenSocket() {
    if(listen(serverSocket, SOMAXCONN) == SOCKET_ERROR) {
        std::cerr << "Errore listen socket" << std::endl;
        return false;
    }
    return true;
}

void HTTPServer::acceptConnections() {
    std::cout << "Server in ascolto su http://localhost:" << port << std::endl;
    std::cout << "Web root: " << webRoot << std::endl;
    std::cout << "Premi Ctrl+C per fermare il server" << std::endl;

    while(running) {
        sockaddr_in clientAddr;
        socklen_t clientAddrLen = sizeof(clientAddr);

        socket_t clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);

        if(clientSocket == INVALID_SOCKET) {
            if(running) {
                std::cerr << "Errore accept" << std::endl;
            }
            continue;
        }

        // Decodifica indirizzo client
#ifdef _WIN32
        char clientIP[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, INET_ADDRSTRLEN);
#else
        char* clientIP = inet_ntoa(clientAddr.sin_addr);
#endif

        std::cout << "Connessione da " << clientIP << std::endl;

        // Accoda il task al thread pool
        threadPool.enqueue([this, clientSocket]() {
            this->handleClient(clientSocket);
        });
    }
}

void HTTPServer::handleClient(socket_t clientSocket) {
    char buffer[4096];
    int bytesReceived = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);

    if(bytesReceived <= 0) {
#ifdef _WIN32
        closesocket(clientSocket);
#else
        close(clientSocket);
#endif
        return;
    }

    buffer[bytesReceived] = '\0';
    std::string request(buffer);

    HttpRequest req = parseRequest(request);
    std::cout << "Thread " << std::this_thread::get_id()
              << " - " << req.method << " " << req.path << std::endl;

    // Decodifica URL
    std::string decodedPath = urlDecode(req.path);

    // Rimuovi query string se presente
    size_t queryPos = decodedPath.find('?');
    if(queryPos != std::string::npos) {
        decodedPath = decodedPath.substr(0, queryPos);
    }

    // Costruisci percorso file
    std::string filePath = webRoot + decodedPath;

    // Se e' directory, prova index.html
    if(filePath.back() == '/') {
        filePath += "index.html";
    }

    std::string response;
    std::string content;
    std::string contentType = getContentType(filePath);

    // Try to read file
    content = readFile(filePath);

    if(!content.empty()) {
        response = buildResponse(200, "OK", contentType, content);
    } else {
        // 404 - File non trovato
        std::string notFoundContent = "<html><body><h1>404 - File Non Trovato</h1><p>Il file richiesto non esiste.</p></body></html>";
        response = buildResponse(404, "Not Found", "text/html", notFoundContent);
    }

    // Invia response
    send(clientSocket, response.c_str(), response.length(), 0);

#ifdef _WIN32
    closesocket(clientSocket);
#else
    close(clientSocket);
#endif
}

HTTPServer::HttpRequest HTTPServer::parseRequest(const std::string& request) {
    HttpRequest req;
    std::istringstream iss(request);
    std::string line;

    // Prima linea: METHOD PATH VERSION
    if(std::getline(iss, line)) {
        // Rimuovi \r se presente
        if(!line.empty() && line.back() == '\r') {
            line.pop_back();
        }

        std::istringstream lineStream(line);
        lineStream >> req.method >> req.path >> req.version;
    }

    return req;
}

std::string HTTPServer::buildResponse(int statusCode, const std::string& statusText,
                                      const std::string& contentType, const std::string& content) {
    std::ostringstream response;
    response << "HTTP/1.1 " << statusCode << " " << statusText << "\r\n";
    response << "Content-Type: " << contentType << "\r\n";
    response << "Content-Length: " << content.length() << "\r\n";
    response << "Connection: close\r\n";
    response << "\r\n";
    response << content;
    return response.str();
}

std::string HTTPServer::getContentType(const std::string& path) {
    std::string ext;
    size_t dotPos = path.rfind('.');

    if(dotPos != std::string::npos) {
        ext = path.substr(dotPos + 1);
        // Converti in minuscolo
        std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
    }

    static const std::map<std::string, std::string> contentTypes = {
        {"html", "text/html"},
        {"htm", "text/html"},
        {"css", "text/css"},
        {"js", "application/javascript"},
        {"json", "application/json"},
        {"png", "image/png"},
        {"jpg", "image/jpeg"},
        {"jpeg", "image/jpeg"},
        {"gif", "image/gif"},
        {"svg", "image/svg+xml"},
        {"ico", "image/x-icon"},
        {"txt", "text/plain"},
        {"pdf", "application/pdf"},
        {"xml", "application/xml"}
    };

    auto it = contentTypes.find(ext);
    if(it != contentTypes.end()) {
        return it->second;
    }

    return "application/octet-stream";
}

std::string HTTPServer::readFile(const std::string& filePath) {
    std::ifstream file(filePath, std::ios::binary);

    if(!file.is_open()) {
        return "";
    }

    // Ottieni dimensione file
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    // Leggi contenuto
    std::string content;
    content.resize(fileSize);
    file.read(&content[0], fileSize);

    if(!file) {
        return "";
    }

    return content;
}

std::string HTTPServer::urlDecode(const std::string& encoded) {
    std::string decoded;
    decoded.reserve(encoded.length());

    for(size_t i = 0; i < encoded.length(); ++i) {
        if(encoded[i] == '%' && i + 2 < encoded.length()) {
            // Convert hex
            std::string hexStr = encoded.substr(i + 1, 2);
            char c = static_cast<char>(std::strtol(hexStr.c_str(), nullptr, 16));
            decoded += c;
            i += 2;
        } else if(encoded[i] == '+') {
            decoded += ' ';
        } else {
            decoded += encoded[i];
        }
    }

    return decoded;
}

bool HTTPServer::start() {
    if(!initWinsock()) {
        return false;
    }

    if(!createSocket()) {
        return false;
    }

    if(!bindSocket()) {
        return false;
    }

    if(!listenSocket()) {
        return false;
    }

    running = true;
    acceptConnections();

    return true;
}

void HTTPServer::stop() {
    running = false;

    if(serverSocket != INVALID_SOCKET) {
#ifdef _WIN32
        closesocket(serverSocket);
        WSACleanup();
#else
        close(serverSocket);
#endif
        serverSocket = INVALID_SOCKET;
    }
}
