# Guida Rapida - Financial Transactions Database

## Setup Rapido

### Windows
```cmd
setup.bat
```

### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
```

### Manuale
```bash
psql -U postgres
CREATE DATABASE financial_transactions;
\c financial_transactions
\i schema.sql
\i sample_data.sql
\i procedures.sql
```

---

## Comandi Essenziali

### Connessione
```bash
psql -U postgres -d financial_transactions
```

### Visualizza tabelle
```sql
\dt
```

### Struttura tabella
```sql
\d accounts
\d transactions
\d customers
```

### Esci
```sql
\q
```

---

## Query Comuni

### 1. Tutti i clienti
```sql
SELECT * FROM customers ORDER BY last_name;
```

### 2. Conti di un cliente
```sql
SELECT * FROM accounts WHERE customer_id = 1;
```

### 3. Saldo conto
```sql
SELECT account_number, balance, status
FROM accounts
WHERE account_number = 'IT00100000000000001';
```

### 4. Ultime transazioni
```sql
SELECT * FROM v_transaction_details
ORDER BY created_date DESC
LIMIT 20;
```

### 5. Transazioni per conto
```sql
SELECT
    to_char(created_date, 'DD/MM/YYYY') AS data,
    amount,
    status,
    description
FROM transactions
WHERE from_account_id = 1 OR to_account_id = 1
ORDER BY created_date DESC;
```

---

## Operazioni con Stored Procedures

### Bonifico
```sql
SELECT * FROM transfer_funds(
    'IT00100000000000001',
    'IT00100000000000003',
    500.00,
    'Bonifico test',
    'Pagamento prova'
);
```

### Verifica saldo
```sql
SELECT * FROM get_account_balance('IT00100000000000001');
```

### Crea conto
```sql
SELECT * FROM create_account(1, 'savings', 1000.00, 'EUR');
```

### Genera estratto
```sql
SELECT * FROM generate_monthly_statement(
    'IT00100000000000001',
    1,
    2024
);
```

---

## Transazioni Manuali

### Bonifico base
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 3;
COMMIT;
```

### Deposito
```sql
BEGIN;
UPDATE accounts SET balance = balance + 500 WHERE id = 1;
INSERT INTO transactions (to_account_id, amount, transaction_type_id, status, reference)
VALUES (1, 500, 3, 'completed', 'DEP-001');
COMMIT;
```

### Rollback su errore
```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
-- Se qualcosa va storto:
ROLLBACK;
```

---

## Concorrenza

### SELECT FOR UPDATE
```sql
BEGIN;
SELECT id, balance FROM accounts
WHERE account_number = 'IT00100000000000001'
FOR UPDATE;

-- Modifiche...
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

### Imposta isolamento
```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- operazioni...
COMMIT;
```

---

## Troubleshooting

### Conta record
```sql
SELECT 'customers' AS tabella, COUNT(*) FROM customers
UNION ALL SELECT 'accounts', COUNT(*) FROM accounts
UNION ALL SELECT 'transactions', COUNT(*) FROM transactions;
```

### Trova transazioni fallite
```sql
SELECT * FROM transactions WHERE status = 'failed';
```

### Verifica lock attivi
```sql
SELECT * FROM pg_locks WHERE NOT granted;
```

### Uccidi connessione bloccata
```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active';
```

---

## File Progetto

| File | Descrizione |
|------|-------------|
| `schema.sql` | Schema database con vincoli ACID |
| `sample_data.sql` | 100+ conti, 50+ clienti, 500+ transazioni |
| `procedures.sql` | 7 stored procedures |
| `queries.sql` | 20+ query di reporting |
| `transactions.sql` | Esempi transazioni ACID |
| `concurrency.sql` | Esempi concorrenza |
| `README.md` | Documentazione completa |
| `QUICKREF.md` | Questa guida |

---

## Proprietà ACID

**A**tomicity - Tutto o nulla
```sql
BEGIN;
-- multiple operazioni
COMMIT;  -- o ROLLBACK
```

**C**onsistency - Dati validi
```sql
-- I vincoli CHECK garantiscono la coerenza
CONSTRAINT positive_balance CHECK (balance >= 0)
```

**I**solation - Transazioni isolate
```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

**D**urability - Dati permanenti
```sql
COMMIT;  -- I dati sono salvati su disco
```

---

## Tips

1. **Usa sempre le stored procedures** per operazioni critiche
2. **Verifica il livello di isolamento** prima di transazioni complesse
3. **Mantieni le transazioni brevi** per ridurre conflitti
4. **Usa SELECT FOR UPDATE** per prevenire race conditions
5. **Monitora i log** per debugging

---

## Risorse

- PostgreSQL Docs: https://www.postgresql.org/docs/
- ACID Properties: README.md
- Concorrenza: concurrency.sql
- Esempi: transactions.sql
