@echo off
echo ========================================
echo   Blog Platform - Quick Start
echo ========================================
echo.

:: Verifica se node_modules esiste
if not exist "node_modules\" (
    echo [1/2] Installazione dipendenze...
    call npm install
    echo.
) else (
    echo [✓] Dipendenze già installate
    echo.
)

echo [2/2] Avvio server...
echo.
echo Server will start on: http://localhost:3000
echo Admin credentials: admin / admin123
echo.
echo Press CTRL+C to stop the server
echo.
call npm start
