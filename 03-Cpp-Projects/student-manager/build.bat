@echo off
REM Build script per Student Management System (Windows)

echo ============================================
echo   Build - Student Management System
echo ============================================
echo.

REM Verifica se g++ è installato
where g++ >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: g++ non trovato!
    echo.
    echo Per compilare questo progetto hai bisogno di:
    echo   - MinGW-w64 (https://www.mingw-w64.org/)
    echo   - Oppure MSYS2 (https://www.msys2.org/)
    echo.
    pause
    exit /b 1
)

echo Compilazione in corso...
echo.

g++ -o student_manager main.cpp student.cpp -std=c++11 -Wall -Wextra

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo   Compilazione completata con successo!
    echo ============================================
    echo.
    echo Eseguibile creato: student_manager.exe
    echo.
    echo Per eseguire il programma:
    echo   .\student_manager.exe
    echo.
) else (
    echo.
    echo ============================================
    echo   ERRORE durante la compilazione!
    echo ============================================
    echo.
)

pause
