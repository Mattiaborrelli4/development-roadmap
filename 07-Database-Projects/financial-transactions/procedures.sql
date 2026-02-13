-- ============================================================================
-- STORED PROCEDURES
-- Sistema di Transazioni Finanziarie
-- ============================================================================

-- ============================================================================
-- 1. PROCEDURA: transfer_funds
-- Trasferimento fondi tra conti con garanzia ACID
-- ============================================================================

CREATE OR REPLACE FUNCTION transfer_funds(
    p_from_account_number VARCHAR,
    p_to_account_number VARCHAR,
    p_amount DECIMAL,
    p_reference TEXT DEFAULT NULL,
    p_description TEXT DEFAULT NULL
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_from_account_id INTEGER;
    v_to_account_id INTEGER;
    v_from_balance DECIMAL;
    v_to_balance DECIMAL;
    v_from_status VARCHAR;
    v_to_status VARCHAR;
    v_fee_amount DECIMAL := 0;
    v_transaction_id INTEGER;
    v_result JSON;
BEGIN
    -- STEP 1: Validazione input
    IF p_amount <= 0 THEN
        RETURN json_build_object(
            'success', false,
            'error', 'L''importo deve essere maggiore di zero',
            'code', 'INVALID_AMOUNT'
        );
    END IF;

    IF p_from_account_number = p_to_account_number THEN
        RETURN json_build_object(
            'success', false,
            'error', 'I conti mittente e beneficiario devono essere diversi',
            'code', 'SAME_ACCOUNT'
        );
    END IF;

    -- STEP 2: Recupera informazioni conti con LOCK
    SELECT id, balance, status
    INTO v_from_account_id, v_from_balance, v_from_status
    FROM accounts
    WHERE account_number = p_from_account_number
    FOR UPDATE;  -- LOCK della riga per prevenire race conditions

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Conto mittente non trovato',
            'code', 'FROM_ACCOUNT_NOT_FOUND'
        );
    END IF;

    SELECT id, balance, status
    INTO v_to_account_id, v_to_balance, v_to_status
    FROM accounts
    WHERE account_number = p_to_account_number
    FOR UPDATE;  -- LOCK della riga

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Conto beneficiario non trovato',
            'code', 'TO_ACCOUNT_NOT_FOUND'
        );
    END IF;

    -- STEP 3: Verifica stato conti
    IF v_from_status != 'active' THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Il conto mittente non è attivo: ' || v_from_status,
            'code', 'FROM_ACCOUNT_INACTIVE'
        );
    END IF;

    IF v_to_status != 'active' THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Il conto beneficiario non è attivo: ' || v_to_status,
            'code', 'TO_ACCOUNT_INACTIVE'
        );
    END IF;

    -- STEP 4: Verifica disponibilità fondi
    IF v_from_balance < p_amount THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Fondi insufficienti. Saldo: ' || v_from_balance || ', Richiesto: ' || p_amount,
            'code', 'INSUFFICIENT_FUNDS',
            'current_balance', v_from_balance,
            'requested_amount', p_amount
        );
    END IF;

    -- STEP 5: Calcola fee (se applicabile)
    SELECT COALESCE(t.fee_percentage, 0) * p_amount / 100
    INTO v_fee_amount
    FROM transaction_types
    WHERE id = 1;  -- Bonifico standard

    -- STEP 6: Esegui trasferimento
    -- Addebita conto mittente
    UPDATE accounts
    SET
        balance = balance - p_amount - v_fee_amount,
        last_activity_date = CURRENT_TIMESTAMP
    WHERE id = v_from_account_id;

    -- Accredita conto beneficiario
    UPDATE accounts
    SET
        balance = balance + p_amount,
        last_activity_date = CURRENT_TIMESTAMP
    WHERE id = v_to_account_id;

    -- STEP 7: Crea record transazione
    INSERT INTO transactions (
        from_account_id,
        to_account_id,
        amount,
        transaction_type_id,
        status,
        processed_date,
        reference,
        description,
        fee_amount
    ) VALUES (
        v_from_account_id,
        v_to_account_id,
        p_amount,
        1,  -- Bonifico
        'completed',
        CURRENT_TIMESTAMP,
        COALESCE(p_reference, 'TRF-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS')),
        COALESCE(p_description, 'Trasferimento fondi'),
        v_fee_amount
    ) RETURNING id INTO v_transaction_id;

    -- STEP 8: Costruisci risultato
    SELECT
        a1.balance,
        a2.balance
    INTO v_from_balance, v_to_balance
    FROM accounts a1, accounts a2
    WHERE a1.id = v_from_account_id AND a2.id = v_to_account_id;

    v_result := json_build_object(
        'success', true,
        'transaction_id', v_transaction_id,
        'from_account', p_from_account_number,
        'to_account', p_to_account_number,
        'amount', p_amount,
        'fee', v_fee_amount,
        'from_balance_after', v_from_balance,
        'to_balance_after', v_to_balance,
        'timestamp', CURRENT_TIMESTAMP
    );

    -- Log per audit
    INSERT INTO transaction_log (transaction_id, status_from, status_to, changed_by, notes)
    VALUES (v_transaction_id, 'pending', 'completed', current_user, 'Trasferimento completato via stored procedure');

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        -- Rollback automatico
        RETURN json_build_object(
            'success', false,
            'error', SQLERRM,
            'code', 'TRANSACTION_ERROR'
        );
END;
$$;

-- Test della procedura
-- SELECT * FROM transfer_funds('IT00100000000000001', 'IT00100000000000003', 100.00, 'Test transfer');


-- ============================================================================
-- 2. PROCEDURA: process_daily_batch
-- Elabora le transazioni in sospeso
-- ============================================================================

CREATE OR REPLACE FUNCTION process_daily_batch()
    RETURNS TABLE(
        processed INTEGER,
        failed INTEGER,
        skipped INTEGER,
        details JSON
    )
LANGUAGE plpgsql
AS $$
DECLARE
    v_transaction RECORD;
    v_processed INTEGER := 0;
    v_failed INTEGER := 0;
    v_skipped INTEGER := 0;
    v_error_msg TEXT;
BEGIN
    -- Processa tutte le transazioni in stato 'pending'
    FOR v_transaction IN
        SELECT id, from_account_id, to_account_id, amount, transaction_type_id, reference
        FROM transactions
        WHERE status = 'pending'
        FOR UPDATE SKIP LOCKED  -- Skip transazioni già bloccate
    LOOP
        BEGIN
            -- Verifica che i conti siano ancora attivi
            IF EXISTS (
                SELECT 1 FROM accounts
                WHERE id IN (v_transaction.from_account_id, v_transaction.to_account_id)
                    AND status != 'active'
            ) THEN
                UPDATE transactions
                SET status = 'failed'
                WHERE id = v_transaction.id;

                v_failed := v_failed + 1;
                CONTINUE;
            END IF;

            -- Esegui transazione
            IF v_transaction.from_account_id IS NOT NULL THEN
                UPDATE accounts
                SET balance = balance - v_transaction.amount,
                    last_activity_date = CURRENT_TIMESTAMP
                WHERE id = v_transaction.from_account_id;
            END IF;

            IF v_transaction.to_account_id IS NOT NULL THEN
                UPDATE accounts
                SET balance = balance + v_transaction.amount,
                    last_activity_date = CURRENT_TIMESTAMP
                WHERE id = v_transaction.to_account_id;
            END IF;

            -- Aggiorna stato transazione
            UPDATE transactions
            SET status = 'completed',
                processed_date = CURRENT_TIMESTAMP
            WHERE id = v_transaction.id;

            v_processed := v_processed + 1;

        EXCEPTION
            WHEN OTHERS THEN
                v_error_msg := SQLERRM;
                UPDATE transactions
                SET status = 'failed'
                WHERE id = v_transaction.id;

                v_failed := v_failed + 1;
        END;
    END LOOP;

    -- Ritorna risultati
    RETURN QUERY SELECT
        v_processed,
        v_failed,
        v_skipped,
        json_build_object(
            'timestamp', CURRENT_TIMESTAMP,
            'total_processed', v_processed + v_failed + v_skipped
        );
END;
$$;

-- Test della procedura
-- SELECT * FROM process_daily_batch();


-- ============================================================================
-- 3. PROCEDURA: generate_monthly_statement
-- Genera estratto conto mensile
-- ============================================================================

CREATE OR REPLACE FUNCTION generate_monthly_statement(
    p_account_number VARCHAR,
    p_month INTEGER,     -- 1-12
    p_year INTEGER
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_account_id INTEGER;
    v_period_start DATE;
    v_period_end DATE;
    v_statement_date DATE;
    v_opening_balance DECIMAL;
    v_closing_balance DECIMAL;
    v_total_debits DECIMAL;
    v_total_credits DECIMAL;
    v_transaction_count INTEGER;
    v_statement_id INTEGER;
    v_result JSON;
BEGIN
    -- Validazione input
    IF p_month < 1 OR p_month > 12 THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Mese non valido. Deve essere tra 1 e 12'
        );
    END IF;

    IF p_year < 2000 OR p_year > EXTRACT(YEAR FROM CURRENT_DATE) + 1 THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Anno non valido'
        );
    END IF;

    -- Recupera ID conto
    SELECT id INTO v_account_id
    FROM accounts
    WHERE account_number = p_account_number;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Conto non trovato: ' || p_account_number
        );
    END IF;

    -- Calcola periodi
    v_period_start := MAKE_DATE(p_year, p_month, 1);
    v_period_end := (v_period_start + INTERVAL '1 month')::DATE - 1;
    v_statement_date := CURRENT_DATE;

    -- Saldo di chiusura (saldo attuale)
    SELECT balance INTO v_closing_balance
    FROM accounts
    WHERE id = v_account_id;

    -- Calcola totali del periodo
    SELECT
        COALESCE(SUM(t.amount), 0),
        COALESCE(COUNT(t.id), 0)
    INTO v_total_credits, v_transaction_count
    FROM transactions t
    WHERE t.to_account_id = v_account_id
        AND t.status = 'completed'
        AND t.processed_date >= v_period_start
        AND t.processed_date <= v_period_end;

    SELECT COALESCE(SUM(t.amount), 0)
    INTO v_total_debits
    FROM transactions t
    WHERE t.from_account_id = v_account_id
        AND t.status = 'completed'
        AND t.processed_date >= v_period_start
        AND t.processed_date <= v_period_end;

    -- Calcola saldo di apertura
    v_opening_balance := v_closing_balance - v_total_credits + v_total_debits;

    -- Verifica se esiste già un estratto per questo periodo
    IF EXISTS (
        SELECT 1 FROM account_statements
        WHERE account_id = v_account_id
            AND statement_date = v_statement_date
            AND period_start = v_period_start
    ) THEN
        -- Aggiorna estratto esistente
        UPDATE account_statements
        SET
            opening_balance = v_opening_balance,
            closing_balance = v_closing_balance,
            total_debits = v_total_debits,
            total_credits = v_total_credits,
            transaction_count = v_transaction_count
        WHERE account_id = v_account_id
            AND statement_date = v_statement_date
            AND period_start = v_period_start;

        v_result := json_build_object(
            'success', true,
            'message', 'Estratto conto aggiornato',
            'statement_type', 'updated'
        );
    ELSE
        -- Crea nuovo estratto
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
        ) RETURNING id INTO v_statement_id;

        v_result := json_build_object(
            'success', true,
            'statement_id', v_statement_id,
            'message', 'Nuovo estratto conto creato',
            'statement_type', 'created'
        );
    END IF;

    -- Aggiungi dettagli al risultato
    v_result := v_result || json_build_object(
        'account', p_account_number,
        'period', v_period_start || ' - ' || v_period_end,
        'opening_balance', v_opening_balance,
        'closing_balance', v_closing_balance,
        'total_debits', v_total_debits,
        'total_credits', v_total_credits,
        'transaction_count', v_transaction_count,
        'net_change', (v_total_credits - v_total_debits)
    );

    RETURN v_result;
END;
$$;

-- Test della procedura
-- SELECT * FROM generate_monthly_statement('IT00100000000000001', 1, 2024);


-- ============================================================================
-- 4. PROCEDURA: approve_transaction
-- Approva o rifiuta una transazione
-- ============================================================================

CREATE OR REPLACE FUNCTION approve_transaction(
    p_transaction_id INTEGER,
    p_approver_id INTEGER,
    p_decision TEXT,  -- 'approved' o 'rejected'
    p_notes TEXT DEFAULT NULL
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_transaction RECORD;
    v_from_account_id INTEGER;
    v_to_account_id INTEGER;
    v_amount DECIMAL;
    v_result JSON;
BEGIN
    -- Validazione input
    IF p_decision NOT IN ('approved', 'rejected') THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Decisione non valida. Usare ''approved'' o ''rejected'''
        );
    END IF;

    -- Recupera transazione con lock
    SELECT t.*, tt.requires_approval
    INTO v_transaction
    FROM transactions t
    JOIN transaction_types tt ON t.transaction_type_id = tt.id
    WHERE t.id = p_transaction_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Transazione non trovata'
        );
    END IF;

    -- Verifica stato
    IF v_transaction.status != 'awaiting_approval' THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Transazione non in attesa di approvazione. Stato attuale: ' || v_transaction.status
        );
    END IF;

    -- Verifica che richieda approvazione
    IF NOT v_transaction.requires_approval THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Questa transazione non richiede approvazione'
        );
    END IF;

    -- Crea record approvazione
    INSERT INTO approvals (
        transaction_id,
        approver_id,
        decision,
        notes
    ) VALUES (
        p_transaction_id,
        p_approver_id,
        p_decision,
        p_notes
    );

    -- Gestisci decisione
    IF p_decision = 'approved' THEN
        -- Approvata: processa transazione
        v_from_account_id := v_transaction.from_account_id;
        v_to_account_id := v_transaction.to_account_id;
        v_amount := v_transaction.amount;

        -- Addebita
        IF v_from_account_id IS NOT NULL THEN
            UPDATE accounts
            SET balance = balance - v_amount,
                last_activity_date = CURRENT_TIMESTAMP
            WHERE id = v_from_account_id;
        END IF;

        -- Accredita
        IF v_to_account_id IS NOT NULL THEN
            UPDATE accounts
            SET balance = balance + v_amount,
                last_activity_date = CURRENT_TIMESTAMP
            WHERE id = v_to_account_id;
        END IF;

        -- Aggiorna transazione
        UPDATE transactions
        SET status = 'completed',
            processed_date = CURRENT_TIMESTAMP
        WHERE id = p_transaction_id;

        v_result := json_build_object(
            'success', true,
            'message', 'Transazione approvata e processata',
            'transaction_id', p_transaction_id,
            'decision', 'approved'
        );

    ELSE
        -- Rifiutata: aggiorna solo stato
        UPDATE transactions
        SET status = 'cancelled'
        WHERE id = p_transaction_id;

        v_result := json_build_object(
            'success', true,
            'message', 'Transazione rifiutata',
            'transaction_id', p_transaction_id,
            'decision', 'rejected'
        );
    END IF;

    -- Log del cambiamento
    INSERT INTO transaction_log (transaction_id, status_from, status_to, changed_by, notes)
    VALUES (
        p_transaction_id,
        'awaiting_approval',
        CASE WHEN p_decision = 'approved' THEN 'completed' ELSE 'cancelled' END,
        'Approver ID: ' || p_approver_id,
        COALESCE(p_notes, 'Nessuna nota')
    );

    RETURN v_result;
END;
$$;

-- Test della procedura
-- SELECT * FROM approve_transaction(1, 1, 'approved', 'Approvato per verifica');


-- ============================================================================
-- 5. PROCEDURA: get_account_balance
-- Recupera saldo con timestamp corrente
-- ============================================================================

CREATE OR REPLACE FUNCTION get_account_balance(
    p_account_number VARCHAR
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_account RECORD;
    v_pending_debits DECIMAL;
    v_pending_credits DECIMAL;
BEGIN
    -- Recupera informazioni conto
    SELECT a.*,
           c.first_name || ' ' || c.last_name AS customer_name
    INTO v_account
    FROM accounts a
    JOIN customers c ON a.customer_id = c.id
    WHERE a.account_number = p_account_number;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Conto non trovato: ' || p_account_number
        );
    END IF;

    -- Calcola importi pendenti
    SELECT COALESCE(SUM(amount), 0)
    INTO v_pending_debits
    FROM transactions
    WHERE from_account_id = v_account.id
        AND status IN ('pending', 'awaiting_approval');

    SELECT COALESCE(SUM(amount), 0)
    INTO v_pending_credits
    FROM transactions
    WHERE to_account_id = v_account.id
        AND status IN ('pending', 'awaiting_approval');

    RETURN json_build_object(
        'success', true,
        'account_number', v_account.account_number,
        'account_type', v_account.account_type,
        'customer_name', v_account.customer_name,
        'current_balance', v_account.balance,
        'currency', v_account.currency,
        'status', v_account.status,
        'pending_debits', v_pending_debits,
        'pending_credits', v_pending_credits,
        'available_balance', v_account.balance - v_pending_debits,
        'credit_limit', v_account.credit_limit,
        'last_activity', v_account.last_activity_date,
        'timestamp', CURRENT_TIMESTAMP
    );
END;
$$;

-- Test
-- SELECT * FROM get_account_balance('IT00100000000000001');


-- ============================================================================
-- 6. PROCEDURA: create_account
-- Crea un nuovo conto per un cliente esistente
-- ============================================================================

CREATE OR REPLACE FUNCTION create_account(
    p_customer_id INTEGER,
    p_account_type VARCHAR,
    p_initial_balance DECIMAL DEFAULT 0,
    p_currency VARCHAR DEFAULT 'EUR'
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_new_account_number VARCHAR;
    v_new_account_id INTEGER;
    v_branch_code VARCHAR := '001';
    v_sequence INTEGER;
BEGIN
    -- Validazione cliente
    IF NOT EXISTS (SELECT 1 FROM customers WHERE id = p_customer_id) THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Cliente non trovato'
        );
    END IF;

    -- Validazione tipo conto
    IF p_account_type NOT IN ('checking', 'savings', 'credit') THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Tipo conto non valido'
        );
    END IF;

    -- Validazione saldo iniziale
    IF p_initial_balance < 0 AND p_account_type != 'credit' THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Il saldo iniziale non può essere negativo per questo tipo di conto'
        );
    END IF;

    -- Genera numero conto
    SELECT COALESCE(MAX(id), 0) + 1 INTO v_sequence FROM accounts;
    v_new_account_number := 'IT' || v_branch_code || LPAD(v_sequence::TEXT, 15, '0');

    -- Crea conto
    INSERT INTO accounts (
        account_number,
        customer_id,
        account_type,
        balance,
        currency,
        status
    ) VALUES (
        v_new_account_number,
        p_customer_id,
        p_account_type,
        p_initial_balance,
        p_currency,
        'active'
    ) RETURNING id INTO v_new_account_id;

    -- Se c'è un deposito iniziale, crea transazione
    IF p_initial_balance > 0 THEN
        INSERT INTO transactions (
            to_account_id,
            amount,
            transaction_type_id,
            status,
            processed_date,
            reference,
            description
        ) VALUES (
            v_new_account_id,
            p_initial_balance,
            3,  -- Deposito
            'completed',
            CURRENT_TIMESTAMP,
            'DEP-OPEN-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS'),
            'Deposito apertura conto'
        );
    END IF;

    RETURN json_build_object(
        'success', true,
        'account_id', v_new_account_id,
        'account_number', v_new_account_number,
        'account_type', p_account_type,
        'initial_balance', p_initial_balance,
        'currency', p_currency,
        'message', 'Conto creato con successo'
    );
END;
$$;

-- Test
-- SELECT * FROM create_account(1, 'savings', 1000.00, 'EUR');


-- ============================================================================
-- 7. PROCEDURA: freeze_account
-- Congela un conto (operazione amministrativa)
-- ============================================================================

CREATE OR REPLACE FUNCTION freeze_account(
    p_account_number VARCHAR,
    p_reason TEXT
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_account_id INTEGER;
    v_old_status VARCHAR;
BEGIN
    -- Recupera e lock conto
    SELECT id, status INTO v_account_id, v_old_status
    FROM accounts
    WHERE account_number = p_account_number
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Conto non trovato'
        );
    END IF;

    -- Verifica stato attuale
    IF v_old_status = 'frozen' THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Il conto è già congelato'
        );
    END IF;

    IF v_old_status = 'closed' THEN
        RETURN json_build_object(
            'success', false,
            'error', 'Non si può congelare un conto chiuso'
        );
    END IF;

    -- Congela conto
    UPDATE accounts
    SET status = 'frozen'
    WHERE id = v_account_id;

    RETURN json_build_object(
        'success', true,
        'account_number', p_account_number,
        'previous_status', v_old_status,
        'new_status', 'frozen',
        'reason', p_reason,
        'timestamp', CURRENT_TIMESTAMP
    );
END;
$$;

-- Test
-- SELECT * FROM freeze_account('IT00100000000000001', 'Verifica attività sospetta');


-- ============================================================================
-- INFO PROCEDURE
-- ============================================================================
COMMENT ON FUNCTION transfer_funds IS 'Trasferimento fondi ACID tra conti';
COMMENT ON FUNCTION process_daily_batch IS 'Processa batch di transazioni pendenti';
COMMENT ON FUNCTION generate_monthly_statement IS 'Genera estratto conto mensile';
COMMENT ON FUNCTION approve_transaction IS 'Approva o rifiuta transazione';
COMMENT ON FUNCTION get_account_balance IS 'Recupera saldo e info conto';
COMMENT ON FUNCTION create_account IS 'Crea nuovo conto cliente';
COMMENT ON FUNCTION freeze_account IS 'Congela conto temporaneamente';
