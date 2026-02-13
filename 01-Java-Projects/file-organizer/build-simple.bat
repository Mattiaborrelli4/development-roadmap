@echo off
REM Script di compilazione per File Organizer (NO external dependencies)
REM Questo script compila il progetto senza richiedere librerie esterne

echo ========================================
echo   Java File Organizer - Build Script
echo   (No External Dependencies Version)
echo ========================================
echo.

REM Verifica Java
echo [1/4] Verifica installazione Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Java non trovato. Installa JDK 11+
    pause
    exit /b 1
)
echo       Java installato correttamente.
echo.

REM Crea directory out
echo [2/4] Preparazione directory...
if not exist "out" mkdir out
echo       Directory out/ creata.
echo.

REM Compila
echo [3/4] Compilazione...
javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
if %errorlevel% neq 0 (
    echo ERRORE: Compilazione fallita.
    pause
    exit /b 1
)
echo       Compilazione completata con successo.
echo.

REM Crea config di default se non esiste
echo [4/4] Verifica configurazione...
if not exist "out\config.properties" (
    echo       Creazione config.properties di default...
    copy /Y "src\main\resources\config.properties" "out\" >nul 2>&1
    if not exist "out\config.properties" (
        echo       ATTENZIONE: config.properties non trovato in src/main/resources/
        echo       Verra' creato al primo avvio.
    )
) else (
    echo       config.properties gia' presente.
)
echo.

echo ========================================
echo   BUILD COMPLETATO!
echo ========================================
echo.
echo Per eseguire:
echo   run-simple.bat
echo.
echo Oppure manualmente:
echo   java -cp out com.organizer.FileOrganizer
echo.
pause
