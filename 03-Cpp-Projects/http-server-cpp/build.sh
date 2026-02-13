#!/bin/bash
# Script di compilazione per Linux/GCC

echo "========================================"
echo "  HTTP Server C++ - Build Script"
echo "========================================"
echo ""

# Verifica se g++ è disponibile
if ! command -v g++ &> /dev/null; then
    echo "ERRORE: g++ non trovato!"
    echo "Installare con: sudo apt install build-essential"
    exit 1
fi

echo "Compilazione con g++..."
g++ -std=c++17 -pthread -o server server.cpp thread_pool.cpp main.cpp -Wall -Wextra

if [ $? -ne 0 ]; then
    echo ""
    echo "ERRORE: Compilazione fallita!"
    exit 1
fi

echo ""
echo "========================================"
echo "  Compilazione completata con successo!"
echo "========================================"
echo ""
echo "Esecuzione: ./server"
echo ""
echo "Opzioni disponibili:"
echo "  --port 8080         Porta del server (default: 8080)"
echo "  --root ./public     Web root directory"
echo "  --threads 4         Numero worker threads"
echo "  --help              Mostra help"
echo ""
