@echo off
REM Task Manager Desktop - Build Script
REM Questo script compila e pacchettizza l'applicazione

echo ========================================
echo Task Manager Desktop - Build Script
echo ========================================
echo.

echo [1/4] Pulizia cartelle di build...
call mvn clean
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: Pulizia fallita!
    pause
    exit /b 1
)

echo.
echo [2/4] Compilazione sorgenti...
call mvn compile
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: Compilazione fallita!
    pause
    exit /b 1
)

echo.
echo [3/4] Pacchettizzazione JAR...
call mvn package
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: Package fallito!
    pause
    exit /b 1
)

echo.
echo [4/4] Completato!
echo.
echo ========================================
echo JAR creato:
echo target/task-manager-desktop-1.0.0.jar
echo ========================================
echo.
echo Per eseguire l'applicazione:
echo   java -jar target/task-manager-desktop-1.0.0.jar
echo.
pause
