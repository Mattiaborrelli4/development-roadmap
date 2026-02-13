@echo off
REM Test Script per Mini Database Engine (Windows)

echo ==========================================
echo   Mini Database Engine - Test Automatico
echo ==========================================
echo.

set DB_EXECUTABLE=minidb.exe
set TEST_DB=test.db
set TEST_INPUT=test_input.txt

REM Verifica esistenza eseguibile
if not exist "%DB_EXECUTABLE%" (
    echo ERRORE: %DB_EXECUTABLE% non trovato!
    echo Esegui prima 'gcc -o minidb.exe main.c database.c' per compilare
    exit /b 1
)

REM Pulisci test precedenti
if exist "%TEST_DB%" del "%TEST_DB%"
if exist "%TEST_INPUT%" del "%TEST_INPUT%"

REM Crea input di test
(
echo SET nome Mario Rossi
echo SET eta 30
echo SET citta Roma
echo SET professione Sviluppatore
echo LIST
echo GET nome
echo GET eta
echo DELETE citta
echo LIST
echo SAVE test.db
echo EXIT
) > "%TEST_INPUT%"

echo Esecuzione test...
echo.

REM Esegui con l'input di test
"%DB_EXECUTABLE%" "%TEST_DB%" < "%TEST_INPUT%"

echo.
echo ==========================================
echo   Test completati!
echo ==========================================
echo.

if exist "%TEST_DB%" (
    echo File database creato: %TEST_DB%
    dir "%TEST_DB%"
) else (
    echo ERRORE: File database non creato
)

echo.
REM Pulizia
set /p CLEAN=Pulire i file di test? (s/n):
if /i "%CLEAN%"=="s" (
    if exist "%TEST_DB%" del "%TEST_DB%"
    if exist "%TEST_INPUT%" del "%TEST_INPUT%"
    echo File di test rimossi
)

echo Test completati!
pause
