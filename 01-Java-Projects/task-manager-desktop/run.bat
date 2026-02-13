@echo off
REM Task Manager Desktop - Run Script
REM Questo script esegue l'applicazione

echo ========================================
echo Task Manager Desktop - Esecuzione
echo ========================================
echo.

if not exist "target\task-manager-desktop-1.0.0.jar" (
    echo ERRORE: JAR non trovato!
    echo Eseguire prima build.bat
    echo.
    pause
    exit /b 1
)

echo Avvio applicazione...
echo.

java -jar target\task-manager-desktop-1.0.0.jar

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Errore durante l'esecuzione.
    pause
)
