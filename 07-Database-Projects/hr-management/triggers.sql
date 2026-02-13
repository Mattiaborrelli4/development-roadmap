-- =====================================================
-- HR MANAGEMENT SYSTEM - TRIGGERS & AUTOMATION
-- Triggers e Procedure per Automazione HR
-- =====================================================
-- Database: PostgreSQL
-- Contenuto: Triggers per automazione e validazione
-- =====================================================

-- =====================================================
-- 1. AUDIT LOG PER CAMBIAMENTI STIPENDIO
-- =====================================================
-- Crea log automatico ogni volta che cambia uno stipendio

-- Pulisci trigger esistenti
DROP TRIGGER IF EXISTS trigger_salary_audit ON salaries;
DROP FUNCTION IF EXISTS log_salary_change();

-- Funzione migliorata per audit log stipendi
CREATE OR REPLACE FUNCTION log_salary_change()
RETURNS TRIGGER AS $$
DECLARE
    v_change_amount DECIMAL(12,2);
    v_change_percentage DECIMAL(5,2);
    v_old_salary DECIMAL(12,2);
    v_employee_name TEXT;
    v_job_title TEXT;
BEGIN
    -- Recupera info dipendente
    SELECT first_name || ' ' || last_name, j.title
    INTO v_employee_name, v_job_title
    FROM employees e
    JOIN jobs j ON e.job_id = j.id
    WHERE e.id = NEW.employee_id;

    -- Caso UPDATE: stipendio modificato
    IF TG_OP = 'UPDATE' AND OLD.amount IS NOT NULL AND NEW.amount IS DISTINCT FROM OLD.amount THEN
        v_change_amount := NEW.amount - OLD.amount;
        v_change_percentage := CASE
            WHEN OLD.amount > 0 THEN ((NEW.amount - OLD.amount) / OLD.amount) * 100
            ELSE NULL
        END;

        INSERT INTO salary_audit_log (
            employee_id,
            old_salary,
            new_salary,
            change_amount,
            change_percentage,
            reason,
            changed_by
        ) VALUES (
            NEW.employee_id,
            OLD.amount,
            NEW.amount,
            v_change_amount,
            v_change_percentage,
            'Salary update from ' || OLD.amount || ' to ' || NEW.amount,
            current_user
        );

        RAISE NOTICE 'Stipendio modificato per % (%): € % -> € % (€ %, % %)',
            v_employee_name, v_job_title, OLD.amount, NEW.amount,
            v_change_amount, v_change_percentage;
    END IF;

    -- Caso INSERT: nuovo stipendio
    IF TG_OP = 'INSERT' THEN
        INSERT INTO salary_audit_log (
            employee_id,
            old_salary,
            new_salary,
            change_amount,
            change_percentage,
            reason,
            changed_by
        ) VALUES (
            NEW.employee_id,
            NULL,
            NEW.amount,
            NEW.amount,
            NULL,
            'Initial salary assignment',
            current_user
        );

        RAISE NOTICE 'Nuovo stipendio assegnato a % (%): € %',
            v_employee_name, v_job_title, NEW.amount;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger per audit
CREATE TRIGGER trigger_salary_audit
    AFTER INSERT OR UPDATE OF amount ON salaries
    FOR EACH ROW
    EXECUTE FUNCTION log_salary_change();

-- =====================================================
-- 2. AUTO-UPDATE DEPARTMENT MANAGER
-- =====================================================
-- Aggiorna automaticamente il manager del dipartimento quando cambia

DROP FUNCTION IF EXISTS auto_update_department_manager();
CREATE OR REPLACE FUNCTION auto_update_department_manager()
RETURNS TRIGGER AS $$
BEGIN
    -- Quando un dipendente viene aggiornato
    IF TG_OP = 'UPDATE' THEN
        -- Se il department_id è cambiato, aggiorna tutti i dipartimenti coinvolti
        IF OLD.department_id IS DISTINCT FROM NEW.department_id THEN

            -- Aggiorna il vecchio dipartimento se questo era il manager
            UPDATE departments
            SET manager_id = NULL
            WHERE id = OLD.department_id
            AND manager_id = NEW.id;

            -- Notifica del cambiamento
            RAISE NOTICE 'Dipendente % trasferito dal dipartimento % al %',
                NEW.first_name || ' ' || NEW.last_name,
                OLD.department_id, NEW.department_id;
        END IF;
    END IF;

    -- Quando un dipendente viene inserito o cancellato
    IF TG_OP = 'INSERT' THEN
        -- Verifica se questo dipendente dovrebbe essere manager di un dipartimento
        -- (Logica personalizzabile in base alle esigenze)
        NULL;
    END IF;

    IF TG_OP = 'DELETE' THEN
        -- Rimuovi il manager dai dipartimenti dove questo era manager
        UPDATE departments
        SET manager_id = NULL
        WHERE manager_id = OLD.id;

        RAISE NOTICE 'Dipendente % rimosso. Manager dipartimenti aggiornato.',
            OLD.first_name || ' ' || OLD.last_name;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_update_dept_manager
    AFTER INSERT OR UPDATE OR DELETE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION auto_update_department_manager();

-- =====================================================
-- 3. VALIDA STIPENDIO IN JOB RANGE
-- =====================================================
-- Verifica che lo stipendio sia nel range definito per il job

DROP TRIGGER IF EXISTS trigger_salary_range_validation ON salaries;
DROP FUNCTION IF FUNCTION validate_salary_range();

CREATE OR REPLACE FUNCTION validate_salary_range()
RETURNS TRIGGER AS $$
DECLARE
    v_job_min_salary DECIMAL(12,2);
    v_job_max_salary DECIMAL(12,2);
    v_job_title TEXT;
    v_employee_name TEXT;
BEGIN
    -- Recupera il range salariale per il job del dipendente
    SELECT j.min_salary, j.max_salary, j.title,
           e.first_name || ' ' || e.last_name
    INTO v_job_min_salary, v_job_max_salary, v_job_title, v_employee_name
    FROM employees e
    JOIN jobs j ON e.job_id = j.id
    WHERE e.id = NEW.employee_id;

    -- Valida che lo stipendio sia nel range permesso
    IF NEW.amount < v_job_min_salary THEN
        RAISE EXCEPTION 'ERRORE: Lo stipendio € % per % (Job: %) è inferiore al minimo consentito (€ %)',
            NEW.amount, v_employee_name, v_job_title, v_job_min_salary;
    END IF;

    IF NEW.amount > v_job_max_salary THEN
        RAISE EXCEPTION 'ERRORE: Lo stipendio € % per % (Job: %) supera il massimo consentito (€ %)',
            NEW.amount, v_employee_name, v_job_title, v_job_max_salary;
    END IF;

    -- Warning se vicino ai limiti (opzionale)
    IF NEW.amount = v_job_min_salary THEN
        RAISE NOTICE 'AVVISO: Stipendio al minimo range per % (Job: %)',
            v_employee_name, v_job_title;
    END IF;

    IF NEW.amount = v_job_max_salary THEN
        RAISE NOTICE 'AVVISO: Stipendio al massimo range per % (Job: %)',
            v_employee_name, v_job_title;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_salary_range_validation
    BEFORE INSERT OR UPDATE OF amount ON salaries
    FOR EACH ROW
    EXECUTE FUNCTION validate_salary_range();

-- =====================================================
-- 4. TRACK EMPLOYEE STATUS CHANGES
-- =====================================================
-- Traccia tutti i cambiamenti di stato dei dipendenti

DROP TABLE IF EXISTS employee_status_history CASCADE;

CREATE TABLE employee_status_history (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100),
    reason TEXT,
    effective_date DATE,

    CONSTRAINT fk_status_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_status_history_employee ON employee_status_history(employee_id);
CREATE INDEX idx_status_history_date ON employee_status_history(change_date);
CREATE INDEX idx_status_history_status ON employee_status_history(new_status);

DROP FUNCTION IF EXISTS track_employee_status_change();

CREATE OR REPLACE FUNCTION track_employee_status_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Traccia cambiamenti status
    IF TG_OP = 'UPDATE' AND OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO employee_status_history (
            employee_id,
            old_status,
            new_status,
            reason,
            changed_by
        ) VALUES (
            NEW.id,
            OLD.status,
            NEW.status,
            'Status changed from ' || OLD.status || ' to ' || NEW.status,
            current_user
        );

        RAISE NOTICE 'Status dipendente % cambiato: % -> %',
            NEW.first_name || ' ' || NEW.last_name,
            OLD.status, NEW.status;

        -- Se il dipendente viene terminato, aggiungi termination_date
        IF NEW.status IN ('terminated', 'resigned') AND NEW.termination_date IS NULL THEN
            NEW.termination_date := CURRENT_DATE;
            RAISE NOTICE 'Impostata termination_date al % per %',
                CURRENT_DATE, NEW.first_name || ' ' || NEW.last_name;
        END IF;

        -- Se il dipendente viene reattivato, rimuovi termination_date
        IF NEW.status = 'active' AND NEW.termination_date IS NOT NULL THEN
            NEW.termination_date := NULL;
            RAISE NOTICE 'Rimossa termination_date per % riattivato',
                NEW.first_name || ' ' || NEW.last_name;
        END IF;
    END IF;

    -- Traccia nuovo dipendente
    IF TG_OP = 'INSERT' THEN
        INSERT INTO employee_status_history (
            employee_id,
            old_status,
            new_status,
            reason,
            changed_by,
            effective_date
        ) VALUES (
            NEW.id,
            NULL,
            NEW.status,
            'Initial status for new hire',
            current_user,
            NEW.hire_date
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_track_status_change
    AFTER INSERT OR UPDATE OF status ON employees
    FOR EACH ROW
    EXECUTE FUNCTION track_employee_status_change();

-- =====================================================
-- 5. VALIDATE JOB HISTORY ENTRIES
-- =====================================================
-- Validazione e normalizzazione job history

DROP TRIGGER IF EXISTS trigger_validate_job_history ON job_history;
DROP FUNCTION IF EXISTS validate_job_history_entry();

CREATE OR REPLACE FUNCTION validate_job_history_entry()
RETURNS TRIGGER AS $$
DECLARE
    v_current_job_id INTEGER;
    v_current_dept_id INTEGER;
BEGIN
    -- Recupera job e department correnti del dipendente
    SELECT job_id, department_id
    INTO v_current_job_id, v_current_dept_id
    FROM employees
    WHERE id = NEW.employee_id;

    -- Validazione date
    IF NEW.start_date > CURRENT_DATE THEN
        RAISE EXCEPTION 'ERRORE: La data inizio % è nel futuro',
            NEW.start_date;
    END IF;

    IF NEW.end_date IS NOT NULL AND NEW.end_date < NEW.start_date THEN
        RAISE EXCEPTION 'ERRORE: La data fine % è precedente alla data inizio %',
            NEW.end_date, NEW.start_date;
    END IF;

    -- Se questo è il job corrente, aggiorna la tabella employees
    IF NEW.end_date IS NULL THEN
        -- Verifica che non ci siano altri job history attivi
        IF EXISTS (
            SELECT 1 FROM job_history
            WHERE employee_id = NEW.employee_id
            AND id != NEW.id
            AND end_date IS NULL
        ) THEN
            RAISE EXCEPTION 'ERRORE: Esiste già un job history attivo per questo dipendente. Chiudere il record precedente.';
        END IF;

        -- Aggiorna employees con il job corrente
        UPDATE employees
        SET job_id = NEW.job_id,
            department_id = NEW.department_id
        WHERE id = NEW.employee_id;

        RAISE NOTICE 'Job corrente aggiornato per dipendente %',
            NEW.employee_id;
    END IF;

    -- Se si chiude un job history, crea un record di audit
    IF TG_OP = 'UPDATE' AND OLD.end_date IS NULL AND NEW.end_date IS NOT NULL THEN
        INSERT INTO employee_status_history (employee_id, old_status, new_status, reason, changed_by)
        VALUES (
            NEW.employee_id,
            'Job ' || NEW.job_id,
            'Job ' || NEW.job_id || ' ended',
            'Job history closed: ' || NEW.reason,
            current_user
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_job_history
    BEFORE INSERT OR UPDATE ON job_history
    FOR EACH ROW
    EXECUTE FUNCTION validate_job_history_entry();

-- =====================================================
-- 6. PREVENT DUPLICATE ATTENDANCE RECORDS
-- =====================================================
-- Previene duplicati nei registri presenze

DROP TRIGGER IF EXISTS trigger_prevent_duplicate_attendance ON attendance;
DROP FUNCTION IF FUNCTION prevent_duplicate_attendance();

CREATE OR REPLACE FUNCTION prevent_duplicate_attendance()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se esiste già un record per lo stesso dipendente e data
    IF EXISTS (
        SELECT 1
        FROM attendance
        WHERE employee_id = NEW.employee_id
        AND attendance_date = NEW.attendance_date
        AND id != COALESCE(NEW.id, 0)
    ) THEN
        RAISE EXCEPTION 'ERRORE: Esiste già un registro presenza per il dipendente % in data %',
            NEW.employee_id, NEW.attendance_date;
    END IF;

    -- Validazione orari
    IF NEW.check_in IS NOT NULL AND NEW.check_out IS NOT NULL THEN
        IF NEW.check_out < NEW.check_in THEN
            RAISE EXCEPTION 'ERRORE: Orario uscita % precedente all''ingresso %',
                NEW.check_out, NEW.check_in;
        END IF;

        -- Calcola automaticamente le ore lavorate se non specificate
        IF NEW.hours_worked IS NULL THEN
            NEW.hours_worked := EXTRACT(EPOCH FROM (NEW.check_out - NEW.check_in)) / 3600;
            RAISE NOTICE 'Calcolate ore lavorate: %', NEW.hours_worked;
        END IF;
    END IF;

    -- Imposta status automatico basato sugli orari
    IF NEW.status IS NULL THEN
        IF NEW.check_in IS NULL THEN
            NEW.status := 'absent';
        ELSE
            NEW.status := 'present';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_prevent_duplicate_attendance
    BEFORE INSERT OR UPDATE ON attendance
    FOR EACH ROW
    EXECUTE FUNCTION prevent_duplicate_attendance();

-- =====================================================
-- 7. AUTO-CALCULATE DEPARTMENT STATS
-- =====================================================
-- Calcola automaticamente statistiche dipartimento

DROP TABLE IF EXISTS department_statistics CASCADE;

CREATE TABLE department_statistics (
    id SERIAL PRIMARY KEY,
    department_id INTEGER NOT NULL UNIQUE,
    stat_date DATE NOT NULL,
    headcount INTEGER DEFAULT 0,
    active_count INTEGER DEFAULT 0,
    total_salary DECIMAL(15,2) DEFAULT 0,
    avg_salary DECIMAL(12,2) DEFAULT 0,
    min_salary DECIMAL(12,2),
    max_salary DECIMAL(12,2),
    total_dependents INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dept_stats_dept
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_dept_stats_department ON department_statistics(department_id);
CREATE INDEX idx_dept_stats_date ON department_statistics(stat_date);

DROP FUNCTION IF FUNCTION update_department_statistics();

CREATE OR REPLACE FUNCTION update_department_statistics()
RETURNS TRIGGER AS $$
BEGIN
    -- Aggiorna le statistiche per il dipartimento interessato
    INSERT INTO department_statistics (
        department_id,
        stat_date,
        headcount,
        active_count,
        total_salary,
        avg_salary,
        min_salary,
        max_salary,
        total_dependents
    )
    SELECT
        e.department_id,
        CURRENT_DATE,
        COUNT(*),
        COUNT(*) FILTER (WHERE e.status = 'active'),
        COALESCE(SUM(s.amount), 0),
        COALESCE(AVG(s.amount), 0),
        MIN(s.amount),
        MAX(s.amount),
        (SELECT COUNT(*) FROM dependents WHERE employee_id IN (SELECT id FROM employees WHERE department_id = e.department_id))
    FROM employees e
    LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
    WHERE e.department_id = COALESCE(NEW.department_id, OLD.department_id)
    GROUP BY e.department_id

    ON CONFLICT (department_id, stat_date)
    DO UPDATE SET
        headcount = EXCLUDED.headcount,
        active_count = EXCLUDED.active_count,
        total_salary = EXCLUDED.total_salary,
        avg_salary = EXCLUDED.avg_salary,
        min_salary = EXCLUDED.min_salary,
        max_salary = EXCLUDED.max_salary,
        total_dependents = EXCLUDED.total_dependents,
        updated_at = CURRENT_TIMESTAMP;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger per aggiornare statistiche dopo modifiche dipendenti o stipendi
CREATE TRIGGER trigger_update_dept_stats_employee
    AFTER INSERT OR UPDATE OR DELETE ON employees
    FOR EACH STATEMENT
    EXECUTE FUNCTION update_department_statistics();

CREATE TRIGGER trigger_update_dept_stats_salary
    AFTER INSERT OR UPDATE OR DELETE ON salaries
    FOR EACH STATEMENT
    EXECUTE FUNCTION update_department_statistics();

-- =====================================================
-- 8. BENEFIT ENROLLMENT VALIDATION
-- =====================================================
-- Valida iscrizioni benefit

DROP TRIGGER IF EXISTS trigger_validate_benefit_enrollment ON benefits;
DROP FUNCTION IF FUNCTION validate_benefit_enrollment();

CREATE OR REPLACE FUNCTION validate_benefit_enrollment()
RETURNS TRIGGER AS $$
DECLARE
    v_active_benefits INTEGER;
BEGIN
    -- Verifica dipendenti attivi possano avere benefits
    IF NOT EXISTS (
        SELECT 1 FROM employees
        WHERE id = NEW.employee_id
        AND status = 'active'
    ) THEN
        RAISE EXCEPTION 'ERRORE: Solo dipendenti attivi possono iscriversi ai benefit';
    END IF;

    -- Conta benefici attivi dello stesso tipo
    SELECT COUNT(*)
    INTO v_active_benefits
    FROM benefits
    WHERE employee_id = NEW.employee_id
    AND benefit_type = NEW.benefit_type
    AND id != COALESCE(NEW.id, 0);

    -- La maggior parte dei benefit deve essere unico per tipo
    IF NEW.benefit_type IN ('health_insurance', 'dental', 'vision', 'retirement_401k', 'disability') THEN
        IF v_active_benefits > 0 THEN
            RAISE EXCEPTION 'ERRORE: Il dipendente ha già un benefit di tipo %',
                NEW.benefit_type;
        END IF;
    END IF;

    -- Valida costi
    IF NEW.cost < 0 THEN
        RAISE EXCEPTION 'ERRORE: Il costo non può essere negativo';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_benefit_enrollment
    BEFORE INSERT OR UPDATE ON benefits
    FOR EACH ROW
    EXECUTE FUNCTION validate_benefit_enrollment();

-- =====================================================
-- 9. PERFORMANCE REVIEW VALIDATION
-- =====================================================
-- Valida le valutazioni performance

DROP TRIGGER IF EXISTS trigger_validate_performance_review ON performance_reviews;
DROP FUNCTION IF FUNCTION validate_performance_review();

CREATE OR REPLACE FUNCTION validate_performance_review()
RETURNS TRIGGER AS $$
DECLARE
    v_employee_exists BOOLEAN;
    v_reviewer_exists BOOLEAN;
    v_recent_review_count INTEGER;
BEGIN
    -- Verifica esistenza dipendente
    SELECT EXISTS(SELECT 1 FROM employees WHERE id = NEW.employee_id)
    INTO v_employee_exists;

    IF NOT v_employee_exists THEN
        RAISE EXCEPTION 'ERRORE: Dipendente % non esiste', NEW.employee_id;
    END IF;

    -- Verifica esistenza revisore
    SELECT EXISTS(SELECT 1 FROM employees WHERE id = NEW.reviewer_id)
    INTO v_reviewer_exists;

    IF NOT v_reviewer_exists THEN
        RAISE EXCEPTION 'ERRORE: Revisore % non esiste', NEW.reviewer_id;
    END IF;

    -- Un dipendente non può revisionare se stesso
    IF NEW.employee_id = NEW.reviewer_id THEN
        RAISE EXCEPTION 'ERRORE: Un dipendente non può revisionare se stesso';
    END IF;

    -- Verifica data nel passato
    IF NEW.review_date > CURRENT_DATE THEN
        RAISE EXCEPTION 'ERRORE: La data valutazione % è nel futuro',
            NEW.review_date;
    END IF;

    -- Verifica rating range
    IF NEW.rating < 1 OR NEW.rating > 5 THEN
        RAISE EXCEPTION 'ERRORE: Il rating deve essere tra 1 e 5';
    END IF;

    -- Opzionale: previene troppe valutazioni nello stesso mese
    SELECT COUNT(*)
    INTO v_recent_review_count
    FROM performance_reviews
    WHERE employee_id = NEW.employee_id
    AND DATE_TRUNC('month', review_date) = DATE_TRUNC('month', NEW.review_date)
    AND id != COALESCE(NEW.id, 0);

    IF v_recent_review_count >= 2 THEN
        RAISE WARNING 'AVVISO: Il dipendente ha già % valutazioni questo mese',
            v_recent_review_count;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_performance_review
    BEFORE INSERT OR UPDATE ON performance_reviews
    FOR EACH ROW
    EXECUTE FUNCTION validate_performance_review();

-- =====================================================
-- 10. DEPENDENT VALIDATION
-- =====================================================
-- Valida inserimento familiari a carico

DROP TRIGGER IF EXISTS trigger_validate_dependent ON dependents;
DROP FUNCTION IF FUNCTION validate_dependent();

CREATE OR REPLACE FUNCTION validate_dependent()
RETURNS TRIGGER AS $$
DECLARE
    v_employee_active BOOLEAN;
BEGIN
    -- Verifica dipendente attivo
    SELECT status = 'active'
    INTO v_employee_active
    FROM employees
    WHERE id = NEW.employee_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ERRORE: Dipendente % non esiste', NEW.employee_id;
    END IF;

    -- Valida data di nascita
    IF NEW.birth_date > CURRENT_DATE THEN
        RAISE EXCEPTION 'ERRORE: La data di nascita % è nel futuro',
            NEW.birth_date;
    END IF;

    -- Verifica relazione valida
    IF NEW.relationship NOT IN ('spouse', 'child', 'parent', 'domestic_partner', 'other') THEN
        RAISE EXCEPTION 'ERRORE: Relazione % non valida', NEW.relationship;
    END IF;

    -- Warning se genitore più giovane del figlio
    IF NEW.relationship = 'child' THEN
        IF EXISTS (
            SELECT 1 FROM employees e
            WHERE e.id = NEW.employee_id
            AND e.birth_date > NEW.birth_date
        ) THEN
            RAISE WARNING 'AVVISO: La data di nascita del figlio precede quella del genitore';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_dependent
    BEFORE INSERT OR UPDATE ON dependents
    FOR EACH ROW
    EXECUTE FUNCTION validate_dependent();

-- =====================================================
-- UTILITÀ: Trigger abilitazione/disabilitazione
-- =====================================================

-- Funzione per disabilitare tutti i trigger
CREATE OR REPLACE FUNCTION disable_all_triggers()
RETURNS VOID AS $$
BEGIN
    SET session_replication_role = 'replica';
    RAISE NOTICE 'Tutti i trigger disabilitati per questa sessione';
END;
$$ LANGUAGE plpgsql;

-- Funzione per abilitare tutti i trigger
CREATE OR REPLACE FUNCTION enable_all_triggers()
RETURNS VOID AS $$
BEGIN
    SET session_replication_role = 'origin';
    RAISE NOTICE 'Tutti i trigger abilitati';
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- REPORTING: Viste per monitoring triggers
-- =====================================================

-- Vista: Log ultimi cambiamenti stipendio
CREATE OR REPLACE VIEW v_recent_salary_changes AS
SELECT
    sal.employee_id,
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee_name,
    d.name AS department,
    sal.old_salary,
    sal.new_salary,
    sal.change_amount,
    sal.change_percentage,
    sal.reason,
    sal.changed_by,
    sal.change_date
FROM salary_audit_log sal
JOIN employees e ON sal.employee_id = e.id
JOIN departments d ON e.department_id = d.id
WHERE sal.change_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY sal.change_date DESC;

-- Vista: Storico cambi status
CREATE OR REPLACE VIEW v_employee_status_changes AS
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    sh.old_status,
    sh.new_status,
    sh.change_date,
    sh.changed_by,
    sh.reason
FROM employee_status_history sh
JOIN employees e ON sh.employee_id = e.id
JOIN departments d ON e.department_id = d.id
ORDER BY sh.change_date DESC;

-- Vista: Statistiche dipartimento più recenti
CREATE OR REPLACE VIEW v_current_department_stats AS
SELECT DISTINCT ON (department_id)
    d.id AS department_id,
    d.name AS department,
    ds.headcount,
    ds.active_count,
    ds.total_salary,
    ds.avg_salary,
    ds.min_salary,
    ds.max_salary,
    d.budget,
    ROUND((ds.total_salary / NULLIF(d.budget, 0)) * 100, 2) AS budget_pct,
    ds.updated_at
FROM department_statistics ds
JOIN departments d ON ds.department_id = d.id
ORDER BY department_id, ds.stat_date DESC;

-- =====================================================
-- TEST DEI TRIGGER
-- =====================================================

-- Test: Inserisci stipendio fuori range (deve fallire)
-- INSERT INTO salaries (employee_id, amount, effective_date)
-- VALUES (1, 500000, CURRENT_DATE);
-- Expected: EXCEPTION

-- Test: Inserisci stipendio valido (deve successo e creare audit log)
-- INSERT INTO salaries (employee_id, amount, effective_date)
-- VALUES (1, 210000, CURRENT_DATE);
-- Expected: SUCCESS + Audit record

-- Test: Cambia status dipendente
-- UPDATE employees SET status = 'terminated' WHERE id = 2;
-- Expected: status record creato + termination_date impostata

-- Test: Prova a inserire duplicato attendance
-- INSERT INTO attendance (employee_id, attendance_date, check_in, check_out, status)
-- VALUES (1, '2024-01-01', '09:00', '18:00', 'present');
-- Due volte Expected: Seconda volta EXCEPTION

-- =====================================================
-- FINE TRIGGERS
-- =====================================================
