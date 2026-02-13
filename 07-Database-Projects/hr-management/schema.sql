-- =====================================================
-- HR MANAGEMENT SYSTEM - DATABASE SCHEMA
-- Sistema di Gestione Risorse Umane
-- =====================================================
-- Database: PostgreSQL
-- Normalizzazione: 3NF (Third Normal Form)
-- Autori: Progetto Database Portfolio
-- =====================================================

-- Elimina le tabelle se esistono (in ordine di dipendenza)
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS performance_reviews CASCADE;
DROP TABLE IF EXISTS benefits CASCADE;
DROP TABLE IF EXISTS dependents CASCADE;
DROP TABLE IF EXISTS job_history CASCADE;
DROP TABLE IF EXISTS salaries CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS salary_audit_log CASCADE;

-- =====================================================
-- TABELLA: locations
-- =====================================================
-- Contiene le informazioni sulle sedi aziendali
-- Entità: 3NF - tutti i campi dipendono dalla chiave primaria
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index per ricerche geografiche
CREATE INDEX idx_locations_city ON locations(city);
CREATE INDEX idx_locations_country ON locations(country);

-- =====================================================
-- TABELLA: departments
-- =====================================================
-- Contiene i dipartimenti aziendali
-- Normalizzazione: department_name e location dipendono solo da department_id
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    location_id INTEGER NOT NULL,
    manager_id INTEGER,
    budget DECIMAL(15,2) NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_department_location
        FOREIGN KEY (location_id)
        REFERENCES locations(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_department_manager
        FOREIGN KEY (manager_id)
        REFERENCES employees(id)
        ON DELETE SET NULL
);

-- Index per performance
CREATE INDEX idx_departments_location ON departments(location_id);
CREATE INDEX idx_departments_manager ON departments(manager_id);

-- =====================================================
-- TABELLA: jobs
-- =====================================================
-- Contiene i tipi di lavoro/posizioni aziendali
-- Normalizzazione: tutti i campi dipendono solo da job_id
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    min_salary DECIMAL(12,2) NOT NULL CHECK (min_salary >= 0),
    max_salary DECIMAL(12,2) NOT NULL CHECK (max_salary >= min_salary),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index per ricerche
CREATE INDEX idx_jobs_title ON jobs(title);

-- =====================================================
-- TABELLA: employees
-- =====================================================
-- Contiene i dati dei dipendenti
-- Normalizzazione 3NF:
-- - Non ci sono dati transizionali (stipendi, storico job in tabelle separate)
-- - manager_id riferisce a employee stesso (gerarchia)
-- - status è stato corrente, non storico
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    birth_date DATE NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE,
    job_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    manager_id INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'terminated', 'on_leave', 'resigned')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_employee_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_employee_manager
        FOREIGN KEY (manager_id)
        REFERENCES employees(id)
        ON DELETE SET NULL,
    CONSTRAINT chk_email_format
        CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_hire_date
        CHECK (hire_date <= CURRENT_DATE),
    CONSTRAINT chk_birth_date
        CHECK (birth_date < hire_date)
);

-- Index per performance query comuni
CREATE INDEX idx_employees_name ON employees(last_name, first_name);
CREATE INDEX idx_employees_email ON employees(email);
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_job ON employees(job_id);
CREATE INDEX idx_employees_manager ON employees(manager_id);
CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_employees_hire_date ON employees(hire_date);

-- =====================================================
-- TABELLA: salaries
-- =====================================================
-- Storico stipendi dei dipendenti
-- Normalizzazione: separata da employees per tracciare cambiamenti
CREATE TABLE salaries (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    effective_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_salary_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_salary_dates
        CHECK (end_date IS NULL OR end_date >= effective_date),
    CONSTRAINT chk_effective_date
        CHECK (effective_date <= CURRENT_DATE)
);

-- Index per查询 storico stipendi
CREATE INDEX idx_salaries_employee ON salaries(employee_id);
CREATE INDEX idx_salaries_effective_date ON salaries(effective_date);
CREATE INDEX idx_salaries_amount ON salaries(amount);

-- Unique constraint: un solo stipendio attivo per dipendente
CREATE UNIQUE INDEX idx_salaries_active_employee
    ON salaries(employee_id)
    WHERE end_date IS NULL;

-- =====================================================
-- TABELLA: job_history
-- =====================================================
-- Storico delle posizioni lavorative dei dipendenti
-- Normalizzazione: traccia tutti i cambiamenti di job/department
CREATE TABLE job_history (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    job_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_job_history_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_job_history_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_job_history_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_job_history_dates
        CHECK (end_date IS NULL OR end_date >= start_date)
);

-- Index per query storico
CREATE INDEX idx_job_history_employee ON job_history(employee_id);
CREATE INDEX idx_job_history_dates ON job_history(start_date, end_date);

-- =====================================================
-- TABELLA: dependents
-- =====================================================
-- Contiene i familiari a carico dei dipendenti
CREATE TABLE dependents (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    relationship VARCHAR(50) NOT NULL
        CHECK (relationship IN ('spouse', 'child', 'parent', 'domestic_partner', 'other')),
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dependent_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE
);

-- Index
CREATE INDEX idx_dependents_employee ON dependents(employee_id);
CREATE INDEX idx_dependents_relationship ON dependents(relationship);

-- =====================================================
-- TABELLA: benefits
-- =====================================================
-- Contiene i benefici assegnati ai dipendenti
CREATE TABLE benefits (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    benefit_type VARCHAR(50) NOT NULL
        CHECK (benefit_type IN ('health_insurance', 'dental', 'vision', 'life_insurance',
                                 'retirement_401k', 'disability', 'transport', 'gym')),
    coverage_amount DECIMAL(10,2),
    cost DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (cost >= 0),
    enrollment_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_benefit_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE
);

-- Index
CREATE INDEX idx_benefits_employee ON benefits(employee_id);
CREATE INDEX idx_benefits_type ON benefits(benefit_type);

-- =====================================================
-- TABELLA: performance_reviews
-- =====================================================
-- Contiene le valutazioni delle performance dei dipendenti
CREATE TABLE performance_reviews (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    review_date DATE NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    goals_met VARCHAR(10),
        CHECK (goals_met IN ('yes', 'no', 'partial', 'na')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_reviewer
        FOREIGN KEY (reviewer_id)
        REFERENCES employees(id)
        ON DELETE RESTRICT
);

-- Index
CREATE INDEX idx_performance_employee ON performance_reviews(employee_id);
CREATE INDEX idx_performance_reviewer ON performance_reviews(reviewer_id);
CREATE INDEX idx_performance_date ON performance_reviews(review_date);
CREATE INDEX idx_performance_rating ON performance_reviews(rating);

-- =====================================================
-- TABELLA: attendance
-- =====================================================
-- Contiene i registri di presenza/assenza
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    attendance_date DATE NOT NULL,
    check_in TIME,
    check_out TIME,
    hours_worked DECIMAL(4,2),
    status VARCHAR(20) NOT NULL DEFAULT 'present'
        CHECK (status IN ('present', 'absent', 'late', 'half_day', 'sick', 'vacation', 'holiday')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attendance_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_attendance_hours
        CHECK (hours_worked IS NULL OR (hours_worked >= 0 AND hours_worked <= 24)),
    CONSTRAINT chk_attendance_times
        CHECK (check_out IS NULL OR check_in IS NULL OR check_out >= check_in)
);

-- Index
CREATE INDEX idx_attendance_employee ON attendance(employee_id);
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_attendance_status ON attendance(status);
CREATE UNIQUE INDEX idx_attendance_employee_date
    ON attendance(employee_id, attendance_date);

-- =====================================================
-- TABELLA: salary_audit_log
-- =====================================================
-- Log di audit per i cambiamenti salariali
CREATE TABLE salary_audit_log (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    old_salary DECIMAL(12,2),
    new_salary DECIMAL(12,2) NOT NULL,
    change_amount DECIMAL(12,2),
    change_percentage DECIMAL(5,2),
    reason VARCHAR(255),
    changed_by VARCHAR(100),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE
);

-- Index
CREATE INDEX idx_audit_employee ON salary_audit_log(employee_id);
CREATE INDEX idx_audit_date ON salary_audit_log(change_date);

-- =====================================================
-- FUNZIONI E TRIGGERS
-- =====================================================

-- Function: Aggiorna updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: updated_at per tutte le tabelle principali
CREATE TRIGGER trigger_locations_updated_at
    BEFORE UPDATE ON locations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_departments_updated_at
    BEFORE UPDATE ON departments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_employees_updated_at
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function: Validazione stipendio within job range
CREATE OR REPLACE FUNCTION validate_salary_range()
RETURNS TRIGGER AS $$
DECLARE
    v_job_min_salary DECIMAL(12,2);
    v_job_max_salary DECIMAL(12,2);
BEGIN
    -- Recupera il range salariale per il job del dipendente
    SELECT j.min_salary, j.max_salary
    INTO v_job_min_salary, v_job_max_salary
    FROM employees e
    JOIN jobs j ON e.job_id = j.id
    WHERE e.id = NEW.employee_id;

    -- Valida che lo stipendio sia nel range permesso
    IF NEW.amount < v_job_min_salary OR NEW.amount > v_job_max_salary THEN
        RAISE EXCEPTION 'Lo stipendio % deve essere compreso tra il range del job: % - %',
            NEW.amount, v_job_min_salary, v_job_max_salary;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Validazione stipendio
CREATE TRIGGER trigger_salary_range_validation
    BEFORE INSERT OR UPDATE OF amount ON salaries
    FOR EACH ROW
    EXECUTE FUNCTION validate_salary_range();

-- Function: Audit log per cambi stipendio
CREATE OR REPLACE FUNCTION log_salary_change()
RETURNS TRIGGER AS $$
DECLARE
    v_change_amount DECIMAL(12,2);
    v_change_percentage DECIMAL(5,2);
BEGIN
    -- Calcola il cambiamento se stiamo aggiornando
    IF TG_OP = 'UPDATE' AND OLD.amount IS NOT NULL AND NEW.amount IS DISTINCT FROM OLD.amount THEN
        v_change_amount := NEW.amount - OLD.amount;
        v_change_percentage := CASE
            WHEN OLD.amount > 0 THEN ((NEW.amount - OLD.amount) / OLD.amount) * 100
            ELSE NULL
        END;

        INSERT INTO salary_audit_log (employee_id, old_salary, new_salary, change_amount, change_percentage)
        VALUES (NEW.employee_id, OLD.amount, NEW.amount, v_change_amount, v_change_percentage);
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO salary_audit_log (employee_id, new_salary, change_amount, change_percentage, reason)
        VALUES (NEW.employee_id, NEW.amount, NEW.amount, NULL, 'Initial salary');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Audit log stipendi
CREATE TRIGGER trigger_salary_audit
    AFTER INSERT OR UPDATE OF amount ON salaries
    FOR EACH ROW
    EXECUTE FUNCTION log_salary_change();

-- =====================================================
-- VISTE UTILI
-- =====================================================

-- Vista: Dipendenti con informazioni complete
CREATE OR REPLACE VIEW v_employee_details AS
SELECT
    e.id,
    e.employee_number,
    e.first_name,
    e.last_name,
    e.email,
    e.phone,
    e.birth_date,
    e.hire_date,
    e.status,
    j.title AS job_title,
    d.name AS department_name,
    l.city AS location_city,
    l.country AS location_country,
    m.first_name || ' ' || m.last_name AS manager_name,
    s.amount AS current_salary,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS years_of_service,
    e.created_at,
    e.updated_at
FROM employees e
JOIN jobs j ON e.job_id = j.id
JOIN departments d ON e.department_id = d.id
JOIN locations l ON d.location_id = l.id
LEFT JOIN employees m ON e.manager_id = m.id
LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL;

-- Vista: Stipendi con dettagli job
CREATE OR REPLACE VIEW v_salary_details AS
SELECT
    s.id,
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee_name,
    j.title AS job_title,
    j.min_salary,
    j.max_salary,
    s.amount,
    s.effective_date,
    s.end_date,
    CASE
        WHEN s.amount < j.min_salary THEN 'Below Range'
        WHEN s.amount > j.max_salary THEN 'Above Range'
        ELSE 'Within Range'
    END AS salary_status,
    ROUND((s.amount - j.min_salary) / NULLIF(j.max_salary - j.min_salary, 0) * 100, 1) AS range_percentage
FROM salaries s
JOIN employees e ON s.employee_id = e.id
JOIN jobs j ON e.job_id = j.id;

-- Vista: Attendance summary
CREATE OR REPLACE VIEW v_attendance_summary AS
SELECT
    e.id AS employee_id,
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee_name,
    d.name AS department_name,
    COUNT(*) AS total_days,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS days_present,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS days_absent,
    SUM(CASE WHEN a.status = 'late' THEN 1 ELSE 0 END) AS days_late,
    SUM(CASE WHEN a.status = 'sick' THEN 1 ELSE 0 END) AS days_sick,
    SUM(CASE WHEN a.status = 'vacation' THEN 1 ELSE 0 END) AS days_vacation,
    SUM(a.hours_worked) AS total_hours,
    ROUND(AVG(a.hours_worked), 2) AS avg_daily_hours,
    ROUND(SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS absenteeism_rate
FROM attendance a
JOIN employees e ON a.employee_id = e.id
JOIN departments d ON e.department_id = d.id
GROUP BY e.id, e.employee_number, e.first_name, e.last_name, d.name;

-- =====================================================
-- COMMENTI ALLE TABELLE
-- =====================================================

COMMENT ON TABLE locations IS 'Sedi aziendali in diverse località geografiche';
COMMENT ON TABLE departments IS 'Dipartimenti/suddvisioni aziendali con budget assegnato';
COMMENT ON TABLE jobs IS 'Posizioni lavorative con range salariali definiti';
COMMENT ON TABLE employees IS 'Anagrafica completa dei dipendenti';
COMMENT ON TABLE salaries IS 'Storico completo degli stipendi con date di validità';
COMMENT ON TABLE job_history IS 'Storico dei cambiamenti di posizione/reparto';
COMMENT ON TABLE dependents IS 'Familiari a carico dei dipendenti';
COMMENT ON TABLE benefits IS 'Benefici aziendali assegnati ai dipendenti';
COMMENT ON TABLE performance_reviews IS 'Valutazioni delle performance con rating 1-5';
COMMENT ON TABLE attendance IS 'Registro presenze e ore lavorate';
COMMENT ON TABLE salary_audit_log IS 'Log di audit per tutti i cambiamenti salariali';

-- =====================================================
-- FINE SCHEMA
-- =====================================================
