#!/bin/bash
# File Monitor - Quick Start per Linux/macOS
# ===========================================

echo ""
echo "====================================================="
echo "  File Monitor - Quick Start"
echo "====================================================="
echo ""

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "ERRORE: Python 3 non è installato"
    echo "Installa Python usando il tuo package manager"
    exit 1
fi

# Controlla se pip è installato
if ! command -v pip3 &> /dev/null; then
    echo "ERRORE: pip3 non è installato"
    exit 1
fi

# Controlla se watchdog è installato
if ! python3 -c "import watchdog" &> /dev/null; then
    echo "Installazione dipendenze..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERRORE: Impossibile installare le dipendenze"
        exit 1
    fi
fi

echo ""
echo "Selezione modalità:"
echo ""
echo "1. Monitora directory corrente"
echo "2. Monitora directory personalizzata"
echo "3. Monitora con output dettagliato (-v)"
echo "4. Monitora e salva log su file"
echo "5. Esegui test automatici"
echo "6. Esci"
echo ""

read -p "Seleziona opzione (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Avvio monitoraggio directory corrente..."
        python3 file_monitor.py
        ;;
    2)
        read -p "Inserisci percorso directory: " path
        echo ""
        echo "Avvio monitoraggio di: $path"
        python3 file_monitor.py "$path"
        ;;
    3)
        echo ""
        echo "Avvio monitoraggio con output dettagliato..."
        python3 file_monitor.py -v
        ;;
    4)
        read -p "Inserisci nome file log (es. monitor.log): " logfile
        echo ""
        echo "Avvio monitoraggio con log su file: $logfile"
        python3 file_monitor.py -l "$logfile" -v
        ;;
    5)
        echo ""
        echo "Esecuzione test automatici..."
        echo "(Assicurati di avere un monitor attivo in un altro terminale!)"
        echo ""
        read -p "Premi Invio per continuare..."
        python3 test_operations.py
        ;;
    6)
        exit 0
        ;;
    *)
        echo ""
        echo "Opzione non valida!"
        exit 1
        ;;
esac
