@echo off
REM Script di installazione per Secure Notes Manager

echo ========================================
echo   Secure Notes Manager - Setup
echo ========================================
echo.

REM Verifica Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRORE] Python non trovato!
    echo Installa Python 3.10+ da https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python trovato
echo.

REM Installa dipendenze
echo Installazione dipendenze...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERRORE] Installazione fallita!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installazione Completata!
echo ========================================
echo.
echo Prossimi passi:
echo   1. python demo.py              - Vedi la demo
echo   2. python main.py init         - Crea vault
echo   3. python main.py unlock        - Sblocca vault
echo.
echo Leggi QUICKSTART.md per iniziare!
echo.
pause
