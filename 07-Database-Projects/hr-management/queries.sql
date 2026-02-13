-- =====================================================
-- HR MANAGEMENT SYSTEM - COMPLEX QUERIES
-- Query Complesse per Analisi HR
-- =====================================================
-- Database: PostgreSQL
-- Contenuto: Query avanzate per report e analisi
-- =====================================================

-- =====================================================
-- 1. ORGANIZZATIONAL CHART (CTE Ricorsivo)
-- =====================================================
-- Mostra la gerarchia completa dell'organizzazione
-- Dalla CEO fino all'ultimo dipendente

WITH RECURSIVE org_hierarchy AS (
    -- Base: top level managers (senza manager)
    SELECT
        id,
        employee_number,
        first_name,
        last_name,
        job_title,
        department_name,
        manager_id,
        manager_name,
        1 AS level,
        first_name || ' ' || last_name AS path,
        ARRAY[first_name || ' ' || last_name] AS names_path
    FROM v_employee_details
    WHERE manager_id IS NULL

    UNION ALL

    -- Ricorsione: tutti i dipendenti che riportano ai manager trovati
    SELECT
        e.id,
        e.employee_number,
        e.first_name,
        e.last_name,
        e.job_title,
        e.department_name,
        e.manager_id,
        e.manager_name,
        o.level + 1,
        o.path || ' > ' || e.first_name || ' ' || e.last_name,
        o.names_path || ARRAY[e.first_name || ' ' || e.last_name]
    FROM v_employee_details e
    INNER JOIN org_hierarchy o
        ON e.manager_id = o.id
)
SELECT
    repeat('....', level) || first_name || ' ' || last_name AS organizational_chart,
    employee_number,
    job_title,
    department_name,
    manager_name,
    level AS hierarchy_level,
    current_salary
FROM org_hierarchy
ORDER BY names_path;

-- Versione compatta con conteggio diretto riportanti
WITH RECURSIVE hierarchy_counts AS (
    SELECT
        id,
        first_name,
        last_name,
        job_title,
        manager_id
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.id,
        e.first_name,
        e.last_name,
        e.job_title,
        e.manager_id
    FROM employees e
    INNER JOIN hierarchy_counts h
        ON e.manager_id = h.id
)
SELECT
    h.first_name || ' ' || h.last_name AS manager,
    j.title AS position,
    d.name AS department,
    COUNT(*) - 1 AS direct_reports,
    (SELECT COUNT(*)
     FROM employees e2
     WHERE e2.id IN (
         WITH RECURSIVE sub_tree AS (
             SELECT id, manager_id FROM employees WHERE manager_id = h.id
             UNION ALL
             SELECT e.id, e.manager_id
             FROM employees e
             INNER JOIN sub_tree st ON e.manager_id = st.id
         )
         SELECT id FROM sub_tree
     )
    ) AS total_reports
FROM hierarchy_counts h
JOIN jobs j ON h.job_id = j.id
JOIN departments d ON h.department_id = d.id
GROUP BY h.id, h.first_name, h.last_name, j.title, d.name
ORDER BY total_reports DESC, manager;

-- =====================================================
-- 2. SALARY RANGES BY DEPARTMENT
-- =====================================================
-- Analisi dettagliata degli stipendi per dipartimento
-- Con confronto rispetto al budget e range job

SELECT
    d.name AS department,
    j.title AS job_title,
    COUNT(*) AS headcount,
    ROUND(AVG(s.amount), 2) AS average_salary,
    ROUND(MIN(s.amount), 2) AS min_actual_salary,
    ROUND(MAX(s.amount), 2) AS max_actual_salary,
    j.min_salary AS job_min_range,
    j.max_salary AS job_max_range,
    ROUND((j.min_salary + j.max_salary) / 2, 2) AS job_midpoint,
    ROUND(
        (AVG(s.amount) - ((j.min_salary + j.max_salary) / 2)) /
        NULLIF((j.max_salary - j.min_salary), 0) * 100,
        2
    ) AS variance_from_midpoint_pct,
    ROUND(SUM(s.amount), 2) AS total_department_cost,
    ROUND(d.budget, 2) AS department_budget,
    ROUND(
        (SUM(s.amount) / NULLIF(d.budget, 0)) * 100,
        2
    ) AS budget_utilization_pct
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
GROUP BY d.name, d.budget, j.title, j.min_salary, j.max_salary
ORDER BY d.name, average_salary DESC;

-- Analisi outlier stipendiali (fuori range)
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    j.title AS job_title,
    s.amount AS current_salary,
    j.min_salary AS job_min,
    j.max_salary AS job_max,
    CASE
        WHEN s.amount < j.min_salary THEN 'Below Range'
        WHEN s.amount > j.max_salary THEN 'Above Range'
        ELSE 'Within Range'
    END AS salary_status,
    s.amount - j.min_salary AS diff_from_min,
    j.max_salary - s.amount AS diff_from_max,
    ROUND(
        (s.amount - j.min_salary) / NULLIF(j.max_salary - j.min_salary, 0) * 100,
        2
    ) AS position_in_range_pct
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
WHERE s.amount < j.min_salary OR s.amount > j.max_salary
ORDER BY ABS(s.amount - (j.min_salary + j.max_salary) / 2) DESC;

-- =====================================================
-- 3. EMPLOYEES WITH DEPENDENTS (Complex JOIN)
-- =====================================================
-- Lista dipendenti con familiari a carico e dettagli benefici

SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.email,
    d.name AS department,
    j.title AS job_title,
    s.amount AS salary,
    COUNT(dep.id) AS number_of_dependents,
    STRING_AGG(
        dep.first_name || ' ' || dep.last_name || ' (' ||
        dep.relationship || ', ' ||
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, dep.birth_date)) || ' anni)',
        ', '
        ORDER BY dep.birth_date DESC
    ) AS dependents_list,
    STRING_AGG(DISTINCT b.benefit_type, ', ') AS benefits_enrolled,
    COUNT(DISTINCT b.benefit_type) AS total_benefits
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
LEFT JOIN dependents dep ON e.id = dep.employee_id
LEFT JOIN benefits b ON e.id = b.employee_id
GROUP BY e.id, e.employee_number, e.first_name, e.last_name,
         e.email, d.name, j.title, s.amount
HAVING COUNT(dep.id) > 0
ORDER BY number_of_dependents DESC, salary DESC;

-- Benefici più comuni per dipendenti con familiari
SELECT
    b.benefit_type,
    COUNT(DISTINCT b.employee_id) AS employees_with_benefit,
    COUNT(DISTINCT CASE WHEN dep.id IS NOT NULL THEN b.employee_id END) AS employees_with_dependents,
    ROUND(AVG(b.cost), 2) AS average_annual_cost,
    ROUND(SUM(b.cost), 2) AS total_annual_cost
FROM benefits b
LEFT JOIN employees e ON b.employee_id = e.id
LEFT JOIN dependents dep ON e.id = dep.employee_id
GROUP BY b.benefit_type
ORDER BY employees_with_benefit DESC;

-- =====================================================
-- 4. TENURE CALCULATION (Date Functions)
-- =====================================================
-- Analisi anzianità dipendenti con statistiche dettagliate

SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    j.title AS job,
    e.hire_date,
    CURRENT_DATE - e.hire_date AS total_days,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS years_of_service,
    EXTRACT(MONTH FROM AGE(CURRENT_DATE, e.hire_date)) AS months_of_service,
    EXTRACT(DAY FROM AGE(CURRENT_DATE, e.hire_date)) AS days_of_service,
    ROUND(
        EXTRACT(EPOCH FROM (CURRENT_DATE - e.hire_date)) / 365.25 / 86400,
        1
    ) AS years_precise,
    CASE
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 10 THEN '10+ Years'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 5 THEN '5-9 Years'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 3 THEN '3-4 Years'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 1 THEN '1-2 Years'
        ELSE 'Less than 1 year'
    END AS tenure_category,
    s.amount AS current_salary,
    CASE
        WHEN s.amount > 0 THEN
            ROUND(
                s.amount / POWER(1.03,
                    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
                ),
                2
            )
        ELSE NULL
    END AS estimated_starting_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
ORDER BY EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) DESC;

-- Distribuzione anzianità per dipartimento
SELECT
    d.name AS department,
    COUNT(*) AS total_employees,
    ROUND(AVG(
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
    ), 2) AS avg_years_tenure,
    ROUND(MIN(
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
    ), 2) AS min_years,
    ROUND(MAX(
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
    ), 2) AS max_years,
    COUNT(*) FILTER (
        WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 5
    ) AS employees_5plus_years,
    ROUND(AVG(s.amount), 2) AS avg_salary,
    ROUND(
        AVG(s.amount) FILTER (
            WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 5
        ),
        2
    ) AS avg_salary_5plus_years
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
GROUP BY d.name
ORDER BY avg_years_tenure DESC;

-- Previsioni turnover (anniversari assunzione prossimi 6 mesi)
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    e.hire_date,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS years_of_service,
    DATE_TRUNC('year', e.hire_date) +
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) + 1 AS next_anniversary,
    CURRENT_DATE AS today,
    (DATE_TRUNC('year', e.hire_date) +
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) + 1) - CURRENT_DATE AS days_until_anniversary,
    j.title AS job,
    s.amount AS salary
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
WHERE (DATE_TRUNC('year', e.hire_date) +
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) + 1) - CURRENT_DATE
      BETWEEN 0 AND 180
ORDER BY days_until_anniversary;

-- =====================================================
-- 5. PERFORMANCE REVIEWS BY DEPARTMENT
-- =====================================================
-- Analisi performance aggregata per dipartimento

SELECT
    d.name AS department,
    COUNT(pr.id) AS total_reviews,
    COUNT(DISTINCT pr.employee_id) AS employees_reviewed,
    ROUND(AVG(pr.rating), 2) AS average_rating,
    ROUND(MIN(pr.rating), 2) AS min_rating,
    ROUND(MAX(pr.rating), 2) AS max_rating,
    ROUND(AVG(pr.rating) FILTER (WHERE pr.rating >= 4), 2) AS avg_top_performers,
    COUNT(*) FILTER (WHERE pr.rating = 5) AS five_star_count,
    COUNT(*) FILTER (WHERE pr.rating = 5) * 100.0 / COUNT(*) AS five_star_percentage,
    COUNT(*) FILTER (WHERE pr.rating <= 2) AS poor_performance_count,
    COUNT(*) FILTER (WHERE pr.goals_met = 'yes') * 100.0 / COUNT(*) AS goals_met_percentage,
    STRING_AGG(DISTINCT j.title, ', ') AS jobs_reviewed
FROM performance_reviews pr
JOIN employees e ON pr.employee_id = e.id
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
GROUP BY d.name
ORDER BY average_rating DESC;

-- Trend performance nel tempo per dipendente
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    pr.review_date,
    EXTRACT(YEAR FROM pr.review_date) AS review_year,
    pr.rating,
    pr.goals_met,
    s.amount AS salary_at_review,
    LAG(pr.rating) OVER (PARTITION BY e.id ORDER BY pr.review_date) AS prev_rating,
    pr.rating - LAG(pr.rating) OVER (PARTITION BY e.id ORDER BY pr.review_date) AS rating_change,
    LAG(s.amount) OVER (PARTITION BY e.id ORDER BY pr.review_date) AS prev_salary,
    s.amount - LAG(s.amount) OVER (PARTITION BY e.id ORDER BY pr.review_date) AS salary_change
FROM performance_reviews pr
JOIN employees e ON pr.employee_id = e.id
JOIN departments d ON e.department_id = d.id
JOIN salaries s ON e.id = s.employee_id
    AND s.effective_date <= pr.review_date
    AND (s.end_date IS NULL OR s.end_date >= pr.review_date)
ORDER BY e.id, pr.review_date;

-- Correlazione rating - stipendio
SELECT
    pr.rating,
    COUNT(*) AS employee_count,
    ROUND(AVG(s.amount), 2) AS average_salary,
    ROUND(MIN(s.amount), 2) AS min_salary,
    ROUND(MAX(s.amount), 2) AS max_salary,
    ROUND(AVG(
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
    ), 2) AS avg_years_service
FROM performance_reviews pr
JOIN employees e ON pr.employee_id = e.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
WHERE pr.review_date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY pr.rating
ORDER BY pr.rating DESC;

-- =====================================================
-- 6. ATTENDANCE ANALYSIS (Absenteeism)
-- =====================================================
-- Analisi dettagliata delle assenze per dipartimento

SELECT
    d.name AS department,
    COUNT(*) AS total_records,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS days_present,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS days_absent,
    SUM(CASE WHEN a.status = 'late' THEN 1 ELSE 0 END) AS days_late,
    SUM(CASE WHEN a.status = 'sick' THEN 1 ELSE 0 END) AS days_sick,
    SUM(CASE WHEN a.status = 'vacation' THEN 1 ELSE 0 END) AS days_vacation,
    SUM(CASE WHEN a.status = 'half_day' THEN 1 ELSE 0 END) AS half_days,
    ROUND(
        SUM(CASE WHEN a.status IN ('absent', 'sick') THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS absenteeism_rate_pct,
    ROUND(
        SUM(CASE WHEN a.status = 'late' THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS late_rate_pct,
    ROUND(SUM(a.hours_worked), 2) AS total_hours_worked,
    ROUND(AVG(a.hours_worked), 2) AS avg_daily_hours
FROM attendance a
JOIN employees e ON a.employee_id = e.id
JOIN departments d ON e.department_id = d.id
GROUP BY d.name
ORDER BY absenteeism_rate_pct DESC;

-- Top dipendenti con problemi di assenteismo
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    COUNT(*) AS total_days,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS days_present,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS days_absent,
    SUM(CASE WHEN a.status = 'late' THEN 1 ELSE 0 END) AS days_late,
    SUM(CASE WHEN a.status = 'sick' THEN 1 ELSE 0 END) AS days_sick,
    ROUND(
        SUM(CASE WHEN a.status IN ('absent', 'sick') THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS absenteeism_rate,
    ROUND(SUM(a.hours_worked), 2) AS total_hours,
    ROUND(AVG(a.hours_worked), 2) AS avg_daily_hours
FROM attendance a
JOIN employees e ON a.employee_id = e.id
JOIN departments d ON e.department_id = d.id
GROUP BY e.employee_number, e.first_name, e.last_name, d.name
HAVING SUM(CASE WHEN a.status IN ('absent', 'sick') THEN 1 ELSE 0 END) > 0
ORDER BY absenteeism_rate DESC
LIMIT 20;

-- Analisi mensile presenze per anno
SELECT
    d.name AS department,
    EXTRACT(YEAR FROM a.attendance_date) AS year,
    EXTRACT(MONTH FROM a.attendance_date) AS month,
    TO_CHAR(a.attendance_date, 'Mon') AS month_name,
    COUNT(*) AS total_days,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_days,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS absent_days,
    SUM(CASE WHEN a.status = 'sick' THEN 1 ELSE 0 END) AS sick_days,
    SUM(CASE WHEN a.status = 'vacation' THEN 1 ELSE 0 END) AS vacation_days,
    ROUND(SUM(a.hours_worked), 2) AS total_hours,
    ROUND(AVG(a.hours_worked), 2) AS avg_daily_hours
FROM attendance a
JOIN employees e ON a.employee_id = e.id
JOIN departments d ON e.department_id = d.id
WHERE a.attendance_date >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
GROUP BY d.name, EXTRACT(YEAR FROM a.attendance_date), EXTRACT(MONTH FROM a.attendance_date), TO_CHAR(a.attendance_date, 'Mon')
ORDER BY d.name, year DESC, month;

-- =====================================================
-- 7. SALARY HISTORY TIMELINE
-- =====================================================
-- Timeline completa cambiamenti stipendio per dipendente

SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    j.title AS job,
    s1.amount AS old_salary,
    s2.amount AS new_salary,
    s2.amount - s1.amount AS salary_change,
    ROUND(
        (s2.amount - s1.amount) / NULLIF(s1.amount, 0) * 100,
        2
    ) AS change_percentage,
    s1.effective_date AS old_salary_from,
    s1.end_date AS old_salary_to,
    s2.effective_date AS new_salary_from,
    s2.end_date AS new_salary_to,
    s2.effective_date - s1.effective_date AS days_between_changes,
    ROUND(
        EXTRACT(DAY FROM (s2.effective_date - s1.effective_date)) / 365.25,
        2
    ) AS years_between_changes
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s1 ON e.id = s1.employee_id
JOIN salaries s2 ON e.id = s2.employee_id
WHERE s2.effective_date = (
    SELECT MIN(effective_date)
    FROM salaries
    WHERE employee_id = e.id
    AND effective_date > s1.effective_date
)
ORDER BY e.id, s2.effective_date;

-- Storico stipendio completo con job history
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    s.effective_date,
    s.end_date,
    s.amount AS salary,
    jh.job_id,
    j.title AS job_title,
    jh.department_id,
    d.name AS department,
    CASE
        WHEN s.amount < j.min_salary THEN 'Below Minimum'
        WHEN s.amount > j.max_salary THEN 'Above Maximum'
        ELSE 'Within Range'
    END AS salary_position,
    ROUND(
        (s.amount - j.min_salary) / NULLIF(j.max_salary - j.min_salary, 0) * 100,
        1
    ) AS percentile_in_range,
    CASE
        WHEN LAG(s.amount) OVER (PARTITION BY e.id ORDER BY s.effective_date) IS NOT NULL THEN
            ROUND(
                (s.amount - LAG(s.amount) OVER (PARTITION BY e.id ORDER BY s.effective_date)) /
                NULLIF(LAG(s.amount) OVER (PARTITION BY e.id ORDER BY s.effective_date), 0) * 100,
                2
            )
        ELSE NULL
    END AS increase_percentage
FROM employees e
JOIN salaries s ON e.id = s.employee_id
JOIN jobs j ON e.job_id = j.id
LEFT JOIN departments d ON e.department_id = d.id
LEFT JOIN job_history jh ON e.id = jh.employee_id
    AND s.effective_date >= jh.start_date
    AND (jh.end_date IS NULL OR s.effective_date <= jh.end_date)
ORDER BY e.id, s.effective_date;

-- =====================================================
-- 8. JOB CHANGES & PROMOTIONS
-- =====================================================
-- Analisi completa delle carriere e promozioni

-- Tutti i cambiamenti di lavoro con confronto stipendi
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    jh1.start_date AS change_date,
    jh1.reason AS change_reason,
    j1.title AS old_job,
    j2.title AS new_job,
    d1.name AS old_department,
    d2.name AS new_department,
    CASE
        WHEN j1.id != j2.id THEN 'Job Change'
        WHEN d1.id != d2.id THEN 'Department Change'
        ELSE 'Other Change'
    END AS change_type,
    s1.amount AS old_salary,
    s2.amount AS new_salary,
    COALESCE(s2.amount, 0) - COALESCE(s1.amount, 0) AS salary_difference,
    ROUND(
        (s2.amount - s1.amount) / NULLIF(s1.amount, 0) * 100,
        2
    ) AS salary_increase_pct
FROM job_history jh1
JOIN job_history jh2 ON jh1.employee_id = jh2.employee_id
    AND jh1.start_date > COALESCE(jh2.start_date, '1900-01-01')
JOIN employees e ON jh1.employee_id = e.id
JOIN jobs j1 ON jh1.job_id = j1.id
JOIN jobs j2 ON jh2.job_id = j2.id
JOIN departments d1 ON jh1.department_id = d1.id
JOIN departments d2 ON jh2.department_id = d2.id
LEFT JOIN salaries s1 ON e.id = s1.employee_id
    AND s1.effective_date <= jh1.start_date
    AND (s1.end_date IS NULL OR s1.end_date >= jh1.start_date)
LEFT JOIN salaries s2 ON e.id = s2.employee_id
    AND s2.effective_date <= jh2.start_date
    AND (s2.end_date IS NULL OR s2.end_date >= jh2.start_date)
WHERE j1.id != j2.id OR d1.id != d2.id
ORDER BY e.id, jh1.start_date DESC;

-- Promozioni (cambiamento job con stipendio più alto)
WITH job_changes AS (
    SELECT
        e.employee_number,
        e.first_name || ' ' || e.last_name AS employee,
        e.hire_date,
        jh.start_date,
        j1.title AS old_title,
        j2.title AS new_title,
        d.name AS department,
        j1.min_salary AS old_min,
        j1.max_salary AS old_max,
        j2.min_salary AS new_min,
        j2.max_salary AS new_max,
        s1.amount AS old_salary,
        s2.amount AS new_salary,
        ROW_NUMBER() OVER (PARTITION BY e.id ORDER BY jh.start_date) AS change_number
    FROM job_history jh
    JOIN employees e ON jh.employee_id = e.id
    JOIN jobs j1 ON jh.job_id = j1.id
    JOIN jobs j2 ON e.job_id = j2.id
    JOIN departments d ON e.department_id = d.id
    LEFT JOIN salaries s1 ON e.id = s1.employee_id
        AND s1.effective_date <= jh.start_date
        AND (s1.end_date IS NULL OR s1.end_date >= jh.start_date)
    LEFT JOIN salaries s2 ON e.id = s2.employee_id
        AND s2.effective_date <= e.hire_date
        AND (s2.end_date IS NULL OR s2.end_date >= e.hire_date)
    WHERE j2.max_salary > j1.max_salary
)
SELECT
    employee_number,
    employee,
    department,
    start_date AS promotion_date,
    old_title || ' -> ' || new_title AS promotion,
    old_salary,
    new_salary,
    new_salary - old_salary AS salary_increase,
    ROUND(
        (new_salary - old_salary) / NULLIF(old_salary, 0) * 100,
        2
    ) AS increase_percentage,
    old_max - old_min AS old_range,
    new_max - new_min AS new_range,
    EXTRACT(YEAR FROM start_date - hire_date) AS years_until_promotion
FROM job_changes
WHERE new_salary > old_salary
ORDER BY increase_percentage DESC;

-- =====================================================
-- 9. DEPARTMENT BUDGET VS ACTUAL SALARIES
-- =====================================================
-- Analisi budget vs costi salariali con proiezioni

SELECT
    d.id AS department_id,
    d.name AS department,
    d.budget AS annual_budget,
    l.city AS location,
    COUNT(e.id) AS headcount,
    COUNT(e.id) FILTER (WHERE e.status = 'active') AS active_employees,
    ROUND(SUM(s.amount), 2) AS total_annual_salaries,
    ROUND(d.budget - SUM(s.amount), 2) AS budget_remaining,
    ROUND(
        (SUM(s.amount) / NULLIF(d.budget, 0)) * 100,
        2
    ) AS budget_utilization_pct,
    ROUND(
        SUM(s.amount) / NULLIF(COUNT(e.id), 0),
        2
    ) AS avg_salary_per_employee,
    j.min_title AS lowest_job_title,
    j.max_title AS highest_job_title,
    ROUND(j.min_salary, 2) AS lowest_paid_salary,
    ROUND(j.max_salary, 2) AS highest_paid_salary,
    -- Proiezione: costo se assumiamo 5 dipendenti in più
    ROUND(SUM(s.amount) + (
        SELECT AVG(amount)
        FROM salaries
        WHERE end_date IS NULL
    ) * 5, 2) AS projected_cost_with_5_hires,
    -- Cap massima assunzioni con budget attuale
    FLOOR((d.budget - SUM(s.amount)) / NULLIF((
        SELECT AVG(amount)
        FROM salaries
        WHERE end_date IS NULL
    ), 0)) AS max_hires_within_budget
FROM departments d
JOIN locations l ON d.location_id = l.id
LEFT JOIN employees e ON d.id = e.department_id AND e.status = 'active'
LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
LEFT JOIN LATERAL (
    SELECT
        MIN(j1.title) AS min_title,
        MAX(j1.title) AS max_title,
        MIN(j1.min_salary) AS min_salary,
        MAX(j1.max_salary) AS max_salary
    FROM jobs j1
    JOIN employees e1 ON e1.job_id = j1.id
    WHERE e1.department_id = d.id
) j ON true
GROUP BY d.id, d.name, d.budget, l.city, j.min_title, j.max_title,
         j.min_salary, j.max_salary
ORDER BY budget_utilization_pct DESC;

-- =====================================================
-- 10. HEADCOUNT BY DEPARTMENT AND JOB
-- =====================================================
-- Matrice organizzativa completa

SELECT
    d.name AS department,
    j.title AS job_title,
    COUNT(e.id) AS headcount,
    COUNT(e.id) FILTER (WHERE e.status = 'active') AS active_count,
    COUNT(e.id) FILTER (WHERE e.status = 'on_leave') AS on_leave_count,
    COUNT(e.id) FILTER (WHERE e.status = 'terminated') AS terminated_count,
    COUNT(e.id) FILTER (WHERE e.status = 'resigned') AS resigned_count,
    ROUND(AVG(
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
    ), 2) AS avg_tenure_years,
    ROUND(AVG(s.amount), 2) AS avg_salary,
    ROUND(MIN(s.amount), 2) AS min_salary,
    ROUND(MAX(s.amount), 2) AS max_salary,
    ROUND(SUM(s.amount), 2) AS total_annual_cost,
    j.min_salary AS job_min_range,
    j.max_salary AS job_max_range,
    -- Percentuale dipendenti sotto range minimo
    ROUND(
        COUNT(*) FILTER (
            WHERE s.amount < j.min_salary
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS pct_below_min_range,
    -- Percentuale dipendenti sopra range massimo
    ROUND(
        COUNT(*) FILTER (
            WHERE s.amount > j.max_salary
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS pct_above_max_range
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
LEFT JOIN jobs j ON e.job_id = j.id
LEFT JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
GROUP BY d.name, j.title, j.min_salary, j.max_salary
ORDER BY d.name, headcount DESC;

-- Pivot table-like view: dipartimenti vs livelli job
SELECT
    d.name AS department,
    COUNT(*) FILTER (WHERE j.title LIKE '%CEO%' OR j.title LIKE '%CTO%' OR j.title LIKE '%CFO%') AS executives,
    COUNT(*) FILTER (WHERE j.title LIKE '%Direttore%' OR j.title LIKE '%Director%') AS directors,
    COUNT(*) FILTER (WHERE j.title LIKE '%Manager%' OR j.title LIKE '%Project%') AS managers,
    COUNT(*) FILTER (WHERE j.title LIKE '%Senior%' OR j.title LIKE '%Lead%') AS seniors,
    COUNT(*) FILTER (WHERE j.title LIKE '%Engineer%' OR j.title LIKE '%Developer%' OR j.title LIKE '%Analyst%') AS professionals,
    COUNT(*) FILTER (WHERE j.title LIKE '%Specialist%' OR j.title LIKE '%Assistant%') AS specialists,
    COUNT(*) FILTER (WHERE j.title LIKE '%Support%' OR j.title LIKE '%Representative%') AS support_staff,
    COUNT(*) AS total
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
LEFT JOIN jobs j ON e.job_id = j.id
GROUP BY d.name
ORDER BY d.name;

-- =====================================================
-- 11. EMPLOYEE ANNIVERSARY DATES
-- =====================================================
-- Lista anniversari lavorativi con anni di servizio

SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    j.title AS job_title,
    e.hire_date,
    -- Calcolo anni di servizio completi
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS completed_years,
    -- Prossimo anniversario
    DATE_TRUNC('year', CURRENT_DATE) +
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) + 1 AS next_anniversary,
    -- Giorni mancanti al prossimo anniversario
    (DATE_TRUNC('year', CURRENT_DATE) +
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) + 1) - CURRENT_DATE AS days_until_anniversary,
    -- Categoria anniversario
    CASE
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 20 THEN '20+ Years - Diamond'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 15 THEN '15+ Years - Ruby'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 10 THEN '10+ Years - Gold'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 5 THEN '5+ Years - Silver'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) >= 1 THEN '1+ Years - Bronze'
        ELSE 'New Hire'
    END AS anniversary_category,
    s.amount AS current_salary,
    -- Stima stipendio iniziale (assumendo 3% inflazione annua)
    ROUND(s.amount / POWER(1.03, EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))), 2) AS estimated_starting_salary,
    ROUND(s.amount - s.amount / POWER(1.03, EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))), 2) AS total_salary_growth
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
ORDER BY EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) DESC, days_until_anniversary;

-- =====================================================
-- 12. ADDITIONAL ANALYTICS QUERIES
-- =====================================================

-- Distribuzione età dipendenti
SELECT
    CASE
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.birth_date)) < 25 THEN 'Under 25'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.birth_date)) < 35 THEN '25-34'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.birth_date)) < 45 THEN '35-44'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.birth_date)) < 55 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS headcount,
    ROUND(AVG(s.amount), 2) AS avg_salary,
    COUNT(*) FILTER (WHERE dep.id IS NOT NULL) AS with_dependents,
    ROUND(AVG(
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date))
    ), 2) AS avg_tenure
FROM employees e
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
LEFT JOIN dependents dep ON e.id = dep.employee_id
GROUP BY age_group
ORDER BY
    CASE age_group
        WHEN 'Under 25' THEN 1
        WHEN '25-34' THEN 2
        WHEN '35-44' THEN 3
        WHEN '45-54' THEN 4
        ELSE 5
    END;

-- Top performer identification (high rating + tenure)
SELECT
    e.employee_number,
    e.first_name || ' ' || e.last_name AS employee,
    d.name AS department,
    j.title AS job,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.hire_date)) AS years_tenure,
    ROUND(AVG(pr.rating), 2) AS avg_performance_rating,
    COUNT(pr.id) AS total_reviews,
    COUNT(*) FILTER (WHERE pr.rating = 5) AS five_star_reviews,
    s.amount AS salary,
    j.min_salary,
    j.max_salary,
    -- Calcola posizione stipendio nel range
    ROUND(
        (s.amount - j.min_salary) / NULLIF(j.max_salary - j.min_salary, 0) * 100,
        1
    ) AS salary_percentile
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN jobs j ON e.job_id = j.id
JOIN salaries s ON e.id = s.employee_id AND s.end_date IS NULL
JOIN performance_reviews pr ON e.id = pr.employee_id
WHERE pr.review_date >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY e.employee_number, e.first_name, e.last_name, d.name,
         j.title, j.min_salary, j.max_salary, s.amount, e.hire_date
HAVING AVG(pr.rating) >= 4.0 AND COUNT(pr.id) >= 2
ORDER BY avg_performance_rating DESC, years_tenure DESC;

-- =====================================================
-- FINE QUERIES
-- =====================================================
