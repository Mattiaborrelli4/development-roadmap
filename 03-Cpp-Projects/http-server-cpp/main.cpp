#include "server.h"
#include <iostream>
#include <csignal>
#include <cstring>

// Global server pointer per signal handler
HTTPServer* g_server = nullptr;

void signalHandler(int signal) {
    std::cout << "\n\nRicevuto segnale di arresto. Chiusura server..." << std::endl;
    if(g_server) {
        g_server->stop();
    }
    exit(0);
}

int main(int argc, char* argv[]) {
    // Configurazione default
    int port = 8080;
    std::string webRoot = "./public";
    size_t numThreads = 4;

    // Parse command line arguments
    for(int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if(arg == "--port" && i + 1 < argc) {
            port = std::atoi(argv[++i]);
        } else if(arg == "--root" && i + 1 < argc) {
            webRoot = argv[++i];
        } else if(arg == "--threads" && i + 1 < argc) {
            numThreads = std::stoul(argv[++i]);
        } else if(arg == "--help" || arg == "-h") {
            std::cout << "Usage: " << argv[0] << " [options]\n"
                      << "Options:\n"
                      << "  --port <port>      Porta del server (default: 8080)\n"
                      << "  --root <path>      Web root directory (default: ./public)\n"
                      << "  --threads <num>    Numero di thread worker (default: 4)\n"
                      << "  --help, -h         Mostra questo help\n";
            return 0;
        }
    }

    // Setup signal handlers
    std::signal(SIGINT, signalHandler);
    std::signal(SIGTERM, signalHandler);

    // Crea e avvia server
    HTTPServer server(port, webRoot, numThreads);
    g_server = &server;

    std::cout << "========================================\n";
    std::cout << "   HTTP Server C++ - Multi-threaded\n";
    std::cout << "========================================\n";
    std::cout << "Configurazione:\n";
    std::cout << "  - Porta: " << port << "\n";
    std::cout << "  - Web Root: " << webRoot << "\n";
    std::cout << "  - Thread Pool: " << numThreads << " worker threads\n";
    std::cout << "========================================\n\n";

    if(!server.start()) {
        std::cerr << "Errore avvio server!" << std::endl;
        return 1;
    }

    return 0;
}
