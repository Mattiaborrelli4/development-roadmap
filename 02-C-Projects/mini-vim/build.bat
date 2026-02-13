@echo off
REM Mini Vim - Script di compilazione per Windows
REM Questo script compila mini-vim su Windows senza richiedere make

echo ====================================
echo Mini Vim - Compilazione Windows
echo ====================================
echo.

REM Verifica se GCC è installato
where gcc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: GCC non trovato!
    echo.
    echo Per compilare mini-vim, devi installare GCC:
    echo 1. Scarica MinGW-w64 da: https://www.mingw-w64.org/
    echo 2. Oppure installa MSYS2 da: https://www.msys2.org/
    echo.
    pause
    exit /b 1
)

echo Compilazione in corso...
echo.

gcc -Wall -Wextra -std=c99 -pedantic -c buffer.c -o buffer.o
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE durante la compilazione di buffer.c
    pause
    exit /b 1
)

gcc -Wall -Wextra -std=c99 -pedantic -c editor.c -o editor.o
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE durante la compilazione di editor.c
    pause
    exit /b 1
)

gcc buffer.o editor.o -o mini-vim.exe
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE durante il linking
    pause
    exit /b 1
)

echo.
echo ====================================
echo Build completata con successo!
echo ====================================
echo.
echo Eseguibile: mini-vim.exe
echo.
echo Per eseguire:
echo   mini-vim.exe
echo   mini-vim.exe nomefile.txt
echo.
echo Per pulire i file oggetto:
echo   cleanup.bat
echo.

REM Chiede se vuole eseguire subito
set /p RUN="Vuoi eseguire mini-vim ora? (s/N): "
if /i "%RUN%"=="s" (
    echo.
    echo Avvio mini-vim...
    mini-vim.exe
)

pause
