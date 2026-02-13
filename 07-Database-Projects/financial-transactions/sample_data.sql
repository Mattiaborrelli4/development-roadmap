-- ============================================================================
-- DATI CAMPIONE - SISTEMA DI TRANSAZIONI FINANZIARIE
-- ============================================================================

-- ============================================================================
-- TIPI DI TRANSAZIONE
-- ============================================================================
INSERT INTO transaction_types (name, code, description, fee_percentage, requires_approval) VALUES
('Bonifico', 'BON', 'Bonifico bancario standard', 0.00, FALSE),
('Bonifico Urgente', 'BURG', 'Bonifico con processazione urgente', 1.50, FALSE),
('Deposito', 'DEP', 'Deposito denaro sul conto', 0.00, FALSE),
('Prelievo', 'PRE', 'Prelievo denaro dal conto', 0.00, FALSE),
('Pagamento Bolletta', 'BOLL', 'Pagamento utenze e bollette', 0.50, FALSE),
('Pagamento Carta', 'CARTA', 'Pagamento carta di credito', 0.00, FALSE),
('Bonifico Estero', 'BEXT', 'Bonifico internazionale', 2.50, TRUE),
('Assegno', 'ASS', 'Emissione assegno', 1.00, FALSE),
('Stipendio', 'STIP', 'Accredito stipendiale', 0.00, FALSE),
('Bonifico Importante', 'BIMP', 'Bonifico di importo elevato', 0.00, TRUE),
('Investimento', 'INV', 'Investimento in fondi', 0.00, TRUE),
('Rimborso', 'RIMB', 'Rimborso spese', 0.00, FALSE);

-- ============================================================================
-- CLIENTI (50+ clienti)
-- ============================================================================
INSERT INTO customers (first_name, last_name, tax_id, email, phone, birth_date) VALUES
('Mario', 'Rossi', 'RSSMRA80A01H501U', 'mario.rossi@email.it', '+39 333 1111111', '1980-01-01'),
('Giulia', 'Bianchi', 'BNCGLL82B12H501U', 'giulia.bianchi@email.it', '+39 333 2222222', '1982-02-12'),
('Luca', 'Ferrari', 'FRRLCU85C15H501U', 'luca.ferrari@email.it', '+39 333 3333333', '1985-03-15'),
('Anna', 'Romano', 'RMNNNA90D20H501U', 'anna.romano@email.it', '+39 333 4444444', '1990-04-20'),
('Paolo', 'Colombo', 'CLMPPL88E25H501U', 'paolo.colombo@email.it', '+39 333 5555555', '1988-05-25'),
('Laura', 'Greco', 'GRCLRA92F30H501U', 'laura.greco@email.it', '+39 333 6666666', '1992-06-30'),
('Marco', 'Sartori', 'SRTRCO78G05H501U', 'marco.sartori@email.it', '+39 333 7777777', '1978-07-05'),
('Francesca', 'Rinaldi', 'RNLFRC85H10H501U', 'francesca.rinaldi@email.it', '+39 333 8888888', '1985-08-10'),
('Alessandro', 'Moretti', 'MRTLSN83I15H501U', 'alessandro.moretti@email.it', '+39 333 9999999', '1983-09-15'),
('Chiara', 'Marino', 'MRNCHR91J20H501U', 'chiara.marino@email.it', '+39 333 1010101', '1991-10-20'),
('Roberto', 'Conti', 'CNTRTT79K25H501U', 'roberto.conti@email.it', '+39 333 1111112', '1979-11-25'),
('Sofia', 'Barbieri', 'BRBSFR94L30H501U', 'sofia.barbieri@email.it', '+39 333 2222223', '1994-12-30'),
('Andrea', 'Galli', 'GLLNDR87M05H501U', 'andrea.galli@email.it', '+39 333 3333334', '1987-01-05'),
('Martina', 'Federici', 'FDCMRT89N10H501U', 'martina.federici@email.it', '+39 333 4444445', '1989-02-10'),
('Davide', 'Bernardi', 'BRNDVD86O15H501U', 'davide.bernardi@email.it', '+39 333 5555556', '1986-03-15'),
('Valentina', 'Martinelli', 'MRTVLN93P20H501U', 'valentina.martinelli@email.it', '+39 333 6666667', '1993-04-20'),
('Matteo', 'Benetti', 'BNTMTT84Q25H501U', 'matteo.benetti@email.it', '+39 333 7777778', '1984-05-25'),
('Elisa', 'Grassi', 'GRSELS96R30H501U', 'elisa.grassi@email.it', '+39 333 8888889', '1996-06-30'),
('Simone', 'Costantini', 'CSTSMN81S05H501U', 'simone.costantini@email.it', '+39 333 9999990', '1981-07-05'),
('Sara', 'D''Amico', 'DMCSRC88T10H501U', 'sara.damico@email.it', '+39 333 1010102', '1988-08-10'),
('Federico', 'Rizzo', 'RZZFDR90U15H501U', 'federico.rizzo@email.it', '+39 333 1111113', '1990-09-15'),
('Alessia', 'Lombardi', 'LMBLSC95V20H501U', 'alessia.lombardi@email.it', '+39 333 2222224', '1995-10-20'),
('Nicola', 'Santini', 'SNTNCL83W25H501U', 'nicola.santini@email.it', '+39 333 3333335', '1983-11-25'),
('Monica', 'Mancini', 'MNCMNC92X30H501U', 'monica.mancini@email.it', '+39 333 4444446', '1992-12-30'),
('Lorenzo', 'Vitale', 'VTLRNZ80Y05H501U', 'lorenzo.vitale@email.it', '+39 333 5555557', '1980-01-05'),
('Veronica', 'Contiero', 'CNTVRN89Z10H501U', 'veronica.contiero@email.it', '+39 333 6666668', '1989-02-10'),
('Emanuele', 'Esposito', 'ESPMNU85A15H501U', 'emanuele.esposito@email.it', '+39 333 7777779', '1985-03-15'),
('Claudia', 'Fabbri', 'FBBCLD91B20H501U', 'claudia.fabbri@email.it', '+39 333 8888880', '1991-04-20'),
('Riccardo', 'Cattaneo', 'CTTRCD87C25H501U', 'riccardo.cattaneo@email.it', '+39 333 9999991', '1987-05-25'),
('Jessica', 'De Luca', 'DLCSJC94D30H501U', 'jessica.deluca@email.it', '+39 333 1010103', '1994-06-30'),
('Francesco', 'Padovano', 'PDVFRN82E05H501U', 'francesco.padovano@email.it', '+39 333 1111114', '1982-07-05'),
('Elena', 'Fontana', 'FNTLNC93F10H501U', 'elena.fontana@email.it', '+39 333 2222225', '1993-08-10'),
('Stefano', 'Serra', 'SRRSTF88G15H501U', 'stefano.serra@email.it', '+39 333 3333336', '1988-09-15'),
('Giorgia', 'Basile', 'BSLGRG96H20H501U', 'giorgia.basile@email.it', '+39 333 4444447', '1996-10-20'),
('Mirko', 'Ferri', 'FRRMRK86I25H501U', 'mirko.ferri@email.it', '+39 333 5555558', '1986-11-25'),
('Cristina', 'Damico', 'DMCCRST90J30H501U', 'cristina.damico@email.it', '+39 333 6666669', '1990-12-30'),
('Daniele', 'Parisi', 'PRSDNL84K05H501U', 'daniele.parisi@email.it', '+39 333 7777770', '1984-01-05'),
('Barbara', 'Ruggiero', 'RGGBRB97L10H501U', 'barbara.ruggiero@email.it', '+39 333 8888881', '1997-02-10'),
('Antonio', 'Peluso', 'PLSNTN81M15H501U', 'antonio.peluso@email.it', '+39 333 9999992', '1981-03-15'),
('Roberta', 'D''Angelo', 'DNGLRB92N20H501U', 'roberta.dangelo@email.it', '+39 333 1010104', '1992-04-20'),
('Paolo', 'Marchetti', 'MRCPPL83O25H501U', 'paolo.marchetti@email.it', '+39 333 1111115', '1983-05-25'),
('Tatiana', 'Moretti', 'MRTTTN95P30H501U', 'tatiana.moretti@email.it', '+39 333 2222226', '1995-06-30'),
('Enrico', 'Fiorini', 'FRRNRC89Q05H501U', 'enrico.fiorini@email.it', '+39 333 3333337', '1989-07-05'),
('Patrizia', 'Rinaldo', 'RNLPTR91R10H501U', 'patrizia.rinaldo@email.it', '+39 333 4444448', '1991-08-10'),
('Giuseppe', 'Montanari', 'MNTGSP80S15H501U', 'giuseppe.montanari@email.it', '+39 333 5555559', '1980-09-15'),
('Emanuela', 'Viviani', 'VVVMNL94T20H501U', 'emanuela.viviani@email.it', '+39 333 6666670', '1994-10-20'),
('Fabrizio', 'Sole', 'SLFRBZ87U25H501U', 'fabrizio.sole@email.it', '+39 333 7777771', '1987-11-25'),
('Renata', 'Amato', 'AMTRNT93V30H501U', 'renata.amato@email.it', '+39 333 8888882', '1993-12-30'),
('Alberto', 'Cocco', 'CCCLRT85W05H501U', 'alberto.cocco@email.it', '+39 333 9999993', '1985-01-05'),
('Marta', 'Cavallo', 'CVLMRT98X10H501U', 'marta.cavallo@email.it', '+39 333 1010105', '1998-02-10'),
('Fernando', 'Rizzo', 'RZZFRN90Y15H501U', 'fernando.rizzo@email.it', '+39 333 1111116', '1990-03-15'),
('Cinzia', 'De Angelis', 'DNGCNZ88Z20H501U', 'cinzia.deangelis@email.it', '+39 333 2222227', '1988-04-20');

-- ============================================================================
-- CONTI (100+ conti)
-- ============================================================================
INSERT INTO accounts (account_number, customer_id, account_type, balance, currency, status, credit_limit) VALUES
-- Conti per Mario Rossi
('IT00100000000000001', 1, 'checking', 5420.50, 'EUR', 'active', 0),
('IT00100000000000002', 1, 'savings', 25000.00, 'EUR', 'active', 0),
-- Conti per Giulia Bianchi
('IT00100000000000003', 2, 'checking', 3210.75, 'EUR', 'active', 0),
('IT00100000000000004', 2, 'savings', 18500.00, 'EUR', 'active', 0),
('IT00100000000000005', 2, 'credit', -1250.00, 'EUR', 'active', 3000.00),
-- Conti per Luca Ferrari
('IT00100000000000006', 3, 'checking', 8750.25, 'EUR', 'active', 0),
('IT00100000000000007', 3, 'savings', 42000.00, 'EUR', 'active', 0),
-- Conti per Anna Romano
('IT00100000000000008', 4, 'checking', 2150.00, 'EUR', 'active', 0),
('IT00100000000000009', 4, 'credit', -850.00, 'EUR', 'active', 2000.00),
-- Conti per Paolo Colombo
('IT00100000000000010', 5, 'checking', 6780.90, 'EUR', 'active', 0),
('IT00100000000000011', 5, 'savings', 32000.50, 'EUR', 'active', 0),
('IT00100000000000012', 5, 'credit', -450.00, 'EUR', 'active', 1500.00),
-- Conti per Laura Greco
('IT00100000000000013', 6, 'checking', 4320.40, 'EUR', 'active', 0),
('IT00100000000000014', 6, 'savings', 28000.00, 'EUR', 'active', 0),
-- Conti per Marco Sartori
('IT00100000000000015', 7, 'checking', 12560.70, 'EUR', 'active', 0),
('IT00100000000000016', 7, 'credit', -2100.00, 'EUR', 'active', 5000.00),
-- Conti per Francesca Rinaldi
('IT00100000000000017', 8, 'checking', 3450.25, 'EUR', 'active', 0),
('IT00100000000000018', 8, 'savings', 15500.00, 'EUR', 'active', 0),
-- Conti per Alessandro Moretti
('IT00100000000000019', 9, 'checking', 9870.60, 'EUR', 'active', 0),
('IT00100000000000020', 9, 'savings', 38500.00, 'EUR', 'active', 0),
('IT00100000000000021', 9, 'credit', -1800.00, 'EUR', 'active', 4000.00),
-- Conti per Chiara Marino
('IT00100000000000022', 10, 'checking', 5430.80, 'EUR', 'active', 0),
('IT00100000000000023', 10, 'savings', 22500.00, 'EUR', 'active', 0),
-- Conti per Roberto Conti
('IT00100000000000024', 11, 'checking', 7650.45, 'EUR', 'active', 0),
('IT00100000000000025', 11, 'credit', -950.00, 'EUR', 'active', 2500.00),
-- Conti per Sofia Barbieri
('IT00100000000000026', 12, 'checking', 2980.30, 'EUR', 'active', 0),
('IT00100000000000027', 12, 'savings', 12500.00, 'EUR', 'active', 0),
-- Conti per Andrea Galli
('IT00100000000000028', 13, 'checking', 11250.90, 'EUR', 'active', 0),
('IT00100000000000029', 13, 'savings', 45000.00, 'EUR', 'active', 0),
-- Conti per Martina Federici
('IT00100000000000030', 14, 'checking', 4560.70, 'EUR', 'active', 0),
('IT00100000000000031', 14, 'credit', -680.00, 'EUR', 'active', 2000.00),
-- Conti per Davide Bernardi
('IT00100000000000032', 15, 'checking', 8920.40, 'EUR', 'active', 0),
('IT00100000000000033', 15, 'savings', 35000.00, 'EUR', 'active', 0),
-- Conti per Valentina Martinelli
('IT00100000000000034', 16, 'checking', 6540.20, 'EUR', 'active', 0),
('IT00100000000000035', 16, 'savings', 28000.00, 'EUR', 'active', 0),
-- Conti per Matteo Benetti
('IT00100000000000036', 17, 'checking', 14230.80, 'EUR', 'active', 0),
('IT00100000000000037', 17, 'credit', -2750.00, 'EUR', 'active', 5000.00),
-- Conti per Elisa Grassi
('IT00100000000000038', 18, 'checking', 3870.50, 'EUR', 'active', 0),
('IT00100000000000039', 18, 'savings', 19000.00, 'EUR', 'active', 0),
-- Conti per Simone Costantini
('IT00100000000000040', 19, 'checking', 10650.60, 'EUR', 'active', 0),
('IT00100000000000041', 19, 'savings', 42000.00, 'EUR', 'active', 0),
('IT00100000000000042', 19, 'credit', -1200.00, 'EUR', 'active', 3000.00),
-- Conti per Sara D''Amico
('IT00100000000000043', 20, 'checking', 5230.40, 'EUR', 'active', 0),
('IT00100000000000044', 20, 'savings', 23500.00, 'EUR', 'active', 0),
-- Conti per Federico Rizzo
('IT00100000000000045', 21, 'checking', 7890.70, 'EUR', 'active', 0),
('IT00100000000000046', 21, 'credit', -560.00, 'EUR', 'active', 1500.00),
-- Conti per Alessia Lombardi
('IT00100000000000047', 22, 'checking', 4320.30, 'EUR', 'active', 0),
('IT00100000000000048', 22, 'savings', 21000.00, 'EUR', 'active', 0),
-- Conti per Nicola Santini
('IT00100000000000049', 23, 'checking', 9760.90, 'EUR', 'active', 0),
('IT00100000000000050', 23, 'savings', 38000.00, 'EUR', 'active', 0),
-- Conti per Monica Mancini
('IT00100000000000051', 24, 'checking', 3650.20, 'EUR', 'active', 0),
('IT00100000000000052', 24, 'credit', -820.00, 'EUR', 'active', 2000.00),
-- Conti per Lorenzo Vitale
('IT00100000000000053', 25, 'checking', 15430.50, 'EUR', 'active', 0),
('IT00100000000000054', 25, 'savings', 52000.00, 'EUR', 'active', 0),
-- Conti per Veronica Contiero
('IT00100000000000055', 26, 'checking', 6890.60, 'EUR', 'active', 0),
('IT00100000000000056', 26, 'savings', 29500.00, 'EUR', 'active', 0),
-- Conti per Emanuele Esposito
('IT00100000000000057', 27, 'checking', 8340.40, 'EUR', 'active', 0),
('IT00100000000000058', 27, 'credit', -1450.00, 'EUR', 'active', 3500.00),
-- Conti per Claudia Fabbri
('IT00100000000000059', 28, 'checking', 4780.30, 'EUR', 'active', 0),
('IT00100000000000060', 28, 'savings', 20500.00, 'EUR', 'active', 0),
-- Conti per Riccardo Cattaneo
('IT00100000000000061', 29, 'checking', 11230.80, 'EUR', 'active', 0),
('IT00100000000000062', 29, 'savings', 41000.00, 'EUR', 'active', 0),
('IT00100000000000063', 29, 'credit', -2200.00, 'EUR', 'active', 4500.00),
-- Conti per Jessica De Luca
('IT00100000000000064', 30, 'checking', 5650.50, 'EUR', 'active', 0),
('IT00100000000000065', 30, 'savings', 24500.00, 'EUR', 'active', 0),
-- Conti per Francesco Padovano
('IT00100000000000066', 31, 'checking', 9980.70, 'EUR', 'active', 0),
('IT00100000000000067', 31, 'credit', -780.00, 'EUR', 'active', 2500.00),
-- Conti per Elena Fontana
('IT00100000000000068', 32, 'checking', 4120.20, 'EUR', 'active', 0),
('IT00100000000000069', 32, 'savings', 18500.00, 'EUR', 'active', 0),
-- Conti per Stefano Serra
('IT00100000000000070', 33, 'checking', 8760.90, 'EUR', 'active', 0),
('IT00100000000000071', 33, 'savings', 35500.00, 'EUR', 'active', 0),
-- Conti per Giorgia Basile
('IT00100000000000072', 34, 'checking', 3340.40, 'EUR', 'active', 0),
('IT00100000000000073', 34, 'credit', -520.00, 'EUR', 'active', 1500.00),
-- Conti per Mirko Ferri
('IT00100000000000074', 35, 'checking', 12890.60, 'EUR', 'active', 0),
('IT00100000000000075', 35, 'savings', 48000.00, 'EUR', 'active', 0),
-- Conti per Cristina Damico
('IT00100000000000076', 36, 'checking', 5670.30, 'EUR', 'active', 0),
('IT00100000000000077', 36, 'savings', 26500.00, 'EUR', 'active', 0),
-- Conti per Daniele Parisi
('IT00100000000000078', 37, 'checking', 9450.80, 'EUR', 'active', 0),
('IT00100000000000079', 37, 'credit', -1650.00, 'EUR', 'active', 4000.00),
-- Conti per Barbara Ruggiero
('IT00100000000000080', 38, 'checking', 3890.50, 'EUR', 'active', 0),
('IT00100000000000081', 38, 'savings', 17000.00, 'EUR', 'active', 0),
-- Conti per Antonio Peluso
('IT00100000000000082', 39, 'checking', 7230.40, 'EUR', 'active', 0),
('IT00100000000000083', 39, 'savings', 33000.00, 'EUR', 'active', 0),
-- Conti per Roberta D''Angelo
('IT00100000000000084', 40, 'checking', 5980.20, 'EUR', 'active', 0),
('IT00100000000000085', 40, 'credit', -920.00, 'EUR', 'active', 2000.00),
-- Conti per Paolo Marchetti
('IT00100000000000086', 41, 'checking', 10670.90, 'EUR', 'active', 0),
('IT00100000000000087', 41, 'savings', 39500.00, 'EUR', 'active', 0),
-- Conti per Tatiana Moretti
('IT00100000000000088', 42, 'checking', 4450.30, 'EUR', 'active', 0),
('IT00100000000000089', 42, 'credit', -740.00, 'EUR', 'active', 1800.00),
-- Conti per Enrico Fiorini
('IT00100000000000090', 43, 'checking', 8560.70, 'EUR', 'active', 0),
('IT00100000000000091', 43, 'savings', 31500.00, 'EUR', 'active', 0),
-- Conti per Patrizia Rinaldo
('IT00100000000000092', 44, 'checking', 6780.40, 'EUR', 'active', 0),
('IT00100000000000093', 44, 'savings', 27500.00, 'EUR', 'active', 0),
-- Conti per Giuseppe Montanari
('IT00100000000000094', 45, 'checking', 14560.80, 'EUR', 'active', 0),
('IT00100000000000095', 45, 'credit', -3100.00, 'EUR', 'active', 6000.00),
-- Conti per Emanuela Viviani
('IT00100000000000096', 46, 'checking', 5120.50, 'EUR', 'active', 0),
('IT00100000000000097', 46, 'savings', 23000.00, 'EUR', 'active', 0),
-- Conti per Fabrizio Sole
('IT00100000000000098', 47, 'checking', 9870.60, 'EUR', 'active', 0),
('IT00100000000000099', 47, 'credit', -1350.00, 'EUR', 'active', 3500.00),
-- Conti per Renata Amato
('IT00100000000000100', 48, 'checking', 6340.20, 'EUR', 'active', 0),
('IT00100000000000101', 48, 'savings', 28500.00, 'EUR', 'active', 0),
-- Conti per Alberto Cocco
('IT00100000000000102', 49, 'checking', 11250.90, 'EUR', 'active', 0),
('IT00100000000000103', 49, 'credit', -2100.00, 'EUR', 'active', 4500.00),
-- Conti per Marta Cavallo
('IT00100000000000104', 50, 'checking', 3980.30, 'EUR', 'active', 0),
('IT00100000000000105', 50, 'savings', 19500.00, 'EUR', 'active', 0);

-- ============================================================================
-- TRANSAZIONI (500+ transazioni)
-- ============================================================================

-- Helper function per generare reference
-- Usiamo cicli per generare molte transazioni

DO $$
DECLARE
    v_from_acc INTEGER;
    v_to_acc INTEGER;
    v_amount DECIMAL;
    v_type INTEGER;
    v_status VARCHAR;
    v_ref VARCHAR;
    v_desc TEXT;
    v_date TIMESTAMP;
    i INTEGER;
BEGIN
    -- Genera 300 bonifici tra conti
    FOR i IN 1..300 LOOP
        v_from_acc := 1 + FLOOR(RANDOM() * 105);
        v_to_acc := 1 + FLOOR(RANDOM() * 105);

        -- Assicurarsi che siano diversi
        WHILE v_from_acc = v_to_acc LOOP
            v_to_acc := 1 + FLOOR(RANDOM() * 105);
        END LOOP;

        v_amount := (RANDOM() * 1000 + 10)::DECIMAL(15,2);
        v_type := 1; -- Bonifico
        v_status := CASE
            WHEN RANDOM() < 0.1 THEN 'failed'
            WHEN RANDOM() < 0.2 THEN 'cancelled'
            WHEN RANDOM() < 0.25 THEN 'pending'
            ELSE 'completed'
        END;
        v_ref := 'BON' || LPAD(i::TEXT, 8, '0');
        v_date := CURRENT_TIMESTAMP - (RANDOM() * 365 || ' days')::INTERVAL;
        v_desc := 'Bonifico da conto ' || v_from_acc || ' a conto ' || v_to_acc;

        INSERT INTO transactions (from_account_id, to_account_id, amount, transaction_type_id, status, created_date, processed_date, reference, description)
        VALUES (v_from_acc, v_to_acc, v_amount, v_type, v_status, v_date,
                CASE WHEN v_status = 'completed' THEN v_date + (RANDOM() * 60 || ' minutes')::INTERVAL ELSE NULL END,
                v_ref, v_desc);
    END LOOP;

    -- Genera 100 prelievi
    FOR i IN 301..400 LOOP
        v_from_acc := 1 + FLOOR(RANDOM() * 105);
        v_amount := (RANDOM() * 500 + 20)::DECIMAL(15,2);
        v_type := 4; -- Prelievo
        v_status := CASE
            WHEN RANDOM() < 0.05 THEN 'failed'
            ELSE 'completed'
        END;
        v_ref := 'PRE' || LPAD(i::TEXT, 8, '0');
        v_date := CURRENT_TIMESTAMP - (RANDOM() * 365 || ' days')::INTERVAL;

        INSERT INTO transactions (from_account_id, amount, transaction_type_id, status, created_date, processed_date, reference, description)
        VALUES (v_from_acc, v_amount, v_type, v_status, v_date,
                CASE WHEN v_status = 'completed' THEN v_date + (RANDOM() * 5 || ' minutes')::INTERVAL ELSE NULL END,
                v_ref, 'Prelievo contante');
    END LOOP;

    -- Genera 100 depositi
    FOR i IN 401..500 LOOP
        v_to_acc := 1 + FLOOR(RANDOM() * 105);
        v_amount := (RANDOM() * 2000 + 50)::DECIMAL(15,2);
        v_type := 3; -- Deposito
        v_status := 'completed';
        v_ref := 'DEP' || LPAD(i::TEXT, 8, '0');
        v_date := CURRENT_TIMESTAMP - (RANDOM() * 365 || ' days')::INTERVAL;

        INSERT INTO transactions (to_account_id, amount, transaction_type_id, status, created_date, processed_date, reference, description)
        VALUES (v_to_acc, v_amount, v_type, v_status, v_date, v_date + (RANDOM() * 5 || ' minutes')::INTERVAL,
                v_ref, 'Deposito contante');
    END LOOP;

    -- Genera 50 pagamenti bollette
    FOR i IN 501..550 LOOP
        v_from_acc := 1 + FLOOR(RANDOM() * 105);
        v_amount := (RANDOM() * 300 + 30)::DECIMAL(15,2);
        v_type := 5; -- Bolletta
        v_status := CASE
            WHEN RANDOM() < 0.08 THEN 'failed'
            ELSE 'completed'
        END;
        v_ref := 'BOL' || LPAD(i::TEXT, 8, '0');
        v_date := CURRENT_TIMESTAMP - (RANDOM() * 180 || ' days')::INTERVAL;

        INSERT INTO transactions (from_account_id, amount, transaction_type_id, status, created_date, processed_date, reference, description)
        VALUES (v_from_acc, v_amount, v_type, v_status, v_date,
                CASE WHEN v_status = 'completed' THEN v_date + (RANDOM() * 120 || ' minutes')::INTERVAL ELSE NULL END,
                v_ref, 'Pagamento bolletta ' || CASE i % 4 WHEN 0 THEN 'luce' WHEN 1 THEN 'gas' WHEN 2 THEN 'acqua' ELSE 'telefono' END);
    END LOOP;
END $$;

-- ============================================================================
-- TRANSACTION LOG (log per alcune transazioni)
-- ============================================================================
INSERT INTO transaction_log (transaction_id, status_from, status_to, changed_by, notes)
SELECT
    id,
    'pending',
    status,
    'system',
    'Transazione processata automaticamente'
FROM transactions
WHERE id <= 50 AND status IN ('completed', 'failed')
UNION ALL
SELECT
    id,
    'completed',
    'cancelled',
    'admin',
    'Transazione annullata su richiesta cliente'
FROM transactions
WHERE id BETWEEN 51 AND 60 AND status = 'cancelled';

-- ============================================================================
-- ESTRATTI CONTO (statements)
-- ============================================================================
INSERT INTO account_statements (account_id, statement_date, period_start, period_end, opening_balance, closing_balance, total_debits, total_credits, transaction_count)
SELECT
    a.id,
    DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '1 month')::DATE,
    DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '1 month')::DATE,
    (DATE_TRUNC('month', CURRENT_TIMESTAMP) - INTERVAL '1 day')::DATE,
    COALESCE(a.balance - COALESCE(SUM(CASE WHEN t.to_account_id = a.id THEN t.amount ELSE -t.amount END), 0), a.balance),
    a.balance,
    COALESCE(SUM(CASE WHEN t.from_account_id = a.id THEN t.amount ELSE 0 END), 0),
    COALESCE(SUM(CASE WHEN t.to_account_id = a.id THEN t.amount ELSE 0 END), 0),
    COALESCE(COUNT(t.id), 0)
FROM accounts a
LEFT JOIN transactions t ON (t.from_account_id = a.id OR t.to_account_id = a.id)
    AND t.created_date >= DATE_TRUNC('month', CURRENT_TIMESTAMP - INTERVAL '1 month')
    AND t.created_date < DATE_TRUNC('month', CURRENT_TIMESTAMP)
    AND t.status = 'completed'
WHERE a.id <= 20
GROUP BY a.id, a.balance;

-- ============================================================================
-- INFO
-- ============================================================================
SELECT 'DATI CAMPIONE INSERITI CON SUCCESSO' AS info;
SELECT 'Clienti: ' || COUNT(*) || ' record' AS info FROM customers;
SELECT 'Conti: ' || COUNT(*) || ' record' AS info FROM accounts;
SELECT 'Transazioni: ' || COUNT(*) || ' record' AS info FROM transactions;
SELECT 'Tipi transazione: ' || COUNT(*) || ' record' AS info FROM transaction_types;
SELECT 'Log transazioni: ' || COUNT(*) || ' record' AS info FROM transaction_log;
SELECT 'Estratti conto: ' || COUNT(*) || ' record' AS info FROM account_statements;
