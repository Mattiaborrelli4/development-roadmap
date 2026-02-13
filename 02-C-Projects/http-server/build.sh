#!/bin/bash
# Script di build per Linux/Unix

echo "========================================"
echo "  HTTP Server - Build Script (Linux)"
echo "========================================"
echo ""

# Verifica che gcc sia installato
if ! command -v gcc &> /dev/null; then
    echo "ERRORE: GCC non trovato!"
    echo ""
    echo "Installa gcc con:"
    echo "  Ubuntu/Debian: sudo apt-get install build-essential"
    echo "  Fedora/RHEL:   sudo dnf install gcc"
    echo "  Arch Linux:    sudo pacman -S base-devel"
    echo ""
    exit 1
fi

# Crea la cartella public se non esiste
if [ ! -d "public" ]; then
    echo "Creazione cartella public..."
    mkdir -p public
fi

echo "Compilazione in corso..."
echo ""

# Compila
gcc -Wall -Wextra -O2 -pthread server.c -o server -pthread

if [ $? -ne 0 ]; then
    echo ""
    echo "ERRORE: Compilazione fallita!"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "  Compilazione Completata!"
echo "========================================"
echo ""
echo "Eseguibile creato: server"
echo ""
echo "Per avviare il server:"
echo "  ./server"
echo ""
echo "Con porta personalizzata:"
echo "  ./server 3000"
echo ""
echo "========================================"
