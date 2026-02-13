#!/bin/bash
# Script di compilazione per File Organizer (NO external dependencies)
# Questo script compila il progetto senza richiedere librerie esterne

echo "========================================"
echo "  Java File Organizer - Build Script"
echo "  (No External Dependencies Version)"
echo "========================================"
echo ""

# Verifica Java
echo "[1/4] Verifica installazione Java..."
if ! command -v java &> /dev/null; then
    echo "ERRORE: Java non trovato. Installa JDK 11+"
    exit 1
fi
echo "      Java installato correttamente."
echo ""

# Crea directory out
echo "[2/4] Preparazione directory..."
mkdir -p out
echo "      Directory out/ creata."
echo ""

# Compila
echo "[3/4] Compilazione..."
javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
if [ $? -ne 0 ]; then
    echo "ERRORE: Compilazione fallita."
    exit 1
fi
echo "      Compilazione completata con successo."
echo ""

# Crea config di default se non esiste
echo "[4/4] Verifica configurazione..."
if [ ! -f "out/config.properties" ]; then
    echo "      Creazione config.properties di default..."
    if [ -f "src/main/resources/config.properties" ]; then
        cp src/main/resources/config.properties out/
    else
        echo "      ATTENZIONE: config.properties non trovato in src/main/resources/"
        echo "      Verra' creato al primo avvio."
    fi
else
    echo "      config.properties gia' presente."
fi
echo ""

echo "========================================"
echo "  BUILD COMPLETATO!"
echo "========================================"
echo ""
echo "Per eseguire:"
echo "  ./run-simple.sh"
echo ""
echo "Oppure manualmente:"
echo "  java -cp out com.organizer.FileOrganizer"
echo ""
