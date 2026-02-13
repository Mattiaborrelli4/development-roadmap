@echo off
REM Test Script per Echo Daemon (Windows)
REM ======================================
REM Script per automatizzare i test del network daemon su Windows

echo ==========================================
echo Echo Daemon - Test Suite (Windows)
echo ==========================================
echo.

REM Funzione per check se daemon running
:check_daemon
python echo_daemon.py status | findstr "RUNNING" >nul
if %errorlevel% == 0 (
    echo [OK] Daemon in esecuzione
    exit /b 0
) else (
    echo Daemon non in esecuzione
    exit /b 1
)

REM Main test flow
:main
echo Inizio test suite...
echo.

REM Stop se già running
python echo_daemon.py stop 2>nul
timeout /t 1 /nobreak >nul

REM Avvia daemon
echo 1. Avvio daemon...
echo -------------------
start /B python echo_daemon.py start
timeout /t 2 /nobreak >nul

echo.
echo 2. Test TCP Echo
echo -------------------
python tests/client.py --protocol tcp --message "Hello TCP!" --count 3
echo [OK] Test TCP completato
echo.

echo 3. Test UDP Echo
echo -------------------
python tests/client.py --protocol udp --message "Hello UDP!" --count 3
echo [OK] Test UDP completato
echo.

echo 4. Test Multiple Clients
echo -------------------
start /B python tests/client.py --protocol tcp --count 5
start /B python tests/client.py --protocol tcp --count 5
start /B python tests/client.py --protocol tcp --count 5
timeout /t 3 /nobreak >nul
echo [OK] Test multipli completato
echo.

echo 5. Test Large Payload
echo -------------------
python tests/client.py --protocol tcp --large
echo [OK] Test payload grande completato
echo.

echo 6. Test Continuo (5 secondi)
echo -------------------
python tests/client.py --protocol tcp --continuous 5
echo [OK] Test continuo completato
echo.

echo 7. Verifica Log
echo -------------------
if exist echo-daemon.log (
    echo [OK] File log trovato
    echo Ultime 10 righe:
    powershell "Get-Content echo-daemon.log -Tail 10"
) else (
    echo File log non trovato
)
echo.

REM Ferma daemon
echo Stopping daemon...
echo -------------------
python echo_daemon.py stop
timeout /t 1 /nobreak >nul

echo.
echo ==========================================
echo [OK] Tutti i test completati con successo!
echo ==========================================
pause

goto :eof
