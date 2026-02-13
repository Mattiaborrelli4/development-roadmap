#!/bin/bash
# Script di esecuzione per File Organizer (NO external dependencies)

echo "========================================"
echo "  Java File Organizer - Starting..."
echo "========================================"
echo ""

# Verifica che sia stato compilato
if [ ! -f "out/com/organizer/FileOrganizer.class" ]; then
    echo "ERRORE: Il progetto non e' stato compilato."
    echo "Esegui prima: ./build-simple.sh"
    exit 1
fi

# Esegui
echo "Avvio monitoraggio Downloads..."
echo "Premi CTRL+C per terminare."
echo ""

java -cp out com.organizer.FileOrganizer "$1" "$2"
