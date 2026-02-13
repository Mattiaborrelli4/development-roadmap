#!/bin/bash
# Script per compilare ed eseguire TodoListApp
# Uso: chmod +x run.sh && ./run.sh

echo "=========================================="
echo "  TodoListApp - Compilazione ed Esecuzione"
echo "=========================================="
echo ""

# Verifica se Java è installato
if ! command -v java &> /dev/null; then
    echo "[ERRORE] Java non è installato o non è nel PATH"
    echo "Installa Java JDK:"
    echo "  Ubuntu/Debian: sudo apt install default-jdk"
    echo "  macOS: brew install openjdk"
    exit 1
fi

echo "[1/3] Pulitura file compilati precedenti..."
rm -f TodoListApp.class

echo ""
echo "[2/3] Compilazione di TodoListApp.java..."
javac TodoListApp.java

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERRORE] Compilazione fallita! Controlla gli errori sopra."
    exit 1
fi

echo ""
echo "[OK] Compilazione completata con successo!"
echo ""
echo "[3/3] Avvio dell'applicazione..."
echo "=========================================="
echo ""

java TodoListApp

echo ""
echo "=========================================="
echo "Applicazione terminata."
echo "=========================================="
