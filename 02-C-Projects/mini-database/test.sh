#!/bin/bash

# Test Script per Mini Database Engine

echo "=========================================="
echo "  Mini Database Engine - Test Automatico"
echo "=========================================="
echo ""

DB_EXECUTABLE="./minidb"
TEST_DB="test.db"
TEST_INPUT="test_input.txt"
TEST_OUTPUT="test_output.txt"

# Verifica esistenza eseguibile
if [ ! -f "$DB_EXECUTABLE" ]; then
    echo "ERRORE: $DB_EXECUTABLE non trovato!"
    echo "Esegui prima 'make' per compilare"
    exit 1
fi

# Pulisci test precedenti
rm -f "$TEST_DB" "$TEST_INPUT" "$TEST_OUTPUT"

# Crea input di test
cat > "$TEST_INPUT" << 'EOF'
SET nome "Mario Rossi"
SET eta 30
SET citta Roma
SET professione Sviluppatore
LIST
GET nome
GET eta
DELETE citta
LIST
SAVE test.db
EXIT
EOF

echo "Esecuzione test..."
echo ""

# Esegui con l'input di test
"$DB_EXECUTABLE" "$TEST_DB" < "$TEST_INPUT" > "$TEST_OUTPUT" 2>&1

# Verifica risultati
echo "Verifica risultati..."

# Controlla se il file database esiste
if [ -f "$TEST_DB" ]; then
    echo "✓ File database creato con successo"
else
    echo "✗ ERRORE: File database non creato"
    exit 1
fi

# Controlla se l'output contiene i comandi eseguiti
if grep -q "Mario Rossi" "$TEST_OUTPUT"; then
    echo "✓ Comando SET eseguito correttamente"
else
    echo "✗ ERRORE: Comando SET fallito"
fi

if grep -q "record" "$TEST_OUTPUT"; then
    echo "✓ Comando LIST eseguito correttamente"
else
    echo "✗ ERRORE: Comando LIST fallito"
fi

if grep -q "salvataggio" "$TEST_OUTPUT"; then
    echo "✓ Comando SAVE eseguito correttamente"
else
    echo "✗ ERRORE: Comando SAVE fallito"
fi

echo ""
echo "=========================================="
echo "  Test completati!"
echo "=========================================="
echo ""
echo "File generati:"
ls -lh "$TEST_DB" "$TEST_OUTPUT" 2>/dev/null
echo ""

# Opzionale: mostra l'output
echo "Output del test:"
echo "----------------"
cat "$TEST_OUTPUT"
echo ""

# Pulizia
read -p "Pulire i file di test? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    rm -f "$TEST_DB" "$TEST_INPUT" "$TEST_OUTPUT"
    echo "File di test rimossi"
fi

echo "Test completati!"
