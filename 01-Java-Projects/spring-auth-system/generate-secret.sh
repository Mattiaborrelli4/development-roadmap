#!/bin/bash
# Script per generare una chiave segreta JWT codificata in Base64

echo "Generazione chiave segreta JWT..."
echo ""

# Genera una stringa casuale
SECRET=$(openssl rand -base64 64)

echo "Chiave segreta generata (Base64):"
echo $SECRET
echo ""

# Per application.properties
echo "Copia questa riga in application.properties:"
echo "jwt.secret=$SECRET"
