@echo off
REM Script di compilazione per Windows con MSVC (Visual Studio)
REM Utilizzare "Developer Command Prompt for VS" o "x64 Native Tools Command Prompt"

echo ========================================
echo   HTTP Server C++ - MSVC Build Script
echo ========================================
echo.

REM Verifica se cl.exe è disponibile
where cl.exe >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: cl.exe non trovato!
    echo.
    echo Aprire questo script dal:
    echo   - "Developer Command Prompt for VS"
    echo   - "x64 Native Tools Command Prompt for VS"
    echo.
    echo Oppure installare Visual Studio Build Tools.
    exit /b 1
)

echo Compilazione con MSVC...
cl.exe /EHsc /std:c++17 /O2 /Fe:server.exe server.cpp thread_pool.cpp main.cpp ws2_32.lib

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE: Compilazione fallita!
    exit /b 1
)

REM Pulisci file temporanei
del *.obj >nul 2>nul

echo.
echo ========================================
echo   Compilazione completata con successo!
echo ========================================
echo.
echo Esecuzione: server.exe
echo.
