# Sistema di Transazioni Finanziarie
## Database PostgreSQL con Focus su ACID, Transazioni e Concorrenza

Questo progetto implementa un database completo per gestire transazioni finanziarie con particolare attenzione alle proprietà ACID, alla gestione delle transazioni e alla concorrenza.

---

## 📋 Indice

- [Panoramica](#panoramica)
- [Proprietà ACID](#proprietà-acid)
- [Struttura del Database](#struttura-del-database)
- [Installazione](#installazione)
- [Transazioni](#transazioni)
- [Concorrenza](#concorrenza)
- [Stored Procedures](#stored-procedures)
- [Query di Reporting](#query-di-reporting)

---

## Panoramica

Questo sistema bancario gestisce:
- **Clienti** e i loro conti bancari
- **Transazioni** tra conti con tracking completo
- **Approvazioni** per operazioni sensibili
- **Estratti conto** mensili
- **Audit log** per compliance
- **Gestione concorrenza** per operazioni simultanee

### Caratteristiche Principali

✅ **ACID Compliance** - Tutte le operazioni rispettano Atomicity, Consistency, Isolation, Durability
✅ **Transaction Support** - Gestione completa di transazioni con rollback
✅ **Concurrency Control** - Livelli di isolamento e lock espliciti
✅ **Audit Trail** - Logging completo di tutte le operazioni
✅ **Data Integrity** - Vincoli e check a livello database
✅ **Error Handling** - Gestione robusta degli errori

---

## Proprietà ACID

### A - Atomicity (Atomicità)

**Tutte le operazioni o nessuna.** Una transazione è indivisibile.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Entrambi gli aggiornamenti sono permanenti
-- Se anche solo uno fallisce, tutto viene annullato (ROLLBACK)
```

**Nel sistema:**
- Ogni bonifico è una transazione atomica
- Se il prelievo dal mittente ha successo ma l'accredito sul beneficiario fallisce, tutto viene annullato
- I saldi rimangono sempre consistenti

### C - Consistency (Coerenza)

**I dati passano sempre da uno stato valido a un altro stato valido.**

```sql
-- Vincolo: Il saldo totale non può mai cambiare in un bonifico
-- Solo la distribuzione cambia
SELECT SUM(balance) FROM accounts;  -- Prima: 100.000 €
-- Bonifico di 500 € dal conto A al conto B
SELECT SUM(balance) FROM accounts;  -- Dopo: 100.000 € (uguale!)
```

**Vincoli implementati:**
```sql
CONSTRAINT positive_balance CHECK (
    CASE
        WHEN account_type IN ('checking', 'savings') THEN balance >= 0
        ELSE TRUE
    END
)
```

**Nel sistema:**
- I conti correnti e di risparmio non possono andare in rosso
- I conti di credito rispettano il limite di fido
- Le somme delle transazioni devono bilanciare

### I - Isolation (Isolamento)

**Le transazioni concorrenti non interferiscono tra loro.**

```sql
-- Livello 1: READ COMMITTED (default)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Legge solo dati commitiati, vulnerabile a non-repeatable reads

-- Livello 2: REPEATABLE READ
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Snapshot all'inizio, letture stabili durante la transazione

-- Livello 3: SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Massimo isolamento, transazioni completamente isolate
```

**Problemi risolti:**

| Problema | Descrizione | Livello che lo previene |
|----------|-------------|------------------------|
| Dirty Read | Leggere dati non ancora committati | Read Committed |
| Non-Repeatable Read | Lo stesso dato cambia durante la transazione | Repeatable Read |
| Phantom Read | Nuove righe appaiono durante la transazione | Serializable |
| Lost Update | Due transazioni sovrascrivono lo stesso dato | Serializable |

### D - Durability (Durata)

**Una volta committata, una transazione è permanente.**

```sql
BEGIN;
-- Modifiche ai dati
COMMIT;
-- I dati sono salvati permanentemente su disco
-- Survivono a crash del server, interruzioni di corrente, etc.
```

**Nel sistema:**
- PostgreSQL garantisce che ogni COMMIT sia scritto su WAL (Write-Ahead Log)
- Le transazioni completate non vengono perse
- Recovery automatico dopo crash

---

## Struttura del Database

### Schema ER

```
┌─────────────┐       ┌──────────────┐       ┌─────────────────┐
│ customers   │──────<│   accounts   │>──────<│  transactions  │
└─────────────┘       └──────────────┘       └─────────────────┘
                                                      │
                                                      │
                                                      v
┌──────────────────┐       ┌────────────────┐   ┌──────────────┐
│transaction_types│       │transaction_log │   │  approvals   │
└──────────────────┘       └────────────────┘   └──────────────┘
                                                      ^
                                                      │
┌──────────────────────┐       ┌─────────────────┐
│account_statements   │──────<│  transactions   │
└──────────────────────┘       └─────────────────┘
```

### Tabelle Principali

#### 1. **customers** - Clienti
```sql
- id: Identificativo unico
- first_name, last_name: Nome e cognome
- tax_id: Codice fiscale / Partita IVA
- email, phone: Contatti
- birth_date: Data di nascita
```

#### 2. **accounts** - Conti Bancari
```sql
- id: Identificativo unico
- account_number: Numero IBAN/conto
- customer_id: Riferimento al cliente
- account_type: checking, savings, credit
- balance: Saldo attuale
- status: active, frozen, closed, blocked
- credit_limit: Limite per conti di credito
```

#### 3. **transactions** - Transazioni
```sql
- id: Identificativo unico
- from_account_id: Conto mittente (NULL per depositi)
- to_account_id: Conto beneficiario (NULL per prelievi)
- amount: Importo
- transaction_type_id: Tipo di transazione
- status: pending, completed, failed, cancelled
- fee_amount: Fee applicate
```

#### 4. **transaction_log** - Log di Audit
```sql
- id: Identificativo unico
- transaction_id: Riferimento alla transazione
- status_from, status_to: Cambiamenti di stato
- changed_by: Chi ha fatto la modifica
- notes: Note aggiuntive
```

#### 5. **approvals** - Approvazioni
```sql
- id: Identificativo unico
- transaction_id: Transazione da approvare
- approver_id: Chi approva
- decision: approved, rejected
- notes: Motivazione
```

#### 6. **account_statements** - Estratti Conto
```sql
- id: Identificativo unico
- account_id: Riferimento al conto
- period_start, period_end: Periodo di riferimento
- opening_balance: Saldo iniziale
- closing_balance: Saldo finale
- total_debits: Totale uscite
- total_credits: Totale entrate
```

---

## Installazione

### Prerequisiti

- PostgreSQL 12 o superiore
- Accesso come superuser o con permessi CREATE DATABASE

### Passo 1: Creare il Database

```bash
# Su Linux/Mac
sudo -u postgres psql
CREATE DATABASE financial_transactions;
\c financial_transactions
```

```bash
# Su Windows
psql -U postgres
CREATE DATABASE financial_transactions;
\c financial_transactions
```

### Passo 2: Eseguire gli Script

```bash
# 1. Creazione schema
psql -U postgres -d financial_transactions -f schema.sql

# 2. Inserimento dati campione
psql -U postgres -d financial_transactions -f sample_data.sql

# 3. Stored procedures (opzionale)
psql -U postgres -d financial_transactions -f procedures.sql
```

### Passo 3: Verifica Installazione

```sql
-- Verifica tabelle create
\dt

-- Verifica dati
SELECT 'customers' AS table, COUNT(*) FROM customers
UNION ALL
SELECT 'accounts', COUNT(*) FROM accounts
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions;
```

---

## Transazioni

### Esempio 1: Bonifico Standard

```sql
-- Inizio transazione
BEGIN;

-- 1. Verifica saldo mittente
SELECT balance FROM accounts WHERE account_number = 'IT00100000000000001';

-- 2. Addebita mittente
UPDATE accounts
SET balance = balance - 500
WHERE account_number = 'IT00100000000000001';

-- 3. Accredita beneficiario
UPDATE accounts
SET balance = balance + 500
WHERE account_number = 'IT00100000000000003';

-- 4. Crea record transazione
INSERT INTO transactions (
    from_account_id,
    to_account_id,
    amount,
    transaction_type_id,
    status,
    processed_date,
    reference
)
SELECT
    (SELECT id FROM accounts WHERE account_number = 'IT00100000000000001'),
    (SELECT id FROM accounts WHERE account_number = 'IT00100000000000003'),
    500,
    1,  -- Bonifico
    'completed',
    CURRENT_TIMESTAMP,
    'BON-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD');

-- 5. Permanenza modifiche
COMMIT;

-- Se c'è un errore, usa ROLLBACK invece di COMMIT
```

### Esempio 2: Gestione Errori

```sql
DO $$
DECLARE
    v_balance DECIMAL;
BEGIN
    -- Inizia blocco transazionale
    BEGIN
        -- Verifica saldo
        SELECT balance INTO v_balance
        FROM accounts
        WHERE account_number = 'IT00100000000000001';

        -- Verifica disponibilità
        IF v_balance < 500 THEN
            RAISE EXCEPTION 'Fondi insufficienti';
        END IF;

        -- Esegui operazioni
        -- ... (codice transazione)

        COMMIT;

    EXCEPTION
        WHEN OTHERS THEN
            -- Rollback automatico
            RAISE NOTICE 'Errore: %', SQLERRM;
            RAISE;
    END;
END $$;
```

### Esempio 3: Stored Procedure

```sql
-- Usa la procedura predefinita
SELECT * FROM transfer_funds(
    'IT00100000000000001',  -- Da conto
    'IT00100000000000003',  -- A conto
    500.00,                  -- Importo
    'Bonifico test',         -- Referenza
    'Pagamento fattura'      -- Descrizione
);

-- Risposta:
-- {
--     "success": true,
--     "transaction_id": 123,
--     "from_account": "IT00100000000000001",
--     "to_account": "IT00100000000000003",
--     "amount": 500.00,
--     "fee": 0,
--     "from_balance_after": 4920.50,
--     "to_balance_after": 3710.75
-- }
```

---

## Concorrenza

### Livelli di Isolamento

PostgreSQL offre 4 livelli di isolamento:

#### 1. READ UNCOMMITTED (Non implementato)
Legge anche dati non ancora committati. **Non usare in finanza.**

#### 2. READ COMMITTED (Default)
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```
- ✅ Legge solo dati committati
- ⚠️ Vulnerabile a non-repeatable reads
- 🚀 **Miglior performance**

**Uso:** Query standard, reportistica

#### 3. REPEATABLE READ
```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```
- ✅ Snapshot all'inizio della transazione
- ✅ Letture stabili durante la transazione
- ⚠️ Può causare serialization failure

**Uso:** Transazioni finanziarie, bonifici

#### 4. SERIALIZABLE
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```
- ✅ Massimo isolamento
- ⚠️ **Peggiore performance**
- ⚠️ Può causare serializzazione failures

**Uso:** Operazioni critiche, trasferimenti grandi importi

### SELECT FOR UPDATE

Lock esplicito delle righe da modificare:

```sql
BEGIN;

-- Lock le righe che verranno modificate
SELECT id, balance
FROM accounts
WHERE account_number = 'IT00100000000000001'
FOR UPDATE;

-- A questo punto nessun''altra transazione può modificare questo conto
-- Altre sessione attendono o falliscono con NOWAIT

UPDATE accounts
SET balance = balance - 100
WHERE account_number = 'IT00100000000000001';

COMMIT;
```

### Gestione Race Conditions

```sql
-- ❌ SBAGLIATO: Due letture separate
SELECT balance INTO v_balance FROM accounts WHERE id = 1;
-- (nel frattempo un''altra transazione modifica il saldo)
IF v_balance >= 100 THEN
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
END IF;

-- ✅ CORRETTO: Update condizionale
UPDATE accounts
SET balance = balance - 100
WHERE id = 1 AND balance >= 100;

IF NOT FOUND THEN
    -- Fondi insufficienti
END IF;
```

### Prevenzione Deadlock

**Regola d'oro:** Lock sempre nello stesso ordine!

```sql
-- ❌ SBAGLIATO (causa deadlock)
-- Sessione 1: Lock A poi B
-- Sessione 2: Lock B poi A

-- ✅ CORRETTO (lock ordinati)
-- Sessione 1: Lock min(A,B) poi max(A,B)
-- Sessione 2: Lock min(A,B) poi max(A,B)

DO $$
DECLARE
    v_acc1_id INTEGER := 1;
    v_acc2_id INTEGER := 2;
BEGIN
    -- Lock sempre dal minore al maggiore
    SELECT id FROM accounts WHERE id = LEAST(v_acc1_id, v_acc2_id) FOR UPDATE;
    SELECT id FROM accounts WHERE id = GREATEST(v_acc1_id, v_acc2_id) FOR UPDATE;

    -- Esegui operazioni
END $$;
```

### Retry Logic per Serialization Failures

```sql
CREATE OR REPLACE FUNCTION transfer_with_retry(
    p_from VARCHAR,
    p_to VARCHAR,
    p_amount DECIMAL
) RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_max_attempts INTEGER := 3;
    v_attempt INTEGER := 0;
BEGIN
    WHILE v_attempt < v_max_attempts LOOP
        BEGIN
            v_attempt := v_attempt + 1;

            -- Tenta il trasferimento
            PERFORM transfer_funds(p_from, p_to, p_amount);

            RETURN 'Successo al tentativo ' || v_attempt;

        EXCEPTION
            WHEN serialization_failure THEN
                -- Riavvia la transazione
                CONTINUE;
        END;
    END LOOP;

    RETURN 'Fallito dopo ' || v_max_attempts || ' tentativi';
END;
$$;
```

---

## Stored Procedures

### 1. transfer_funds()

Trasferimento fondi ACID completo.

```sql
SELECT * FROM transfer_funds(
    'IT00100000000000001',  -- Da
    'IT00100000000000003',  -- A
    500.00,                  -- Importo
    'Ref123',               -- Referenza
    'Bonifico test'         -- Descrizione
);
```

**Caratteristiche:**
- ✅ Verifica disponibilità fondi
- ✅ Lock atomico dei conti
- ✅ Calcolo automatico fee
- ✅ Rollback su errore
- ✅ Audit logging

### 2. get_account_balance()

Recupera saldo con info complete.

```sql
SELECT * FROM get_account_balance('IT00100000000000001');
```

**Ritorna:**
```json
{
    "success": true,
    "account_number": "IT00100000000000001",
    "account_type": "checking",
    "current_balance": 5420.50,
    "pending_debits": 150.00,
    "pending_credits": 500.00,
    "available_balance": 5270.50
}
```

### 3. create_account()

Crea nuovo conto per cliente esistente.

```sql
SELECT * FROM create_account(
    1,              -- customer_id
    'savings',      -- account_type
    1000.00,        -- initial_balance
    'EUR'           -- currency
);
```

### 4. process_daily_batch()

Processa tutte le transazioni pendenti.

```sql
SELECT * FROM process_daily_batch();
```

**Ritorna:**
- `processed`: Numero transazioni elaborate
- `failed`: Numero transazioni fallite
- `skipped`: Numero transazioni saltate

### 5. generate_monthly_statement()

Genera estratto conto mensile.

```sql
SELECT * FROM generate_monthly_statement(
    'IT00100000000000001',  -- account_number
    1,                      -- month (1-12)
    2024                    -- year
);
```

### 6. approve_transaction()

Approva o rifiuta transazioni sensibili.

```sql
SELECT * from approve_transaction(
    123,    -- transaction_id
    1,      -- approver_id
    'approved',  -- decision: 'approved' o 'rejected'
    'Verifica completata'  -- notes
);
```

### 7. freeze_account()

Congela un conto (operazione amministrativa).

```sql
SELECT * FROM freeze_account(
    'IT00100000000000001',
    'Verifica attività sospetta'
);
```

---

## Query di Reporting

### Query 1: Saldo Conto

```sql
SELECT
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer,
    a.account_type,
    a.balance,
    a.currency
FROM accounts a
JOIN customers c ON a.customer_id = c.id
WHERE a.account_number = 'IT00100000000000001';
```

### Query 2: Storico Transazioni

```sql
SELECT
    to_char(t.created_date, 'DD/MM/YYYY HH24:MI') AS date,
    CASE
        WHEN t.from_account_id = 1 THEN 'USCITA'
        ELSE 'ENTRATA'
    END AS direction,
    tt.name AS type,
    t.amount,
    t.status
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.id
WHERE t.from_account_id = 1 OR t.to_account_id = 1
ORDER BY t.created_date DESC;
```

### Query 3: Totali Giornalieri

```sql
SELECT
    t.created_date::DATE AS date,
    COUNT(*) AS transactions,
    SUM(CASE WHEN t.from_account_id IS NOT NULL THEN t.amount ELSE 0 END) AS total_out,
    SUM(CASE WHEN t.to_account_id IS NOT NULL THEN t.amount ELSE 0 END) AS total_in
FROM transactions t
WHERE t.status = 'completed'
    AND t.created_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY t.created_date::DATE
ORDER BY date DESC;
```

### Query 4: Clienti Top per Saldo

```sql
SELECT
    c.first_name || ' ' || c.last_name AS customer,
    COUNT(a.id) AS num_accounts,
    SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a ON c.customer_id = c.id
WHERE a.status = 'active'
GROUP BY c.id, c.first_name, c.last_name
ORDER BY total_balance DESC
LIMIT 10;
```

### Query 5: Verifica Integrità

```sql
-- Verifica che i saldi bilancino
WITH checks AS (
    SELECT
        SUM(CASE WHEN from_account_id IS NOT NULL THEN -amount ELSE 0 END) AS debits,
        SUM(CASE WHEN to_account_id IS NOT NULL THEN amount ELSE 0 END) AS credits
    FROM transactions
    WHERE status = 'completed'
)
SELECT
    debits,
    credits,
    (credits - debits) AS difference,
    CASE
        WHEN (credits - debits) = 0 THEN '✅ OK'
        ELSE '❌ ERRORE'
    END AS status
FROM checks;
```

---

## Troubleshooting

### Deadlock

**Sintomo:**
```
ERROR: deadlock detected
```

**Soluzione:**
1. Identifica le transazioni in conflitto
2. Implementa lock ordinati (vedi sezione Prevenzione Deadlock)
3. Usa retry logic

### Serialization Failure

**Sintomo:**
```
ERROR: could not serialize access due to concurrent update
```

**Soluzione:**
1. Implementa retry logic
2. Usa livello di isolamento più basso se appropriato
3. Riduci durata delle transazioni

### Lock Timeout

**Sintomo:**
```
ERROR: canceling statement due to lock timeout
```

**Soluzione:**
1. Aumenta `lock_timeout`
2. Usa `SELECT FOR UPDATE NOWAIT` per fail fast
3. Identifica lock di lunga durata con `pg_locks`

---

## Performance Tips

### 1. Indici

Già creati nello schema:
```sql
-- Indici frequenti
idx_transactions_from_account
idx_transactions_to_account
idx_transactions_status
idx_transactions_created_date
```

### 2. Partitioning (per grandi volumi)

```sql
-- Partiziona transazioni per data
CREATE TABLE transactions_y2024 PARTITION OF transactions
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### 3. Connection Pooling

Usa PgBouncer per gestire molte connessioni.

### 4. Vacuum Regolare

```sql
-- Configura autovacuum in postgresql.conf
autovacuum = on
autovacuum_analyze_scale_factor = 0.05
```

---

## Compliance e Audit

### Logging Completo

Tutte le operazioni sono loggate in `transaction_log`:

```sql
SELECT * FROM transaction_log
WHERE changed_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY changed_date DESC;
```

### Audit Trail

```sql
-- Chi ha fatto cosa e quando
SELECT
    t.reference,
    tl.changed_date,
    tl.status_from,
    tl.status_to,
    tl.changed_by,
    c.first_name || ' ' || c.last_name AS customer
FROM transaction_log tl
JOIN transactions t ON tl.transaction_id = t.id
JOIN accounts a ON t.from_account_id = a.id OR t.to_account_id = a.id
JOIN customers c ON a.customer_id = c.id
ORDER BY tl.changed_date DESC;
```

---

## Esempi Pratici

### Scenario 1: Bonifico tra Conti

```sql
SELECT * FROM transfer_funds(
    'IT00100000000000001',  -- Mario Rossi
    'IT00100000000000003',  -- Giulia Bianchi
    250.00,
    'Bonifico affitto',
    'Affitto Gennaio 2024'
);
```

### Scenario 2: Deposito Stipendio

```sql
BEGIN;
INSERT INTO transactions (
    to_account_id,
    amount,
    transaction_type_id,
    status,
    processed_date,
    reference,
    description
)
SELECT
    id,
    2500.00,
    9,  -- Stipendio
    'completed',
    CURRENT_TIMESTAMP,
    'STIP-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD'),
    'Accredito stipendiale'
FROM accounts
WHERE account_number = 'IT00100000000000001';

UPDATE accounts
SET balance = balance + 2500.00
WHERE account_number = 'IT00100000000000001';

COMMIT;
```

### Scenario 3: Pagamento Bolletta

```sql
-- Con procedura automatica
SELECT * FROM transfer_funds(
    'IT00100000000000001',  -- Da conto corrente
    'IT00100000000000001',  -- A stesso conto (per transazione tipo 5)
    85.50,
    'BOLL-2024-001',
    'Pagamento bolletta luce'
);
```

---

## Conclusioni

Questo sistema dimostra:

✅ **Implementazione completa delle proprietà ACID**
✅ **Gestione robusta della concorrenza**
✅ **Stored procedures per operazioni critiche**
✅ **Query di reporting avanzate**
✅ **Audit trail per compliance**
✅ **Best practices PostgreSQL**

### Per l'uso in Produzione

- Implementa autenticazione forte
- Cripta dati sensibili (pgcrypto)
- Configura backup regolari
- Monitora performance con pg_stat_statements
- Implementa limitazioni di frequenza (rate limiting)
- Considera partitioning per grandi volumi

---

**Autore:** Portfolio Project
**Database:** PostgreSQL 15+
**Linguaggio:** PL/pgSQL, SQL
**Focus:** ACID, Transazioni, Concorrenza
