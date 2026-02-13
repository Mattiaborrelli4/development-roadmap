-- =====================================================
-- HR MANAGEMENT SYSTEM - QUICK START GUIDE
-- Guida Rapida per Iniziare
-- =====================================================

-- SEI PRONTO? Questi comandi ti aiuteranno a iniziare subito!

-- =====================================================
-- STEP 1: CREA IL DATABASE
-- =====================================================
-- Apri il terminale o pgAdmin ed esegui:

CREATE DATABASE hr_management;
\c hr_management

-- =====================================================
-- STEP 2: CARICA LO SCHEMA
-- =====================================================
-- Esegui il file schema.sql prima:
psql -U postgres -d hr_management -f schema.sql

-- Oppure in pgAdmin:
-- Apri schema.sql -> Esegui (F5)

-- =====================================================
-- STEP 3: CARICA I DATI DI ESEMPIO
-- =====================================================
-- Esegui sample_data.sql:
psql -U postgres -d hr_management -f sample_data.sql

-- =====================================================
-- STEP 4: ABILITA I TRIGGERS
-- =====================================================
-- Esegui triggers.sql:
psql -U postgres -d hr_management -f triggers.sql

-- =====================================================
-- STEP 5: VERIFICA L'INSTALLAZIONE
-- =====================================================
-- Queste query dovrebbero funzionare subito:

-- 1. Conta i dipendenti
SELECT COUNT(*) AS "Totale Dipendenti" FROM employees;
-- Risultato atteso: 55

-- 2. Lista i dipartimenti
SELECT name AS "Dipartimento", budget AS "Budget €"
FROM departments
ORDER BY name;

-- 3. Vedi i dettagli dipendente
SELECT
    employee_number AS "Matricola",
    first_name || ' ' || last_name AS "Nome",
    email AS "Email"
FROM employees
LIMIT 10;

-- 4. Media stipendi per dipartimento
SELECT
    d.name AS "Dipartimento",
    ROUND(AVG(s.amount), 2) AS "Stipendio Medio",
    COUNT(*) AS "Dipendenti"
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
GROUP BY d.name
ORDER BY "Stipendio Medio" DESC;

-- 5. Vedi organigramma (prime 5 righe)
WITH RECURSIVE org_chart AS (
    SELECT
        id,
        first_name || ' ' || last_name AS name,
        manager_id,
        1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.first_name || ' ' || e.last_name,
        e.manager_id,
        o.level + 1
    FROM employees e
    INNER JOIN org_chart o ON e.manager_id = o.id
)
SELECT
    repeat('   ', level) || name AS "Organigramma"
FROM org_chart
ORDER BY level
LIMIT 10;

-- =====================================================
-- QUERY UTILI RAPIDE
-- =====================================================

-- Trova CEO e Direttori
SELECT
    first_name || ' ' || last_name AS "Executive",
    title AS "Posizione",
    name AS "Dipartimento"
FROM v_employee_details
WHERE title LIKE '%CEO%'
   OR title LIKE '%CTO%'
   OR title LIKE '%CFO%'
   OR title LIKE '%Direttore%'
ORDER BY title;

-- Top 5 stipendi più alti
SELECT
    first_name || ' ' || last_name AS "Dipendente",
    title AS "Posizione",
    amount AS "Stipendio Annuale"
FROM employees e
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
ORDER BY s.amount DESC
LIMIT 5;

-- Dipendenti con più anni di servizio
SELECT
    first_name || ' ' || last_name AS "Dipendente",
    hire_date AS "Data Assunzione",
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) AS "Anni di Servizio",
    amount AS "Stipendio Attuale"
FROM employees e
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
ORDER BY "Anni di Servizio" DESC
LIMIT 10;

-- Presenze ultimo mese
SELECT
    e.first_name || ' ' || e.last_name AS "Dipendente",
    COUNT(*) AS "Giorni Totali",
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS "Presenti",
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS "Assenti",
    SUM(CASE WHEN a.status = 'sick' THEN 1 ELSE 0 END) AS "Malattia"
FROM attendance a
JOIN employees e ON a.employee_id = e.id
WHERE a.attendance_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY e.id, e.first_name, e.last_name
ORDER BY "Giorni Totali" DESC
LIMIT 10;

-- Performance media per dipartimento
SELECT
    d.name AS "Dipartimento",
    ROUND(AVG(pr.rating), 2) AS "Rating Medio",
    COUNT(pr.id) AS "Valutazioni Totali",
    COUNT(DISTINCT pr.employee_id) AS "Dipendenti Valutati"
FROM performance_reviews pr
JOIN employees e ON pr.employee_id = e.id
JOIN departments d ON e.department_id = d.id
WHERE pr.review_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY d.name
ORDER BY "Rating Medio" DESC;

-- =====================================================
-- TEST I TRIGGERS
-- =====================================================

-- TEST 1: Aumento stipendio (crea automaticamente audit log)
BEGIN;
UPDATE salaries
SET amount = 70000
WHERE employee_id = 11 AND end_date IS NULL;

-- Verifica log creato
SELECT * FROM salary_audit_log
WHERE employee_id = 11
ORDER BY change_date DESC
LIMIT 1;
ROLLBACK;  -- Rollback per annullare il test

-- TEST 2: Cambio status dipendente (crea history record)
BEGIN;
UPDATE employees
SET status = 'terminated'
WHERE id = 50;

-- Verifica history
SELECT * FROM employee_status_history
WHERE employee_id = 50
ORDER BY change_date DESC
LIMIT 1;
ROLLBACK;  -- Rollback per annullare il test

-- TEST 3: Trova dipendenti con stipendi fuori range
SELECT
    e.first_name || ' ' || e.last_name AS "Dipendente",
    j.title AS "Posizione",
    s.amount AS "Stipendio",
    j.min_salary AS "Min Range",
    j.max_salary AS "Max Range",
    CASE
        WHEN s.amount < j.min_salary THEN 'Sotto Minimo'
        WHEN s.amount > j.max_salary THEN 'Sopra Massimo'
        ELSE 'Nel Range'
    END AS "Status"
FROM employees e
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
WHERE s.amount < j.min_salary OR s.amount > j.max_salary;

-- =====================================================
-- ESEMPI DI REPORTISTICA
-- =====================================================

-- REPORT 1: Dashboard Dipartimenti
SELECT
    d.name AS "Dipartimento",
    l.city AS "Città",
    l.country AS "Paese",
    COUNT(e.id) AS "Dipendenti",
    ROUND(SUM(s.amount), 2) AS "Costo Totale",
    ROUND(d.budget, 2) AS "Budget",
    ROUND((SUM(s.amount) / NULLIF(d.budget, 0)) * 100, 2) AS "% Budget Usato"
FROM departments d
JOIN locations l ON d.location_id = l.id
LEFT JOIN employees e ON d.id = e.department_id AND e.status = 'active'
LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
GROUP BY d.name, d.budget, l.city, l.country
ORDER BY "Costo Totale" DESC;

-- REPORT 2: Analisi Turnover
SELECT
    d.name AS "Dipartimento",
    COUNT(*) FILTER (WHERE e.status = 'active') AS "Attivi",
    COUNT(*) FILTER (WHERE e.status = 'terminated') AS "Terminati",
    COUNT(*) FILTER (WHERE e.status = 'resigned') AS "Dimissioni",
    COUNT(*) FILTER (WHERE e.status = 'on_leave') AS "In Congedo",
    COUNT(*) AS "Totale"
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.name
ORDER BY "Attivi" DESC;

-- REPORT 3: Distribuzione Job
SELECT
    j.title AS "Posizione",
    COUNT(*) AS "Numero",
    ROUND(AVG(s.amount), 2) AS "Stipendio Medio",
    ROUND(MIN(s.amount), 2) AS "Minimo",
    ROUND(MAX(s.amount), 2) AS "Massimo"
FROM jobs j
LEFT JOIN employees e ON j.id = e.job_id
LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
GROUP BY j.id, j.title
HAVING COUNT(*) > 0
ORDER BY "Stipendio Medio" DESC;

-- =====================================================
-- MANUTENZIONE
-- =====================================================

-- Pulisci il database (ATTENZIONE: elimina tutti i dati!)
-- DROP DATABASE hr_management;

-- Backup rapido
-- pg_dump -U postgres hr_management > backup_hr.sql

-- Ripristina da backup
-- psql -U postgres hr_management < backup_hr.sql

-- Analizza performance
-- VACUUM ANALYZE;

-- =====================================================
-- RISOLUZIONE PROBLEMI
-- =====================================================

-- Problema: "relation already exists"
-- Soluzione: Lo schema è già caricato. Continua con sample_data.sql

-- Problema: "trigger already exists"
-- Soluzione: I trigger sono già attivi. Non serve eseguire triggers.sql di nuovo

-- Problema: "duplicate key value violates unique constraint"
-- Soluzione: I dati sono già caricati. Continua con le query

-- =====================================================
-- RISORSE
-- =====================================================

-- Documentazione PostgreSQL
-- https://www.postgresql.org/docs/

-- Tutorial SQL
-- https://www.w3schools.com/sql/

-- PostgreSQL Cheat Sheet
-- https://www.postgresql.org/docs/current/sql-commands.html

-- =====================================================
-- FINE QUICK START
-- =====================================================

-- Sei pronto! Ora puoi:
-- 1. Esplorare i dati con le query sopra
-- 2. Aprire queries.sql per query avanzate
-- 3. Guardare transactions.sql per esempi pratici
-- 4. Leggere README.md per documentazione completa

-- Buon lavoro! 🚀
