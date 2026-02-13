@echo off
REM File Monitor - Quick Start per Windows
REM ========================================

echo.
echo =====================================================
echo   File Monitor - Quick Start
echo =====================================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non è installato o non è in PATH
    echo Installa Python da https://www.python.org/
    pause
    exit /b 1
)

REM Controlla se watchdog è installato
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo Installazione dipendenze...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRORE: Impossibile installare le dipendenze
        pause
        exit /b 1
    )
)

echo.
echo Selezione modalita:
echo.
echo 1. Monitora directory corrente
echo 2. Monitora directory personalizzata
echo 3. Monitora con output dettagliato (-v)
echo 4. Monitora e salva log su file
echo 5. Esegui test automatici
echo 6. Esci
echo.

set /p choice="Seleziona opzione (1-6): "

if "%choice%"=="1" (
    echo.
    echo Avvio monitoraggio directory corrente...
    python file_monitor.py
) else if "%choice%"=="2" (
    set /p path="Inserisci percorso directory: "
    echo.
    echo Avvio monitoraggio di: %path%
    python file_monitor.py "%path%"
) else if "%choice%"=="3" (
    echo.
    echo Avvio monitoraggio con output dettagliato...
    python file_monitor.py -v
) else if "%choice%"=="4" (
    set /p logfile="Inserisci nome file log (es. monitor.log): "
    echo.
    echo Avvio monitoraggio con log su file: %logfile%
    python file_monitor.py -l %logfile% -v
) else if "%choice%"=="5" (
    echo.
    echo Esecuzione test automatici...
    echo (Assicurati di avere un monitor attivo in un altro terminale!)
    echo.
    pause
    python test_operations.py
) else if "%choice%"=="6" (
    exit /b 0
) else (
    echo.
    echo Opzione non valida!
    pause
    exit /b 1
)
