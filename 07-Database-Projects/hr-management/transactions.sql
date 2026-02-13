-- =====================================================
-- HR MANAGEMENT SYSTEM - TRANSACTIONS
-- Esempi di Transazioni SQL per Operazioni HR
-- =====================================================
-- Database: PostgreSQL
-- Contenuto: Transazioni complesse con ACID properties
-- =====================================================

-- Nota: Queste transazioni mostrano operazioni reali
-- che dovrebbero essere eseguite come blocco atomico

-- =====================================================
-- 1. TRASFERIMENTO DIPENDENTE TRA DIPARTIMENTI
-- =====================================================
-- Scenario: Trasferire un dipendente con tutto il suo contesto
-- Impatto: employees, job_history, salaries, department_statistics

-- ESEMPIO 1: Trasferimento semplice
BEGIN;

    -- 1. Definisci variabili per il trasferimento
    -- Sostituisci con ID reali
    DO $$
    DECLARE
        v_employee_id INTEGER := 11;  -- ID dipendente da trasferire
        v_new_department_id INTEGER := 4;  -- Nuovo dipartimento (es. Marketing)
        v_old_department_id INTEGER;
        v_employee_name TEXT;
        v_old_dept_name TEXT;
        v_new_dept_name TEXT;
        v_new_job_id INTEGER;
        v_transfer_date DATE := CURRENT_DATE;
        v_salary_amount DECIMAL(12,2);
    BEGIN
        -- Recupera informazioni
        SELECT e.department_id,
               e.first_name || ' ' || e.last_name,
               e.job_id
        INTO v_old_department_id, v_employee_name, v_new_job_id
        FROM employees e
        WHERE e.id = v_employee_id;

        SELECT name INTO v_old_dept_name FROM departments WHERE id = v_old_department_id;
        SELECT name INTO v_new_dept_name FROM departments WHERE id = v_new_department_id;
        SELECT amount INTO v_salary_amount FROM salaries WHERE employee_id = v_employee_id AND end_date IS NULL;

        RAISE NOTICE 'Trasferimento di % da % a %',
            v_employee_name, v_old_dept_name, v_new_dept_name;

        -- 2. Chiudi il job history corrente
        UPDATE job_history
        SET end_date = v_transfer_date - 1,
            reason = 'Transfer to ' || v_new_dept_name
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- 3. Crea nuovo job history
        INSERT INTO job_history (
            employee_id, start_date, job_id, department_id, reason
        ) VALUES (
            v_employee_id, v_transfer_date, v_new_job_id,
            v_new_department_id, 'Transfer from ' || v_old_dept_name
        );

        -- 4. Aggiorna dipartimento dipendente
        UPDATE employees
        SET department_id = v_new_department_id,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = v_employee_id;

        -- 5. Log della transazione
        INSERT INTO employee_status_history (
            employee_id, old_status, new_status, reason, changed_by
        ) VALUES (
            v_employee_id,
            'Dept ' || v_old_department_id,
            'Dept ' || v_new_department_id,
            'Transfer: ' || v_old_dept_name || ' -> ' || v_new_dept_name,
            current_user
        );

        -- 6. Aggiorna statistiche (il trigger si attiverà automaticamente)
        -- Forza aggiornamento esplicito se necessario
        PERFORM update_department_statistics();

        COMMIT;

        RAISE NOTICE 'Trasferimento completato con successo!';
    END;
    $$;

END;

-- ESEMPIO 2: Trasferimento con cambio posizione (promozione)
BEGIN;

    DO $$
    DECLARE
        v_employee_id INTEGER := 12;
        v_old_dept_id INTEGER;
        v_new_dept_id INTEGER := 4;
        v_old_job_id INTEGER;
        v_new_job_id INTEGER;
        v_new_salary DECIMAL(12,2);
        v_old_salary DECIMAL(12,2);
    BEGIN
        -- Recupera stato corrente
        SELECT department_id, job_id
        INTO v_old_dept_id, v_old_job_id
        FROM employees
        WHERE id = v_employee_id;

        SELECT amount INTO v_old_salary
        FROM salaries
        WHERE employee_id = v_employee_id AND end_date IS NULL;

        -- Nuovi valori (personalizzabili)
        v_new_job_id := 13; -- Marketing Specialist
        v_new_salary := v_old_salary * 1.10; -- Aumento 10%

        -- Chiudi job history vecchio
        UPDATE job_history
        SET end_date = CURRENT_DATE - 1
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- Nuovo job history
        INSERT INTO job_history (employee_id, start_date, job_id, department_id, reason)
        VALUES (v_employee_id, CURRENT_DATE, v_new_job_id, v_new_dept_id, 'Promotion & Transfer');

        -- Aggiorna employee
        UPDATE employees
        SET department_id = v_new_dept_id,
            job_id = v_new_job_id
        WHERE id = v_employee_id;

        -- Chiudi vecchio stipendio
        UPDATE salaries
        SET end_date = CURRENT_DATE - 1
        WHERE employee_id = v_employee_id AND end_date IS NULL;

        -- Nuovo stipendio
        INSERT INTO salaries (employee_id, amount, effective_date)
        VALUES (v_employee_id, v_new_salary, CURRENT_DATE);

        COMMIT;
        RAISE NOTICE 'Promozione e trasferimento completati!';
    END;
    $$;

END;

-- =====================================================
-- 2. AGGIORNAMENTO STIPENDIO CON AUDIT COMPLETO
-- =====================================================
-- Scenario: Aumento stipendio con tracciamento completo
-- Utilizza le transazioni per garantire consistenza

BEGIN;

    DO $$
    DECLARE
        v_employee_id INTEGER := 14;
        v_increase_percentage DECIMAL(5,2) := 8.5; -- Aumento 8.5%
        v_reason TEXT := 'Performance review 2024 - Excellent rating';
        v_old_salary DECIMAL(12,2);
        v_new_salary DECIMAL(12,2);
        v_employee_name TEXT;
        v_job_min DECIMAL(12,2);
        v_job_max DECIMAL(12,2);
    BEGIN
        -- Recupera stipendio attuale
        SELECT s.amount,
               e.first_name || ' ' || e.last_name,
               j.min_salary,
               j.max_salary
        INTO v_old_salary, v_employee_name, v_job_min, v_job_max
        FROM salaries s
        JOIN employees e ON s.employee_id = e.id
        JOIN jobs j ON e.job_id = j.id
        WHERE s.employee_id = v_employee_id
        AND s.end_date IS NULL;

        -- Calcola nuovo stipendio
        v_new_salary := v_old_salary * (1 + v_increase_percentage / 100);

        -- Valida range
        IF v_new_salary > v_job_max THEN
            RAISE EXCEPTION 'ERRORE: Nuovo stipendio % supera il massimo job (%)',
                v_new_salary, v_job_max;
        END IF;

        -- Chiudi stipendio vecchio
        UPDATE salaries
        SET end_date = CURRENT_DATE - 1
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- Inserisci nuovo stipendio
        INSERT INTO salaries (employee_id, amount, effective_date)
        VALUES (v_employee_id, v_new_salary, CURRENT_DATE);

        -- L'audit log viene creato automaticamente dal trigger
        -- Ma possiamo aggiungere note aggiuntive
        UPDATE salary_audit_log
        SET reason = v_reason
        WHERE id = (
            SELECT id FROM salary_audit_log
            WHERE employee_id = v_employee_id
            ORDER BY change_date DESC
            LIMIT 1
        );

        COMMIT;

        RAISE NOTICE 'Stipendio aggiornato per %: € % -> € % (+% %)',
            v_employee_name, v_old_salary, v_new_salary, v_increase_percentage;
    END;
    $$;

END;

-- =====================================================
-- 3. AUMENTO STIPENDI MASSIVO (PER DIPARTIMENTO)
-- =====================================================
-- Scenario: Aumento generalizzato per dipartimento
-- Tipo: Batch transaction con error handling

BEGIN;

    DO $$
    DECLARE
        v_department_id INTEGER := 3; -- Informatica
        v_increase_pct DECIMAL(5,2) := 5.0; -- 5% aumento
        v_min_tenure_years INTEGER := 2; -- Solo dipendenti con 2+ anni
        v_updated_count INTEGER := 0;
        v_total_cost_increase DECIMAL(15,2) := 0;
        emp_record RECORD;
        v_old_sal DECIMAL(12,2);
        v_new_sal DECIMAL(12,2);
    BEGIN
        -- Loop attraverso dipendenti qualificati
        FOR emp_record IN
            SELECT e.id, s.amount
            FROM employees e
            JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
            WHERE e.department_id = v_department_id
            AND e.status = 'active'
            AND EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= v_min_tenure_years
        LOOP
            v_old_sal := emp_record.amount;
            v_new_sal := v_old_sal * (1 + v_increase_pct / 100);

            -- Chiudi vecchio stipendio
            UPDATE salaries
            SET end_date = CURRENT_DATE - 1
            WHERE employee_id = emp_record.id
            AND end_date IS NULL;

            -- Nuovo stipendio
            INSERT INTO salaries (employee_id, amount, effective_date)
            VALUES (emp_record.id, v_new_sal, CURRENT_DATE);

            v_updated_count := v_updated_count + 1;
            v_total_cost_increase := v_total_cost_increase + (v_new_sal - v_old_sal);
        END LOOP;

        COMMIT;

        RAISE NOTICE 'Aumenti completati: % dipendenti, Costo totale aggiuntivo: € %',
            v_updated_count, v_total_cost_increase;
    END;
    $$;

END;

-- =====================================================
-- 4. TERMINAZIONE DIPENDENTE (CASCADE EFFECTS)
-- =====================================================
-- Scenario: Licenziamento volontario/involontario
-- Impatta: employees, salaries, benefits, access

BEGIN;

    DO $$
    DECLARE
        v_employee_id INTEGER := 20;
        v_termination_date DATE := CURRENT_DATE;
        v_termination_reason TEXT := 'Resignation - New opportunity';
        v_employee_name TEXT;
        v_department_id INTEGER;
        v_final_salary DECIMAL(12,2);
    BEGIN
        -- Recupera informazioni
        SELECT e.first_name || ' ' || e.last_name,
               e.department_id,
               s.amount
        INTO v_employee_name, v_department_id, v_final_salary
        FROM employees e
        LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
        WHERE e.id = v_employee_id;

        -- 1. Aggiorna stato dipendente
        UPDATE employees
        SET status = 'resigned',
            termination_date = v_termination_date
        WHERE id = v_employee_id;

        -- 2. Chiudi stipendio attivo
        UPDATE salaries
        SET end_date = v_termination_date
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- 3. Termina benefici (fine copertura)
        UPDATE benefits
        SET cost = 0  -- Sospendi costo ma mantieni record
        WHERE employee_id = v_employee_id;

        -- 4. Chiudi job history
        UPDATE job_history
        SET end_date = v_termination_date - 1,
            reason = v_termination_reason
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- 5. Log nel history
        INSERT INTO employee_status_history (
            employee_id, old_status, new_status, reason, changed_by
        ) VALUES (
            v_employee_id,
            'active',
            'resigned',
            v_termination_reason || ' - Final salary: € ' || v_final_salary,
            current_user
        );

        -- 6. Aggiorna statistiche dipartimento
        PERFORM update_department_statistics();

        -- 7. Se era manager, rimuovi dai dipartimenti
        UPDATE departments
        SET manager_id = NULL
        WHERE manager_id = v_employee_id;

        COMMIT;

        RAISE NOTICE 'Dipendente % terminato con successo', v_employee_name;
        RAISE NOTICE 'Tutti i sistemi aggiornati, benefici sospesi, statistics aggiornate';
    END;
    $$;

END;

-- =====================================================
-- 5. NUOVO ASSUNZIONE COMPLETA
-- =====================================================
-- Scenario: Onboarding completo di un nuovo dipendente
-- Crea: employee, salary, job_history, benefits iniziali

BEGIN;

    DO $$
    DECLARE
        v_emp_num VARCHAR(20) := 'EMP100';
        v_first_name VARCHAR(50) := 'Giovanni';
        v_last_name VARCHAR(50) := 'Rossi';
        v_email VARCHAR(100) := 'giovanni.rossi@company.it';
        v_phone VARCHAR(20) := '+39 02 9999999';
        v_birth_date DATE := '1990-05-15';
        v_hire_date DATE := CURRENT_DATE;
        v_job_id INTEGER := 8; -- Software Engineer
        v_department_id INTEGER := 3; -- Informatica
        v_manager_id INTEGER := 8; -- Massimo Moretti
        v_salary DECIMAL(12,2) := 50000.00;
        v_new_employee_id INTEGER;
    BEGIN
        -- 1. Crea dipendente
        INSERT INTO employees (
            employee_number, first_name, last_name, email, phone,
            birth_date, hire_date, job_id, department_id, manager_id, status
        ) VALUES (
            v_emp_num, v_first_name, v_last_name, v_email, v_phone,
            v_birth_date, v_hire_date, v_job_id, v_department_id,
            v_manager_id, 'active'
        )
        RETURNING id INTO v_new_employee_id;

        -- 2. Crea stipendio iniziale
        INSERT INTO salaries (employee_id, amount, effective_date)
        VALUES (v_new_employee_id, v_salary, v_hire_date);

        -- 3. Crea job history iniziale
        INSERT INTO job_history (
            employee_id, start_date, job_id, department_id, reason
        ) VALUES (
            v_new_employee_id, v_hire_date, v_job_id, v_department_id, 'Initial Hire'
        );

        -- 4. Iscribi benefit standard
        INSERT INTO benefits (employee_id, benefit_type, cost, enrollment_date)
        VALUES
            (v_new_employee_id, 'health_insurance', 3000.00, v_hire_date),
            (v_new_employee_id, 'transport', 800.00, v_hire_date);

        -- 5. Log assunzione
        INSERT INTO employee_status_history (
            employee_id, new_status, reason, changed_by, effective_date
        ) VALUES (
            v_new_employee_id, 'active', 'New hire - ' || v_emp_num, current_user, v_hire_date
        );

        COMMIT;

        RAISE NOTICE 'Nuovo dipendente % creato con ID %',
            v_first_name || ' ' || v_last_name, v_new_employee_id;
    END;
    $$;

END;

-- =====================================================
-- 6. PROMOZIONE DIPENDENTE
-- =====================================================
-- Scenario: Promozione con aumento stipendio e cambio job

BEGIN;

    DO $$
    DECLARE
        v_employee_id INTEGER := 29;
        v_new_job_id INTEGER := 9; -- Senior Developer
        v_increase_pct DECIMAL(5,2) := 15.0; -- 15% aumento
        v_promotion_date DATE := CURRENT_DATE;
        v_employee_name TEXT;
        v_old_job_title TEXT;
        v_new_job_title TEXT;
        v_old_salary DECIMAL(12,2);
        v_new_salary DECIMAL(12,2);
        v_old_min DECIMAL(12,2);
        v_old_max DECIMAL(12,2);
        v_new_min DECIMAL(12,2);
        v_new_max DECIMAL(12,2);
    BEGIN
        -- Recupera informazioni
        SELECT
            e.first_name || ' ' || e.last_name,
            j_old.title,
            j_new.title,
            s.amount,
            j_old.min_salary,
            j_old.max_salary,
            j_new.min_salary,
            j_new.max_salary
        INTO
            v_employee_name,
            v_old_job_title,
            v_new_job_title,
            v_old_salary,
            v_old_min,
            v_old_max,
            v_new_min,
            v_new_max
        FROM employees e
        JOIN jobs j_old ON e.job_id = j_old.id
        JOIN jobs j_new ON v_new_job_id = j_new.id
        JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
        WHERE e.id = v_employee_id;

        -- Calcola nuovo stipendio
        v_new_salary := v_old_salary * (1 + v_increase_pct / 100);

        -- Valida range
        IF v_new_salary < v_new_min OR v_new_salary > v_new_max THEN
            RAISE EXCEPTION 'ERRORE: Nuovo stipendio % fuori range job (€ % - € %)',
                v_new_salary, v_new_min, v_new_max;
        END IF;

        -- 1. Chiudi job history precedente
        UPDATE job_history
        SET end_date = v_promotion_date - 1,
            reason = 'Promoted to ' || v_new_job_title
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- 2. Crea nuovo job history
        INSERT INTO job_history (
            employee_id, start_date, job_id, department_id, reason
        ) VALUES (
            v_employee_id, v_promotion_date, v_new_job_id,
            (SELECT department_id FROM employees WHERE id = v_employee_id),
            'Promotion: ' || v_old_job_title || ' -> ' || v_new_job_title
        );

        -- 3. Aggiorna job dipendente
        UPDATE employees
        SET job_id = v_new_job_id
        WHERE id = v_employee_id;

        -- 4. Chiudi stipendio vecchio
        UPDATE salaries
        SET end_date = v_promotion_date - 1
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- 5. Nuovo stipendio
        INSERT INTO salaries (employee_id, amount, effective_date)
        VALUES (v_employee_id, v_new_salary, v_promotion_date);

        -- 6. Log promozione
        INSERT INTO employee_status_history (
            employee_id, old_status, new_status, reason, changed_by
        ) VALUES (
            v_employee_id,
            v_old_job_title,
            v_new_job_title,
            'Promotion with ' || v_increase_pct || '% raise: € ' || v_old_salary || ' -> € ' || v_new_salary,
            current_user
        );

        COMMIT;

        RAISE NOTICE 'Promozione completata: % -> % (+% %)',
            v_old_job_title, v_new_job_title, v_increase_pct;
        RAISE NOTICE 'Stipendio: € % -> € %', v_old_salary, v_new_salary;
    END;
    $$;

END;

-- =====================================================
-- 7. TRASFERIMENTO CON ESUBERO PERSONALE
-- =====================================================
-- Scenario: Riorganizzazione con trasferimenti multipli

BEGIN;

    DO $$
    DECLARE
        v_old_dept_id INTEGER := 6; -- Produzione
        v_new_dept_id INTEGER := 5; -- Vendite
        v_transfer_count INTEGER := 0;
        emp_record RECORD;
    BEGIN
        -- Trasferisci dipendenti specifici
        FOR emp_record IN
            SELECT id, first_name || ' ' || last_name AS name
            FROM employees
            WHERE department_id = v_old_dept_id
            AND status = 'active'
            AND id IN (28, 29, 30)  -- Specific dipendenti
        LOOP
            -- Chiudi job history
            UPDATE job_history
            SET end_date = CURRENT_DATE - 1,
                reason = 'Department reorganization'
            WHERE employee_id = emp_record.id
            AND end_date IS NULL;

            -- Nuovo job history
            INSERT INTO job_history (employee_id, start_date, job_id, department_id, reason)
            SELECT emp_record.id, CURRENT_DATE, job_id, v_new_dept_id, 'Reorganization transfer'
            FROM employees WHERE id = emp_record.id;

            -- Aggiorna dipendente
            UPDATE employees
            SET department_id = v_new_dept_id
            WHERE id = emp_record.id;

            v_transfer_count := v_transfer_count + 1;
            RAISE NOTICE 'Trasferito: %', emp_record.name;
        END LOOP;

        COMMIT;
        RAISE NOTICE 'Riorganizzazione completata: % dipendenti trasferiti', v_transfer_count;
    END;
    $$;

END;

-- =====================================================
-- 8. ROLLBACK ESEMPI
-- =====================================================
-- Esempi di gestione errori con ROLLBACK

-- ESEMPIO: Tentativo di stipendio fuori range (fallisce e fa rollback)
BEGIN;

    DO $$
    DECLARE
        v_employee_id INTEGER := 1;
        v_invalid_salary DECIMAL(12,2) := 500000.00; -- Fuori range CEO
    BEGIN
        -- Questo fallirà per il trigger di validazione
        UPDATE salaries
        SET amount = v_invalid_salary
        WHERE employee_id = v_employee_id
        AND end_date IS NULL;

        -- Questo codice non verrà eseguito
        RAISE NOTICE 'Stipendio aggiornato';

    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'ERRORE: Transazione rollback - %', SQLERRM;
            RAISE NOTICE 'Nessuna modifica apportata al database';
    END;
    $$;

    -- Rollback esplicito
    ROLLBACK;

END;

-- =====================================================
-- 9. SAVEPOINT ESEMPI
-- =====================================================
-- Esempio di savepoints per rollback parziale

BEGIN;

    -- Aggiorna stipendio primo dipendente
    UPDATE salaries
    SET amount = amount * 1.05
    WHERE employee_id = 11 AND end_date IS NULL;

    -- Crea savepoint
    SAVEPOINT sp1;

    -- Aggiorna stipendio secondo dipendente (potrebbe fallire)
    BEGIN
        UPDATE salaries
        SET amount = 999999  -- Fuori range
        WHERE employee_id = 12 AND end_date IS NULL;
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'Errore secondo aggiornamento, rollback to savepoint';
            ROLLBACK TO SAVEPOINT sp1;
    END;

    -- Continua con altri aggiornamenti
    UPDATE salaries
    SET amount = amount * 1.03
    WHERE employee_id = 13 AND end_date IS NULL;

    COMMIT;
    RAISE NOTICE 'Transazione completata con rollback parziale';

END;

-- =====================================================
-- 10. REPORTING TRANSAZIONI
-- =====================================================
-- Query per verificare le operazioni

-- Verifica ultimi trasferimenti
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d_old.name AS from_department,
    d_new.name AS to_department,
    jh.start_date AS transfer_date,
    jh.reason
FROM job_history jh
JOIN employees e ON jh.employee_id = e.id
JOIN departments d_old ON jh.department_id = d_old.id
LEFT JOIN departments d_new ON e.department_id = d_new.id
WHERE jh.reason LIKE '%Transfer%'
   OR jh.reason LIKE '%transfer%'
ORDER BY jh.start_date DESC;

-- Verifica ultimi aumenti stipendio
SELECT
    sal.employee_id,
    e.employee_number,
    e.first_name || ' ' || e.last_name,
    d.name AS department,
    sal.old_salary,
    sal.new_salary,
    sal.change_amount,
    sal.change_percentage,
    sal.change_date,
    sal.reason
FROM salary_audit_log sal
JOIN employees e ON sal.employee_id = e.id
JOIN departments d ON e.department_id = d.id
WHERE sal.change_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY sal.change_date DESC;

-- Verifica dipendenti terminati di recente
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name,
    d.name AS department,
    j.title AS job,
    e.termination_date,
    sh.new_status AS final_status,
    sh.reason,
    s.amount AS final_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
LEFT JOIN employee_status_history sh ON e.id = sh.employee_id
    AND sh.new_status IN ('terminated', 'resigned')
LEFT JOIN salaries s ON e.id = s.employee_id
    AND s.end_date >= e.termination_date
WHERE e.status IN ('terminated', 'resigned')
ORDER BY e.termination_date DESC;

-- =====================================================
-- FINE TRANSAZIONI
-- =====================================================
