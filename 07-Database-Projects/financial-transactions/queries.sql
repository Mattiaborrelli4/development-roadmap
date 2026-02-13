-- ============================================================================
-- QUERY DI REPORTING E ANALISI
-- Sistema di Transazioni Finanziarie
-- ============================================================================

\echo '=========================================='
\echo 'QUERY 1: Verifica Saldo Conto'
\echo '=========================================='

-- Recupera il saldo attuale di un conto specifico
-- Parametro: Sostituisci il valore di account_number
SELECT
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    a.account_type,
    a.balance,
    a.currency,
    a.status,
    a.created_date,
    a.last_activity_date
FROM accounts a
JOIN customers c ON a.customer_id = c.id
WHERE a.account_number = 'IT00100000000000001';  -- Modifica questo valore

\echo ''
\echo '=========================================='
\echo 'QUERY 2: Storico Transazioni per Conto'
\echo '=========================================='

-- Visualizza tutte le transazioni di un conto (sia in uscita che in entrata)
-- Mostra anche il saldo running (cumulativo)
WITH all_transactions AS (
    -- Transazioni in uscita
    SELECT
        t.id,
        t.created_date,
        t.reference,
        'USCITA' AS direction,
        t.amount,
        t.status,
        tt.name AS transaction_type,
        COALESCE(ac2.account_number, 'N/A') AS other_account
    FROM transactions t
    JOIN transaction_types tt ON t.transaction_type_id = tt.id
    LEFT JOIN accounts ac2 ON t.to_account_id = ac2.id
    WHERE t.from_account_id = (SELECT id FROM accounts WHERE account_number = 'IT00100000000000001')

    UNION ALL

    -- Transazioni in entrata
    SELECT
        t.id,
        t.created_date,
        t.reference,
        'ENTRATA' AS direction,
        t.amount,
        t.status,
        tt.name AS transaction_type,
        COALESCE(ac1.account_number, 'N/A') AS other_account
    FROM transactions t
    JOIN transaction_types tt ON t.transaction_type_id = tt.id
    LEFT JOIN accounts ac1 ON t.from_account_id = ac1.id
    WHERE t.to_account_id = (SELECT id FROM accounts WHERE account_number = 'IT00100000000000001')
)
SELECT
    to_char(created_date, 'DD/MM/YYYY HH24:MI') AS date_time,
    direction,
    transaction_type,
    amount,
    status,
    other_account
FROM all_transactions
ORDER BY created_date DESC
LIMIT 50;

\echo ''
\echo '=========================================='
\echo 'QUERY 3: Riepilogo Tutti i Conti Cliente'
\echo '=========================================='

-- Mostra tutti i conti di un cliente con saldo totale
SELECT
    c.id AS customer_id,
    c.first_name,
    c.last_name,
    c.tax_id,
    c.email,
    c.phone,
    a.account_number,
    a.account_type,
    a.balance,
    a.currency,
    a.status,
    a.created_date
FROM customers c
LEFT JOIN accounts a ON c.id = a.customer_id
WHERE c.id = 1  -- Sostituisci con l'ID del cliente
ORDER BY a.account_type, a.created_date;

\echo ''
\echo '=========================================='
\echo 'QUERY 4: Totali Transazioni Giornalieri'
\echo '=========================================='

-- Report delle transazioni per giorno
SELECT
    t.created_date::DATE AS transaction_date,
    to_char(t.created_date, 'Day') AS day_name,
    COUNT(*) AS transaction_count,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) AS completed_count,
    COUNT(CASE WHEN t.status = 'failed' THEN 1 END) AS failed_count,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) AS pending_count,
    COALESCE(SUM(CASE WHEN t.from_account_id IS NOT NULL THEN t.amount ELSE 0 END), 0) AS total_debits,
    COALESCE(SUM(CASE WHEN t.to_account_id IS NOT NULL THEN t.amount ELSE 0 END), 0) AS total_credits,
    COALESCE(SUM(t.fee_amount), 0) AS total_fees
FROM transactions t
WHERE t.created_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY t.created_date::DATE, to_char(t.created_date, 'Day')
ORDER BY transaction_date DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 5: Report Transazioni Fallite'
\echo '=========================================='

-- Analisi delle transazioni fallite
SELECT
    t.id,
    t.reference,
    tt.name AS transaction_type,
    a1.account_number AS from_account,
    c1.first_name || ' ' || c1.last_name AS from_customer,
    a2.account_number AS to_account,
    c2.first_name || ' ' || c2.last_name AS to_customer,
    t.amount,
    t.description,
    t.created_date,
    tl.notes AS failure_reason
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
LEFT JOIN accounts a1 ON t.from_account_id = a1.id
LEFT JOIN customers c1 ON a1.customer_id = c1.id
LEFT JOIN accounts a2 ON t.to_account_id = a2.id
LEFT JOIN customers c2 ON a2.customer_id = c2.id
LEFT JOIN transaction_log tl ON t.id = tl.transaction_id AND tl.status_to = 'failed'
WHERE t.status = 'failed'
ORDER BY t.created_date DESC
LIMIT 100;

\echo ''
\echo '=========================================='
\echo 'QUERY 6: Approvazioni In Attesa'
\echo '=========================================='

-- Transazioni che richiedono approvazione
SELECT
    t.id,
    t.created_date,
    tt.name AS transaction_type,
    a1.account_number AS from_account,
    c1.first_name || ' ' || c1.last_name AS from_customer,
    a2.account_number AS to_account,
    c2.first_name || ' ' || c2.last_name AS to_customer,
    t.amount,
    t.reference,
    t.description,
    CASE
        WHEN tt.requires_approval THEN 'Required'
        ELSE 'Not Required'
    END AS approval_status,
    tt.requires_approval,
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - t.created_date)) AS days_pending
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
LEFT JOIN accounts a1 ON t.from_account_id = a1.id
LEFT JOIN customers c1 ON a1.customer_id = c1.id
LEFT JOIN accounts a2 ON t.to_account_id = a2.id
LEFT JOIN customers c2 ON a2.customer_id = c2.id
WHERE t.status IN ('pending', 'awaiting_approval')
    AND tt.requires_approval = TRUE
ORDER BY t.created_date ASC;

\echo ''
\echo '=========================================='
\echo 'QUERY 7: Generazione Estratto Conto (per periodo)'
\echo '=========================================='

-- Genera estratto conto per un periodo specifico
WITH account_info AS (
    SELECT
        a.id,
        a.account_number,
        c.first_name || ' ' || c.last_name AS customer_name,
        a.balance AS current_balance
    FROM accounts a
    JOIN customers c ON a.customer_id = c.id
    WHERE a.account_number = 'IT00100000000000001'  -- Modifica qui
),
period_transactions AS (
    SELECT
        t.created_date,
        t.reference,
        CASE
            WHEN t.from_account_id = (SELECT id FROM account_info) THEN 'USCITA'
            ELSE 'ENTRATA'
        END AS direction,
        tt.name AS transaction_type,
        t.amount,
        t.description,
        t.status
    FROM transactions t
    JOIN transaction_types tt ON t.transaction_type_id = tt.id
    WHERE (t.from_account_id = (SELECT id FROM account_info)
           OR t.to_account_id = (SELECT id FROM account_info))
        AND t.status = 'completed'
        AND t.processed_date >= '2024-01-01'  -- Data inizio - Modifica qui
        AND t.processed_date < '2024-02-01'   -- Data fine - Modifica qui
),
opening_balance AS (
    SELECT
        COALESCE(SUM(CASE WHEN direction = 'ENTRATA' THEN amount ELSE -amount END), 0) AS period_change
    FROM period_transactions
)
SELECT
    ai.customer_name,
    ai.account_number,
    (ai.current_balance - COALESCE(ob.period_change, 0)) AS opening_balance,
    COALESCE(SUM(CASE WHEN direction = 'USCITA' THEN amount ELSE 0 END), 0) AS total_debits,
    COALESCE(SUM(CASE WHEN direction = 'ENTRATA' THEN amount ELSE 0 END), 0) AS total_credits,
    ai.current_balance AS closing_balance,
    COUNT(*) AS transaction_count
FROM account_info ai
CROSS JOIN opening_balance ob
LEFT JOIN period_transactions pt ON 1=1
GROUP BY ai.customer_name, ai.account_number, ai.current_balance, ob.period_change;

\echo ''
\echo '=========================================='
\echo 'QUERY 8: Analisi Attività Conto'
\echo '=========================================='

-- Statistiche di utilizzo del conto
SELECT
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    a.account_type,
    a.balance,
    COUNT(t.id) AS total_transactions,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) AS completed_transactions,
    COUNT(CASE WHEN t.status = 'failed' THEN 1 END) AS failed_transactions,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) AS pending_transactions,
    COALESCE(SUM(CASE WHEN t.from_account_id = a.id THEN t.amount ELSE 0 END), 0) AS total_sent,
    COALESCE(SUM(CASE WHEN t.to_account_id = a.id THEN t.amount ELSE 0 END), 0) AS total_received,
    COALESCE(SUM(t.fee_amount), 0) AS total_fees_paid,
    MAX(t.created_date) AS last_transaction_date,
    a.created_date AS account_opened_date,
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - a.created_date)) AS days_open
FROM accounts a
JOIN customers c ON a.customer_id = c.id
LEFT JOIN transactions t ON (a.id = t.from_account_id OR a.id = t.to_account_id)
WHERE a.account_number = 'IT00100000000000001'  -- Modifica qui
GROUP BY a.id, c.first_name, c.last_name;

\echo ''
\echo '=========================================='
\echo 'QUERY 9: Top 10 Clienti per Saldo Totale'
\echo '=========================================='

-- Clienti con i saldi più elevati
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    c.tax_id,
    c.email,
    COUNT(a.id) AS total_accounts,
    SUM(a.balance) AS total_balance,
    SUM(CASE WHEN a.account_type = 'checking' THEN a.balance ELSE 0 END) AS checking_balance,
    SUM(CASE WHEN a.account_type = 'savings' THEN a.balance ELSE 0 END) AS savings_balance,
    SUM(CASE WHEN a.account_type = 'credit' THEN a.balance ELSE 0 END) AS credit_balance
FROM customers c
JOIN accounts a ON c.id = a.customer_id
WHERE a.status = 'active'
GROUP BY c.id, c.first_name, c.last_name, c.tax_id, c.email
ORDER BY total_balance DESC
LIMIT 10;

\echo ''
\echo '=========================================='
\echo 'QUERY 10: Transazioni per Tipo e Stato'
\echo '=========================================='

-- Statistiche aggregate per tipo di transazione
SELECT
    tt.name AS transaction_type,
    tt.code,
    tt.fee_percentage,
    COUNT(t.id) AS total_count,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) AS completed,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) AS pending,
    COUNT(CASE WHEN t.status = 'failed' THEN 1 END) AS failed,
    COUNT(CASE WHEN t.status = 'cancelled' THEN 1 END) AS cancelled,
    COALESCE(SUM(CASE WHEN t.status = 'completed' THEN t.amount ELSE 0 END), 0) AS total_amount_processed,
    COALESCE(SUM(t.fee_amount), 0) AS total_fees_collected,
    COALESCE(AVG(CASE WHEN t.status = 'completed' THEN t.amount END), 0) AS avg_transaction_amount
FROM transaction_types tt
LEFT JOIN transactions t ON tt.id = t.transaction_type_id
GROUP BY tt.id, tt.name, tt.code, tt.fee_percentage
ORDER BY total_amount_processed DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 11: Conti Congelati o Bloccati'
\echo '=========================================='

-- Report conti con problemi
SELECT
    a.account_number,
    a.account_type,
    a.status,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.phone,
    a.balance,
    a.credit_limit,
    a.last_activity_date,
    COUNT(t.id) AS pending_transactions,
    CASE
        WHEN a.status = 'frozen' THEN 'Conto congelato - richiede intervento'
        WHEN a.status = 'blocked' THEN 'Conto bloccato - verifica necessaria'
        WHEN a.status = 'closed' THEN 'Conto chiuso'
        ELSE 'Attivo'
    END AS status_description
FROM accounts a
JOIN customers c ON a.customer_id = c.id
LEFT JOIN transactions t ON a.id = t.from_account_id AND t.status = 'pending'
WHERE a.status IN ('frozen', 'blocked', 'closed')
GROUP BY a.id, c.id
ORDER BY a.status, a.last_activity_date DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 12: Audit Log delle Transazioni'
\echo '=========================================='

-- Log completo delle modifiche allo stato delle transazioni
SELECT
    t.reference,
    tl.changed_date,
    tl.status_from,
    tl.status_to,
    tl.changed_by,
    tl.notes,
    a1.account_number AS from_account,
    a2.account_number AS to_account,
    t.amount
FROM transaction_log tl
JOIN transactions t ON tl.transaction_id = t.id
LEFT JOIN accounts a1 ON t.from_account_id = a1.id
LEFT JOIN accounts a2 ON t.to_account_id = a2.id
WHERE t.created_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY tl.changed_date DESC
LIMIT 100;

\echo ''
\echo '=========================================='
\echo 'QUERY 13: Riepilogo Mensile per Cliente'
\echo '=========================================='

-- Report mensile attività cliente
SELECT
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    DATE_TRUNC('month', t.created_date) AS month,
    COUNT(DISTINCT t.id) AS total_transactions,
    COUNT(DISTINCT CASE WHEN t.from_account_id IN (SELECT id FROM accounts WHERE customer_id = c.id) THEN t.id END) AS outgoing_transactions,
    COUNT(DISTINCT CASE WHEN t.to_account_id IN (SELECT id FROM accounts WHERE customer_id = c.id) THEN t.id END) AS incoming_transactions,
    COALESCE(SUM(CASE WHEN t.from_account_id IN (SELECT id FROM accounts WHERE customer_id = c.id) THEN t.amount ELSE 0 END), 0) AS total_sent,
    COALESCE(SUM(CASE WHEN t.to_account_id IN (SELECT id FROM accounts WHERE customer_id = c.id) THEN t.amount ELSE 0 END), 0) AS total_received,
    COALESCE(SUM(t.fee_amount), 0) AS total_fees
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN transactions t ON (t.from_account_id = a.id OR t.to_account_id = a.id)
WHERE t.status = 'completed'
    AND t.created_date >= DATE_TRUNC('year', CURRENT_DATE)
GROUP BY c.id, c.first_name, c.last_name, DATE_TRUNC('month', t.created_date)
ORDER BY c.id, month DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 14: Verifica Integrità Contabile'
\echo '=========================================='

-- Verifica che i saldi siano consistenti (somma zero = OK)
WITH transaction_balances AS (
    SELECT
        SUM(CASE
            WHEN from_account_id IS NOT NULL THEN -amount
            ELSE 0
        END) AS total_debits,
        SUM(CASE
            WHEN to_account_id IS NOT NULL THEN amount
            ELSE 0
        END) AS total_credits
    FROM transactions
    WHERE status = 'completed'
)
SELECT
    total_debits,
    total_credits,
    (total_credits - total_debits) AS balance_difference,
    CASE
        WHEN (total_credits - total_debits) = 0 THEN 'INTEGRAZIONE OK'
        ELSE 'ERRORE DI INTEGRAZIONE'
    END AS integrity_status
FROM transaction_balances;

\echo ''
\echo '=========================================='
\echo 'QUERY 15: Saldo Totale del Sistema'
\echo '=========================================='

-- Somma di tutti i saldi (per verifica)
SELECT
    account_type,
    currency,
    COUNT(*) AS account_count,
    SUM(balance) AS total_balance,
    AVG(balance) AS average_balance,
    MIN(balance) AS minimum_balance,
    MAX(balance) AS maximum_balance
FROM accounts
WHERE status != 'closed'
GROUP BY account_type, currency
ORDER BY account_type, currency;

\echo ''
\echo '=========================================='
\echo 'QUERY 16: Tempo Medio di Elaborazione'
\echo '=========================================='

-- Analisi tempo di elaborazione transazioni
SELECT
    tt.name AS transaction_type,
    COUNT(*) AS transaction_count,
    AVG(EXTRACT(EPOCH FROM (processed_date - created_date))/60) AS avg_minutes_to_process,
    MIN(EXTRACT(EPOCH FROM (processed_date - created_date))/60) AS min_minutes_to_process,
    MAX(EXTRACT(EPOCH FROM (processed_date - created_date))/60) AS max_minutes_to_process,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (processed_date - created_date))/60) AS median_minutes
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
WHERE t.status = 'completed'
    AND t.processed_date IS NOT NULL
GROUP BY tt.name
ORDER BY avg_minutes_to_process DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 17: Ricerca Transazioni per Importo'
\echo '=========================================='

-- Trova transazioni per intervallo di importo
SELECT
    t.id,
    t.reference,
    t.created_date,
    tt.name AS transaction_type,
    t.amount,
    t.status,
    a1.account_number AS from_account,
    c1.first_name || ' ' || c1.last_name AS from_customer,
    a2.account_number AS to_account,
    c2.first_name || ' ' || c2.last_name AS to_customer
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
LEFT JOIN accounts a1 ON t.from_account_id = a1.id
LEFT JOIN customers c1 ON a1.customer_id = c1.id
LEFT JOIN accounts a2 ON t.to_account_id = a2.id
LEFT JOIN customers c2 ON a2.customer_id = c2.id
WHERE t.amount BETWEEN 100 AND 500  -- Modifica intervallo qui
    AND t.status = 'completed'
ORDER BY t.amount DESC
LIMIT 50;

\echo ''
\echo '=========================================='
\echo 'QUERY 18: Report Approvazioni'
\echo '=========================================='

-- Storico approvazioni
SELECT
    t.reference,
    t.created_date AS transaction_date,
    tt.name AS transaction_type,
    t.amount,
    c.first_name || ' ' || c.last_name AS approver,
    a.approval_date,
    a.decision,
    a.notes AS approval_notes
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
JOIN approvals a ON t.id = a.transaction_id
JOIN customers c ON a.approver_id = c.id
WHERE t.created_date >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY a.approval_date DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 19: Clienti Inattivi'
\echo '=========================================='

-- Clienti senza transazioni da X giorni
SELECT
    c.id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.phone,
    MAX(a.last_activity_date) AS last_activity,
    COUNT(a.id) AS total_accounts,
    COALESCE(SUM(a.balance), 0) AS total_balance,
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - MAX(a.last_activity_date))) AS days_inactive
FROM customers c
JOIN accounts a ON c.id = a.customer_id
GROUP BY c.id, c.first_name, c.last_name, c.email, c.phone
HAVING MAX(a.last_activity_date) < CURRENT_TIMESTAMP - INTERVAL '90 days'
ORDER BY days_inactive DESC;

\echo ''
\echo '=========================================='
\echo 'QUERY 20: Prospetto Cash Flow Giornaliero'
\echo '=========================================='

-- Analisi flusso di cassa giornaliero
WITH daily_flow AS (
    SELECT
        t.created_date::DATE AS flow_date,
        COALESCE(SUM(CASE WHEN t.from_account_id IS NOT NULL THEN t.amount ELSE 0 END), 0) AS cash_out,
        COALESCE(SUM(CASE WHEN t.to_account_id IS NOT NULL THEN t.amount ELSE 0 END), 0) AS cash_in,
        COALESCE(SUM(t.fee_amount), 0) AS fees_in
    FROM transactions t
    WHERE t.status = 'completed'
        AND t.created_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY t.created_date::DATE
)
SELECT
    flow_date,
    cash_in,
    cash_out,
    fees_in,
    (cash_in - cash_out) AS net_flow,
    (cash_in - cash_out + fees_in) AS net_flow_with_fees,
    LAG(cash_in - cash_out + fees_in, 1, 0) OVER (ORDER BY flow_date) AS previous_net_flow,
    SUM(cash_in - cash_out + fees_in) OVER (ORDER BY flow_date) AS cumulative_flow
FROM daily_flow
ORDER BY flow_date DESC;
