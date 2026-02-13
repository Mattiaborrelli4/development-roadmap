@echo off
REM Script per compilare ed eseguire TodoListApp
REM Uso: run.bat

echo ==========================================
echo   TodoListApp - Compilazione ed Esecuzione
echo ==========================================
echo.

REM Verifica se Java e' installato
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRORE] Java non e' installato o non e' nel PATH
    echo Installa Java JDK da: https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)

echo [1/3] Pulitura file compilati precedenti...
if exist TodoListApp.class del TodoListApp.class

echo.
echo [2/3] Compilazione di TodoListApp.java...
javac TodoListApp.java

if %errorlevel% neq 0 (
    echo.
    echo [ERRORE] Compilazione fallita! Controlla gli errori sopra.
    pause
    exit /b 1
)

echo.
echo [OK] Compilazione completata con successo!
echo.
echo [3/3] Avvio dell'applicazione...
echo ==========================================
echo.

java TodoListApp

echo.
echo ==========================================
echo Applicazione terminata.
echo ==========================================
pause
