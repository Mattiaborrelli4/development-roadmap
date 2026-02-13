@echo off
REM Demo Script per Mini Shell (Windows)
REM Esegue una serie di comandi per dimostrare le funzionalità

echo ================================
echo   Mini Shell - Demo Script
echo ================================
echo.

REM Verifica che la shell sia compilata
if not exist "mini-shell.exe" (
    echo Errore: mini-shell.exe non trovato.
    echo Compila prima con: make
    pause
    exit /b 1
)

echo Avvio demo con i seguenti comandi:
echo   1. echo   - Stampa messaggio
echo   2. cd     - Cambia directory
echo   3. pwd    - Mostra directory
echo   4. help   - Mostra aiuto
echo   5. exit   - Esce
echo.

REM Esegui la shell con comandi predefiniti
(
    echo Demo Mini Shell
    echo pwd
    echo echo "Ciao dalla Mini Shell!"
    echo echo.
    echo cd C:\Temp
    echo pwd
    echo help
    echo exit
) | mini-shell.exe

echo.
echo ================================
echo   Demo completata!
echo ================================
pause
