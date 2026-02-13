-- ============================================================================
-- ESEMPI DI CONCORRENZA E ISOLAMENTO
-- Sistema di Transazioni Finanziarie
-- ============================================================================

\echo '============================================================'
\echo 'DEMO LIVELLI DI ISOLAMENTO E CONCORRENZA'
\echo '============================================================'

-- ============================================================================
-- INTRODUZIONE AI LIVELLI DI ISOLAMENTO
-- ============================================================================

\echo ''
\echo 'LIVELLI DI ISOLAMENTO POSTGRESQL:'
\echo '================================'
\echo ''
\echo '1. READ UNCOMMITTED (non implementato in PostgreSQL)'
\echo '   - Lettura dati non commitmenti (dirty reads)'
\echo '   - Non raccomandato per transazioni finanziarie'
\echo ''
\echo '2. READ COMMITTED (default in PostgreSQL)'
\echo '   - Legge solo dati commitmenti'
\echo '   - Protegge da dirty reads'
\echo '   - Vulnerabile a non-repeatable reads e phantom reads'
\echo ''
\echo '3. REPEATABLE READ'
\echo '   - Garantisce letture ripetibili'
\echo '   - Snapshot all''inizio della transazione'
\echo '   - Può causare serialization failure'
\echo ''
\echo '4. SERIALIZABLE'
\echo '   - Isolamento completo'
\echo '   - Massima protezione'
\echo '   - Migliori performance overhead'


-- ============================================================================
-- 1. DEMO: READ COMMITTED (livello default)
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 1: READ COMMITTED (Default)'
\echo '============================================================'

-- Sessione 1: Inizia transazione
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

\echo 'Sessione 1: Inizio transazione READ COMMITTED'

-- Legge il saldo del conto 1
SELECT
    account_number,
    balance AS initial_balance_session1
FROM accounts
WHERE account_number = 'IT00100000000000001';

-- A questo punto, Sessione 1 ha letto il saldo
-- Nota: In un ambiente reale, un''altra sessione potrebbe modificare
-- il saldo e Sessione 1 vedrebbe il nuovo valore al prossimo SELECT

-- Per simulare, modifichiamo il saldo nella stessa sessione
UPDATE accounts
SET balance = balance - 100
WHERE account_number = 'IT00100000000000001';

\echo 'Sessione 1: Saldo aggiornato (ancora non committato)'

-- Legge il saldo modificato
SELECT
    account_number,
    balance AS updated_balance_session1
FROM accounts
WHERE account_number = 'IT00100000000000001';

ROLLBACK;

\echo 'Sessione 1: ROLLBACK eseguito'
\echo 'Nota: Modifiche annullate'


-- ============================================================================
-- 2. DEMO: REPEATABLE READ
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 2: REPEATABLE READ'
\echo '============================================================'

BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

\echo 'Sessione 1: Inizio transazione REPEATABLE READ'

-- Primo snapshot: leggiamo i saldi
DROP TABLE IF EXISTS temp_balance_snapshot;
CREATE TEMP TABLE temp_balance_snapshot AS
SELECT
    account_number,
    balance AS snapshot_balance
FROM accounts
WHERE account_number IN ('IT00100000000000001', 'IT00100000000000003');

SELECT * FROM temp_balance_snapshot;

\echo 'Sessione 1: Snapshot creato - saldi bloccati per questa transazione'

-- Simula un ritardo (in produzione, qui altre sessioni potrebbero modificare)
SELECT pg_sleep(1);

-- Qualsiasi modifica fatta qui non interferirà con il nostro snapshot
UPDATE accounts
SET balance = balance + 500
WHERE account_number = 'IT00100000000000003';

SELECT
    account_number,
    balance AS after_update_balance
FROM accounts
WHERE account_number = 'IT00100000000000003';

COMMIT;

\echo 'Sessione 1: COMMIT eseguito'
\echo 'Nota: Le letture all''interno della transazione vedono sempre lo snapshot iniziale'


-- ============================================================================
-- 3. DEMO: SERIALIZABLE - Massima Isolazione
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 3: SERIALIZABLE (Massima Protezione)'
\echo '============================================================'

BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

\echo 'Sessione 1: Inizio transazione SERIALIZABLE'

-- Questa transazione è completamente isolata
-- Se un''altra transazione tentasse di modificare gli stessi dati,
-- PostgreSQL genererebbe un errore di serializzazione

-- Legge informazioni conti
SELECT
    account_number,
    balance,
    account_type
FROM accounts
WHERE account_number IN ('IT00100000000000001', 'IT00100000000000006')
ORDER BY account_number;

-- Esegue un trasferimento
UPDATE accounts
SET balance = balance - 200
WHERE account_number = 'IT00100000000000001';

UPDATE accounts
SET balance = balance + 200
WHERE account_number = 'IT00100000000000006';

-- Verifica
SELECT
    account_number,
    balance AS final_balance
FROM accounts
WHERE account_number IN ('IT00100000000000001', 'IT00100000000000006')
ORDER BY account_number;

COMMIT;

\echo 'Sessione 1: COMMIT SERIALIZABLE eseguito con successo'


-- ============================================================================
-- 4. USO DEI LOCK - SELECT FOR UPDATE
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 4: LOCK SELETTIVO (SELECT FOR UPDATE)'
\echo '============================================================'

-- Simula una transazione che deve prenotare fondi
BEGIN;

\echo 'Sessione 1: Inizio blocco conti con SELECT FOR UPDATE'

-- Lock specifico delle righe che verranno modificate
SELECT
    account_number,
    balance
FROM accounts
WHERE account_number = 'IT00100000000000001'
FOR UPDATE;  -- LOCK della riga

\echo 'Sessione 1: Conto IT00100000000000001 LOCKATO'
\echo 'Nota: In un ambiente multi-sessione, nessun''altra transazione può modificare questo conto'

-- Verifica fondi
SELECT
    account_number,
    balance,
    status
FROM accounts
WHERE account_number = 'IT00100000000000001';

-- Esegue il bonifico
UPDATE accounts
SET balance = balance - 150,
    last_activity_date = CURRENT_TIMESTAMP
WHERE account_number = 'IT00100000000000001';

UPDATE accounts
SET balance = balance + 150,
    last_activity_date = CURRENT_TIMESTAMP
WHERE account_number = 'IT00100000000000003';

-- Crea transazione
INSERT INTO transactions (
    from_account_id,
    to_account_id,
    amount,
    transaction_type_id,
    status,
    processed_date,
    reference,
    description
)
SELECT
    (SELECT id FROM accounts WHERE account_number = 'IT00100000000000001'),
    (SELECT id FROM accounts WHERE account_number = 'IT00100000000000003'),
    150,
    1,  -- Bonifico
    'completed',
    CURRENT_TIMESTAMP,
    'LOCK-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
    'Bonifico con lock esplicito';

COMMIT;

\echo 'Sessione 1: COMMIT eseguito, lock rilasciato'


-- ============================================================================
-- 5. DEMO: LOCK NOWAIT - Gestione concorrenza aggressiva
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 5: LOCK CON NOWAIT (fail fast)'
\echo '============================================================'

BEGIN;

\echo 'Sessione 1: Tentativo lock immediato'

-- Tenta di ottenere il lock senza attendere
DO $$
DECLARE
    v_account_id INTEGER;
BEGIN
    -- Tenta il lock con NOWAIT
    SELECT id INTO v_account_id
    FROM accounts
    WHERE account_number = 'IT00100000000000001'
    FOR UPDATE NOWAIT;  -- Se già lockato, fallisce immediatamente

    RAISE NOTICE 'Lock ottenuto con successo!';
END $$;

-- Modifica il saldo
UPDATE accounts
SET balance = balance - 50
WHERE account_number = 'IT00100000000000001';

\echo 'Sessione 1: Modifica completata'

COMMIT;

\echo 'Sessione 1: COMMIT eseguito'


-- ============================================================================
-- 6. PREVENZIONE DEADLOCK
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 6: PREVENZIONE DEADLOCK'
\echo '============================================================'
\echo 'Regola d''oro: LOCK sempre le righe nello stesso ordine!'
\echo ''

-- ❌ APPROCCIO SBAGLIATO (può causare deadlock)
\echo 'APPROCCIO SBAGLIATO (da evitare):'
\echo 'Sessione 1: Lock conto A, poi conto B'
\echo 'Sessione 2: Lock conto B, poi conto A'
\echo 'Risultato: DEADLOCK!'
\echo ''

-- ✅ APPROCCIO CORRETTO
\echo 'APPROCCIO CORRETTO (ordinamento per ID):'

BEGIN;

-- LOCK sempre in ordine di ID (minore a maggiore)
DO $$
DECLARE
    v_acc1_id INTEGER;
    v_acc2_id INTEGER;
    v_min_id INTEGER;
    v_max_id INTEGER;
BEGIN
    SELECT id INTO v_acc1_id FROM accounts WHERE account_number = 'IT00100000000000001';
    SELECT id INTO v_acc2_id FROM accounts WHERE account_number = 'IT00100000000000003';

    v_min_id := LEAST(v_acc1_id, v_acc2_id);
    v_max_id := GREATEST(v_acc1_id, v_acc2_id);

    -- LOCK sempre dal minore al maggiore
    SELECT id FROM accounts WHERE id = v_min_id FOR UPDATE;
    SELECT id FROM accounts WHERE id = v_max_id FOR UPDATE;

    RAISE NOTICE 'Lock ottenuti in ordine: %, then %', v_min_id, v_max_id;
END $$;

COMMIT;

\echo 'Deadlock prevenuto con lock ordinati!'


-- ============================================================================
-- 7. GESTIONE RACE CONDITIONS
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 7: GESTIONE RACE CONDITION'
\echo '============================================================'

-- Scenario: Due prelievi simultanei dallo stesso conto
-- Soluzione: Usare un''unico UPDATE con condition

DO $$
DECLARE
    v_account_number VARCHAR := 'IT00100000000000001';
    v_withdrawal_amount DECIMAL := 100;
    v_rows_affected INTEGER;
BEGIN
    -- Tenta il prelievo in un''unica operazione atomica
    UPDATE accounts
    SET
        balance = balance - v_withdrawal_amount,
        last_activity_date = CURRENT_TIMESTAMP
    WHERE account_number = v_account_number
        AND balance >= v_withdrawal_amount;

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;

    IF v_rows_affected = 0 THEN
        RAISE NOTICE 'Prelievo fallito: fondi insufficienti';
    ELSE
        RAISE NOTICE 'Prelievo riuscito: €%', v_withdrawal_amount;

        -- Crea transazione solo se l''update ha successo
        INSERT INTO transactions (
            from_account_id,
            amount,
            transaction_type_id,
            status,
            processed_date,
            reference,
            description
        )
        SELECT
            id,
            v_withdrawal_amount,
            4,  -- Prelievo
            'completed',
            CURRENT_TIMESTAMP,
            'RACE-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
            'Prelievo con gestione race condition'
        FROM accounts
        WHERE account_number = v_account_number;
    END IF;
END $$;

\echo 'Race condition gestita con UPDATE condizionale'


-- ============================================================================
-- 8. SIMULAZIONE CONCORRENZA REALE
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 8: SIMULAZIONE MULTI-SESSIONE'
\echo '============================================================'

-- Creiamo una funzione per simulare una transazione concorrente
CREATE OR REPLACE FUNCTION concurrent_transfer_test(
    p_acc1 VARCHAR,
    p_acc2 VARCHAR,
    p_amount DECIMAL
) RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_balance1 DECIMAL;
    v_attempts INTEGER := 0;
    v_max_attempts INTEGER := 3;
BEGIN
    -- Retry loop per gestire serialization failures
    WHILE v_attempts < v_max_attempts LOOP
        BEGIN
            v_attempts := v_attempts + 1;

            -- Inizia transazione con REPEATABLE READ
            BEGIN
                -- Verifica saldo e lock
                SELECT balance INTO v_balance1
                FROM accounts
                WHERE account_number = p_acc1
                FOR UPDATE;

                IF v_balance1 < p_amount THEN
                    RETURN 'Fondi insufficienti';
                END IF;

                -- Esegui trasferimento
                UPDATE accounts
                SET balance = balance - p_amount
                WHERE account_number = p_acc1;

                UPDATE accounts
                SET balance = balance + p_amount
                WHERE account_number = p_acc2;

                -- Crea transazione
                INSERT INTO transactions (
                    from_account_id,
                    to_account_id,
                    amount,
                    transaction_type_id,
                    status,
                    processed_date,
                    reference,
                    description
                )
                SELECT
                    (SELECT id FROM accounts WHERE account_number = p_acc1),
                    (SELECT id FROM accounts WHERE account_number = p_acc2),
                    p_amount,
                    1,
                    'completed',
                    CURRENT_TIMESTAMP,
                    'CONC-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
                    'Test concorrenza';

                RETURN 'Trasferimento completato in ' || v_attempts || ' tentativi(i)';

            EXCEPTION
                WHEN serialization_failure THEN
                    -- Riavvia la transazione
                    IF v_attempts >= v_max_attempts THEN
                        RETURN 'Errore: troppe collisioni (' || v_max_attempts || ' tentativi)';
                    END IF;
                WHEN OTHERS THEN
                    RETURN 'Errore: ' || SQLERRM;
            END;

        COMMIT;
        RETURN 'Successo';

        EXCEPTION
            WHEN OTHERS THEN
                ROLLBACK;
                IF v_attempts >= v_max_attempts THEN
                    RETURN 'Fallito dopo ' || v_max_attempts || ' tentativi';
                END IF;
        END;
    END LOOP;

    RETURN 'Timeout';
END;
$$;

-- Test della funzione
SELECT concurrent_transfer_test('IT00100000000000001', 'IT00100000000000003', 75.00);


-- ============================================================================
-- 9. ESEMPI DI LIVELLI DI ISOLAMENTO IN CONFRONTO
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 9: CONFRONTO LIVELLI ISOLAMENTO'
\echo '============================================================'

-- Tabella riassuntiva dei problemi risolti
CREATE TEMP TABLE isolation_levels (
    level VARCHAR,
    dirty_reads BOOLEAN,
    non_repeatable_reads BOOLEAN,
    phantom_reads BOOLEAN,
    performance_impact VARCHAR,
    use_case VARCHAR
);

INSERT INTO isolation_levels VALUES
('READ UNCOMMITTED', TRUE, TRUE, TRUE, 'Minimo', 'Mai in finanza'),
('READ COMMITTED', FALSE, TRUE, TRUE, 'Basso', 'Query standard, reporting'),
('REPEATABLE READ', FALSE, FALSE, TRUE, 'Medio', 'Transazioni bancarie'),
('SERIALIZABLE', FALSE, FALSE, FALSE, 'Alto', 'Operazioni critiche');

SELECT * FROM isolation_levels;


-- ============================================================================
-- 10. ADVISORY LOCKS - Lock applicativi custom
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 10: ADVISORY LOCKS (Lock Applicativi)'
\echo '============================================================'

-- Gli advisory locks permettono di creare lock custom a livello applicazione
-- Utili per coordinare operazioni complesse

DO $$
DECLARE
    v_lock_key INTEGER := 12345;  -- Chiave univoca per l''operazione
    v_lock_obtained BOOLEAN;
BEGIN
    -- Tenta di ottenere un advisory lock esclusivo
    v_lock_obtained := pg_try_advisory_lock(v_lock_key);

    IF v_lock_obtained THEN
        RAISE NOTICE 'Lock ottenuto! Esecuzione operazione critica...';

        -- Simula operazione critica
        SELECT pg_sleep(1);

        -- Rilascia il lock
        PERFORM pg_advisory_unlock(v_lock_key);

        RAISE NOTICE 'Lock rilasciato, operazione completata';
    ELSE
        RAISE NOTICE 'Impossibile ottenere lock, operazione già in corso';
    END IF;
END $$;


-- ============================================================================
-- 11. TRANSAZIONI AUTONOME (autonomous transactions)
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'ESEMPIO 11: LOGGING CON AUTONOMOUS TRANSACTION'
\echo '============================================================'

-- PostgreSQL non supporta vere autonomous transactions
-- Possiamo simulare con dblink o procedure separate

-- Esempio: Logging che persiste anche se la transazione principale fallisce
CREATE OR REPLACE FUNCTION log_transaction_attempt(
    p_operation VARCHAR,
    p_details TEXT
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Questo log persiste indipendentemente dal commit/rollback della transazione chiamante
    INSERT INTO transaction_log (transaction_id, status_from, status_to, changed_by, notes)
    VALUES (
        0,  -- Transaction ID 0 = operazione di sistema
        'system',
        'logged',
        current_user,
        p_operation || ': ' || p_details
    );
END;
$$;

-- Utilizzo
SELECT log_transaction_attempt('BANK_TRANSFER', 'Tentativo bonifico tra conti');


-- ============================================================================
-- RIEPILOGO
-- ============================================================================

\echo ''
\echo '============================================================'
\echo 'RIEPILOGO CONCORRENZA'
\echo '============================================================'
\echo ''
\echo 'BEST PRACTICE:'
\echo '1. Usa READ COMMITTED per query standard'
\echo '2. Usa REPEATABLE READ per transazioni finanziarie'
\echo '3. Usa SERIALIZABLE solo per operazioni critiche'
\echo '4. LOCK sempre le righe nello stesso ordine'
\echo '5. Usa SELECT FOR UPDATE per modifiche esplicite'
\echo '6. Gestisci serialization failures con retry logic'
\echo '7. Considera advisory locks per coordinamento applicativo'
\echo '8. Mantieni le transazioni brevi'
\echo '9. Evita lock espliciti quando possibile'
\echo '10. Monitora deadlocks e performance'
