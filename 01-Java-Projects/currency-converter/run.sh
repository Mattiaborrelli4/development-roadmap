#!/bin/bash

# Script per avviare il Currency Converter

echo "===================================="
echo "Currency Converter - Avvio..."
echo "===================================="
echo ""

# Controlla se Maven è installato
if ! command -v mvn &> /dev/null; then
    echo "ERRORE: Maven non trovato!"
    echo "Assicurati di avere Maven installato e nel PATH"
    exit 1
fi

# Controlla se Java è installato
if ! command -v java &> /dev/null; then
    echo "ERRORE: Java non trovato!"
    echo "Assicurati di avere Java 17+ installato e nel PATH"
    exit 1
fi

echo "Avvio applicazione..."
echo ""

# Avvia l'applicazione con Maven
mvn clean javafx:run

echo ""
echo "===================================="
echo "Applicazione chiusa"
echo "===================================="
