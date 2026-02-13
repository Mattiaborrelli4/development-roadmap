#!/bin/bash
# ============================================================================
-- SETUP SCRIPT - Financial Transactions Database
-- ============================================================================

echo "============================================"
echo "Financial Transactions Database Setup"
echo "============================================"
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica PostgreSQL
if ! command -v psql &> /dev/null
then
    echo -e "${RED}Errore: PostgreSQL non trovato${NC}"
    echo "Installa PostgreSQL prima di eseguire questo script"
    exit 1
fi

echo -e "${GREEN}✓${NC} PostgreSQL trovato"

# Nome database
DB_NAME="financial_transactions"

echo ""
echo "Creazione database '$DB_NAME'..."

# Crea database
psql -U postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
psql -U postgres -c "CREATE DATABASE $DB_NAME;"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Database creato con successo"
else
    echo -e "${RED}✗${NC} Errore nella creazione del database"
    exit 1
fi

echo ""
echo "Esecuzione schema.sql..."
psql -U postgres -d $DB_NAME -f schema.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Schema creato con successo"
else
    echo -e "${RED}✗${NC} Errore nella creazione dello schema"
    exit 1
fi

echo ""
echo "Esecuzione sample_data.sql..."
psql -U postgres -d $DB_NAME -f sample_data.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Dati campione inseriti"
else
    echo -e "${RED}✗${NC} Errore nell''inserimento dei dati"
    exit 1
fi

echo ""
echo "Esecuzione procedures.sql..."
psql -U postgres -d $DB_NAME -f procedures.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Stored procedure create"
else
    echo -e "${YELLOW}⚠${NC} Avviso: Alcune procedure potrebbero non essere state create"
fi

echo ""
echo "============================================"
echo -e "${GREEN}INSTALLAZIONE COMPLETATA!${NC}"
echo "============================================"
echo ""
echo "Connessione al database:"
echo -e "  ${YELLOW}psql -U postgres -d $DB_NAME${NC}"
echo ""
echo "File disponibili:"
echo "  - schema.sql       : Struttura database"
echo "  - sample_data.sql  : Dati campione"
echo "  - procedures.sql   : Stored procedures"
echo "  - queries.sql      : Query di reporting"
echo "  - transactions.sql : Esempi transazioni"
echo "  - concurrency.sql  : Esempi concorrenza"
echo "  - README.md        : Documentazione completa"
echo ""
echo "Quick test:"
psql -U postgres -d $DB_NAME -c "
SELECT
    'Clienti' AS tipo, COUNT(*) AS totale FROM customers
UNION ALL
SELECT 'Conti', COUNT(*) FROM accounts
UNION ALL
SELECT 'Transazioni', COUNT(*) FROM transactions
UNION ALL
SELECT 'Tipi Transazione', COUNT(*) FROM transaction_types;
"

echo ""
echo "Buon lavoro! 🚀"
