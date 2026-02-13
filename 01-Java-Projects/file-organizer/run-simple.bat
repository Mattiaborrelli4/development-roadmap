@echo off
REM Script di esecuzione per File Organizer (NO external dependencies)

echo ========================================
echo   Java File Organizer - Starting...
echo ========================================
echo.

REM Verifica che sia stato compilato
if not exist "out\com\organizer\FileOrganizer.class" (
    echo ERRORE: Il progetto non e' stato compilato.
    echo Esegui prima: build-simple.bat
    pause
    exit /b 1
)

REM Esegui
echo Avvio monitoraggio Downloads...
echo Premi CTRL+C per terminare.
echo.

java -cp out com.organizer.FileOrganizer %1 %2

pause
