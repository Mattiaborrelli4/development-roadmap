@echo off
REM Script di compilazione per File Organizer
REM Questo script compila il progetto e prepara i file necessari

echo ========================================
echo   Java File Organizer - Build Script
echo ========================================
echo.

REM Verifica Java
echo [1/5] Verifica installazione Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Java non trovato. Installa JDK 11+
    pause
    exit /b 1
)
echo       Java installato correttamente.
echo.

REM Verifica Gson
echo [2/5] Verifica libreria Gson...
if not exist "lib\gson-*.jar" (
    echo ATTENZIONE: Gson JAR non trovato in lib/
    echo.
    echo Scarica Gson da: https://github.com/google/gson/releases
    echo Metti il file JAR nella cartella lib/
    echo.
    pause
    exit /b 1
)
echo       Gson trovato.
echo.

REM Crea directory out
echo [3/5] Preparazione directory...
if not exist "out" mkdir out
echo       Directory out/ creata.
echo.

REM Compila
echo [4/5] Compilazione...
javac -cp "lib/*" -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
if %errorlevel% neq 0 (
    echo ERRORE: Compilazione fallita.
    pause
    exit /b 1
)
echo       Compilazione completata con successo.
echo.

REM Copia config.json
echo [5/5] Copia file di configurazione...
copy /Y "src\main\resources\config.json" "out\" >nul
if %errorlevel% neq 0 (
    echo ATTENZIONE: config.json non copiato.
)
echo       config.json copiato in out/.
echo.

echo ========================================
echo   BUILD COMPLETATO!
echo ========================================
echo.
echo Per eseguire:
echo   run.bat
echo.
echo Oppure manualmente:
echo   java -cp "out;lib/*" com.organizer.FileOrganizer
echo.
pause
