@echo off
REM ============================================================================
REM Script di Compilazione per Snake Game - Windows
REM ============================================================================
REM Questo script facilita la compilazione del progetto Snake
REM Utilizza MinGW/GCC se disponibile, altrimenti prova cl (MSVC)
REM ============================================================================

echo.
echo ========================================
echo   Snake Game - Build Script
echo ========================================
echo.

REM Verifica se esiste il file sorgente
if not exist "ConsoleGame.cpp" (
    echo [ERRORE] ConsoleGame.cpp non trovato!
    echo Assicurati di essere nella directory corretta.
    pause
    exit /b 1
)

REM Prova a compilare con g++ (MinGW)
where g++ >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Compilatore trovato: g++ (MinGW)
    echo.
    g++ --version | findstr "g++"
    echo.
    echo [INFO] Compilazione in corso...
    g++ -std=c++17 -Wall -Wextra -o snake.exe ConsoleGame.cpp

    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [SUCCESSO] Compilazione completata!
        echo Esegui il gioco con: snake.exe
        echo.
    ) else (
        echo.
        echo [ERRORE] Compilazione fallita! Controlla gli errori sopra.
        echo.
    )

    pause
    exit /b 0
)

REM Se g++ non è disponibile, prova con cl (Visual Studio)
where cl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Compilatore trovato: cl (MSVC)
    echo.
    echo [INFO] Compilazione in corso...
    cl /EHsc /std:c++17 /W3 /Fe:snake.exe ConsoleGame.cpp

    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [SUCCESSO] Compilazione completata!
        echo Esegui il gioco con: snake.exe
        echo.
        REM Rimuovi i file oggetto di Visual Studio
        del *.obj >nul 2>&1
    ) else (
        echo.
        echo [ERRORE] Compilazione fallita! Controlla gli errori sopra.
        echo.
    )

    pause
    exit /b 0
)

REM Nessun compilatore trovato
echo [ERRORE] Nessun compilatore trovato!
echo.
echo Per compilare questo progetto, hai bisogno di:
echo   1. Visual Studio (con C++): https://visualstudio.microsoft.com/
echo   2. OPPURE MinGW-w64: https://www.msys2.org/
echo.
echo Dopo l'installazione, apri questo script dalla Developer Command Prompt
echo (per Visual Studio) o dal terminale MSYS2 MinGW (per MinGW).
echo.
pause
exit /b 1
