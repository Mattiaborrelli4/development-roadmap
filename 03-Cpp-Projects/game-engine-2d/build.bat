@echo off
REM Build script per Game Engine 2D (Windows)

echo ========================================
echo   2D Game Engine - Build Script
echo ========================================
echo.

REM Controlla se g++ è disponibile
where g++ >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Trovato MinGW/GCC
    echo.
    echo [1/3] Compilazione con g++...
    g++ -std=c++17 -Wall -Wextra -O2 main.cpp -o game.exe -static-libgcc -static-libstdc++ -mconsole

    if %ERRORLEVEL% EQU 0 (
        echo [OK] Compilazione completata!
        echo.
        echo [2/3] Esecuzione...
        echo.
        game.exe
    ) else (
        echo [ERRORE] Compilazione fallita!
    )
    goto :end
)

REM Controlla se cl (MSVC) è disponibile
where cl >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Trovato MSVC
    echo.
    echo [1/3] Compilazione con MSVC...
    cl /EHsc /std:c++17 /O2 main.cpp

    if %ERRORLEVEL% EQU 0 (
        echo [OK] Compilazione completata!
        echo.
        echo [2/3] Esecuzione...
        echo.
        main.exe
    ) else (
        echo [ERRORE] Compilazione fallita!
    )
    goto :end
)

REM Nessun compilatore trovato
echo [ERRORE] Nessun compilatore trovato!
echo.
echo Installa uno dei seguenti:
echo   - MinGW-w64: https://www.mingw-w64.org/
echo   - Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
echo   - MSYS2: https://www.msys2.org/

:end
echo.
echo ========================================
pause
