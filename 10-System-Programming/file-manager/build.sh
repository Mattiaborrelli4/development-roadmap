#!/bin/bash

# =============================================
# Script di Compilazione per File Manager
# =============================================

echo "╔══════════════════════════════════════════════╗"
echo "║     File Manager - Script di Compilazione    ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Verifica se gcc è installato
if ! command -v gcc &> /dev/null; then
    echo "❌ Errore: gcc non è installato"
    echo "Installa con: sudo apt-get install build-essential"
    exit 1
fi

echo "✓ Trovato gcc: $(gcc --version | head -n1)"
echo ""

# Compila il programma
echo "🔨 Compilazione in corso..."
gcc -Wall -Wextra -std=c99 -pedantic file_manager.c -o file_manager

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║       ✓ Compilazione Completata!           ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""
    echo "Per eseguire il programma:"
    echo "  ./file_manager"
    echo ""
    echo "Oppure usa Make:"
    echo "  make run"
    echo ""

    # Chiede se eseguire
    read -p "Vuoi eseguire il programma ora? (s/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        ./file_manager
    fi
else
    echo ""
    echo "❌ Compilazione fallita"
    echo "Controlla gli errori sopra riportati"
    exit 1
fi
