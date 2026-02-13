#!/bin/bash
#
# Demo Script per Mini Shell
# Esegue una serie di comandi per dimostrare le funzionalità

echo "================================"
echo "  Mini Shell - Demo Script"
echo "================================"
echo ""

# Verifica che la shell sia compilata
if [ ! -f "./mini-shell" ] && [ ! -f "./mini-shell.exe" ]; then
    echo "Errore: mini-shell non trovato."
    echo "Compila prima con: make"
    exit 1
fi

echo "Avvio demo con i seguenti comandi:"
echo "  1. pwd      - Mostra directory corrente"
echo "  2. ls       - Lista file"
echo "  3. echo     - Stampa messaggio"
echo "  4. cd ..    - Cambia directory"
echo "  5. history  - Mostra cronologia"
echo "  6. help     - Mostra aiuto"
echo "  7. exit     - Esce"
echo ""

# Esegui la shell con comandi predefiniti
if [ -f "./mini-shell" ]; then
    # Linux/Unix
    ./mini-shell <<EOF
pwd
ls
echo "Ciao dalla Mini Shell!"
echo ""
cd /tmp
pwd
cd -
history
help
exit
EOF
elif [ -f "./mini-shell.exe" ]; then
    # Windows
    ./mini-shell.exe <<EOF
pwd
ls
echo "Ciao dalla Mini Shell!"
echo ""
cd /tmp
pwd
cd -
history
help
exit
EOF
fi

echo ""
echo "================================"
echo "  Demo completata!"
echo "================================"
