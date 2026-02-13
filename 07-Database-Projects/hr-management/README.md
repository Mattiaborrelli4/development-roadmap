# Sistema di Gestione Risorse Umane (HR Management System)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql)
![Database](https://img.shields.io/badge/Database-HR%20System-009639?style=for-the-badge)
![Normalization](https://img.shields.io/badge/Normalization-3NF-blue?style=for-the-badge)

Un database completo per la gestione delle Risorse Umane, progettato per aziende medie-grandi. Sistema normalizzato (3NF) con funzionalità avanzate di tracciamento, reporting e automazione.

## 📋 Indice

- [Caratteristiche](#-caratteristiche)
- [Schema Database](#-schema-del-database)
- [Prerequisiti](#-prerequisiti)
- [Installazione](#-installazione)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Documentazione Schema](#-documentazione-schema)
- [Query Utili](#-query-utili)
- [Triggers e Automazione](#-triggers-e-automazione)
- [Transazioni](#-transazioni)
- [Best Practices](#-best-practices)

## 🌟 Caratteristiche

### Funzionalità Principali

- **Gestione Dipendenti Completa**: Anagrafica, dati contatto, gerarchia organizzativa
- **Tracciamento Stipendi**: Storico completo con date di validità e audit log
- **Job History**: Registro completo di promozioni, trasferimenti e cambi ruolo
- **Performance Management**: Sistema di valutazioni con rating 1-5
- **Gestione Presenze**: Registro ore lavorate, assenze, malattie, ferie
- **Benefit Aziendali**: Gestione assicurazioni, 401k, trasporti, palestra
- **Familiari a Carico**: Anagrafica dipendenti con familiari
- **Automazione**: Triggers per validazione e audit automatico
- **Reporting**: Query complesse per analisi organizzative

### Caratteristiche Tecniche

- ✅ Normalizzazione 3NF (Terza Forma Normale)
- ✅ Integrità Referenziale completa (Foreign Keys)
- ✅ CHECK Constraints per validazione dati
- ✅ Unique Constraints per prevenire duplicati
- ✅ Index per performance ottimale
- ✅ Triggers per automazione e audit
- ✅ Viste materializzate per reporting
- ✅ Transaction support con ACID properties
- ✅ Gestione errori robusta

## 📊 Schema del Database

### Diagramma ER (Entity Relationship)

```
┌─────────────────┐
│   locations     │
├─────────────────┤
│ • id (PK)       │
│ • address       │
│ • city          │
│ • country       │
│ • postal_code   │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐       ┌──────────────┐       ┌──────────────────┐
│  departments   │       │    jobs      │       │    employees     │
├─────────────────┤       ├──────────────┤       ├──────────────────┤
│ • id (PK)       │       │ • id (PK)    │◄──────│ • id (PK)        │
│ • name          │       │ • title      │       │ • employee_number│
│ • location_id   │──────│ • min_salary │       │ • first_name     │
│ • manager_id    │       │ • max_salary │       │ • last_name      │
│ • budget        │       └──────────────┘       │ • email          │
└────────┬────────┘                          │ • phone          │
         │                                   │ • birth_date     │
         │                                   │ • hire_date      │
         │ 1:N                               │ • job_id         │
         ▼                                   │ • department_id  │
┌─────────────────┐                          │ • manager_id     │
│  employees      │                          │ • status         │
├─────────────────┤                          └────────┬─────────┘
│ • id (PK)       │                                   │
│ • ...           │                                   │ 1:N
└────────┬────────┘                                   ▼
         │                           ┌──────────────────────────────┐
         │                           │        salaries              │
         │ 1:N                       ├──────────────────────────────┤
         │                           │ • id (PK)                    │
         ▼                           │ • employee_id                │
┌─────────────────┐                  │ • amount                     │
│  job_history    │                  │ • effective_date             │
├─────────────────┤                  │ • end_date                   │
│ • id (PK)       │                  └──────────────────────────────┘
│ • employee_id   │
│ • start_date    │                  ┌──────────────────────────────┐
│ • end_date      │                  │        attendance            │
│ • job_id        │                  ├──────────────────────────────┤
│ • department_id │                  │ • id (PK)                    │
└─────────────────┘                  │ • employee_id                │
                                    │ • date                       │
┌─────────────────┐                  │ • check_in                   │
│   dependents    │                  │ • check_out                  │
├─────────────────┤                  │ • hours_worked               │
│ • id (PK)       │                  │ • status                     │
│ • employee_id   │                  └──────────────────────────────┘
│ • name          │
│ • relationship │                  ┌──────────────────────────────┐
└─────────────────┘                  │     performance_reviews      │
                                    ├──────────────────────────────┤
┌─────────────────┐                  │ • id (PK)                    │
│    benefits     │                  │ • employee_id                │
├─────────────────┤                  │ • reviewer_id                │
│ • id (PK)       │                  │ • review_date                │
│ • employee_id   │                  │ • rating (1-5)               │
│ • benefit_type  │                  │ • comments                   │
│ • coverage_amt  │                  └──────────────────────────────┘
│ • cost          │
└─────────────────�
```

### Tabelle Principali

| Tabella | Descrizione | Record |
|---------|-------------|--------|
| **locations** | Sedi aziendali | 10 |
| **departments** | Dipartimenti con budget | 10 |
| **jobs** | Posizioni lavorative | 22 |
| **employees** | Anagrafica dipendenti | 55 |
| **salaries** | Storico stipendi | 60+ |
| **job_history** | Storico posizioni | 13 |
| **dependents** | Familiari a carico | 30+ |
| **benefits** | Benefit aziendali | 50+ |
| **performance_reviews** | Valutazioni | 30+ |
| **attendance** | Registro presenze | 250+ |
| **salary_audit_log** | Log audit | Auto |

## 🔧 Prerequisiti

- **PostgreSQL**: versione 15.0 o superiore
- **psql**: client a riga di comando PostgreSQL
- **Spazio disco**: minimo 100 MB
- **RAM**: minimo 512 MB (raccomandato 1 GB+)

### Opzionale

- **pgAdmin**: interfaccia grafica per PostgreSQL
- **DBeaver**: IDE database universale
- **VS Code** con estensione PostgreSQL

## 📦 Installazione

### 1. Clona il Repository

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\07-Database-Projects\hr-management"
```

### 2. Crea il Database

```bash
# Connettiti a PostgreSQL
psql -U postgres

# Crea il database
CREATE DATABASE hr_management;
\c hr_management
```

### 3. Esegui gli Script in Ordine

```bash
# 1. Crea schema e tabelle
psql -U postgres -d hr_management -f schema.sql

# 2. Carica dati di esempio
psql -U postgres -d hr_management -f sample_data.sql

# 3. Configura triggers
psql -U postgres -d hr_management -f triggers.sql
```

### 4. Verifica l'Installazione

```sql
-- Verifica numero dipendenti
SELECT COUNT(*) FROM employees;  -- Dovrebbe restituire 55

-- Verifica stipendi attivi
SELECT COUNT(*) FROM salaries WHERE end_date IS NULL;

-- Verifica tutti i dipartimenti
SELECT name FROM departments ORDER BY name;
```

## 📁 Struttura del Progetto

```
hr-management/
├── schema.sql              # Schema database completo (3NF)
├── sample_data.sql         # Dati realistici per testing
├── queries.sql             # Query complesse per analisi
├── triggers.sql            # Automazione e triggers
├── transactions.sql        # Esempi di transazioni
└── README.md               # Questo file
```

### Descrizione File

#### schema.sql
Definisce la struttura completa del database:

- 10 tabelle principali
- Relazioni foreign key
- CHECK constraints
- Unique constraints
- Index per performance
- Viste materializzate
- Commenti alle tabelle

#### sample_data.sql
Dati di esempio realistici:

- 55 dipendenti
- 10 dipartimenti
- 22 posizioni lavorative
- Storico stipendi
- Job history
- 30+ familiari a carico
- 50+ benefit
- 30+ valutazioni
- 250+ record presenze

#### queries.sql
12 categorie di query avanzate:

1. **Organizational Chart** - Gerarchia ricorsiva con CTE
2. **Salary Ranges** - Analisi stipendi per dipartimento
3. **Employees with Dependents** - JOIN complessi
4. **Tenure Calculation** - Funzioni date
5. **Performance Reviews** - Analisi performance
6. **Attendance** - Analisi assenteismo
7. **Salary History** - Timeline stipendi
8. **Job Changes** - Promozioni e trasferimenti
9. **Budget vs Actual** - Analisi budget
10. **Headcount** - Matrice organizzativa
11. **Anniversaries** - Date importanti
12. **Analytics** - Statistiche avanzate

#### triggers.sql
10 triggers per automazione:

1. **Salary Audit Log** - Traccia ogni cambio stipendio
2. **Auto-update Manager** - Aggiorna manager dipartimento
3. **Salary Validation** - Verifica range stipendi
4. **Status Tracking** - Log cambiamenti status
5. **Job History Validation** - Normalizza storico
6. **Duplicate Prevention** - Evita duplicati presenze
7. **Department Stats** - Calcola statistiche automatiche
8. **Benefit Validation** - Valida iscrizioni benefit
9. **Performance Review Validation** - Valida valutazioni
10. **Dependent Validation** - Valida familiari

#### transactions.sql
Esempi di transazioni ACID:

1. Trasferimento dipartimento
2. Aggiornamento stipendio con audit
3. Aumenti massivi
4. Terminazione dipendente
5. Nuovo assunzione
6. Promozioni
7. Riorganizzazioni
8. Rollback examples
9. Savepoint examples
10. Reporting transazioni

## 📚 Documentazione Schema

### Tabella: employees

```sql
CREATE TABLE employees (
    id                      SERIAL PRIMARY KEY,
    employee_number         VARCHAR(20) UNIQUE NOT NULL,
    first_name              VARCHAR(50) NOT NULL,
    last_name               VARCHAR(50) NOT NULL,
    email                   VARCHAR(100) UNIQUE NOT NULL,
    phone                   VARCHAR(20),
    birth_date              DATE NOT NULL,
    hire_date               DATE NOT NULL,
    termination_date        DATE,
    job_id                  INTEGER NOT NULL,
    department_id           INTEGER NOT NULL,
    manager_id              INTEGER,  -- Self-reference
    status                  VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'terminated', 'on_leave', 'resigned')),
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Campi Chiave:**
- `employee_number`: Codice univoco dipendente
- `manager_id`: Auto-referenza per gerarchia
- `status`: active, terminated, on_leave, resigned
- `email`: Unico e validato con regex

**Indici:**
- `idx_employees_name` (last_name, first_name)
- `idx_employees_email` (email)
- `idx_employees_department` (department_id)
- `idx_employees_status` (status)

### Tabella: salaries

```sql
CREATE TABLE salaries (
    id              SERIAL PRIMARY KEY,
    employee_id     INTEGER NOT NULL,
    amount          DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    effective_date  DATE NOT NULL,
    end_date        DATE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_salary_dates
        CHECK (end_date IS NULL OR end_date >= effective_date)
);
```

**Caratteristiche:**
- Storico completo con date di validità
- Un solo stipendio attivo per dipendente (`end_date IS NULL`)
- Trigger per audit automatico
- Validazione range salariale job

### Tabella: job_history

```sql
CREATE TABLE job_history (
    id              SERIAL PRIMARY KEY,
    employee_id     INTEGER NOT NULL,
    start_date      DATE NOT NULL,
    end_date        DATE,
    job_id          INTEGER NOT NULL,
    department_id   INTEGER NOT NULL,
    reason          VARCHAR(255)
);
```

**Utilizzo:**
- Traccia promozioni, trasferimenti
- Mantenuto automaticamente dai triggers
- Supporta analisi carriere

### Tabella: performance_reviews

```sql
CREATE TABLE performance_reviews (
    id              SERIAL PRIMARY KEY,
    employee_id     INTEGER NOT NULL,
    reviewer_id     INTEGER NOT NULL,  -- Non può essere = employee_id
    review_date     DATE NOT NULL,
    rating          INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments        TEXT,
    goals_met       VARCHAR(10)
        CHECK (goals_met IN ('yes', 'no', 'partial', 'na'))
);
```

**Rating:**
- 5 = Eccellente
- 4 = Molto buono
- 3 = Buono
- 2 = Insufficiente
- 1 = Scarso

## 🔍 Query Utili

### 1. Organizational Chart Completo

```sql
WITH RECURSIVE org_hierarchy AS (
    SELECT
        id,
        first_name || ' ' || last_name AS name,
        job_title,
        manager_id,
        1 AS level
    FROM v_employee_details
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.first_name || ' ' || e.last_name,
        e.job_title,
        e.manager_id,
        o.level + 1
    FROM v_employee_details e
    INNER JOIN org_hierarchy o ON e.manager_id = o.id
)
SELECT
    repeat('....', level) || name AS org_chart,
    job_title,
    level
FROM org_hierarchy
ORDER BY level;
```

### 2. Dipendenti con Stipendi Fuori Range

```sql
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name,
    j.title AS job,
    s.amount AS salary,
    j.min_salary AS min_range,
    j.max_salary AS max_range,
    CASE
        WHEN s.amount < j.min_salary THEN 'Below Range'
        WHEN s.amount > j.max_salary THEN 'Above Range'
        ELSE 'Within Range'
    END AS status
FROM employees e
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
WHERE s.amount < j.min_salary OR s.amount > j.max_salary
ORDER BY ABS(s.amount - (j.min_salary + j.max_salary) / 2) DESC;
```

### 3. Analisi Assenteismo

```sql
SELECT
    d.name AS department,
    COUNT(*) AS total_records,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS days_absent,
    SUM(CASE WHEN a.status = 'sick' THEN 1 ELSE 0 END) AS days_sick,
    ROUND(
        SUM(CASE WHEN a.status IN ('absent', 'sick') THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS absenteeism_rate_pct
FROM attendance a
JOIN employees e ON a.employee_id = e.id
JOIN departments d ON e.department_id = d.id
GROUP BY d.name
ORDER BY absenteeism_rate_pct DESC;
```

### 4. Top Performers

```sql
SELECT
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    j.title AS job,
    ROUND(AVG(pr.rating), 2) AS avg_rating,
    COUNT(pr.id) AS reviews,
    s.amount AS salary,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS tenure_years
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
JOIN performance_reviews pr ON e.id = pr.employee_id
WHERE pr.review_date >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY e.id, e.first_name, e.last_name, d.name, j.title, s.amount, e.hire_date
HAVING AVG(pr.rating) >= 4.0
ORDER BY avg_rating DESC, tenure_years DESC;
```

## ⚙️ Triggers e Automazione

### Salary Audit Trigger

Ogni volta che uno stipendio viene modificato, il trigger crea automaticamente un record di audit:

```sql
-- Esempio: Modifica stipendio
UPDATE salaries
SET amount = 65000
WHERE employee_id = 11 AND end_date IS NULL;

-- Viene creato automaticamente in salary_audit_log:
-- • old_salary: 62000
-- • new_salary: 65000
-- • change_amount: 3000
-- • change_percentage: 4.84%
-- • change_date: timestamp
```

### Salary Validation Trigger

Previene stipendi fuori dal range definito per il job:

```sql
-- Questo fallirà se 500000 è fuori range
INSERT INTO salaries (employee_id, amount, effective_date)
VALUES (1, 500000, CURRENT_DATE);

-- ERRORE: Lo stipendio € 500000.00 supera il massimo consentito (€ 250000.00)
```

### Status Tracking Trigger

Traccia automaticamente i cambiamenti di stato:

```sql
UPDATE employees
SET status = 'terminated'
WHERE id = 2;

-- Effetti automatici:
-- 1. Creazione record in employee_status_history
-- 2. Impostazione termination_date = CURRENT_DATE
-- 3. Log dell'operazione
```

## 💾 Transazioni

### Esempio: Nuova Assunzione

```sql
BEGIN;

-- 1. Crea dipendente
INSERT INTO employees (
    employee_number, first_name, last_name, email,
    hire_date, job_id, department_id, status
) VALUES (
    'EMP100', 'Mario', 'Bianchi', 'mario.bianchi@company.it',
    CURRENT_DATE, 8, 3, 'active'
);

-- 2. Crea stipendio iniziale
INSERT INTO salaries (employee_id, amount, effective_date)
VALUES (currval('employees_id_seq'), 50000, CURRENT_DATE);

-- 3. Crea job history
INSERT INTO job_history (employee_id, start_date, job_id, department_id)
VALUES (currval('employees_id_seq'), CURRENT_DATE, 8, 3);

-- 4. Iscrivi benefit
INSERT INTO benefits (employee_id, benefit_type, cost, enrollment_date)
VALUES (currval('employees_id_seq'), 'health_insurance', 3000, CURRENT_DATE);

COMMIT;
```

### Esempio: Trasferimento con Rollback

```sql
BEGIN;

-- ... operazioni ...

SAVEPOINT sp1;

-- Operazione che potrebbe fallire
UPDATE salaries SET amount = 999999 WHERE employee_id = 12;

-- Se fallisce, torna al savepoint
ROLLBACK TO SAVEPOINT sp1;

-- Continua con altre operazioni
UPDATE salaries SET amount = amount * 1.03 WHERE employee_id = 13;

COMMIT;
```

## 📈 Best Practices

### Performance

1. **Usa gli indici**: Le query frequenti hanno già indici ottimizzati
2. **Evita SELECT ***: Seleziona solo le colonne necessarie
3. **Usa le viste**: `v_employee_details` per query comuni
4. **Limita i risultati**: Usa `LIMIT` per dataset grandi

### Normalizzazione

1. **3NF rispettata**: Nessuna ridondanza dei dati
2. **Tabelle separate**: salaries, job_history in tabelle distinte
3. **Auto-referenza**: employees.manager_id per gerarchie
4. **Lookup tables**: jobs, departments, locations

### Security

1. **Prepared statements**: Previene SQL injection
2. **Validazione lato database**: CHECK constraints
3. **Audit logging**: Traccia ogni modifica importante
4. **Ruoli PostgreSQL**: Configura permessi appropriati

### Manutenzione

```sql
-- VACUUM regolarmente
VACUUM ANALYZE;

-- Ricrea indici se necessario
REINDEX DATABASE hr_management;

-- Backup regolare
pg_dump hr_management > backup.sql
```

## 🐛 Troubleshooting

### Errore: "salary outside job range"

**Causa**: Lo stipendio non è nel range definito per il job

**Soluzione**:
```sql
-- Verifica il range
SELECT title, min_salary, max_salary
FROM jobs
WHERE id = (SELECT job_id FROM employees WHERE id = ?);

-- Aggiorna il range o lo stipendio
UPDATE jobs SET max_salary = 300000 WHERE id = 1;
```

### Errore: "duplicate attendance record"

**Causa**: Esiste già un registro per quel dipendente e data

**Soluzione**:
```sql
-- Verifica duplicati
SELECT * FROM attendance
WHERE employee_id = ? AND attendance_date = '2024-01-01';

-- Aggiorna il record esistente invece di inserire
UPDATE attendance SET status = 'present' WHERE id = ?;
```

### Performance lenta

**Soluzione**:
```sql
-- Analizza le query lente
EXPLAIN ANALYZE SELECT ... ;

-- Ricrea indici
REINDEX TABLE employees;

-- Aggiorna statistiche
ANALYZE employees;
```

## 📞 Supporto

Per domande o problemi:

1. Controlla la documentazione PostgreSQL: https://www.postgresql.org/docs/
2. Verifica gli errori con `SELECT * FROM pg_stat_activity;`
3. Analizza i log: `/var/log/postgresql/`

## 📄 Licenza

Questo progetto è creato a scopo educativo e dimostrativo per portfolio professionale.

## 👨‍💻 Autore

Progetto Database - Portfolio Professionale
- **Database**: PostgreSQL 15+
- **Normalizzazione**: Third Normal Form (3NF)
- **Anno**: 2024

---

**Nota**: Questo database include dati di esempio fittizi. Non utilizzare per dati reali di dipendenti senza adeguata protezione e conformità GDPR.
