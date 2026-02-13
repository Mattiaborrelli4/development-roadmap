#!/bin/bash
# Script di installazione per Secure Notes Manager

echo "========================================"
echo "  Secure Notes Manager - Setup"
echo "========================================"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "[ERRORE] Python non trovato!"
    echo "Installa Python 3.10+ dal tuo package manager"
    exit 1
fi

echo "[OK] Python trovato"
python3 --version
echo ""

# Installa dipendenze
echo "Installazione dipendenze..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERRORE] Installazione fallita!"
    exit 1
fi

echo ""
echo "========================================"
echo "  Installazione Completata!"
echo "========================================"
echo ""
echo "Prossimi passi:"
echo "  1. python3 demo.py              - Vedi la demo"
echo "  2. python3 main.py init         - Crea vault"
echo "  3. python3 main.py unlock        - Sblocca vault"
echo ""
echo "Leggi QUICKSTART.md per iniziare!"
echo ""
