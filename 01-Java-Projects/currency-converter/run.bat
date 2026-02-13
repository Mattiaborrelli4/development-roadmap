@echo off
REM Script per avviare il Currency Converter
echo ====================================
echo Currency Converter - Avvio...
echo ====================================
echo.

REM Controlla se Maven è installato
mvn --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERRORE: Maven non trovato!
    echo Assicurati di avere Maven installato e nel PATH
    pause
    exit /b 1
)

REM Controlla se Java è installato
java -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERRORE: Java non trovato!
    echo Assicurati di avere Java 17+ installato e nel PATH
    pause
    exit /b 1
)

echo Avvio applicazione...
echo.

REM Avvia l'applicazione con Maven
call mvn clean javafx:run

echo.
echo ====================================
echo Applicazione chiusa
echo ====================================
pause
