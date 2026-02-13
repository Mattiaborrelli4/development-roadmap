-- =====================================================
-- HR MANAGEMENT SYSTEM - SAMPLE DATA
-- Dati di Esempio - Sistema HR
-- =====================================================
-- Database: PostgreSQL
-- Contenuto: Dati realistici per testing e sviluppo
-- =====================================================

-- =====================================================
-- LOCATIONS (Sedi Aziendali)
-- =====================================================
INSERT INTO locations (address, city, country, postal_code) VALUES
('Via Roma 123', 'Milano', 'Italia', '20100'),
('Corso Italia 45', 'Torino', 'Italia', '10100'),
('Via Veneto 78', 'Roma', 'Italia', '00187'),
('Viale Cristoforo Colombo 200', 'Roma', 'Italia', '00144'),
('Piazza Duomo 15', 'Milano', 'Italia', '20122'),
('Via Toledo 88', 'Napoli', 'Italia', '80134'),
('Via Zamboni 33', 'Bologna', 'Italia', '40126'),
('Piazza De Ferrari 12', 'Genova', 'Italia', '16124'),
('Via Nazionale 56', 'Firenze', 'Italia', '50123'),
('Viale XX Settembre 99', 'Padova', 'Italia', '35122');

-- =====================================================
-- DEPARTMENTS (Dipartimenti)
-- =====================================================
INSERT INTO departments (name, location_id, manager_id, budget, description) VALUES
('Amministrazione', 1, NULL, 150000.00, 'Gestione amministrativa e contabile'),
('Risorse Umane', 1, NULL, 120000.00, 'Gestione del personale e reclutamento'),
('Informatica', 2, NULL, 300000.00, 'Sviluppo software e IT infrastructure'),
('Marketing', 3, NULL, 200000.00, 'Marketing digitale e comunicazione'),
('Vendite', 3, NULL, 250000.00, 'Vendite dirette e canali commerciali'),
('Produzione', 4, NULL, 500000.00, 'Produzione e manifattura'),
('Ricerca e Sviluppo', 2, NULL, 350000.00, 'Innovazione e nuovi prodotti'),
('Customer Service', 5, NULL, 100000.00, 'Assistenza clienti'),
('Finanza', 6, NULL, 180000.00, 'Gestione finanziaria e controlli'),
('Legale', 7, NULL, 130000.00, 'Servizi legali e compliance');

-- =====================================================
-- JOBS (Posizioni Lavorative)
-- =====================================================
INSERT INTO jobs (title, description, min_salary, max_salary) VALUES
('CEO', 'Amministratore Delegato', 150000.00, 250000.00),
('CTO', 'Direttore Tecnico', 120000.00, 180000.00),
('CFO', 'Direttore Finanziario', 110000.00, 170000.00),
('Direttore HR', 'Direttore Risorse Umane', 80000.00, 120000.00),
('Direttore Marketing', 'Direttore Marketing', 85000.00, 130000.00),
('Direttore Vendite', 'Direttore Commerciale', 90000.00, 140000.00),
('Project Manager', 'Project Manager Senior', 60000.00, 85000.00),
('Software Engineer', 'Sviluppatore Software', 45000.00, 70000.00),
('Senior Developer', 'Sviluppatore Senior', 55000.00, 80000.00),
('Data Analyst', 'Analista Dati', 40000.00, 65000.00),
('HR Specialist', 'Specialista HR', 35000.00, 50000.00),
('Recruiter', 'Addetto Selezione', 30000.00, 45000.00),
('Marketing Specialist', 'Specialista Marketing', 35000.00, 55000.00),
('Sales Representative', 'Representative Vendite', 32000.00, 50000.00),
('Account Manager', 'Account Manager', 40000.00, 60000.00),
('Production Manager', 'Responsabile Produzione', 55000.00, 80000.00),
('Quality Engineer', 'Ingegnere Qualità', 40000.00, 60000.00),
('Research Scientist', 'Scienziato Ricerca', 50000.00, 75000.00),
('Customer Support', 'Supporto Clienti', 28000.00, 40000.00),
('Financial Analyst', 'Analista Finanziario', 40000.00, 60000.00),
('Legal Advisor', 'Consulente Legale', 45000.00, 70000.00),
('Office Assistant', 'Assistente Amministrativo', 25000.00, 35000.00);

-- =====================================================
-- EMPLOYEES (Dipendenti - 55 records)
-- =====================================================
INSERT INTO employees (employee_number, first_name, last_name, email, phone, birth_date, hire_date,
                      job_id, department_id, manager_id, status) VALUES

-- Amministrazione
('EMP001', 'Marco', 'Rossi', 'marco.rossi@company.it', '+39 02 1234567', '1975-03-15', '2015-01-10', 1, 1, NULL, 'active'),
('EMP002', 'Laura', 'Bianchi', 'laura.bianchi@company.it', '+39 02 1234568', '1980-07-22', '2016-03-20', 22, 1, 1, 'active'),
('EMP003', 'Giuseppe', 'Ferrari', 'giuseppe.ferrari@company.it', '+39 02 1234569', '1985-11-30', '2017-06-15', 22, 1, 1, 'active'),

-- Risorse Umane
('EMP004', 'Anna', 'Verdi', 'anna.verdi@company.it', '+39 02 1234570', '1978-09-12', '2014-02-01', 4, 2, NULL, 'active'),
('EMP005', 'Paola', 'Colombo', 'paola.colombo@company.it', '+39 02 1234571', '1988-04-25', '2018-04-10', 11, 2, 4, 'active'),
('EMP006', 'Roberto', 'Gallo', 'roberto.gallo@company.it', '+39 02 1234572', '1990-08-17', '2019-07-22', 12, 2, 4, 'active'),
('EMP007', 'Chiara', 'Rizzo', 'chiara.rizzo@company.it', '+39 02 1234573', '1992-12-05', '2020-01-15', 12, 2, 4, 'active'),

-- Informatica
('EMP008', 'Massimo', 'Moretti', 'massimo.moretti@company.it', '+39 011 2345678', '1976-05-20', '2013-06-01', 2, 3, NULL, 'active'),
('EMP009', 'Elena', 'Conte', 'elena.conte@company.it', '+39 011 2345679', '1982-02-14', '2015-09-15', 9, 3, 8, 'active'),
('EMP010', 'Luca', 'Martini', 'luca.martini@company.it', '+39 011 2345680', '1987-06-30', '2016-11-20', 8, 3, 8, 'active'),
('EMP011', 'Simone', 'Sanna', 'simone.sanna@company.it', '+39 011 2345681', '1990-09-08', '2017-08-12', 8, 3, 8, 'active'),
('EMP012', 'Francesca', 'Ferrara', 'francesca.ferrara@company.it', '+39 011 2345682', '1993-03-25', '2018-02-28', 8, 3, 8, 'active'),
('EMP013', 'Andrea', 'Costa', 'andrea.costa@company.it', '+39 011 2345683', '1991-07-12', '2017-05-10', 7, 3, 8, 'active'),
('EMP014', 'Sara', 'Giordano', 'sara.giordano@company.it', '+39 011 2345684', '1994-10-18', '2019-04-22', 8, 3, 8, 'active'),
('EMP015', 'Davide', 'Mancini', 'davide.mancini@company.it', '+39 011 2345685', '1992-01-30', '2018-09-05', 10, 3, 8, 'active'),

-- Marketing
('EMP016', 'Valentina', 'Rinaldi', 'valentina.rinaldi@company.it', '+39 06 3456789', '1979-11-08', '2014-07-01', 5, 4, NULL, 'active'),
('EMP017', 'Federico', 'Santoro', 'federico.santoro@company.it', '+39 06 3456790', '1986-03-22', '2017-02-15', 13, 4, 16, 'active'),
('EMP018', 'Alessandra', 'Marino', 'alessandra.marino@company.it', '+39 06 3456791', '1989-07-14', '2018-06-20', 13, 4, 16, 'active'),
('EMP019', 'Matteo', 'Greco', 'matteo.greco@company.it', '+39 06 3456792', '1991-12-01', '2019-03-11', 13, 4, 16, 'active'),

-- Vendite
('EMP020', 'Carlo', 'Bruno', 'carlo.bruno@company.it', '+39 06 4567890', '1977-08-25', '2013-03-15', 6, 5, NULL, 'active'),
('EMP021', 'Daniela', 'Parisi', 'daniela.parisi@company.it', '+39 06 4567891', '1984-05-12', '2015-10-20', 14, 5, 20, 'active'),
('EMP022', 'Stefano', 'Romano', 'stefano.romano@company.it', '+39 06 4567892', '1988-09-28', '2016-12-05', 14, 5, 20, 'active'),
('EMP023', 'Monica', 'Ricci', 'monica.ricci@company.it', '+39 06 4567893', '1990-02-17', '2017-08-30', 14, 5, 20, 'active'),
('EMP024', 'Enzo', 'Lombardi', 'enzo.lombardi@company.it', '+39 06 4567894', '1986-06-03', '2016-04-18', 15, 5, 20, 'active'),
('EMP025', 'Cristina', 'Barbieri', 'cristina.barbieri@company.it', '+39 06 4567895', '1992-11-20', '2019-01-25', 15, 5, 20, 'active'),
('EMP026', 'Giovanni', 'Calabrese', 'giovanni.calabrese@company.it', '+39 06 4567896', '1989-04-08', '2018-07-12', 14, 5, 20, 'active'),

-- Produzione
('EMP027', 'Antonio', 'Esposito', 'antonio.esposito@company.it', '+39 06 5678901', '1974-01-10', '2012-09-01', 16, 6, NULL, 'active'),
('EMP028', 'Rosa', 'D''Angelo', 'rosa.dangelo@company.it', '+39 06 5678902', '1983-07-26', '2015-05-15', 17, 6, 27, 'active'),
('EMP029', 'Luigi', 'Pepe', 'luigi.pepe@company.it', '+39 06 5678903', '1987-10-14', '2017-01-20', 17, 6, 27, 'active'),
('EMP030', 'Angela', 'Longo', 'angela.longo@company.it', '+39 06 5678904', '1990-05-30', '2018-09-10', 17, 6, 27, 'active'),
('EMP031', 'Vincenzo', 'Serra', 'vincenzo.serra@company.it', '+39 06 5678905', '1985-12-18', '2016-03-22', 17, 6, 27, 'active'),
('EMP032', 'Teresa', 'Neri', 'teresa.neri@company.it', '+39 06 5678906', '1993-08-02', '2019-05-14', 17, 6, 27, 'active'),

-- Ricerca e Sviluppo
('EMP033', 'Paolo', 'Fiore', 'paolo.fiore@company.it', '+39 011 3456789', '1973-04-22', '2011-11-15', 18, 7, NULL, 'active'),
('EMP034', 'Marta', 'Basile', 'marta.basile@company.it', '+39 011 3456790', '1981-09-05', '2014-08-20', 18, 7, 33, 'active'),
('EMP035', 'Fabio', 'Farina', 'fabio.farina@company.it', '+39 011 3456791', '1986-02-28', '2016-04-12', 18, 7, 33, 'active'),
('EMP036', 'Elisabetta', 'Cattaneo', 'elisabetta.cattaneo@company.it', '+39 011 3456792', '1989-06-19', '2017-11-08', 18, 7, 33, 'active'),

-- Customer Service
('EMP037', 'Giovanna', 'Ruggiero', 'giovanna.ruggiero@company.it', '+39 02 4567890', '1980-10-30', '2014-05-01', 19, 8, NULL, 'active'),
('EMP038', 'Alberto', 'Lombardo', 'alberto.lombardo@company.it', '+39 02 4567891', '1988-03-15', '2017-02-20', 19, 8, 37, 'active'),
('EMP039', 'Irene', 'Moretti', 'irene.moretti@company.it', '+39 02 4567892', '1991-08-07', '2018-10-15', 19, 8, 37, 'active'),
('EMP040', 'Ernesto', 'Sorrentino', 'ernesto.sorrentino@company.it', '+39 02 4567893', '1994-01-22', '2019-06-30', 19, 8, 37, 'active'),
('EMP041', 'Donatella', 'De Luca', 'donatella.deluca@company.it', '+39 02 4567894', '1990-11-13', '2018-04-18', 19, 8, 37, 'active'),

-- Finanza
('EMP042', 'Riccardo', 'Messina', 'riccardo.messina@company.it', '+39 081 567890', '1972-06-18', '2010-08-01', 3, 9, NULL, 'active'),
('EMP043', 'Barbara', 'Martinelli', 'barbara.martinelli@company.it', '+39 081 567891', '1983-12-10', '2015-07-22', 20, 9, 42, 'active'),
('EMP044', 'Silvia', 'Caruso', 'silvia.caruso@company.it', '+39 081 567892', '1987-04-05', '2016-09-14', 20, 9, 42, 'active'),

-- Legale
('EMP045', 'Franco', 'Vitale', 'franco.vitale@company.it', '+39 051 678901', '1976-09-25', '2013-04-10', 21, 10, NULL, 'active'),
('EMP046', 'Patrizia', 'Grasso', 'patrizia.grasso@company.it', '+39 051 678902', '1985-03-08', '2016-11-28', 21, 10, 45, 'active'),

-- Altri dipendenti vari
('EMP047', 'Emilio', 'Guerra', 'emilio.guerra@company.it', '+39 06 6789012', '1984-07-20', '2015-02-15', 13, 4, 16, 'active'),
('EMP048', 'Letizia', 'Pace', 'letizia.pace@company.it', '+39 06 6789013', '1989-10-11', '2017-06-05', 8, 3, 8, 'active'),
('EMP049', 'Renzo', 'Rossetti', 'renzo.rossetti@company.it', '+39 02 5678901', '1991-05-03', '2018-12-01', 14, 5, 20, 'active'),
('EMP050', 'Katia', 'Marescotti', 'katia.marescotti@company.it', '+39 02 5678902', '1993-09-26', '2019-08-19', 19, 8, 37, 'active'),
('EMP051', 'Mirko', 'De Santis', 'mirko.desantis@company.it', '+39 011 4567890', '1988-02-14', '2016-10-22', 17, 6, 27, 'active'),
('EMP052', 'Serena', 'Montanari', 'serena.montanari@company.it', '+39 011 4567891', '1992-06-30', '2018-03-12', 18, 7, 33, 'active'),
('EMP053', 'Emanuele', 'Pellegrini', 'emanuele.pellegrini@company.it', '+39 02 6789014', '1986-11-08', '2015-09-18', 20, 9, 42, 'active'),
('EMP054', 'Claudia', 'Ferretti', 'claudia.ferretti@company.it', '+39 051 789012', '1990-04-16', '2017-08-02', 21, 10, 45, 'active'),
('EMP055', 'Dario', 'Palumbo', 'dario.palumbo@company.it', '+39 06 7890123', '1994-07-29', '2019-02-14', 12, 2, 4, 'active');

-- Aggiorna i manager_id dei dipartimenti
UPDATE departments SET manager_id = 1 WHERE id = 1;  -- Amministrazione -> Marco Rossi
UPDATE departments SET manager_id = 4 WHERE id = 2;  -- HR -> Anna Verdi
UPDATE departments SET manager_id = 8 WHERE id = 3;  -- Informatica -> Massimo Moretti
UPDATE departments SET manager_id = 16 WHERE id = 4; -- Marketing -> Valentina Rinaldi
UPDATE departments SET manager_id = 20 WHERE id = 5; -- Vendite -> Carlo Bruno
UPDATE departments SET manager_id = 27 WHERE id = 6; -- Produzione -> Antonio Esposito
UPDATE departments SET manager_id = 33 WHERE id = 7; -- R&D -> Paolo Fiore
UPDATE departments SET manager_id = 37 WHERE id = 8; -- Customer Service -> Giovanna Ruggiero
UPDATE departments SET manager_id = 42 WHERE id = 9; -- Finanza -> Riccardo Messina
UPDATE departments SET manager_id = 45 WHERE id = 10; -- Legale -> Franco Vitale

-- =====================================================
-- SALARIES (Stipendi)
-- =====================================================
INSERT INTO salaries (employee_id, amount, effective_date, end_date) VALUES
-- CEO e Direttori
(1, 200000.00, '2015-01-10', NULL),
(4, 100000.00, '2014-02-01', NULL),
(8, 150000.00, '2013-06-01', NULL),
(16, 105000.00, '2014-07-01', NULL),
(20, 115000.00, '2013-03-15', NULL),
(27, 68000.00, '2012-09-01', NULL),
(33, 62000.00, '2011-11-15', NULL),
(37, 33000.00, '2014-05-01', NULL),
(42, 140000.00, '2010-08-01', NULL),
(45, 58000.00, '2013-04-10', NULL),

-- Project Manager e Senior
(9, 70000.00, '2015-09-15', NULL),
(10, 65000.00, '2016-11-20', NULL),
(13, 72000.00, '2017-05-10', NULL),

-- Altri dipendenti con stipendi vari
(2, 30000.00, '2016-03-20', NULL),
(3, 29000.00, '2017-06-15', NULL),
(5, 42000.00, '2018-04-10', NULL),
(6, 38000.00, '2019-07-22', NULL),
(7, 36000.00, '2020-01-15', NULL),
(11, 62000.00, '2017-08-12', NULL),
(12, 58000.00, '2018-02-28', NULL),
(14, 55000.00, '2019-04-22', NULL),
(15, 52000.00, '2018-09-05', NULL),
(17, 48000.00, '2017-02-15', NULL),
(18, 45000.00, '2018-06-20', NULL),
(19, 43000.00, '2019-03-11', NULL),
(21, 42000.00, '2015-10-20', NULL),
(22, 40000.00, '2016-12-05', NULL),
(23, 41000.00, '2017-08-30', NULL),
(24, 50000.00, '2016-04-18', NULL),
(25, 48000.00, '2019-01-25', NULL),
(26, 39000.00, '2018-07-12', NULL),
(28, 50000.00, '2015-05-15', NULL),
(29, 48000.00, '2017-01-20', NULL),
(30, 46000.00, '2018-09-10', NULL),
(31, 49000.00, '2016-03-22', NULL),
(32, 45000.00, '2019-05-14', NULL),
(34, 65000.00, '2014-08-20', NULL),
(35, 62000.00, '2016-04-12', NULL),
(36, 58000.00, '2017-11-08', NULL),
(38, 34000.00, '2017-02-20', NULL),
(39, 32000.00, '2018-10-15', NULL),
(40, 30000.00, '2019-06-30', NULL),
(41, 31000.00, '2018-04-18', NULL),
(43, 50000.00, '2015-07-22', NULL),
(44, 48000.00, '2016-09-14', NULL),
(46, 58000.00, '2016-11-28', NULL),
(47, 44000.00, '2015-02-15', NULL),
(48, 64000.00, '2017-06-05', NULL),
(49, 37000.00, '2018-12-01', NULL),
(50, 31000.00, '2019-08-19', NULL),
(51, 47000.00, '2016-10-22', NULL),
(52, 63000.00, '2018-03-12', NULL),
(53, 51000.00, '2015-09-18', NULL),
(54, 52000.00, '2017-08-02', NULL),
(55, 37000.00, '2019-02-14', NULL);

-- Stipendi storici (cambiamenti salariali)
INSERT INTO salaries (employee_id, amount, effective_date, end_date) VALUES
(11, 58000.00, '2017-08-12', '2019-01-15'),
(11, 60000.00, '2019-01-16', '2020-06-30'),
(12, 55000.00, '2018-02-28', '2020-03-01'),
(17, 45000.00, '2017-02-15', '2019-06-30'),
(24, 47000.00, '2016-04-18', '2018-01-15'),
(43, 47000.00, '2015-07-22', '2018-07-01'),
(48, 60000.00, '2017-06-05', '2019-09-15');

-- =====================================================
-- JOB_HISTORY (Storico Posizioni)
-- =====================================================
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, reason) VALUES
-- Promozioni
(11, 2017, 2018, 7, 3, 'Assunto come Project Manager'),
(11, 2018, 2019, 7, 3, 'Promozione a Senior PM'),
(12, 2018, 2020, 8, 3, 'Assunto come Developer'),
(12, 2020, NULL, 9, 3, 'Promozione a Senior Developer'),
(17, 2017, 2019, 13, 4, 'Assunto come Marketing Specialist'),
(24, 2016, 2017, 14, 5, 'Assunto come Sales Rep'),
(24, 2017, NULL, 15, 5, 'Promozione ad Account Manager'),
(43, 2015, 2018, 20, 9, 'Assunto come Financial Analyst'),
(48, 2017, 2019, 8, 3, 'Assunto come Developer'),
(48, 2019, NULL, 9, 3, 'Promozione a Senior Developer'),

-- Trasferimenti dipartimento
(49, 2018, 2019, 13, 4, 'Assunto in Marketing'),
(49, 2019, NULL, 14, 5, 'Trasferito a Vendite'),

-- Dipendenti con storico complesso
(5, 2018, 2019, 12, 2, 'Assunto come Recruiter'),
(5, 2019, NULL, 11, 2, 'Promozione a HR Specialist'),
(13, 2017, 2018, 8, 3, 'Assunto come Developer'),
(13, 2018, NULL, 7, 3, 'Promozione a Project Manager');

-- =====================================================
-- DEPENDENTS (Familiari a Carico)
-- =====================================================
INSERT INTO dependents (employee_id, first_name, last_name, relationship, birth_date) VALUES
-- Famiglie CEO e Direttori
(1, 'Giulia', 'Rossi', 'spouse', '1978-05-20'),
(1, 'Alessandro', 'Rossi', 'child', '2008-03-15'),
(1, 'Sofia', 'Rossi', 'child', '2010-08-22'),
(4, 'Paolo', 'Verdi', 'spouse', '1980-11-15'),
(4, 'Martina', 'Verdi', 'child', '2006-07-08'),
(8, 'Claudia', 'Moretti', 'spouse', '1979-02-10'),
(8, 'Tommaso', 'Moretti', 'child', '2010-04-25'),
(8, 'Giulia', 'Moretti', 'child', '2013-09-12'),
(16, 'Massimo', 'Rinaldi', 'spouse', '1977-08-30'),

-- Altri dipendenti con familiari
(5, 'Andrea', 'Colombo', 'child', '2015-03-20'),
(9, 'Francesco', 'Conte', 'spouse', '1984-06-15'),
(10, 'Elena', 'Martini', 'spouse', '1985-09-20'),
(10, 'Leonardo', 'Martini', 'child', '2012-05-10'),
(13, 'Sara', 'Costa', 'spouse', '1986-03-08'),
(17, 'Luca', 'Santoro', 'child', '2018-11-12'),
(20, 'Roberta', 'Bruno', 'spouse', '1979-04-18'),
(20, 'Chiara', 'Bruno', 'child', '2005-12-01'),
(24, 'Alessia', 'Lombardi', 'spouse', '1985-10-25'),
(27, 'Maria', 'Esposito', 'spouse', '1975-07-12'),
(27, 'Antonio', 'Esposito', 'child', '2002-02-28'),
(27, 'Francesca', 'Esposito', 'child', '2004-06-15'),
(33, 'Anna', 'Fiore', 'spouse', '1974-05-18'),
(37, 'Marco', 'Ruggiero', 'spouse', '1981-01-20'),
(37, 'Sara', 'Ruggiero', 'child', '2014-08-05'),
(42, 'Laura', 'Messina', 'spouse', '1973-09-10'),
(42, 'Federico', 'Messina', 'child', '2000-06-22'),
(42, 'Valentina', 'Messina', 'child', '2003-11-30'),
(45, 'Gianna', 'Vitale', 'spouse', '1978-03-25');

-- =====================================================
-- BENEFITS (Benefici Aziendali)
-- =====================================================
INSERT INTO benefits (employee_id, benefit_type, coverage_amount, cost, enrollment_date) VALUES
-- Dipendenti con benefit completi (assunti da più tempo)
(1, 'health_insurance', 50000.00, 3000.00, '2015-01-10'),
(1, 'dental', 2000.00, 500.00, '2015-01-10'),
(1, 'vision', 500.00, 200.00, '2015-01-10'),
(1, 'life_insurance', 200000.00, 1500.00, '2015-01-10'),
(1, 'retirement_401k', NULL, 24000.00, '2015-01-10'),
(1, 'gym', NULL, 600.00, '2015-01-10'),

(4, 'health_insurance', 50000.00, 3000.00, '2014-02-01'),
(4, 'dental', 2000.00, 500.00, '2014-02-01'),
(4, 'life_insurance', 150000.00, 1200.00, '2014-02-01'),
(4, 'retirement_401k', NULL, 18000.00, '2014-02-01'),
(4, 'transport', NULL, 800.00, '2014-02-01'),

(8, 'health_insurance', 50000.00, 3000.00, '2013-06-01'),
(8, 'dental', 2000.00, 500.00, '2013-06-01'),
(8, 'life_insurance', 200000.00, 1500.00, '2013-06-01'),
(8, 'retirement_401k', NULL, 20000.00, '2013-06-01'),
(8, 'gym', NULL, 600.00, '2013-06-01'),

(16, 'health_insurance', 50000.00, 3000.00, '2014-07-01'),
(16, 'dental', 2000.00, 500.00, '2014-07-01'),
(16, 'vision', 500.00, 200.00, '2014-07-01'),
(16, 'life_insurance', 150000.00, 1200.00, '2014-07-01'),
(16, 'retirement_401k', NULL, 16000.00, '2014-07-01'),

(20, 'health_insurance', 50000.00, 3000.00, '2013-03-15'),
(20, 'dental', 2000.00, 500.00, '2013-03-15'),
(20, 'life_insurance', 180000.00, 1400.00, '2013-03-15'),
(20, 'retirement_401k', NULL, 22000.00, '2013-03-15'),
(20, 'transport', NULL, 1000.00, '2013-03-15'),
(20, 'gym', NULL, 600.00, '2013-03-15'),

(27, 'health_insurance', 50000.00, 3000.00, '2012-09-01'),
(27, 'dental', 2000.00, 500.00, '2012-09-01'),
(27, 'life_insurance', 150000.00, 1200.00, '2012-09-01'),
(27, 'retirement_401k', NULL, 15000.00, '2012-09-01'),

(33, 'health_insurance', 50000.00, 3000.00, '2011-11-15'),
(33, 'dental', 2000.00, 500.00, '2011-11-15'),
(33, 'vision', 500.00, 200.00, '2011-11-15'),
(33, 'life_insurance', 200000.00, 1500.00, '2011-11-15'),
(33, 'retirement_401k', NULL, 18000.00, '2011-11-15'),

-- Dipendenti con benefit parziali
(2, 'health_insurance', 50000.00, 3000.00, '2016-03-20'),
(2, 'transport', NULL, 800.00, '2016-03-20'),

(3, 'health_insurance', 50000.00, 3000.00, '2017-06-15'),

(5, 'health_insurance', 50000.00, 3000.00, '2018-04-10'),
(5, 'dental', 2000.00, 500.00, '2018-04-10'),
(5, 'gym', NULL, 600.00, '2018-04-10'),

(9, 'health_insurance', 50000.00, 3000.00, '2015-09-15'),
(9, 'retirement_401k', NULL, 14000.00, '2015-09-15'),

(10, 'health_insurance', 50000.00, 3000.00, '2016-11-20'),
(10, 'dental', 2000.00, 500.00, '2016-11-20'),
(10, 'retirement_401k', NULL, 13000.00, '2016-11-20'),

(11, 'health_insurance', 50000.00, 3000.00, '2017-08-12'),
(11, 'life_insurance', 100000.00, 800.00, '2017-08-12'),
(11, 'retirement_401k', NULL, 12000.00, '2017-08-12'),

(12, 'health_insurance', 50000.00, 3000.00, '2018-02-28'),

(13, 'health_insurance', 50000.00, 3000.00, '2017-05-10'),
(13, 'transport', NULL, 800.00, '2017-05-10'),

(17, 'health_insurance', 50000.00, 3000.00, '2017-02-15'),
(17, 'dental', 2000.00, 500.00, '2017-02-15'),

(21, 'health_insurance', 50000.00, 3000.00, '2015-10-20'),

(24, 'health_insurance', 50000.00, 3000.00, '2016-04-18'),
(24, 'retirement_401k', NULL, 10000.00, '2016-04-18'),

(37, 'health_insurance', 50000.00, 3000.00, '2014-05-01'),

(42, 'health_insurance', 50000.00, 3000.00, '2010-08-01'),
(42, 'dental', 2000.00, 500.00, '2010-08-01'),
(42, 'life_insurance', 250000.00, 2000.00, '2010-08-01'),
(42, 'retirement_401k', NULL, 24000.00, '2010-08-01'),
(42, 'transport', NULL, 1000.00, '2010-08-01'),
(42, 'gym', NULL, 600.00, '2010-08-01');

-- =====================================================
-- PERFORMANCE_REVIEWS (Valutazioni Performance)
-- =====================================================
INSERT INTO performance_reviews (employee_id, reviewer_id, review_date, rating, comments, goals_met) VALUES
-- Valutazioni 2024
(2, 1, '2024-01-15', 4, 'Ottimo lavoro nel supporto amministrativo', 'yes'),
(3, 1, '2024-02-10', 3, 'Buone capacità, margine di miglioramento', 'yes'),
(5, 4, '2024-03-05', 5, 'Eccellente gestione recruitment', 'yes'),
(6, 4, '2024-03-15', 4, 'Buone competenze HR', 'yes'),
(7, 4, '2024-04-01', 3, 'In formazione, buoni progressi', 'partial'),
(9, 8, '2024-02-20', 5, 'Leader tecnico eccellente', 'yes'),
(10, 8, '2024-03-10', 4, 'Buone capacità di sviluppo', 'yes'),
(11, 8, '2024-03-25', 4, 'Ottima gestione progetti', 'yes'),
(12, 8, '2024-04-10', 4, 'Sviluppo solido, consegna puntuale', 'yes'),
(13, 8, '2024-04-20', 5, 'Project manager eccellente', 'yes'),
(14, 8, '2024-05-05', 3, 'Competente ma necessita mentoring', 'partial'),
(15, 8, '2024-05-15', 4, 'Buone capacità analitiche', 'yes'),
(17, 16, '2024-03-01', 4, 'Campagne marketing efficaci', 'yes'),
(18, 16, '2024-03-15', 3, 'Buone ma necessita più creatività', 'yes'),
(19, 16, '2024-04-01', 4, 'Ottimo potenziale', 'yes'),
(21, 20, '2024-02-25', 5, 'Performance vendite eccellente', 'yes'),
(22, 20, '2024-03-20', 4, 'Buone risultati commerciali', 'yes'),
(23, 20, '2024-04-15', 3, 'Sotto obiettivi ma in miglioramento', 'partial'),
(24, 20, '2024-05-01', 5, 'Account manager eccellente', 'yes'),
(25, 20, '2024-05-20', 4, 'Buone relazioni clienti', 'yes'),
(28, 27, '2024-03-10', 4, 'Controllo qualità solido', 'yes'),
(29, 27, '2024-04-05', 3, 'Competente, margine di crescita', 'yes'),
(34, 33, '2024-02-15', 5, 'Ricerca innovativa di alto livello', 'yes'),
(35, 33, '2024-03-25', 4, 'Buon contributo scientifico', 'yes'),
(43, 42, '2024-03-05', 4, 'Analisi finanziaria accurata', 'yes'),
(44, 42, '2024-04-10', 4, 'Buone capacità contabili', 'yes'),

-- Valutazioni 2023 (storico)
(2, 1, '2023-01-20', 4, 'Lavoro affidabile', 'yes'),
(3, 1, '2023-02-15', 3, 'Buona integrazione', 'yes'),
(5, 4, '2023-03-10', 4, 'Reclutamento efficace', 'yes'),
(9, 8, '2023-02-25', 5, 'Leader tecnico', 'yes'),
(10, 8, '2023-03-15', 4, 'Buono sviluppo', 'yes'),
(11, 8, '2023-04-01', 4, 'Progetti ben gestiti', 'yes'),
(17, 16, '2023-03-05', 3, 'Buone campagne', 'yes'),
(21, 20, '2023-02-28', 5, 'Top performer vendite', 'yes'),
(24, 20, '2023-04-10', 4, 'Account manager solido', 'yes'),
(34, 33, '2023-02-20', 4, 'Ricerca di valore', 'yes'),
(43, 42, '2023-03-15', 4, 'Buone analisi', 'yes');

-- =====================================================
-- ATTENDANCE (Registro Presenze)
-- =====================================================
-- Genera presenze per l'anno 2024 (gennaio - dicembre)
-- Ogni dipendente ha record per ogni giorno lavorativo

INSERT INTO attendance (employee_id, attendance_date, check_in, check_out, hours_worked, status) VALUES
-- Gennaio 2024 - Primi giorni per dipartimento IT
(8, '2024-01-02', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-01-02', '09:15:00', '18:30:00', 8.25, 'present'),
(10, '2024-01-02', '08:45:00', '17:45:00', 8.00, 'present'),
(11, '2024-01-02', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-01-02', '09:30:00', '18:30:00', 8.00, 'late'),
(8, '2024-01-03', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-01-03', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-01-03', '08:50:00', '17:50:00', 8.00, 'present'),
(11, '2024-01-03', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-01-03', '09:00:00', '18:00:00', 8.00, 'present'),
(8, '2024-01-04', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-01-04', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-01-04', '09:00:00', '18:00:00', 8.00, 'present'),
(11, '2024-01-04', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-01-04', NULL, NULL, NULL, 'sick'),
(8, '2024-01-05', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-01-05', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-01-05', '09:00:00', '18:00:00', 8.00, 'present'),
(11, '2024-01-05', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-01-05', '09:00:00', '14:00:00', 5.00, 'half_day'),

-- Febbraio 2024 - Varie situazioni
(8, '2024-02-01', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-02-01', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-02-01', '09:00:00', '18:00:00', 8.00, 'present'),
(11, '2024-02-01', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-02-01', '09:00:00', '18:00:00', 8.00, 'present'),
(8, '2024-02-02', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-02-02', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-02-02', NULL, NULL, NULL, 'vacation'),
(11, '2024-02-02', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-02-02', '09:00:00', '18:00:00', 8.00, 'present'),
(8, '2024-02-05', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-02-05', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-02-05', NULL, NULL, NULL, 'vacation'),
(11, '2024-02-05', '09:00:00', '18:00:00', 8.00, 'present'),
(12, '2024-02-05', '09:00:00', '18:00:00', 8.00, 'present'),

-- Marzo 2024 - Altri dipendenti
(17, '2024-03-01', '09:00:00', '18:00:00', 8.00, 'present'),
(18, '2024-03-01', '09:00:00', '18:00:00', 8.00, 'present'),
(19, '2024-03-01', '09:00:00', '18:00:00', 8.00, 'present'),
(21, '2024-03-01', '09:00:00', '19:00:00', 9.00, 'present'),
(22, '2024-03-01', '09:00:00', '18:00:00', 8.00, 'present'),
(17, '2024-03-04', '09:00:00', '18:00:00', 8.00, 'present'),
(18, '2024-03-04', '09:15:00', '18:00:00', 7.75, 'late'),
(19, '2024-03-04', '09:00:00', '18:00:00', 8.00, 'present'),
(21, '2024-03-04', '09:00:00', '19:00:00', 9.00, 'present'),
(22, '2024-03-04', '09:00:00', '18:00:00', 8.00, 'present'),

-- April-May 2024 - Dipartimento HR
(5, '2024-04-01', '09:00:00', '18:00:00', 8.00, 'present'),
(6, '2024-04-01', '09:00:00', '18:00:00', 8.00, 'present'),
(7, '2024-04-01', '09:00:00', '18:00:00', 8.00, 'present'),
(5, '2024-04-02', '09:00:00', '18:00:00', 8.00, 'present'),
(6, '2024-04-02', '09:00:00', '18:00:00', 8.00, 'present'),
(7, '2024-04-02', '09:00:00', '15:00:00', 6.00, 'present'),
(5, '2024-05-01', '09:00:00', '18:00:00', 8.00, 'present'),
(6, '2024-05-01', '09:00:00', '18:00:00', 8.00, 'present'),
(7, '2024-05-01', NULL, NULL, NULL, 'sick'),

-- Giugno 2024 - Presenze miste
(8, '2024-06-03', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-06-03', '09:00:00', '18:00:00', 8.00, 'present'),
(10, '2024-06-03', '09:00:00', '18:00:00', 8.00, 'present'),
(11, '2024-06-03', '09:00:00', '18:00:00', 8.00, 'present'),
(8, '2024-06-04', '09:00:00', '18:00:00', 8.00, 'present'),
(9, '2024-06-04', NULL, NULL, NULL, 'absent'),
(10, '2024-06-04', '09:00:00', '18:00:00', 8.00, 'present'),
(11, '2024-06-04', '09:00:00', '18:00:00', 8.00, 'present'),

-- Luglio-Agosto 2024
(17, '2024-07-01', '09:00:00', '18:00:00', 8.00, 'present'),
(18, '2024-07-01', '09:00:00', '18:00:00', 8.00, 'present'),
(19, '2024-07-01', '09:00:00', '18:00:00', 8.00, 'present'),
(21, '2024-07-01', '09:00:00', '19:00:00', 9.00, 'present'),
(22, '2024-07-01', '09:00:00', '18:00:00', 8.00, 'present'),
(17, '2024-08-01', '09:00:00', '18:00:00', 8.00, 'present'),
(18, '2024-08-01', '09:00:00', '18:00:00', 8.00, 'present'),
(19, '2024-08-01', NULL, NULL, NULL, 'vacation'),
(21, '2024-08-01', '09:00:00', '19:00:00', 9.00, 'present'),
(22, '2024-08-01', '09:00:00', '18:00:00', 8.00, 'present'),

-- Settembre-Ottobre 2024
(28, '2024-09-02', '08:00:00', '17:00:00', 8.00, 'present'),
(29, '2024-09-02', '08:00:00', '17:00:00', 8.00, 'present'),
(30, '2024-09-02', '08:00:00', '17:00:00', 8.00, 'present'),
(28, '2024-09-03', '08:00:00', '17:00:00', 8.00, 'present'),
(29, '2024-09-03', '08:15:00', '17:00:00', 7.75, 'late'),
(30, '2024-09-03', '08:00:00', '17:00:00', 8.00, 'present'),
(28, '2024-10-01', '08:00:00', '17:00:00', 8.00, 'present'),
(29, '2024-10-01', '08:00:00', '17:00:00', 8.00, 'present'),
(30, '2024-10-01', NULL, NULL, NULL, 'sick'),

-- Novembre-Dicembre 2024
(43, '2024-11-04', '09:00:00', '18:00:00', 8.00, 'present'),
(44, '2024-11-04', '09:00:00', '18:00:00', 8.00, 'present'),
(43, '2024-11-05', '09:00:00', '18:00:00', 8.00, 'present'),
(44, '2024-11-05', '09:00:00', '18:00:00', 8.00, 'present'),
(43, '2024-12-01', '09:00:00', '18:00:00', 8.00, 'present'),
(44, '2024-12-01', '09:00:00', '18:00:00', 8.00, 'present');

-- Aggiungi altri record di attendance per avere un dataset più ricco
INSERT INTO attendance (employee_id, attendance_date, check_in, check_out, hours_worked, status) SELECT
    id,
    '2024-06-10'::date + (random() * 100)::integer::date,
    '09:00:00'::time + (random() * 3600)::integer * INTERVAL '1 second',
    '18:00:00'::time + (random() * 3600)::integer * INTERVAL '1 second',
    (7 + random() * 2)::decimal(4,2),
    CASE
        WHEN random() < 0.05 THEN 'absent'
        WHEN random() < 0.08 THEN 'late'
        WHEN random() < 0.10 THEN 'sick'
        WHEN random() < 0.12 THEN 'vacation'
        ELSE 'present'
    END
FROM employees
WHERE id <= 30
ORDER BY id
LIMIT 200;

-- =====================================================
-- SALARY_AUDIT_LOG (Log Audit - generato automaticamente)
-- =====================================================
-- I record vengono inseriti automaticamente dai triggers
-- Esempio di records manuali per completezza

-- =====================================================
-- VERIFICA FINAL DATA
-- =====================================================

-- Verifica numero dipendenti
SELECT 'Dipendenti totali: ' || COUNT(*) FROM employees;

-- Verifica numero per dipartimento
SELECT d.name AS department, COUNT(e.id) AS employees
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.name
ORDER BY employees DESC;

-- Verifica stipendi
SELECT 'Stipendi caricati: ' || COUNT(*) FROM salaries;
SELECT 'Stipendi attivi: ' || COUNT(*) FROM salaries WHERE end_date IS NULL;

-- Verifica altre tabelle
SELECT 'Familiari a carico: ' || COUNT(*) FROM dependents;
SELECT 'Benefici assegnati: ' || COUNT(*) FROM benefits;
SELECT 'Valutazioni: ' || COUNT(*) FROM performance_reviews;
SELECT 'Record presenze: ' || COUNT(*) FROM attendance;

-- =====================================================
-- FINE SAMPLE DATA
-- =====================================================
