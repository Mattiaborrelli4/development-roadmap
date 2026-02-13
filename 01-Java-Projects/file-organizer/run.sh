#!/bin/bash
# Script di esecuzione per File Organizer (Linux/Mac)

echo "========================================"
echo "  Java File Organizer"
echo "========================================"
echo

# Verifica se il progetto e' compilato
if [ ! -f "out/com/organizer/FileOrganizer.class" ]; then
    echo "ERRORE: Progetto non compilato."
    echo "Esegui prima: ./build.sh"
    exit 1
fi

# Verifica config.json
if [ ! -f "out/config.json" ]; then
    echo "ATTENZIONE: config.json non trovato in out/"
    echo "Copia da src/main/resources/..."
    cp src/main/resources/config.json out/
fi

# Esegui con argomenti se forniti, altrimenti usa default
if [ -z "$1" ]; then
    echo
    echo "Monitoraggio cartella Downloads..."
    echo
    java -cp "out:lib/*" com.organizer.FileOrganizer
else
    echo
    echo "Monitoraggio cartella: $1"
    echo
    if [ -z "$2" ]; then
        java -cp "out:lib/*" com.organizer.FileOrganizer "$1"
    else
        java -cp "out:lib/*" com.organizer.FileOrganizer "$1" "$2"
    fi
fi

echo
echo "========================================"
echo "  Organizer terminato"
echo "========================================"
echo
