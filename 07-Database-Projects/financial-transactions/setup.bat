@echo off
REM ============================================================================
REM SETUP SCRIPT - Financial Transactions Database (Windows)
REM ============================================================================

echo ============================================
echo Financial Transactions Database Setup
echo ============================================
echo.

REM Verifica PostgreSQL
where psql >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRORE] PostgreSQL non trovato
    echo Installa PostgreSQL prima di eseguire questo script
    pause
    exit /b 1
)

echo [OK] PostgreSQL trovato
echo.

REM Nome database
set DB_NAME=financial_transactions

echo Creazione database '%DB_NAME%'...
echo.

REM Crea database
psql -U postgres -c "DROP DATABASE IF EXISTS %DB_NAME%;"
psql -U postgres -c "CREATE DATABASE %DB_NAME%;"

if %errorlevel% equ 0 (
    echo [OK] Database creato con successo
) else (
    echo [ERRORE] Errore nella creazione del database
    pause
    exit /b 1
)

echo.
echo Esecuzione schema.sql...
psql -U postgres -d %DB_NAME% -f schema.sql

if %errorlevel% equ 0 (
    echo [OK] Schema creato con successo
) else (
    echo [ERRORE] Errore nella creazione dello schema
    pause
    exit /b 1
)

echo.
echo Esecuzione sample_data.sql...
psql -U postgres -d %DB_NAME% -f sample_data.sql

if %errorlevel% equ 0 (
    echo [OK] Dati campione inseriti
) else (
    echo [ERRORE] Errore nell'inserimento dei dati
    pause
    exit /b 1
)

echo.
echo Esecuzione procedures.sql...
psql -U postgres -d %DB_NAME% -f procedures.sql

if %errorlevel% equ 0 (
    echo [OK] Stored procedure create
) else (
    echo [AVVISO] Alcune procedure potrebbero non essere state create
)

echo.
echo ============================================
echo [SUCCESSO] INSTALLAZIONE COMPLETATA!
echo ============================================
echo.
echo Connessione al database:
echo   psql -U postgres -d %DB_NAME%
echo.
echo File disponibili:
echo   - schema.sql       : Struttura database
echo   - sample_data.sql  : Dati campione
echo   - procedures.sql   : Stored procedures
echo   - queries.sql      : Query di reporting
echo   - transactions.sql : Esempi transazioni
echo   - concurrency.sql  : Esempi concorrenza
echo   - README.md        : Documentazione completa
echo.
echo Quick test:
psql -U postgres -d %DB_NAME% -c "SELECT 'Clienti' AS tipo, COUNT(*) AS totale FROM customers UNION ALL SELECT 'Conti', COUNT(*) FROM accounts UNION ALL SELECT 'Transazioni', COUNT(*) FROM transactions UNION ALL SELECT 'Tipi Transazione', COUNT(*) FROM transaction_types;"

echo.
echo Buon lavoro!
pause
