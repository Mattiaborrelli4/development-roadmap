#!/bin/bash
# Test Script per Echo Daemon
# ============================
# Script per automatizzare i test del network daemon

set -e  # Exit on error

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Echo Daemon - Test Suite"
echo "=========================================="
echo ""

# Funzione per check se daemon running
check_daemon() {
    if python echo_daemon.py status | grep -q "RUNNING"; then
        echo -e "${GREEN}✓ Daemon in esecuzione${NC}"
        return 0
    else
        echo -e "${YELLOW}✓ Daemon non in esecuzione${NC}"
        return 1
    fi
}

# Funzione per avviare daemon
start_daemon() {
    echo ""
    echo "1. Avvio daemon..."
    echo "-------------------"
    python echo_daemon.py start &
    DAEMON_PID=$!
    sleep 2

    if check_daemon; then
        echo -e "${GREEN}✓ Daemon avviato con successo${NC}"
    else
        echo -e "${RED}✗ Errore avvio daemon${NC}"
        exit 1
    fi
}

# Funzione per fermare daemon
stop_daemon() {
    echo ""
    echo "Stopping daemon..."
    echo "-------------------"
    python echo_daemon.py stop
    sleep 1
}

# Funzione per test TCP
test_tcp() {
    echo ""
    echo "2. Test TCP Echo"
    echo "-------------------"
    python tests/client.py --protocol tcp --message "Hello TCP!" --count 3
    echo -e "${GREEN}✓ Test TCP completato${NC}"
}

# Funzione per test UDP
test_udp() {
    echo ""
    echo "3. Test UDP Echo"
    echo "-------------------"
    python tests/client.py --protocol udp --message "Hello UDP!" --count 3
    echo -e "${GREEN}✓ Test UDP completato${NC}"
}

# Funzione per test multipli
test_multiple() {
    echo ""
    echo "4. Test Multiple Clients"
    echo "-------------------"
    python tests/client.py --protocol tcp --count 5 &
    python tests/client.py --protocol tcp --count 5 &
    python tests/client.py --protocol tcp --count 5 &

    wait
    echo -e "${GREEN}✓ Test multipli completato${NC}"
}

# Funzione per test payload grande
test_large() {
    echo ""
    echo "5. Test Large Payload"
    echo "-------------------"
    python tests/client.py --protocol tcp --large
    echo -e "${GREEN}✓ Test payload grande completato${NC}"
}

# Funzione per test continuo
test_continuous() {
    echo ""
    echo "6. Test Continuo (5 secondi)"
    echo "-------------------"
    python tests/client.py --protocol tcp --continuous 5
    echo -e "${GREEN}✓ Test continuo completato${NC}"
}

# Funzione per verifica log
check_logs() {
    echo ""
    echo "7. Verifica Log"
    echo "-------------------"

    LOG_FILE="echo-daemon.log"
    if [ -f "$LOG_FILE" ]; then
        echo -e "${GREEN}✓ File log trovato${NC}"
        echo "Ultime 10 righe:"
        tail -n 10 "$LOG_FILE"
    else
        echo -e "${YELLOW}✗ File log non trovato${NC}"
    fi
}

# Main test flow
main() {
    echo "Inizio test suite..."
    echo ""

    # Stop se già running
    python echo_daemon.py stop 2>/dev/null || true
    sleep 1

    # Avvia daemon
    start_daemon

    # Esegui test
    test_tcp
    test_udp
    test_multiple
    test_large
    test_continuous

    # Verifica log
    check_logs

    # Ferma daemon
    stop_daemon

    echo ""
    echo "=========================================="
    echo -e "${GREEN}✓ Tutti i test completati con successo!${NC}"
    echo "=========================================="
}

# Parse arguments
case "${1:-all}" in
    tcp)
        start_daemon
        test_tcp
        stop_daemon
        ;;
    udp)
        start_daemon
        test_udp
        stop_daemon
        ;;
    multiple)
        start_daemon
        test_multiple
        stop_daemon
        ;;
    large)
        start_daemon
        test_large
        stop_daemon
        ;;
    continuous)
        start_daemon
        test_continuous
        stop_daemon
        ;;
    all)
        main
        ;;
    start)
        start_daemon
        echo "Daemon running. Press Ctrl+C to stop tests."
        trap stop_daemon EXIT
        sleep infinity
        ;;
    stop)
        stop_daemon
        ;;
    *)
        echo "Uso: $0 [all|tcp|udp|multiple|large|continuous|start|stop]"
        exit 1
        ;;
esac
