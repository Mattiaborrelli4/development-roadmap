-- ============================================================================
-- ESEMPI DI TRANSAZIONI - DIMOSTRAZIONE PROPRIETÀ ACID
-- ============================================================================

-- ============================================================================
-- 1. BONIFICO TRA CONTI (Transazione ACID completa)
-- ============================================================================

-- Esempio di transazione che dimostra tutte le proprietà ACID:
-- A - Atomicity: Tutte le operazioni o nessuna
-- C - Consistency: Il saldo totale rimane invariato
-- I - Isolation: Le operazioni sono isolate da altre transazioni
-- D - Durability: Una volta commit, i dati sono permanenti

\echo '========================================'
\echo 'BONIFICO STANDARD - ESEMPIO ACID'
\echo '========================================'

-- INIZIO TRANSAZIONE
BEGIN;

-- Dichiara variabili per il test
DO $$
DECLARE
    v_from_account_id INTEGER := 1;   -- Conto di Mario Rossi (checking)
    v_to_account_id INTEGER := 6;     -- Conto di Luca Ferrari (checking)
    v_amount DECIMAL := 500.00;
    v_from_balance_before DECIMAL;
    v_to_balance_before DECIMAL;
    v_from_balance_after DECIMAL;
    v_to_balance_after DECIMAL;
BEGIN
    -- STEP 1: Verifica saldi iniziali (Consistency check)
    RAISE NOTICE 'STEP 1: Verifica saldi iniziali';
    SELECT balance INTO v_from_balance_before FROM accounts WHERE id = v_from_account_id;
    SELECT balance INTO v_to_balance_before FROM accounts WHERE id = v_to_account_id;

    RAISE NOTICE 'Saldo conto mittente (prima): €%', v_from_balance_before;
    RAISE NOTICE 'Saldo conto beneficiario (prima): €%', v_to_balance_before;

    -- STEP 2: Verifica disponibilità fondi
    RAISE NOTICE '';
    RAISE NOTICE 'STEP 2: Verifica disponibilità fondi';
    IF v_from_balance_before < v_amount THEN
        RAISE EXCEPTION 'Fondi insufficienti! Saldo: €%, Richiesto: €%', v_from_balance_before, v_amount;
    END IF;
    RAISE NOTICE 'Fondi sufficienti. Procedo con il bonifico.';

    -- STEP 3: Addebito conto mittente
    RAISE NOTICE '';
    RAISE NOTICE 'STEP 3: Addebito conto mittente';
    UPDATE accounts
    SET balance = balance - v_amount
    WHERE id = v_from_account_id;

    -- STEP 4: Accredito conto beneficiario
    RAISE NOTICE 'STEP 4: Accredito conto beneficiario';
    UPDATE accounts
    SET balance = balance + v_amount
    WHERE id = v_to_account_id;

    -- STEP 5: Creazione record transazione
    RAISE NOTICE 'STEP 5: Creazione record transazione';
    INSERT INTO transactions (
        from_account_id,
        to_account_id,
        amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description
    ) VALUES (
        v_from_account_id,
        v_to_account_id,
        v_amount,
        1, -- Bonifico
        'completed',
        CURRENT_TIMESTAMP,
        'BONIFICO-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
        'Bonifico da conto ' || v_from_account_id || ' a conto ' || v_to_account_id
    );

    -- STEP 6: Verifica saldi finali
    RAISE NOTICE '';
    RAISE NOTICE 'STEP 6: Verifica saldi finali';
    SELECT balance INTO v_from_balance_after FROM accounts WHERE id = v_from_account_id;
    SELECT balance INTO v_to_balance_after FROM accounts WHERE id = v_to_account_id;

    RAISE NOTICE 'Saldo conto mittente (dopo): €%', v_from_balance_after;
    RAISE NOTICE 'Saldo conto beneficiario (dopo): €%', v_to_balance_after;

    -- Verifica consistenza: totale deve essere uguale
    RAISE NOTICE '';
    RAISE NOTICE 'VERIFICA CONSISTENZA (C di ACID):';
    RAISE NOTICE 'Totale prima: €%', v_from_balance_before + v_to_balance_before;
    RAISE NOTICE 'Totale dopo: €%', v_from_balance_after + v_to_balance_after;
    RAISE NOTICE 'Differenza: €%', (v_from_balance_after + v_to_balance_after) - (v_from_balance_before + v_to_balance_before);

    IF (v_from_balance_after + v_to_balance_after) != (v_from_balance_before + v_to_balance_before) THEN
        RAISE EXCEPTION 'ERRORE DI CONSISTENZA! I saldi non corrispondono!';
    END IF;

    RAISE NOTICE '';
    RAISE NOTICE 'TRANSAZIONE COMPLETATA CON SUCCESSO!';
END $$;

-- COMMIT: Rende permanenti tutte le modifiche (Durability)
COMMIT;
\echo 'COMMIT eseguito. Le modifiche sono ora permanenti.';


-- ============================================================================
-- 2. DEPOSITO SUL CONTO
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'DEPOSITO SUL CONTO'
\echo '========================================'

BEGIN;

DO $$
DECLARE
    v_account_id INTEGER := 2;  -- Conto saving di Mario Rossi
    v_amount DECIMAL := 1000.00;
    v_balance_before DECIMAL;
    v_balance_after DECIMAL;
BEGIN
    RAISE NOTICE 'Eseguo deposito di €% sul conto %', v_amount, v_account_id;

    -- Saldo iniziale
    SELECT balance INTO v_balance_before FROM accounts WHERE id = v_account_id;

    -- Esegui deposito
    UPDATE accounts
    SET balance = balance + v_amount
    WHERE id = v_account_id;

    -- Crea transazione
    INSERT INTO transactions (
        to_account_id,
        amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description
    ) VALUES (
        v_account_id,
        v_amount,
        3, -- Deposito
        'completed',
        CURRENT_TIMESTAMP,
        'DEP-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
        'Deposito contante'
    );

    -- Verifica
    SELECT balance INTO v_balance_after FROM accounts WHERE id = v_account_id;

    RAISE NOTICE 'Saldo prima: €%', v_balance_before;
    RAISE NOTICE 'Saldo dopo: €%', v_balance_after;
    RAISE NOTICE 'Deposito completato con successo!';
END $$;

COMMIT;


-- ============================================================================
-- 3. PRELIEVO DAL CONTO
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'PRELIEVO DAL CONTO'
\echo '========================================'

BEGIN;

DO $$
DECLARE
    v_account_id INTEGER := 1;  -- Conto checking di Mario Rossi
    v_amount DECIMAL := 200.00;
    v_balance_before DECIMAL;
BEGIN
    -- Verifica saldo
    SELECT balance INTO v_balance_before FROM accounts WHERE id = v_account_id;

    RAISE NOTICE 'Tentativo prelievo di €% dal conto %', v_amount, v_account_id;
    RAISE NOTICE 'Saldo disponibile: €%', v_balance_before;

    -- Verifica fondi sufficienti
    IF v_balance_before < v_amount THEN
        RAISE NOTICE 'ERRORE: Fondi insufficienti per il prelievo!';
        ROLLBACK;
        RETURN;
    END IF;

    -- Esegui prelievo
    UPDATE accounts
    SET balance = balance - v_amount
    WHERE id = v_account_id;

    -- Crea transazione
    INSERT INTO transactions (
        from_account_id,
        amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description
    ) VALUES (
        v_account_id,
        v_amount,
        4, -- Prelievo
        'completed',
        CURRENT_TIMESTAMP,
        'PRE-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
        'Prelievo contante'
    );

    RAISE NOTICE 'Prelievo completato con successo!';
END $$;

COMMIT;


-- ============================================================================
-- 4. PAGAMENTO BOLLETTA (con fee)
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'PAGAMENTO BOLLETTA (con fee)'
\echo '========================================'

BEGIN;

DO $$
DECLARE
    v_account_id INTEGER := 3;  -- Conto checking di Giulia Bianchi
    v_amount DECIMAL := 85.50;
    v_fee DECIMAL;
    v_transaction_type_id INTEGER := 5; -- Pagamento Bolletta
    v_fee_percentage DECIMAL;
    v_total_amount DECIMAL;
BEGIN
    RAISE NOTICE 'Pagamento bolletta di €%', v_amount;

    -- Recupera fee percentuale
    SELECT fee_percentage INTO v_fee_percentage
    FROM transaction_types
    WHERE id = v_transaction_type_id;

    -- Calcola fee
    v_fee := v_amount * (v_fee_percentage / 100);
    v_total_amount := v_amount + v_fee;

    RAISE NOTICE 'Fee applicata: €% (%%%)', v_fee, v_fee_percentage;
    RAISE NOTICE 'Totale addebitato: €%', v_total_amount;

    -- Verifica saldo
    IF NOT EXISTS (
        SELECT 1 FROM accounts
        WHERE id = v_account_id AND balance >= v_total_amount
    ) THEN
        RAISE NOTICE 'ERRORE: Fondi insufficienti per il pagamento!';
        ROLLBACK;
        RETURN;
    END IF;

    -- Addebita importo totale
    UPDATE accounts
    SET balance = balance - v_total_amount
    WHERE id = v_account_id;

    -- Crea transazione
    INSERT INTO transactions (
        from_account_id,
        amount,
        fee_amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description
    ) VALUES (
        v_account_id,
        v_amount,
        v_fee,
        v_transaction_type_id,
        'completed',
        CURRENT_TIMESTAMP,
        'BOLL-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
        'Pagamento bolletta luce'
    );

    RAISE NOTICE 'Pagamento bolletta completato!';
END $$;

COMMIT;


-- ============================================================================
-- 5. GESTIONE TRANSAZIONE FALLITA (Rollback)
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'TRANSAZIONE FALLITA (Rollback)'
\echo '========================================'

BEGIN;

DO $$
DECLARE
    v_from_account_id INTEGER := 99;  -- Conto inesistente
    v_to_account_id INTEGER := 1;
    v_amount DECIMAL := 5000.00;
BEGIN
    RAISE NOTICE 'Tentativo bonifico da conto inesistente';

    -- Questo fallirà perché il conto non esiste
    UPDATE accounts
    SET balance = balance - v_amount
    WHERE id = v_from_account_id;

    -- Questo codice non verrà mai raggiunto a causa dell'errore sopra
    INSERT INTO transactions (
        from_account_id,
        to_account_id,
        amount,
        transaction_type_id,
        status,
        description
    ) VALUES (
        v_from_account_id,
        v_to_account_id,
        v_amount,
        1,
        'completed',
        'Test'
    );

    RAISE NOTICE 'Questo messaggio non apparirà mai';
END $$;

-- ROLLBACK automatico per errore
-- In PostgreSQL, se una transazione fallisce, tutte le modifiche vengono annullate
ROLLBACK;

\echo 'ROLLBACK eseguito a causa dell''errore. Nessuna modifica applicata.';


-- ============================================================================
-- 6. TRANSAZIONE CON GESTIONE ERRORI (Try/Catch simile)
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'TRANSAZIONE CON GESTIONE ERRORI'
\echo '========================================'

DO $$
DECLARE
    v_from_account_id INTEGER := 1;
    v_to_account_id INTEGER := 2;
    v_amount DECIMAL := 999999.99;  -- Importo eccessivo
    v_balance DECIMAL;
BEGIN
    -- Nuova transazione
    BEGIN
        -- Verifica saldo
        SELECT balance INTO v_balance FROM accounts WHERE id = v_from_account_id;

        IF v_balance < v_amount THEN
            RAISE EXCEPTION 'Fondi insufficienti. Saldo: €%, Richiesto: €%',
                v_balance, v_amount;
        END IF;

        -- Tentativo di bonifico
        UPDATE accounts SET balance = balance - v_amount WHERE id = v_from_account_id;
        UPDATE accounts SET balance = balance + v_amount WHERE id = v_to_account_id;

        RAISE NOTICE 'Bonifico completato';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'Errore catturato: %', SQLERRM;
            RAISE NOTICE 'La transazione è stata automaticamente annullata (rollback).';
            RAISE;
    END;
END $$;


-- ============================================================================
-- 7. BONIFICO MULTIPLA OPERAZIONI (Transazione complessa)
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'BONIFICO COMPLESSO CON PIÙ OPERAZIONI'
\echo '========================================'

BEGIN;

DO $$
DECLARE
    v_from_account_id INTEGER := 3;  -- Giulia Bianchi
    v_to_account_1 INTEGER := 1;     -- Mario Rossi
    v_to_account_2 INTEGER := 6;     -- Luca Ferrari
    v_amount_1 DECIMAL := 300.00;
    v_amount_2 DECIMAL := 200.00;
    v_balance_before DECIMAL;
BEGIN
    RAISE NOTICE 'Eseguo bonifico multiplo: €% a Mario, €% a Luca', v_amount_1, v_amount_2;

    -- Verifica saldo iniziale
    SELECT balance INTO v_balance_before FROM accounts WHERE id = v_from_account_id;

    IF v_balance_before < (v_amount_1 + v_amount_2) THEN
        RAISE EXCEPTION 'Fondi insufficienti per bonifico multiplo!';
    END IF;

    -- Prima operazione
    UPDATE accounts SET balance = balance - v_amount_1 WHERE id = v_from_account_id;
    UPDATE accounts SET balance = balance + v_amount_1 WHERE id = v_to_account_1;

    -- Seconda operazione
    UPDATE accounts SET balance = balance - v_amount_2 WHERE id = v_from_account_id;
    UPDATE accounts SET balance = balance + v_amount_2 WHERE id = v_to_account_2;

    -- Crea transazione master
    INSERT INTO transactions (
        from_account_id,
        to_account_id,
        amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description
    ) VALUES (
        v_from_account_id,
        v_to_account_1,
        v_amount_1,
        1, -- Bonifico
        'completed',
        CURRENT_TIMESTAMP,
        'MULTI-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
        'Bonifico multi-beneficiario - Parte 1'
    );

    INSERT INTO transactions (
        from_account_id,
        to_account_id,
        amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description
    ) VALUES (
        v_from_account_id,
        v_to_account_2,
        v_amount_2,
        1, -- Bonifico
        'completed',
        CURRENT_TIMESTAMP,
        'MULTI-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
        'Bonifico multi-beneficiario - Parte 2'
    );

    RAISE NOTICE 'Bonifico multiplo completato con successo!';
END $$;

COMMIT;

\echo 'Transazioni completate. Tutte le operazioni sono state salvate.';


-- ============================================================================
-- 8. CREAZIONE ESTRTTO CONTO
-- ============================================================================

\echo ''
\echo '========================================'
\echo 'CREAZIONE ESTRATTO CONTO'
\echo '========================================'

BEGIN;

DO $$
DECLARE
    v_account_id INTEGER := 1;
    v_statement_date DATE := CURRENT_DATE;
    v_period_start DATE := DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')::DATE;
    v_period_end DATE := DATE_TRUNC('month', CURRENT_DATE)::DATE - 1;
    v_opening_balance DECIMAL;
    v_closing_balance DECIMAL;
    v_total_debits DECIMAL;
    v_total_credits DECIMAL;
    v_transaction_count INTEGER;
BEGIN
    RAISE NOTICE 'Generazione estratto conto per conto %', v_account_id;
    RAISE NOTICE 'Periodo: % al %', v_period_start, v_period_end;

    -- Saldo di chiusura (saldo attuale)
    SELECT balance INTO v_closing_balance FROM accounts WHERE id = v_account_id;

    -- Calcola totali
    SELECT
        COALESCE(SUM(amount), 0),
        COALESCE(COUNT(*), 0)
    INTO v_total_credits, v_transaction_count
    FROM transactions
    WHERE to_account_id = v_account_id
        AND status = 'completed'
        AND processed_date >= v_period_start
        AND processed_date <= v_period_end;

    SELECT
        COALESCE(SUM(amount), 0)
    INTO v_total_debits
    FROM transactions
    WHERE from_account_id = v_account_id
        AND status = 'completed'
        AND processed_date >= v_period_start
        AND processed_date <= v_period_end;

    -- Calcola saldo di apertura
    v_opening_balance := v_closing_balance - v_total_credits + v_total_debits;

    RAISE NOTICE 'Saldo apertura: €%', v_opening_balance;
    RAISE NOTICE 'Totale addebiti: €%', v_total_debits;
    RAISE NOTICE 'Totale accrediti: €%', v_total_credits;
    RAISE NOTICE 'Saldo chiusura: €%', v_closing_balance;
    RAISE NOTICE 'Numero transazioni: %', v_transaction_count;

    -- Inserisci estratto conto
    INSERT INTO account_statements (
        account_id,
        statement_date,
        period_start,
        period_end,
        opening_balance,
        closing_balance,
        total_debits,
        total_credits,
        transaction_count
    ) VALUES (
        v_account_id,
        v_statement_date,
        v_period_start,
        v_period_end,
        v_opening_balance,
        v_closing_balance,
        v_total_debits,
        v_total_credits,
        v_transaction_count
    );

    RAISE NOTICE 'Estratto conto generato con successo!';
END $$;

COMMIT;

\echo ''
\echo '========================================'
\echo 'RIEPILOGO'
\echo '========================================'
\echo 'Tutte le transazioni sono state eseguite rispettando ACID:'
\echo 'A - Atomicity: Operazioni "tutto o nulla"'
\echo 'C - Consistency: Vincoli e regole rispettati'
\echo 'I - Isolation: Transazioni isolate tra loro'
\echo 'D - Durability: Dati permanenti dopo commit'
