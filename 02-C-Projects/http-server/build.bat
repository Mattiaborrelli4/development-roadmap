@echo off
REM Script di build per Windows (senza Make)
REM Richiede MinGW con gcc nel PATH

echo ========================================
echo   HTTP Server - Build Script (Windows)
echo ========================================
echo.

REM Verifica che gcc sia installato
where gcc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: GCC non trovato nel PATH!
    echo.
    echo Per compilare questo progetto, installa MinGW-w64:
    echo https://www.mingw-w64.org/
    echo.
    echo Oppure usa MS Visual Studio con il comando:
    echo   cl server.c /link ws2_32.lib
    echo.
    pause
    exit /b 1
)

REM Controlla se la cartella public esiste
if not exist "public" (
    echo Creazione cartella public...
    mkdir public
)

echo Compilazione in corso...
echo.

gcc -Wall -Wextra -O2 server.c -o server.exe -lws2_32

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE: Compilazione fallita!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Compilazione Completata!
echo ========================================
echo.
echo Eseguibile creato: server.exe
echo.
echo Per avviare il server:
echo   server.exe
echo.
echo Con porta personalizzata:
echo   server.exe 3000
echo.
echo ========================================
pause
