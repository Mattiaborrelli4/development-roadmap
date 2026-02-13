#!/bin/bash

echo "========================================"
echo "  Blog Platform - Quick Start"
echo "========================================"
echo ""

# Verifica se node_modules esiste
if [ ! -d "node_modules" ]; then
    echo "[1/2] Installazione dipendenze..."
    npm install
    echo ""
else
    echo "[✓] Dipendenze già installate"
    echo ""
fi

echo "[2/2] Avvio server..."
echo ""
echo "Server will start on: http://localhost:3000"
echo "Admin credentials: admin / admin123"
echo ""
echo "Press CTRL+C to stop the server"
echo ""
npm start
