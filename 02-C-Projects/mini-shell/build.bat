@echo off
REM Build Script per Mini Shell (Windows)
REM Usa MinGW-w64 o Visual Studio

echo ================================
echo   Mini Shell - Build Script
echo ================================
echo.

REM Check for GCC (MinGW)
where gcc >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [1/3] Compilazione con GCC (MinGW)...
    gcc -Wall -Wextra -std=c99 -o mini-shell.exe shell.c
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Compilazione completata con successo!
        echo.
        echo Per eseguire: mini-shell.exe
        echo.
        goto :success
    ) else (
        echo [ERRORE] Compilazione fallita!
        goto :error
    )
)

REM Check for CL (Visual Studio)
where cl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [1/3] Compilazione con CL (Visual Studio)...
    cl shell.c /Fe:mini-shell.exe /W3
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Compilazione completata con successo!
        echo.
        echo Per eseguire: mini-shell.exe
        echo.
        goto :success
    ) else (
        echo [ERRORE] Compilazione fallita!
        goto :error
    )
)

REM Nessun compilatore trovato
echo [ERRORE] Nessun compilatore trovato!
echo.
echo Installa uno dei seguenti:
echo   - MinGW-w64: https://www.mingw-w64.org/
echo   - Visual Studio Community: https://visualstudio.microsoft.com/
goto :error

:success
echo ================================
echo   Build Completata!
echo ================================
pause
exit /b 0

:error
echo ================================
echo   Build Fallita!
echo ================================
pause
exit /b 1
