@echo off
REM Script di esecuzione per File Organizer
REM Puoi passare come argomento la cartella da monitorare

echo ========================================
echo   Java File Organizer
echo ========================================
echo.

REM Verifica se il progetto e' compilato
if not exist "out\com\organizer\FileOrganizer.class" (
    echo ERRORE: Progetto non compilato.
    echo Esegui prima: build.bat
    echo.
    pause
    exit /b 1
)

REM Verifica config.json
if not exist "out\config.json" (
    echo ATTENZIONE: config.json non trovato in out/
    echo Copia da src/main/resources/...
    copy /Y "src\main\resources\config.json" "out\" >nul
)

REM Esegui con argomenti se forniti, altrimenti usa default
if "%~1"=="" (
    echo.
    echo Monitoraggio cartella Downloads...
    echo.
    java -cp "out;lib/*" com.organizer.FileOrganizer
) else (
    echo.
    echo Monitoraggio cartella: %~1
    echo.
    if "%~2"=="" (
        java -cp "out;lib/*" com.organizer.FileOrganizer "%~1"
    ) else (
        java -cp "out;lib/*" com.organizer.FileOrganizer "%~1" "%~2"
    )
)

echo.
echo ========================================
echo   Organizer terminato
echo ========================================
echo.
pause
