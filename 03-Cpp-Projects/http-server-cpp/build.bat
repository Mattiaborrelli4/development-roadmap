@echo off
REM Script di compilazione per Windows con MinGW-w64
REM Assicurarsi di avere g++ nel PATH

echo ========================================
echo   HTTP Server C++ - Build Script
echo ========================================
echo.

REM Verifica se g++ è disponibile
where g++ >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: g++ non trovato nel PATH!
    echo Installare MinGW-w64 o aggiungere al PATH.
    exit /b 1
)

echo Compilazione con g++...
g++ -std=c++17 -pthread -o server.exe server.cpp thread_pool.cpp main.cpp -lws2_32 -static-libgcc -static-libstdc++

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE: Compilazione fallita!
    exit /b 1
)

echo.
echo ========================================
echo   Compilazione completata con successo!
echo ========================================
echo.
echo Esecuzione: server.exe
echo.
echo Opzioni disponibili:
echo   --port 8080         Porta del server (default: 8080)
echo   --root ./public     Web root directory
echo   --threads 4         Numero worker threads
echo   --help              Mostra help
echo.
