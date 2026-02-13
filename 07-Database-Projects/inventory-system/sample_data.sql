-- ============================================
-- SISTEMA DI GESTIONE INVENTARIO
-- Dati di Esempio
-- PostgreSQL
-- ============================================

-- Abilita l'estensione per generare UUID (se necessario)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- INSERIMENTO CATEGORIES
-- ============================================
INSERT INTO categories (name, description) VALUES
('Elettronica', 'Prodotti elettronici e gadget'),
('Informatica', 'Computer, laptop e accessori'),
('Telefonia', 'Smartphone e accessori per telefonia'),
('Elettrodomestici', 'Elettrodomestici per la casa'),
('Abbigliamento', 'Vestiti e accessori moda'),
('Sport e Tempo Libero', 'Attrezzatura sportiva e tempo libero'),
('Casa e Giardino', 'Articoli per la casa e il giardino'),
('Alimentari', 'Prodotti alimentari e bevande'),
('Bellezza e Salute', 'Prodotti per la cura personale'),
('Cartoleria', 'Articoli di cancelleria e ufficio'),
('Giocattoli', 'Giochi e giocattoli per bambini'),
('Auto e Moto', 'Accessori e ricambi per veicoli');

-- ============================================
-- INSERIMENTO SUPPLIERS
-- ============================================
INSERT INTO suppliers (name, contact_person, email, phone, address) VALUES
('TechSupply Italia Srl', 'Mario Rossi', 'mario.rossi@techsupply.it', '02 1234567', 'Via Roma 123, Milano'),
('EuroTrade SpA', 'Laura Bianchi', 'laura.bianchi@eurotrade.eu', '051 7654321', 'Viale Italia 45, Bologna'),
('GlobalImports GmbH', 'Hans Mueller', 'hans.mueller@globalimports.de', '+49 89 123456', 'Bahnhofstrasse 78, Monaco'),
('AsiaPacific Trading', 'Chen Wei', 'chen.wei@asiapacific.com', '+86 21 9876543', 'Nanjing Road 567, Shanghai'),
('Mediterranea Supply', 'Giuseppe Verdi', 'giuseppe.verdi@medsupply.it', '081 2345678', 'Corso Italia 89, Napoli'),
('NordDistribution Sagl', 'Anna Ferrari', 'anna.ferrari@norddist.ch', '+41 91 3456789', 'Via Cantonale 12, Lugano'),
('IberiaExport SA', 'Carlos Garcia', 'carlos.garcia@iberiaexport.es', '+34 93 4567890', 'Passeig de Gracia 234, Barcellona'),
('EastConnect Ltd', 'John Smith', 'john.smith@eastconnect.uk', '+44 20 3456789', 'Oxford Street 67, Londra'),
('CentralEurope Trade', 'Jan Novak', 'jan.novak@cetrade.cz', '+420 2 5678901', 'Wenceslas Square 34, Praga'),
('LocalProducers Italia', 'Marco Colombo', 'marco.colombo@localprod.it', '045 678901', 'Via del Lavoro 890, Verona');

-- ============================================
-- INSERIMENTO PRODUCTS (50+ prodotti)
-- ============================================
INSERT INTO products (name, sku, category_id, supplier_id, cost_price, sell_price, current_stock, min_stock, max_stock, reorder_point) VALUES
-- Elettronica (1)
('Smart TV 55" 4K', 'TV-SAM-554K', 1, 1, 350.00, 599.99, 45, 5, 50, 10),
('Soundbar Bluetooth', 'SB-SONY-BT', 1, 1, 80.00, 149.99, 30, 5, 40, 10),
('Cuffie Wireless', 'HP-JBL-WN', 1, 2, 35.00, 79.99, 120, 15, 150, 25),
('Telecamera WiFi', 'CAM-TPL-WF', 1, 2, 25.00, 59.99, 8, 10, 50, 15),
('Smart Watch', 'SW-APP-SE', 1, 1, 120.00, 249.99, 25, 5, 40, 10),
('Lampada Smart LED', 'LP-PHL-SL', 1, 3, 18.00, 39.99, 60, 10, 80, 20),
('Altoparlante Portatile', 'SP-JBL-PT', 1, 2, 40.00, 89.99, 5, 10, 40, 15),

-- Informatica (2)
('Laptop 15.6" i5', 'LP-HP-15I5', 2, 1, 450.00, 799.99, 15, 3, 25, 5),
('Mouse Wireless', 'MO-LOG-WL', 2, 3, 8.00, 19.99, 200, 30, 250, 50),
('Tastiera Meccanica', 'KB-COR-MX', 2, 3, 45.00, 89.99, 35, 10, 50, 15),
('Monitor 27" IPS', 'MN-ASU-27', 2, 1, 180.00, 349.99, 20, 5, 30, 8),
('Webcam HD 1080p', 'WC-LOG-HD', 2, 3, 25.00, 49.99, 40, 10, 60, 15),
('Stampante Laser', 'PR-CAN-LA', 2, 1, 120.00, 249.99, 12, 3, 20, 5),
('Hard Disk 2TB', 'HD-SE2-2TB', 2, 3, 55.00, 99.99, 45, 10, 60, 15),
('SSD 500GB', 'SD-SAM-500', 2, 1, 40.00, 79.99, 80, 15, 100, 25),
('Router WiFi 6', 'RT-TPL-W6', 2, 2, 35.00, 69.99, 28, 8, 40, 12),

-- Telefonia (3)
('Smartphone Android', 'PH-SAM-A54', 3, 1, 250.00, 499.99, 18, 5, 25, 8),
('Cover iPhone', 'CV-APP-IP', 3, 3, 5.00, 14.99, 150, 25, 200, 40),
('Caricabatterie USB-C', 'CB-ANK-UC', 3, 3, 8.00, 19.99, 90, 20, 120, 30),
('Cabllo USB-C', 'CB-USB-2M', 3, 2, 3.00, 9.99, 180, 30, 250, 50),
('Power Bank 20000', 'PB-XIA-20', 3, 4, 15.00, 34.99, 65, 12, 80, 20),
('Auricolari Bluetooth', 'EA-XIA-BT', 3, 4, 12.00, 29.99, 7, 15, 60, 20),
('Supporto Auto', 'SC-NDK-AT', 3, 2, 6.00, 15.99, 55, 12, 70, 20),

-- Elettrodomestici (4)
('Frigorifero 300L', 'FR-BOS-300', 4, 5, 350.00, 699.99, 8, 2, 15, 4),
('Lavatrice 8kg', 'LW-IND-8K', 4, 5, 280.00, 549.99, 10, 2, 15, 4),
('Aspirapolvere Ciclonico', 'VC-DY-CL', 4, 6, 120.00, 249.99, 15, 3, 25, 5),
('Forno Elettrico', 'OV-SME-60', 4, 5, 200.00, 399.99, 6, 2, 12, 3),
('Microonde', 'MW-LG-25', 4, 6, 80.00, 159.99, 22, 5, 30, 8),

-- Abbigliamento (5)
('T-Shirt Uomo', 'TS-BN-M', 5, 7, 8.00, 19.99, 150, 25, 200, 40),
('Jeans Donna', 'JN-LV-F', 5, 7, 18.00, 49.99, 80, 15, 100, 25),
('Giacca Invernale', 'JK-NO-M', 5, 7, 45.00, 99.99, 30, 8, 45, 12),
('Scarpe Sportive', 'SH-NK-SP', 5, 6, 35.00, 79.99, 55, 10, 70, 18),
('Cintura Pelle', 'BT-AR-U', 5, 7, 12.00, 29.99, 95, 20, 120, 30),

-- Sport e Tempo Libero (6)
('Bicicletta MTB', 'BI-TR-MTB', 6, 6, 180.00, 399.99, 12, 2, 20, 4),
('Pallone Calcio', 'BL-AD-FB', 6, 8, 12.00, 24.99, 60, 15, 80, 20),
('Tappeto Yoga', 'YG-ND-YG', 6, 6, 15.00, 29.99, 45, 10, 60, 18),
('Borraccia 1L', 'BT-SP-1L', 6, 8, 4.00, 9.99, 200, 35, 250, 50),
('Zaino Trekking', 'PK-ND-TR', 6, 6, 28.00, 59.99, 25, 8, 35, 12),

-- Casa e Giardino (7)
('Set Attrezzi', 'TL-ST-BA', 7, 5, 35.00, 69.99, 40, 10, 50, 15),
('Piante Ortaggi', 'PL-GR-VE', 7, 10, 3.00, 7.99, 120, 25, 150, 40),
('Vaso Ceramica', 'VA-GR-30', 7, 10, 8.00, 18.99, 75, 15, 100, 25),
('Tavolo Giardino', 'TB-GR-CT', 7, 10, 65.00, 149.99, 8, 2, 15, 4),
('Sedia Pieghevole', 'CH-GR-FL', 7, 10, 15.00, 34.99, 50, 12, 70, 18),

-- Alimentari (8)
('Olio Extra Vergine', 'OL-IT-1L', 8, 9, 7.00, 14.99, 180, 30, 250, 50),
('Pasta Grano Duro', 'PS-IT-500', 8, 9, 0.80, 1.99, 300, 50, 400, 80),
('Vino Rosso', 'WN-IT-75', 8, 9, 6.00, 12.99, 95, 20, 120, 30),
('Caffè Macinato', 'CF-IT-500', 8, 9, 4.00, 8.99, 140, 25, 180, 40),
('Formaggio Parmigiano', 'CH-IT-200', 8, 9, 9.00, 18.99, 60, 15, 80, 20),

-- Bellezza e Salute (9)
('Shampoo', 'SH-HE-30', 9, 3, 3.00, 7.99, 150, 25, 200, 40),
('Crema Viso', 'CR-LO-50', 9, 3, 12.00, 29.99, 75, 15, 100, 25),
('Spazzola Capelli', 'BR-RE-HD', 9, 3, 15.00, 34.99, 35, 8, 50, 12),
('Deodorante', 'DO-NK-10', 9, 8, 2.00, 5.99, 200, 40, 300, 60),
('Spugna Viso', 'SP-CL-FC', 9, 3, 4.00, 9.99, 85, 18, 110, 28);

-- ============================================
-- INSERIMENTO SALES (100+ vendite)
-- ============================================
INSERT INTO sales (sale_date, customer_name, total_amount, payment_method, status) VALUES
('2024-01-05 10:30:00', 'Mario Bianchi', 1299.98, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-05 14:20:00', 'Laura Verdi', 89.99, 'CASH', 'COMPLETED'),
('2024-01-06 09:15:00', 'Giuseppe Rossi', 249.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-06 16:45:00', 'Anna Ferrari', 19.99, 'PAYPAL', 'COMPLETED'),
('2024-01-07 11:30:00', 'Marco Colombo', 599.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-07 15:00:00', 'Chiara Neri', 159.99, 'CASH', 'COMPLETED'),
('2024-01-08 10:00:00', 'Luca Costa', 79.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-08 14:30:00', 'Sofia Greco', 349.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-09 09:45:00', 'Paolo Martinelli', 149.99, 'CASH', 'COMPLETED'),
('2024-01-09 13:20:00', 'Elena Marini', 99.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-01-10 10:50:00', 'Andrea Rizzo', 499.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-10 15:40:00', 'Francesca Leone', 59.99, 'PAYPAL', 'COMPLETED'),
('2024-01-11 11:10:00', 'Roberto Sanna', 249.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-11 16:25:00', 'Giulia Moretti', 89.99, 'CASH', 'COMPLETED'),
('2024-01-12 09:30:00', 'Stefano Conti', 799.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-12 14:15:00', 'Valentina Ricci', 39.99, 'PAYPAL', 'COMPLETED'),
('2024-01-15 10:20:00', 'Davide Esposito', 199.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-15 14:50:00', 'Martina Bruno', 69.99, 'CASH', 'COMPLETED'),
('2024-01-16 09:40:00', 'Simone Gallo', 149.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-16 13:30:00', 'Sara Mancini', 299.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-01-17 11:00:00', 'Matteo Lombardo', 499.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-17 15:15:00', 'Claudia D''Angelo', 79.99, 'PAYPAL', 'COMPLETED'),
('2024-01-18 10:10:00', 'Federico Marchetti', 349.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-18 14:40:00', 'Alessia Parisi', 119.99, 'CASH', 'COMPLETED'),
('2024-01-19 09:25:00', 'Nicolas Romano', 599.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-19 13:50:00', 'Benedetta Rossetti', 49.99, 'PAYPAL', 'COMPLETED'),
('2024-01-22 10:35:00', 'Alessandro Ferri', 199.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-22 15:25:00', 'Monica Gatti', 159.99, 'CASH', 'COMPLETED'),
('2024-01-23 11:45:00', 'Emanuele Pallini', 249.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-23 16:10:00', 'Daniela Bernardi', 89.99, 'PAYPAL', 'COMPLETED'),
('2024-01-24 09:55:00', 'Fabio Colletti', 699.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-01-24 14:20:00', 'Tatiana Benedetti', 39.99, 'CASH', 'COMPLETED'),
('2024-01-25 10:40:00', 'Salvatore Vinci', 179.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-25 15:30:00', 'Serena Serra', 69.99, 'PAYPAL', 'COMPLETED'),
('2024-01-26 09:20:00', 'Luigi Fontana', 449.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-26 13:40:00', 'Martina Cassano', 129.99, 'CASH', 'COMPLETED'),
('2024-01-29 11:15:00', 'Vincenzo Marino', 299.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-01-29 15:50:00', 'Federica Monti', 59.99, 'PAYPAL', 'COMPLETED'),
('2024-01-30 10:05:00', 'Giovanni Barbieri', 799.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-01-30 14:35:00', 'Elisa Gregori', 99.99, 'CASH', 'COMPLETED'),
('2024-01-31 09:50:00', 'Antonio Valentini', 349.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-01 11:25:00', 'Silvia Gialli', 149.99, 'PAYPAL', 'COMPLETED'),
('2024-02-01 16:00:00', 'Daniele Amato', 89.99, 'CASH', 'COMPLETED'),
('2024-02-02 10:15:00', 'Cristian Pepe', 599.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-02 14:45:00', 'Samanta Longo', 79.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-05 09:35:00', 'Michele Calabrese', 249.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-02-05 14:10:00', 'Rita Serra', 119.99, 'CASH', 'COMPLETED'),
('2024-02-06 11:30:00', 'Paolo Bellini', 499.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-06 15:20:00', 'Lucia Redaelli', 69.99, 'PAYPAL', 'COMPLETED'),
('2024-02-07 10:25:00', 'Diego Fumagalli', 199.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-07 14:55:00', 'Patrizia Sala', 39.99, 'CASH', 'COMPLETED'),
('2024-02-08 09:40:00', 'Riccardo Donati', 699.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-08 13:30:00', 'Barbara Leone', 159.99, 'PAYPAL', 'COMPLETED'),
('2024-02-09 11:00:00', 'Claudio Parisi', 299.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-09 15:40:00', 'Monica Rinaldi', 89.99, 'CASH', 'COMPLETED'),
('2024-02-12 10:50:00', 'Enzo Grassi', 449.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-12 15:15:00', 'Franca Pelliccia', 49.99, 'PAYPAL', 'COMPLETED'),
('2024-02-13 09:15:00', 'Sandro Napolitano', 179.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-13 14:30:00', 'Emanuela Tarquini', 99.99, 'CASH', 'COMPLETED'),
('2024-02-14 11:45:00', 'Alberto Coppola', 599.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-14 16:25:00', 'Raffaella Vitale', 79.99, 'PAYPAL', 'COMPLETED'),
('2024-02-15 10:00:00', 'Mauro Spinelli', 349.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-15 14:20:00', 'Carla Bacci', 129.99, 'CASH', 'COMPLETED'),
('2024-02-16 09:30:00', 'Filippo Carbone', 249.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-16 13:50:00', 'Giada Martino', 59.99, 'PAYPAL', 'COMPLETED'),
('2024-02-19 11:10:00', 'Renzo Ferretti', 799.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-02-19 15:45:00', 'Pierpaolo Cattaneo', 149.99, 'CASH', 'COMPLETED'),
('2024-02-20 10:35:00', 'Gabriele Moretti', 199.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-20 14:15:00', 'Tiziana D''Amico', 89.99, 'PAYPAL', 'COMPLETED'),
('2024-02-21 09:25:00', 'Angelo Palmieri', 499.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-21 13:40:00', 'Loredana Polli', 69.99, 'CASH', 'COMPLETED'),
('2024-02-22 11:20:00', 'Bruno Montanari', 299.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-22 15:55:00', 'Gabriella Gaspari', 119.99, 'PAYPAL', 'COMPLETED'),
('2024-02-23 10:05:00', 'Stefania Benedetti', 599.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-23 14:40:00', 'Giorgio Valeri', 39.99, 'CASH', 'COMPLETED'),
('2024-02-26 09:50:00', 'Mirco Mariani', 349.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-26 13:30:00', 'Roberta Gobbi', 159.99, 'PAYPAL', 'COMPLETED'),
('2024-02-27 11:15:00', 'Adriano Zanini', 249.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-27 15:00:00', 'Angela Ausilia', 79.99, 'CASH', 'COMPLETED'),
('2024-02-28 10:30:00', 'Domenico De Angelis', 699.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-02-28 14:15:00', 'Paola Ludovici', 99.99, 'PAYPAL', 'COMPLETED'),
('2024-02-29 09:45:00', 'Luigi Sprovieri', 199.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-02-29 13:20:00', 'Mariarosaria Bisceglia', 49.99, 'CASH', 'COMPLETED'),
('2024-03-01 11:00:00', 'Vittorio Esposito', 449.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-03-01 15:30:00', 'Antonella Mattei', 129.99, 'PAYPAL', 'COMPLETED'),
('2024-03-04 10:15:00', 'Cosimo Greco', 299.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-03-04 14:50:00', 'Cinzia Ferrara', 89.99, 'CASH', 'COMPLETED'),
('2024-03-05 09:20:00', 'Ernesto Mazzola', 799.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-03-05 13:45:00', 'Ester Ruggieri', 179.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-03-06 11:30:00', 'Silvestro Conte', 149.99, 'PAYPAL', 'COMPLETED'),
('2024-03-06 16:10:00', 'Caterina Basile', 59.99, 'CASH', 'COMPLETED'),
('2024-03-07 10:40:00', 'Gastone Milanesi', 499.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-03-07 15:25:00', 'Ornella Sartori', 99.99, 'PAYPAL', 'COMPLETED'),
('2024-03-08 09:55:00', 'Primo Barone', 349.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-03-08 14:35:00', 'Vilma De Luca', 69.99, 'CASH', 'COMPLETED'),
('2024-03-11 11:20:00', 'Osvaldo Pugliese', 599.99, 'DEBIT_CARD', 'COMPLETED'),
('2024-03-11 15:05:00', 'Lina Caputo', 119.99, 'PAYPAL', 'COMPLETED'),
('2024-03-12 10:10:00', 'Adriano Lombardi', 249.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-03-12 14:45:00', 'Rosaria Pellegrino', 39.99, 'CASH', 'COMPLETED'),
('2024-03-13 09:35:00', 'Noel Giordano', 699.99, 'BANK_TRANSFER', 'COMPLETED'),
('2024-03-13 13:50:00', 'Dina Nicotra', 159.99, 'PAYPAL', 'COMPLETED'),
('2024-03-14 11:25:00', 'Amedeo Lanza', 199.99, 'CREDIT_CARD', 'COMPLETED'),
('2024-03-14 15:15:00', 'Loredana Palumbo', 79.99, 'DEBIT_CARD', 'COMPLETED');

-- ============================================
-- INSERIMENTO SALE_ITEMS
-- ============================================
-- Aggiungo items per le vendite (alcuni esempi significativi)
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
-- Sale 1: Mario Bianchi - Laptop + Monitor + SSD
(1, 8, 1, 799.99, 799.99),
(1, 11, 1, 349.99, 349.99),
(1, 14, 1, 79.99, 79.99),
-- Sale 2: Laura Verdi - Mouse + Tastiera
(2, 9, 2, 19.99, 39.98),
(2, 10, 1, 89.99, 89.99),
-- Sale 3: Giuseppe Rossi - Smartphone
(3, 23, 1, 499.99, 499.99),
-- Sale 4: Anna Ferrari - Cover iPhone
(4, 24, 1, 14.99, 14.99),
(4, 27, 1, 9.99, 9.99),
-- Sale 5: Marco Colombo - Smart TV
(5, 1, 1, 599.99, 599.99),
-- Sale 6: Chiara Neri - Soundbar + Cuffie
(6, 2, 1, 149.99, 149.99),
(6, 3, 1, 79.99, 79.99),
-- Continuo con altre vendite...
(7, 9, 3, 19.99, 59.97),
(7, 10, 1, 89.99, 89.99),
(8, 11, 1, 349.99, 349.99),
(9, 1, 1, 149.99, 149.99),
(10, 15, 1, 99.99, 99.99),
(11, 23, 1, 499.99, 499.99),
(12, 6, 1, 59.99, 59.99),
(13, 2, 1, 149.99, 149.99),
(13, 3, 1, 79.99, 79.99),
(14, 26, 1, 89.99, 89.99),
(15, 8, 1, 799.99, 799.99),
(16, 5, 1, 39.99, 39.99),
(17, 11, 1, 349.99, 349.99),
(18, 2, 1, 69.99, 69.99),
(18, 6, 1, 89.99, 89.99),
(19, 23, 1, 149.99, 149.99),
(20, 12, 1, 299.99, 299.99),
(21, 1, 1, 499.99, 499.99),
(22, 9, 3, 19.99, 59.97),
(22, 10, 1, 89.99, 89.99),
(23, 11, 1, 349.99, 349.99),
(24, 5, 1, 39.99, 39.99),
(25, 8, 1, 599.99, 599.99),
(26, 6, 1, 49.99, 49.99),
(27, 2, 1, 199.99, 199.99),
(28, 3, 1, 69.99, 69.99),
(29, 23, 1, 249.99, 249.99),
(30, 26, 1, 89.99, 89.99),
(31, 8, 1, 699.99, 699.99),
(32, 5, 1, 39.99, 39.99),
(33, 11, 1, 179.99, 179.99),
(34, 6, 1, 69.99, 69.99),
(35, 1, 1, 449.99, 449.99),
(36, 23, 1, 129.99, 129.99),
(37, 2, 1, 299.99, 299.99),
(38, 3, 1, 59.99, 59.99),
(39, 8, 1, 799.99, 799.99),
(40, 9, 5, 19.99, 99.95),
(41, 23, 1, 249.99, 249.99),
(42, 26, 1, 119.99, 119.99),
(43, 11, 1, 499.99, 499.99),
(44, 6, 1, 69.99, 69.99),
(45, 2, 1, 199.99, 199.99),
(46, 5, 1, 39.99, 39.99),
(47, 8, 1, 699.99, 699.99),
(48, 3, 1, 159.99, 159.99),
(49, 1, 1, 299.99, 299.99),
(50, 23, 1, 89.99, 89.99);

-- Aggiungo più items per raggiungere copertura adeguata
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal)
SELECT
    (random() * 99 + 1)::int as sale_id,
    (random() * 49 + 1)::int as product_id,
    (random() * 4 + 1)::int as quantity,
    (SELECT sell_price FROM products WHERE id = (random() * 49 + 1)::int) as unit_price,
    0.00 as subtotal
FROM generate_series(1, 150);

-- Aggiorno i subtotali
UPDATE sale_items SET subtotal = quantity * unit_price WHERE subtotal = 0.00;

-- ============================================
-- INSERIMENTO PURCHASE_ORDERS (20+ ordini)
-- ============================================
INSERT INTO purchase_orders (supplier_id, order_date, expected_date, status, total_cost, notes) VALUES
(1, '2024-01-02', '2024-01-15', 'RECEIVED', 8500.00, 'Ordine mensile elettronica'),
(2, '2024-01-05', '2024-01-20', 'RECEIVED', 5200.00, 'Rifornimento informatica'),
(3, '2024-01-08', '2024-01-25', 'RECEIVED', 3200.00, 'Accessori tech'),
(1, '2024-01-12', '2024-01-28', 'RECEIVED', 6800.00, 'Nuovi arrivi TV'),
(4, '2024-01-15', '2024-02-05', 'RECEIVED', 9500.00, 'Importazione Asia'),
(5, '2024-01-18', '2024-02-08', 'RECEIVED', 4500.00, 'Elettrodomestici'),
(2, '2024-01-22', '2024-02-10', 'RECEIVED', 3800.00, 'Accessori PC'),
(6, '2024-01-25', '2024-02-12', 'RECEIVED', 5200.00, 'Articoli vari'),
(7, '2024-02-01', '2024-02-20', 'RECEIVED', 6200.00, 'Abbigliamento primavera'),
(8, '2024-02-05', '2024-02-25', 'RECEIVED', 2800.00, 'Sport e tempo libero'),
(9, '2024-02-08', '2024-02-28', 'RECEIVED', 1500.00, 'Alimentari locali'),
(10, '2024-02-12', '2024-03-05', 'RECEIVED', 980.00, 'Prodotti freschi'),
(1, '2024-02-15', '2024-03-10', 'ORDERED', 7200.00, 'Ordine marzo'),
(3, '2024-02-18', '2024-03-12', 'ORDERED', 4100.00, 'Accessori global'),
(4, '2024-02-22', '2024-03-15', 'ORDERED', 8900.00, 'Contenitore Asia'),
(5, '2024-02-25', '2024-03-18', 'PENDING', 3800.00, 'Elettrodomestici Q2'),
(6, '2024-02-28', '2024-03-22', 'PENDING', 5500.00, 'Riassortimento nord'),
(7, '2024-03-01', '2024-03-25', 'PENDING', 4600.00, 'Collezione estate'),
(8, '2024-03-05', '2024-03-28', 'PENDING', 2100.00, 'Sportivi'),
(9, '2024-03-08', '2024-04-01', 'PENDING', 1200.00, 'Prodotti stagionali'),
(10, '2024-03-12', '2024-04-05', 'PENDING', 850.00, 'Locali freschi');

-- ============================================
-- INSERIMENTO PURCHASE_ITEMS
-- ============================================
INSERT INTO purchase_items (order_id, product_id, quantity, unit_cost) VALUES
-- PO 1: TechSupply
(1, 1, 50, 350.00),
(1, 2, 40, 80.00),
(1, 5, 30, 120.00),
-- PO 2: EuroTrade
(2, 8, 20, 450.00),
(2, 11, 30, 180.00),
(2, 12, 100, 25.00),
-- PO 3: GlobalImports
(3, 9, 150, 8.00),
(3, 10, 50, 45.00),
(3, 14, 80, 40.00),
-- PO 4: TechSupply
(4, 1, 45, 350.00),
(4, 3, 100, 35.00),
-- PO 5: AsiaPacific
(5, 8, 25, 450.00),
(5, 23, 60, 250.00),
(5, 26, 200, 12.00),
-- PO 6: Mediterranea
(6, 29, 15, 350.00),
(6, 30, 20, 280.00),
-- PO 7: EuroTrade
(7, 11, 25, 180.00),
(7, 13, 50, 120.00),
-- PO 8: NordDistribution
(8, 31, 120, 280.00),
(8, 33, 80, 45.00),
-- PO 9: IberiaExport
(9, 35, 200, 8.00),
(9, 36, 150, 18.00),
-- PO 10: EastConnect
(10, 41, 50, 12.00),
(10, 42, 80, 0.80),
-- PO 11: TechSupply
(11, 1, 40, 350.00),
(11, 2, 40, 80.00),
-- PO 12: GlobalImports
(12, 9, 200, 8.00),
(12, 10, 60, 45.00),
-- PO 13: AsiaPacific
(13, 8, 30, 450.00),
(13, 23, 80, 250.00),
-- PO 14: Mediterranea
(14, 29, 12, 350.00),
(14, 30, 18, 280.00),
-- PO 15-21: Altri ordini
(15, 11, 30, 180.00),
(16, 35, 180, 8.00),
(17, 8, 25, 450.00),
(18, 41, 60, 12.00),
(19, 23, 50, 250.00),
(20, 9, 150, 8.00),
(21, 42, 100, 0.80);

-- ============================================
-- INSERIMENTO STOCK_MOVEMENTS (200+ movimenti)
-- ============================================
-- Movimenti IN per ordini di acquisto ricevuti
INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, movement_date, notes) VALUES
(1, 'IN', 50, 1, '2024-01-15 10:00:00', 'Ricezione PO-001'),
(2, 'IN', 40, 1, '2024-01-15 10:00:00', 'Ricezione PO-001'),
(5, 'IN', 30, 1, '2024-01-15 10:00:00', 'Ricezione PO-001'),
(8, 'IN', 20, 2, '2024-01-20 14:00:00', 'Ricezione PO-002'),
(11, 'IN', 30, 2, '2024-01-20 14:00:00', 'Ricezione PO-002'),
(12, 'IN', 100, 2, '2024-01-20 14:00:00', 'Ricezione PO-002'),
(9, 'IN', 150, 3, '2024-01-25 09:00:00', 'Ricezione PO-003'),
(10, 'IN', 50, 3, '2024-01-25 09:00:00', 'Ricezione PO-003'),
(14, 'IN', 80, 3, '2024-01-25 09:00:00', 'Ricezione PO-003'),
(1, 'IN', 45, 4, '2024-01-28 16:00:00', 'Ricezione PO-004'),
(3, 'IN', 100, 4, '2024-01-28 16:00:00', 'Ricezione PO-004'),
(8, 'IN', 25, 5, '2024-02-05 11:00:00', 'Ricezione PO-005'),
(23, 'IN', 60, 5, '2024-02-05 11:00:00', 'Ricezione PO-005'),
(26, 'IN', 200, 5, '2024-02-05 11:00:00', 'Ricezione PO-005'),
(29, 'IN', 15, 6, '2024-02-08 15:00:00', 'Ricezione PO-006'),
(30, 'IN', 20, 6, '2024-02-08 15:00:00', 'Ricezione PO-006'),
(11, 'IN', 25, 7, '2024-02-10 10:00:00', 'Ricezione PO-007'),
(13, 'IN', 50, 7, '2024-02-10 10:00:00', 'Ricezione PO-007'),
(31, 'IN', 120, 8, '2024-02-12 14:00:00', 'Ricezione PO-008'),
(33, 'IN', 80, 8, '2024-02-12 14:00:00', 'Ricezione PO-008'),
(35, 'IN', 200, 9, '2024-02-20 09:00:00', 'Ricezione PO-009'),
(36, 'IN', 150, 9, '2024-02-20 09:00:00', 'Ricezione PO-009');

-- Movimenti OUT per vendite
INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, movement_date, notes) VALUES
(8, 'OUT', 1, 1, '2024-01-05 10:30:00', 'Vendita SA-001'),
(11, 'OUT', 1, 1, '2024-01-05 10:30:00', 'Vendita SA-001'),
(14, 'OUT', 1, 1, '2024-01-05 10:30:00', 'Vendita SA-001'),
(9, 'OUT', 2, 2, '2024-01-05 14:20:00', 'Vendita SA-002'),
(10, 'OUT', 1, 2, '2024-01-05 14:20:00', 'Vendita SA-002'),
(23, 'OUT', 1, 3, '2024-01-06 09:15:00', 'Vendita SA-003'),
(24, 'OUT', 1, 4, '2024-01-06 16:45:00', 'Vendita SA-004'),
(27, 'OUT', 1, 4, '2024-01-06 16:45:00', 'Vendita SA-004'),
(1, 'OUT', 1, 5, '2024-01-07 11:30:00', 'Vendita SA-005'),
(2, 'OUT', 1, 6, '2024-01-07 15:00:00', 'Vendita SA-006'),
(3, 'OUT', 1, 6, '2024-01-07 15:00:00', 'Vendita SA-006'),
(9, 'OUT', 3, 7, '2024-01-08 10:00:00', 'Vendita SA-007'),
(10, 'OUT', 1, 7, '2024-01-08 10:00:00', 'Vendita SA-007'),
(11, 'OUT', 1, 8, '2024-01-08 14:30:00', 'Vendita SA-008'),
(1, 'OUT', 1, 9, '2024-01-09 09:45:00', 'Vendita SA-009'),
(15, 'OUT', 1, 10, '2024-01-09 13:20:00', 'Vendita SA-010'),
(23, 'OUT', 1, 11, '2024-01-10 10:50:00', 'Vendita SA-011'),
(6, 'OUT', 1, 12, '2024-01-10 15:40:00', 'Vendita SA-012'),
(2, 'OUT', 1, 13, '2024-01-11 11:10:00', 'Vendita SA-013'),
(3, 'OUT', 1, 13, '2024-01-11 11:10:00', 'Vendita SA-013'),
(26, 'OUT', 1, 14, '2024-01-11 16:25:00', 'Vendita SA-014'),
(8, 'OUT', 1, 15, '2024-01-12 09:30:00', 'Vendita SA-015'),
(5, 'OUT', 1, 16, '2024-01-12 14:15:00', 'Vendita SA-016'),
(11, 'OUT', 1, 17, '2024-01-15 10:20:00', 'Vendita SA-017'),
(2, 'OUT', 1, 18, '2024-01-15 14:50:00', 'Vendita SA-018'),
(6, 'OUT', 1, 18, '2024-01-15 14:50:00', 'Vendita SA-018'),
(23, 'OUT', 1, 19, '2024-01-16 09:40:00', 'Vendita SA-019'),
(12, 'OUT', 1, 20, '2024-01-16 13:30:00', 'Vendita SA-020'),
(1, 'OUT', 1, 21, '2024-01-17 11:00:00', 'Vendita SA-021'),
(9, 'OUT', 3, 22, '2024-01-17 15:15:00', 'Vendita SA-022'),
(10, 'OUT', 1, 22, '2024-01-17 15:15:00', 'Vendita SA-022'),
(11, 'OUT', 1, 23, '2024-01-18 10:35:00', 'Vendita SA-023'),
(5, 'OUT', 1, 24, '2024-01-18 14:40:00', 'Vendita SA-024'),
(8, 'OUT', 1, 25, '2024-01-19 09:25:00', 'Vendita SA-025'),
(6, 'OUT', 1, 26, '2024-01-19 13:50:00', 'Vendita SA-026'),
(2, 'OUT', 1, 27, '2024-01-22 11:45:00', 'Vendita SA-027'),
(3, 'OUT', 1, 28, '2024-01-22 15:25:00', 'Vendita SA-028'),
(23, 'OUT', 1, 29, '2024-01-23 09:55:00', 'Vendita SA-029'),
(26, 'OUT', 1, 30, '2024-01-23 14:20:00', 'Vendita SA-030'),
(8, 'OUT', 1, 31, '2024-01-24 10:40:00', 'Vendita SA-031'),
(5, 'OUT', 1, 32, '2024-01-24 15:30:00', 'Vendita SA-032'),
(11, 'OUT', 1, 33, '2024-01-25 09:20:00', 'Vendita SA-033'),
(6, 'OUT', 1, 34, '2024-01-25 13:40:00', 'Vendita SA-034'),
(1, 'OUT', 1, 35, '2024-01-26 11:15:00', 'Vendita SA-035'),
(23, 'OUT', 1, 36, '2024-01-26 15:50:00', 'Vendita SA-036'),
(2, 'OUT', 1, 37, '2024-01-29 10:05:00', 'Vendita SA-037'),
(3, 'OUT', 1, 38, '2024-01-29 14:35:00', 'Vendita SA-038'),
(8, 'OUT', 1, 39, '2024-01-30 09:50:00', 'Vendita SA-039'),
(9, 'OUT', 5, 40, '2024-01-30 14:20:00', 'Vendita SA-040'),
(23, 'OUT', 1, 41, '2024-01-31 11:25:00', 'Vendita SA-041'),
(26, 'OUT', 1, 42, '2024-01-31 16:00:00', 'Vendita SA-042'),
(11, 'OUT', 1, 43, '2024-02-01 10:15:00', 'Vendita SA-043'),
(6, 'OUT', 1, 44, '2024-02-01 14:45:00', 'Vendita SA-044'),
(2, 'OUT', 1, 45, '2024-02-05 09:35:00', 'Vendita SA-045'),
(5, 'OUT', 1, 46, '2024-02-05 14:10:00', 'Vendita SA-046'),
(8, 'OUT', 1, 47, '2024-02-06 11:30:00', 'Vendita SA-047'),
(3, 'OUT', 1, 48, '2024-02-06 15:20:00', 'Vendita SA-048'),
(1, 'OUT', 1, 49, '2024-02-07 10:25:00', 'Vendita SA-049'),
(23, 'OUT', 1, 50, '2024-02-07 14:55:00', 'Vendita SA-050');

-- Movimenti ADJUSTMENT (aggiustamenti inventario)
INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, movement_date, notes) VALUES
(4, 'ADJUSTMENT', 5, NULL, '2024-01-15 12:00:00', 'Inventario: merce danneggiata'),
(7, 'ADJUSTMENT', -3, NULL, '2024-01-20 15:00:00', 'Correzione inventario'),
(13, 'ADJUSTMENT', 2, NULL, '2024-01-25 10:00:00', 'Recupero merce'),
(16, 'ADJUSTMENT', -1, NULL, '2024-02-01 14:00:00', 'Merce persa'),
(19, 'ADJUSTMENT', 4, NULL, '2024-02-05 11:00:00', 'Errore di conteggio'),
(22, 'ADJUSTMENT', -2, NULL, '2024-02-10 09:00:00', 'Danni trasporto'),
(25, 'ADJUSTMENT', 3, NULL, '2024-02-15 16:00:00', 'Recupero stock'),
(28, 'ADJUSTMENT', -5, NULL, '2024-02-20 13:00:00', 'Prodotto scaduto'),
(34, 'ADJUSTMENT', 1, NULL, '2024-02-25 10:00:00', 'Correzione inventario'),
(37, 'ADJUSTMENT', -4, NULL, '2024-03-01 15:00:00', 'Merce danneggiata'),
(40, 'ADJUSTMENT', 2, NULL, '2024-03-05 12:00:00', 'Recupero merce'),
(43, 'ADJUSTMENT', -3, NULL, '2024-03-10 14:00:00', 'Errore sistema'),
(46, 'ADJUSTMENT', 6, NULL, '2024-03-12 11:00:00', 'Stock errato'),
(49, 'ADJUSTMENT', -1, NULL, '2024-03-14 16:00:00', 'Prodotto deteriorato');

-- Movimenti RETURN (resi clienti)
INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, movement_date, notes) VALUES
(8, 'RETURN', 1, 15, '2024-01-20 10:00:00', 'Reso cliente SA-015'),
(23, 'RETURN', 1, 11, '2024-01-25 14:00:00', 'Reso cliente SA-011'),
(1, 'RETURN', 1, 5, '2024-02-01 11:00:00', 'Reso cliente SA-005'),
(2, 'RETURN', 1, 18, '2024-02-05 15:00:00', 'Reso cliente SA-018'),
(11, 'RETURN', 1, 33, '2024-02-10 12:00:00', 'Reso cliente SA-033');

-- Movimenti DAMAGE (merce danneggiata)
INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, movement_date, notes) VALUES
(4, 'DAMAGE', -3, NULL, '2024-01-18 09:00:00', 'Merce danneggiata in magazzino'),
(7, 'DAMAGE', -2, NULL, '2024-01-28 13:00:00', 'Danni durante trasporto interno'),
(14, 'DAMAGE', -1, NULL, '2024-02-08 10:00:00', 'Prodotto rotto'),
(21, 'DAMAGE', -4, NULL, '2024-02-18 14:00:00', 'Umidità danneggia'),
(28, 'DAMAGE', -2, NULL, '2024-02-28 11:00:00', 'Imballo danneggiato'),
(35, 'DAMAGE', -1, NULL, '2024-03-08 15:00:00', 'Prodotto danneggiato');

-- Altri movimenti OUT per vendite successive
INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, movement_date, notes)
SELECT
    (random() * 49 + 1)::int,
    'OUT',
    (random() * 3 + 1)::int,
    (random() * 99 + 1)::int,
    '2024-02-01 10:00:00'::timestamp + (random() * 50 || ' days')::interval,
    'Vendita automatica'
FROM generate_series(1, 80);

-- ============================================
-- FINE DATI DI ESEMPIo
-- ============================================
