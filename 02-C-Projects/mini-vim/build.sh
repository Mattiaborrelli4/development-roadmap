#!/bin/bash
# Mini Vim - Script di compilazione per Linux/Unix

echo "===================================="
echo "Mini Vim - Compilazione Linux/Unix"
echo "===================================="
echo ""

# Verifica se GCC è installato
if ! command -v gcc &> /dev/null; then
    echo "ERRORE: GCC non trovato!"
    echo ""
    echo "Per compilare mini-vim, devi installare GCC:"
    echo "  Ubuntu/Debian: sudo apt-get install build-essential"
    echo "  Fedora/RHEL:   sudo dnf install gcc"
    echo "  Arch Linux:    sudo pacman -S base-devel"
    echo ""
    exit 1
fi

echo "Compilazione in corso..."
echo ""

gcc -Wall -Wextra -std=c99 -pedantic -c buffer.c -o buffer.o
if [ $? -ne 0 ]; then
    echo "ERRORE durante la compilazione di buffer.c"
    exit 1
fi

gcc -Wall -Wextra -std=c99 -pedantic -c editor.c -o editor.o
if [ $? -ne 0 ]; then
    echo "ERRORE durante la compilazione di editor.c"
    exit 1
fi

gcc buffer.o editor.o -o mini-vim
if [ $? -ne 0 ]; then
    echo "ERRORE durante il linking"
    exit 1
fi

echo ""
echo "===================================="
echo "Build completata con successo!"
echo "===================================="
echo ""
echo "Eseguibile: mini-vim"
echo ""
echo "Per eseguire:"
echo "  ./mini-vim"
echo "  ./mini-vim nomefile.txt"
echo ""
echo "Per rendere eseguibile:"
echo "  chmod +x mini-vim"
echo ""
echo "Per installare nel sistema:"
echo "  sudo cp mini-vim /usr/local/bin/"
echo ""
