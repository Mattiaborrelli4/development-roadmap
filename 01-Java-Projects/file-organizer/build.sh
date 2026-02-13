#!/bin/bash
# Script di compilazione per File Organizer (Linux/Mac)

echo "========================================"
echo "  Java File Organizer - Build Script"
echo "========================================"
echo

# Verifica Java
echo "[1/5] Verifica installazione Java..."
if ! command -v java &> /dev/null; then
    echo "ERRORE: Java non trovato. Installa JDK 11+"
    exit 1
fi
echo "      Java installato correttamente."
echo

# Verifica Gson
echo "[2/5] Verifica libreria Gson..."
if ! ls lib/gson-*.jar 1> /dev/null 2>&1; then
    echo "ATTENZIONE: Gson JAR non trovato in lib/"
    echo
    echo "Scarica Gson da: https://github.com/google/gson/releases"
    echo "Metti il file JAR nella cartella lib/"
    exit 1
fi
echo "      Gson trovato."
echo

# Crea directory out
echo "[3/5] Preparazione directory..."
mkdir -p out
echo "      Directory out/ creata."
echo

# Compila
echo "[4/5] Compilazione..."
javac -cp "lib/*" -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
if [ $? -ne 0 ]; then
    echo "ERRORE: Compilazione fallita."
    exit 1
fi
echo "      Compilazione completata con successo."
echo

# Copia config.json
echo "[5/5] Copia file di configurazione..."
cp src/main/resources/config.json out/
echo "      config.json copiato in out/."
echo

echo "========================================"
echo "  BUILD COMPLETATO!"
echo "========================================"
echo
echo "Per eseguire:"
echo "  ./run.sh"
echo
echo "Oppure manualmente:"
echo "  java -cp \"out:lib/*\" com.organizer.FileOrganizer"
echo
