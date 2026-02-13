-- ============================================================================
-- SCHEMA DEL SISTEMA DI TRANSAZIONI FINANZIARIE
-- Database: PostgreSQL
-- Focus: Proprietà ACID, Transazioni, Integrità dei Dati
-- ============================================================================

-- Eliminazione delle tabelle esistenti (in ordine di dipendenza)
DROP TABLE IF EXISTS approvals CASCADE;
DROP TABLE IF EXISTS transaction_log CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS account_statements CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS transaction_types CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ============================================================================
-- TABELLA: customers (Clienti)
-- ============================================================================
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    tax_id VARCHAR(20) UNIQUE NOT NULL,  -- Codice Fiscale/P.IVA
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

-- ============================================================================
-- TABELLA: transaction_types (Tipi di Transazione)
-- ============================================================================
CREATE TABLE transaction_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    description TEXT,
    fee_percentage DECIMAL(5,2) DEFAULT 0.00,
    requires_approval BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

-- ============================================================================
-- TABELLA: accounts (Conti)
-- ============================================================================
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    account_type VARCHAR(20) NOT NULL,  -- 'checking', 'savings', 'credit'
    balance DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'frozen', 'closed', 'blocked'
    credit_limit DECIMAL(15,2) DEFAULT 0.00,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity_date TIMESTAMP WITH TIME ZONE,
    CONSTRAINT valid_account_type CHECK (account_type IN ('checking', 'savings', 'credit')),
    CONSTRAINT valid_status CHECK (status IN ('active', 'frozen', 'closed', 'blocked')),
    CONSTRAINT valid_currency CHECK (currency IN ('EUR', 'USD', 'GBP', 'CHF')),
    CONSTRAINT positive_balance CHECK (
        CASE
            WHEN account_type IN ('checking', 'savings') THEN balance >= 0
            ELSE TRUE  -- I conti di credito possono avere saldo negativo
        END
    ),
    CONSTRAINT credit_limit_valid CHECK (
        CASE
            WHEN account_type = 'credit' THEN balance >= -credit_limit
            ELSE TRUE
        END
    ),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================================================
-- TABELLA: transactions (Transazioni)
-- ============================================================================
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    from_account_id INTEGER,  -- NULL per depositi
    to_account_id INTEGER,    -- NULL per prelievi
    amount DECIMAL(15,2) NOT NULL,
    transaction_type_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'pending', 'completed', 'failed', 'cancelled'
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_date TIMESTAMP WITH TIME ZONE,
    reference VARCHAR(50),
    description TEXT,
    fee_amount DECIMAL(15,2) DEFAULT 0.00,
    CONSTRAINT valid_transaction_status CHECK (status IN ('pending', 'completed', 'failed', 'cancelled', 'awaiting_approval')),
    CONSTRAINT positive_amount CHECK (amount > 0),
    CONSTRAINT either_account CHECK (
        from_account_id IS NOT NULL OR to_account_id IS NOT NULL
    ),
    CONSTRAINT different_accounts CHECK (
        from_account_id IS NULL OR to_account_id IS NULL OR from_account_id != to_account_id
    ),
    CONSTRAINT fk_from_account FOREIGN KEY (from_account_id)
        REFERENCES accounts(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_to_account FOREIGN KEY (to_account_id)
        REFERENCES accounts(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_transaction_type FOREIGN KEY (transaction_type_id)
        REFERENCES transaction_types(id)
);

-- ============================================================================
-- TABELLA: transaction_log (Log delle Transazioni)
-- ============================================================================
CREATE TABLE transaction_log (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    status_from VARCHAR(20),
    status_to VARCHAR(20) NOT NULL,
    changed_by VARCHAR(100),
    changed_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    CONSTRAINT fk_transaction FOREIGN KEY (transaction_id)
        REFERENCES transactions(id)
        ON DELETE CASCADE
);

-- ============================================================================
-- TABELLA: account_statements (Estratti Conto)
-- ============================================================================
CREATE TABLE account_statements (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    statement_date DATE NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    opening_balance DECIMAL(15,2) NOT NULL,
    closing_balance DECIMAL(15,2) NOT NULL,
    total_debits DECIMAL(15,2) NOT NULL,
    total_credits DECIMAL(15,2) NOT NULL,
    transaction_count INTEGER DEFAULT 0,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_period CHECK (period_end >= period_start),
    CONSTRAINT fk_account FOREIGN KEY (account_id)
        REFERENCES accounts(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_statement UNIQUE (account_id, statement_date)
);

-- ============================================================================
-- TABELLA: approvals (Approvazioni)
-- ============================================================================
CREATE TABLE approvals (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    approver_id INTEGER NOT NULL,  -- ID del cliente approvatore o admin
    approval_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    decision VARCHAR(20) NOT NULL,  -- 'approved', 'rejected'
    notes TEXT,
    CONSTRAINT valid_decision CHECK (decision IN ('approved', 'rejected')),
    CONSTRAINT fk_approval_transaction FOREIGN KEY (transaction_id)
        REFERENCES transactions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_approver FOREIGN KEY (approver_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT
);

-- ============================================================================
-- INDICI PER LE PERFORMANCE
-- ============================================================================

-- Indici per ricerche comuni
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_accounts_status ON accounts(status);
CREATE INDEX idx_accounts_account_number ON accounts(account_number);
CREATE INDEX idx_transactions_from_account ON transactions(from_account_id);
CREATE INDEX idx_transactions_to_account ON transactions(to_account_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_date ON transactions(created_date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type_id);
CREATE INDEX idx_transaction_log_transaction ON transaction_log(transaction_id);
CREATE INDEX idx_transaction_log_date ON transaction_log(changed_date);
CREATE INDEX idx_approvals_transaction ON approvals(transaction_id);
CREATE INDEX idx_approvals_approver ON approvals(approver_id);
CREATE INDEX idx_statements_account ON account_statements(account_id);
CREATE INDEX idx_statements_date ON account_statements(statement_date);

-- ============================================================================
-- TRIGGER PER AUTOMAZIONE
-- ============================================================================

-- Funzione per aggiornare last_activity_date
CREATE OR REPLACE FUNCTION update_account_activity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE accounts
    SET last_activity_date = CURRENT_TIMESTAMP
    WHERE id IN (NEW.from_account_id, NEW.to_account_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_activity
    AFTER INSERT ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_account_activity();

-- Funzione per logging automatico dei cambi di stato
CREATE OR REPLACE FUNCTION log_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO transaction_log (transaction_id, status_from, status_to, changed_by, notes)
        VALUES (NEW.id, OLD.status, NEW.status, current_user, 'Stato cambiato automaticamente');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_status_change
    BEFORE UPDATE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION log_status_change();

-- ============================================================================
-- VISTE UTILI
-- ============================================================================

-- Vista per transazioni con dettagli
CREATE OR REPLACE VIEW v_transaction_details AS
SELECT
    t.id,
    t.reference,
    t.amount,
    t.status,
    t.created_date,
    t.processed_date,
    tt.name AS transaction_type_name,
    fa.account_number AS from_account,
    fa.account_type AS from_account_type,
    fc.first_name || ' ' || fc.last_name AS from_customer,
    ta.account_number AS to_account,
    ta.account_type AS to_account_type,
    tc.first_name || ' ' || tc.last_name AS to_customer,
    t.description
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
LEFT JOIN accounts fa ON t.from_account_id = fa.id
LEFT JOIN customers fc ON fa.customer_id = fc.id
LEFT JOIN accounts ta ON t.to_account_id = ta.id
LEFT JOIN customers tc ON ta.customer_id = tc.id;

-- Vista per saldi dei clienti
CREATE OR REPLACE VIEW v_customer_balances AS
SELECT
    c.id AS customer_id,
    c.first_name,
    c.last_name,
    c.tax_id,
    COUNT(a.id) AS total_accounts,
    SUM(CASE WHEN a.account_type = 'checking' THEN a.balance ELSE 0 END) AS checking_balance,
    SUM(CASE WHEN a.account_type = 'savings' THEN a.balance ELSE 0 END) AS savings_balance,
    SUM(CASE WHEN a.account_type = 'credit' THEN a.balance ELSE 0 END) AS credit_balance,
    SUM(a.balance) AS total_balance
FROM customers c
LEFT JOIN accounts a ON c.id = a.customer_id
WHERE a.status != 'closed'
GROUP BY c.id, c.first_name, c.last_name, c.tax_id;

-- ============================================================================
-- COMMENTI
-- ============================================================================

COMMENT ON TABLE customers IS 'Tabella clienti del sistema bancario';
COMMENT ON TABLE accounts IS 'Conti bancari con vincoli ACID per saldi';
COMMENT ON TABLE transactions IS 'Transazioni finanziarie con supporto ACID';
COMMENT ON TABLE transaction_log IS 'Log di audit per tutte le transazioni';
COMMENT ON TABLE transaction_types IS 'Catalogo dei tipi di transazione';
COMMENT ON TABLE account_statements IS 'Estratti conto mensili';
COMMENT ON TABLE approvals IS 'Approvazioni per transazioni che richiedono autorizzazione';

COMMENT ON COLUMN transactions.status IS 'pending: in attesa, completed: completata, failed: fallita, cancelled: cancellata';
COMMENT ON COLUMN accounts.status IS 'active: attivo, frozen: congelato, closed: chiuso, blocked: bloccato';

-- ============================================================================
-- FINE SCHEMA
-- ============================================================================
