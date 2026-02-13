-- ============================================
-- BIBLIOTECA - DATI DI ESEMPIO
-- Library Management System Sample Data
-- ============================================

-- ============================================
-- INSERIMENTO EDITORI (Publishers)
-- ============================================
INSERT INTO editori (nome, indirizzo, telefono, email) VALUES
('Mondadori', 'Via Bianca di Livorno 10, Milano', '02 7541 1', 'info@mondadori.it'),
('Einaudi', 'Via Bianca di Livorno 12, Milano', '02 7421 1', 'info@einaudi.it'),
('Feltrinelli', 'Via G. Verdi 4, Milano', '02 3666 1', 'info@feltrinelli.it'),
('Salani', 'Via Grandi 5, Milano', '02 8950 1', 'info@salani.it'),
('Rizzoli', 'Largo Donegani 2, Milano', '02 7611 1', 'info@rizzoli.it'),
('Laterza', 'Via Mileto 16, Bari', '080 522 2111', 'info@laterza.it'),
('Utet', 'Via Giuseppe Ponsioli 4, Torino', '011 561 1111', 'info@utet.it'),
('Il Saggiatore', 'Via Berchet 2, Milano', '02 8699 1', 'info@ilsaggiatore.it'),
('Garzanti', 'Via Garzanti 15, Milano', '02 7421 1', 'info@garzanti.it'),
('Bompiani', 'Via Vincenzo Monti 8, Milano', '02 7611 1', 'info@bompiani.it');

-- ============================================
-- INSERIMENTO CATEGORIE (Categories)
-- ============================================
INSERT INTO categorie (nome, descrizione) VALUES
('Romanzo', 'Romanzi di narrativa contemporanea e classica'),
('Thriller', 'Romanzi thriller, gialli e mystery'),
('Fantascienza', 'Romanzi di fantascienza e futurismo'),
('Fantasy', 'Romanzi fantasy e mondo magico'),
('Storia', 'Libri di storia, saggi storici e biografie'),
('Filosofia', 'Libri di filosofia, saggi e trattati'),
('Scienza', 'Libri di scienza, divulgazione scientifica'),
('Poesia', 'Raccolte poetiche e poesia'),
('Bambini', 'Libri per bambini e ragazzi'),
('Saggistica', 'Saggi vari e attualità');

-- ============================================
-- INSERIMENTO AUTORI (Authors)
-- ============================================
INSERT INTO autori (nome, anno_nascita, biografia, nazionalita) VALUES
('Elena Ferrante', 1943, 'Scrittrice italiana anonima, autrice della tetralogia napoletana', 'Italiana'),
('Alessandro Baricco', 1958, 'Scrittore, drammaturgo e critico musicale italiano', 'Italiana'),
('Umberto Eco', 1932, 'Semiologo, scrittore e filosofo italiano', 'Italiana'),
('Andrea Camilleri', 1925, 'Scrittore e regista italiano, creatore del commissario Montalbano', 'Italiana'),
('Italo Calvino', 1923, 'Scrittore e giornalista italiano, uno dei maggiori narratori del Novecento', 'Italiana'),
('Margaret Atwood', 1939, 'Poetessa e scrittrice canadese', 'Canadese'),
('George Orwell', 1903, 'Scrittore e giornalista britannico', 'Britannica'),
('J.K. Rowling', 1965, 'Scrittrice britannica, creatrice di Harry Potter', 'Britannica'),
('J.R.R. Tolkien', 1892, 'Scrittore e filologo britannico, padre della fantasy moderna', 'Britannica'),
('Isaac Asimov', 1920, 'Scrittore e biochimico russo naturalizzato statunitense', 'Statunitense'),
('Stephen King', 1947, 'Scrittore statunitense, re del thriller e dell''horror', 'Statunitense'),
('Agatha Christie', 1890, 'Scrittrice britannica, regina del giallo', 'Britannica'),
('Gabriel García Márquez', 1927, 'Scrittore e giornalista colombiano', 'Colombiana'),
('Haruki Murakami', 1949, 'Scrittore giapponese di romanzi e racconti', 'Giapponese'),
('Philip K. Dick', 1928, 'Scrittore statunitense di fantascienza', 'Statunitense'),
('Arthur C. Clarke', 1917, 'Scrittore britannico di fantascienza e inventore', 'Britannica'),
('J.D. Salinger', 1919, 'Scrittore statunitense', 'Statunitense'),
('Ernest Hemingway', 1899, 'Scrittore e giornalista statunitense', 'Statunitense'),
('F. Scott Fitzgerald', 1896, 'Scrittore statunitense', 'Statunitense'),
('Virginia Woolf', 1882, 'Scrittrice britannica, pioniera del modernismo', 'Britannica'),
('Kazuo Ishiguro', 1954, 'Scrittore britannico di origini giapponesi', 'Britannica'),
('Dante Alighieri', 1265, 'Poeta e scrittore italiano, padre della lingua italiana', 'Italiana'),
('Niccolò Machiavelli', 1469, 'Diplomatico, filosofo e scrittore italiano', 'Italiana'),
('Immanuel Kant', 1724, 'Filosofo tedesco', 'Tedesca'),
('Friedrich Nietzsche', 1844, 'Filosofo e poeta tedesco', 'Tedesca'),
('Eugenio Montale', 1896, 'Poeta e scrittore italiano', 'Italiana');

-- ============================================
-- INSERIMENTO LIBRI (Books)
-- ============================================
INSERT INTO libri (titolo, isbn, anno_pubblicazione, editore_id, categoria_id, copie_totali, copie_disponibili, descrizione, lingua) VALUES
-- Romanzi italiani
('L''amica geniale', '9788806222407', 2011, 1, 1, 3, 2, 'Primo volume della tetralogia napoletana', 'Italiano'),
('Storia del nuovo cognome', '9788806233120', 2012, 1, 1, 2, 2, 'Secondo volume della tetralogia napoletana', 'Italiano'),
('Those Who Leave and Those Who Stay', '9781609450144', 2013, 1, 1, 2, 1, 'Terzo volume della tetralogia napoletana', 'Italiano'),
('Oceano Mare', '9788806144242', 1993, 2, 1, 3, 3, 'Romanzo che racconta storie intrecciate ambientate in un albergo', 'Italiano'),
('Seta', '9788806145270', 1996, 2, 1, 4, 3, 'Romanzo su un commerciante di seta francese in Giappone', 'Italiano'),
('Il nome della rosa', '9788806134382', 1980, 1, 2, 5, 3, 'Romanzo storico ambientato in un monastero medievale', 'Italiano'),
('Il pendolo di Foucault', '9788806155128', 1988, 1, 2, 3, 2, 'Romanzo sul complotto e i templari', 'Italiano'),
('La forma dell''acqua', '9788806177432', 1994, 1, 2, 4, 4, 'Primo caso del commissario Montalbano', 'Italiano'),
('Il visone di luna', '9788806177449', 1995, 1, 2, 3, 2, 'Secondo caso del commissario Montalbano', 'Italiano'),
('Le cosmicomiche', '9788806174865', 1965, 2, 1, 2, 2, 'Racconti fantascientifici e filosofici', 'Italiano'),
('Se una notte d''inverno un viaggiatore', '9788806164279', 1979, 2, 1, 3, 1, 'Romanzo sperimentale sulla lettura', 'Italiano'),

-- Thriller e Mystery
('The Silent Patient', '9781250301696', 2019, 10, 2, 3, 2, 'Thriller psicologico su una donna che smette di parlare', 'Inglese'),
('Assassinio sull''Orient Express', '9788804660247', 1934, 4, 2, 4, 3, 'Hercule Poirot indaga su un omicidio sul treno', 'Italiano'),
('Dieci piccoli indiani', '9788804660230', 1939, 4, 2, 3, 2, 'Dieci persone su un''isola vengono uccise una per una', 'Italiano'),
('Shining', '9788806201234', 1977, 4, 2, 2, 1, 'Horror psicologico in un hotel isolato', 'Italiano'),
('It', '9788806156789', 1986, 4, 2, 3, 2, 'Thriller horror su un mostro che assume la forma di un clown', 'Italiano'),
('Misery', '9788806165123', 1987, 4, 2, 2, 1, 'Uno scrittore viene tenuto prigioniero dalla sua fan numero uno', 'Italiano'),

-- Fantascienza
('1984', '9780451524935', 1949, 4, 3, 5, 3, 'Romanzo distopico su un regime totalitario', 'Italiano'),
('La fattoria degli animali', '9780451526342', 1945, 4, 3, 4, 3, 'Allegoria satirica del regime sovietico', 'Italiano'),
('Io, Robot', '9780553382563', 1950, 4, 3, 3, 2, 'Racconti sulla robotica e le tre leggi della robotica', 'Inglese'),
('Fondazione', '9780553293357', 1951, 4, 3, 3, 1, 'Primo libro del ciclo della Fondazione', 'Inglese'),
('Cavalleria spaziale', '9780345325300', 1952, 4, 3, 2, 2, 'Romanzo che tratta le tre leggi della robotica', 'Inglese'),
('Ubik', '9780679743710', 1969, 4, 3, 2, 1, 'Romanzo sulla realtà e percezione', 'Inglese'),
('2001: Odissea nello spazio', '9780451457990', 1968, 4, 3, 3, 2, 'Romanzo di fantascenza basato sul soggetto omonimo', 'Inglese'),

-- Fantasy
('Harry Potter e la pietra filosofale', '9788868331539', 1997, 4, 4, 6, 4, 'Primo capitolo delle avventure di Harry Potter', 'Italiano'),
('Harry Potter e la camera dei segreti', '9788868331546', 1998, 4, 4, 5, 3, 'Secondo capitolo delle avventure di Harry Potter', 'Italiano'),
('Harry Potter e il prigioniero di Azkaban', '9788868331553', 1999, 4, 4, 5, 4, 'Terzo capitolo delle avventure di Harry Potter', 'Italiano'),
('Lo Hobbit', '9788845291410', 1937, 4, 4, 5, 3, 'Prequel de Il Signore degli Anelli', 'Italiano'),
('Il Signore degli Anelli: La Compagnia dell''Anello', '9788845291212', 1954, 4, 4, 4, 2, 'Primo volume de Il Signore degli Anelli', 'Italiano'),
('Il Signore degli Anelli: Le due torri', '9788845291229', 1954, 4, 4, 4, 3, 'Secondo volume de Il Signore degli Anelli', 'Italiano'),
('Il Signore degli Anelli: Il ritorno del re', '9788845291236', 1955, 4, 4, 4, 2, 'Terzo volume de Il Signore degli Anelli', 'Italiano'),
('Il Silmarillion', '9788845291243', 1977, 4, 4, 3, 2, 'Storia antica della Terra di Mezzo', 'Italiano'),

-- Storia e Saggistica
('Gomorra', '9788806174841', 2006, 1, 5, 3, 2, 'Inchiesta sul sistema economico camorristico', 'Italiano'),
('Sapiens: Da animali a dei', '9788806705208', 2011, 1, 5, 4, 3, 'Breve storia dell''umanità', 'Italiano'),
('Homo Deus', '9788806705215', 2015, 1, 5, 3, 2, 'Breve storia del futuro', 'Italiano'),
('21 lezioni per il XXI secolo', '9788806705222', 2018, 1, 5, 2, 2, 'Analisi delle sfide del presente', 'Italiano'),
('Il Principe', '9788806174889', 1532, 4, 5, 3, 2, 'Trattato di politica moderna', 'Italiano'),
('Critica della ragion pura', '9788806174896', 1781, 4, 6, 2, 1, 'Opera fondamentale della filosofia kantiana', 'Italiano'),
('Così parlò Zarathustra', '9788806174902', 1883, 4, 6, 2, 1, 'Opera filosofica di Nietzsche', 'Italiano'),

-- Letteratura classica
('Il giovane Holden', '9780451526374', 1951, 4, 1, 3, 2, 'Romanzo di formazione americano', 'Italiano'),
('Il grande Gatsby', '9780743273565', 1925, 4, 1, 4, 3, 'Romanzo sull''American Dream', 'Inglese'),
('Addio alle armi', '9780684801469', 1929, 4, 1, 3, 2, 'Romanzo sulla prima guerra mondiale', 'Inglese'),
('Mrs Dalloway', '9780156628000', 1925, 4, 1, 2, 1, 'Romanzo sul modernismo britannico', 'Inglese'),
('Non lasciarmi', '9780571215435', 2005, 4, 1, 3, 2, 'Romanzo distopico di Ishiguro', 'Inglese'),
('Cent''anni di solitudine', '9780060883287', 1967, 4, 1, 4, 3, 'Capolavoro del realismo magico', 'Spagnolo'),

-- Poesia
('Ossi di seppia', '9788806174858', 1925, 2, 8, 2, 2, 'Prima raccolta poetica di Montale', 'Italiano'),
('Le occasioni', '9788806174872', 1931, 2, 8, 2, 1, 'Seconda raccolta poetica di Montale', 'Italiano');

-- ============================================
-- INSERIMENTO LIBRI_AUTORI (Book_Authors)
-- ============================================
INSERT INTO libri_autori (libro_id, autore_id) VALUES
-- Elena Ferrante (1-3)
(1, 1), (2, 1), (3, 1),
-- Alessandro Baricco (4-5)
(4, 2), (5, 2),
-- Umberto Eco (6-7)
(6, 3), (7, 3),
-- Andrea Camilleri (8-9)
(8, 4), (9, 4),
-- Italo Calvino (10-11)
(10, 5), (11, 5),
-- Alex Michaelides (12)
(12, 6),
-- Agatha Christie (13-14)
(13, 12), (14, 12),
-- Stephen King (15-17)
(15, 11), (16, 11), (17, 11),
-- George Orwell (18-19)
(18, 7), (19, 7),
-- Isaac Asimov (20-22)
(20, 10), (21, 10), (22, 10),
-- Philip K. Dick (23)
(23, 15),
-- Arthur C. Clarke (24)
(24, 16),
-- J.K. Rowling (25-27)
(25, 8), (26, 8), (27, 8),
-- J.R.R. Tolkien (28-31)
(28, 9), (29, 9), (30, 9), (31, 9),
-- Roberto Saviano (32)
(32, 4),
-- Yuval Noah Harari (33-35)
(33, 10), (34, 10), (35, 10),
-- Niccolò Machiavelli (36)
(36, 24),
-- Immanuel Kant (37)
(37, 23),
-- Friedrich Nietzsche (38)
(38, 24),
-- J.D. Salinger (39)
(39, 17),
-- F. Scott Fitzgerald (40)
(40, 19),
-- Ernest Hemingway (41)
(41, 18),
-- Virginia Woolf (42)
(42, 20),
-- Kazuo Ishiguro (43)
(43, 21),
-- Gabriel García Márquez (44)
(44, 13),
-- Eugenio Montale (45-46)
(45, 26), (46, 26);

-- ============================================
-- INSERIMENTO MEMBRI (Members)
-- ============================================
INSERT INTO membri (nome, cognome, email, telefono, data_iscrizione, stato, note) VALUES
('Marco', 'Rossi', 'marco.rossi@email.com', '333 1234567', '2020-01-15', 'attivo', NULL),
('Giulia', 'Bianchi', 'giulia.bianchi@email.com', '333 2345678', '2020-02-20', 'attivo', NULL),
('Luca', 'Ferrari', 'luca.ferrari@email.com', '333 3456789', '2020-03-10', 'attivo', 'Lettore appassionato di fantascienza'),
('Francesca', 'Romano', 'francesca.romano@email.com', '333 4567890', '2020-04-05', 'attivo', NULL),
('Andrea', 'Conti', 'andrea.conti@email.com', '333 5678901', '2020-05-12', 'attivo', NULL),
('Maria', 'Ricci', 'maria.ricci@email.com', '333 6789012', '2020-06-18', 'attivo', NULL),
('Paolo', 'Marino', 'paolo.marino@email.com', '333 7890123', '2020-07-22', 'attivo', NULL),
('Anna', 'Greco', 'anna.greco@email.com', '333 8901234', '2020-08-30', 'attivo', NULL),
('Davide', 'Costa', 'davide.costa@email.com', '333 9012345', '2020-09-14', 'attivo', NULL),
('Sara', 'Mancini', 'sara.mancini@email.com', '333 0123456', '2020-10-25', 'attivo', NULL),
('Matteo', 'Rizzo', 'matteo.rizzo@email.com', '333 1234568', '2020-11-08', 'attivo', NULL),
('Chiara', 'Lombardi', 'chiara.lombardi@email.com', '333 2345679', '2020-12-03', 'attivo', NULL),
('Alessandro', 'Moretti', 'alessandro.moretti@email.com', '333 3456780', '2021-01-17', 'attivo', NULL),
('Valentina', 'Martinelli', 'valentina.martinelli@email.com', '333 4567891', '2021-02-28', 'attivo', NULL),
('Simone', 'Colombo', 'simone.colombo@email.com', '333 5678902', '2021-03-19', 'attivo', NULL),
('Elisa', 'Sanna', 'elisa.sanna@email.com', '333 6789013', '2021-04-11', 'attivo', NULL),
('Federico', 'Ferrara', 'federico.ferrara@email.com', '333 7890124', '2021-05-23', 'attivo', NULL),
('Laura', 'Galli', 'laura.galli@email.com', '333 8901235', '2021-06-07', 'attivo', NULL),
('Nicola', 'Barbieri', 'nicola.barbieri@email.com', '333 9012346', '2021-07-15', 'attivo', NULL),
('Claudia', 'Morelli', 'claudia.morelli@email.com', '333 0123457', '2021-08-29', 'attivo', NULL),
('Riccardo', 'Bernardi', 'riccardo.bernardi@email.com', '333 1234569', '2021-09-12', 'attivo', NULL),
('Cristina', 'Palmieri', 'cristina.palmieri@email.com', '333 2345670', '2021-10-21', 'attivo', NULL),
('Mirko', 'D''Angelo', 'mirko.dangelo@email.com', '333 3456781', '2021-11-05', 'attivo', NULL),
('Diana', 'Rinaldi', 'diana.rinaldi@email.com', '333 4567892', '2021-12-18', 'attivo', NULL),
('Emanuele', 'Donati', 'emanuele.donati@email.com', '333 5678903', '2022-01-09', 'attivo', NULL),
('Veronica', 'Carbone', 'veronica.carbone@email.com', '333 6789014', '2022-02-14', 'attivo', NULL),
('Tommaso', 'Serra', 'tommaso.serra@email.com', '333 7890125', '2022-03-25', 'attivo', NULL),
('Ilaria', 'Basile', 'ilaria.basile@email.com', '333 8901236', '2022-04-30', 'sospeso', 'Membro sospeso per ritardi ripetuti'),
('Giovanni', 'Parisi', 'giovanni.parisi@email.com', '333 9012347', '2022-05-16', 'attivo', NULL),
('Martina', 'Farina', 'martina.farina@email.com', '333 0123458', '2022-06-22', 'attivo', NULL),
('Daniele', 'Cattaneo', 'daniele.cattaneo@email.com', '333 1234570', '2022-07-08', 'inattivo', 'Richiesta di disattivazione'),
('Silvia', 'Marchetti', 'silvia.marchetti@email.com', '333 2345671', '2022-08-19', 'attivo', NULL),
('Fabio', 'Testa', 'fabio.testa@email.com', '333 3456782', '2022-09-27', 'attivo', NULL),
('Patrizia', 'Bruno', 'patrizia.bruno@email.com', '333 4567893', '2022-10-11', 'attivo', NULL),
('Renato', 'Grasso', 'renato.grasso@email.com', '333 5678904', '2022-11-24', 'attivo', NULL),
('Angela', 'Guerra', 'angela.guerra@email.com', '333 6789015', '2022-12-05', 'attivo', NULL),
('Luigi', 'Pellegrini', 'luigi.pellegrini@email.com', '333 7890126', '2023-01-13', 'attivo', NULL),
('Elena', 'Ruggiero', 'elena.ruggiero@email.com', '333 8901237', '2023-02-28', 'attivo', NULL),
('Massimo', 'Longo', 'massimo.longo@email.com', '333 9012348', '2023-03-17', 'attivo', NULL),
('Teresa', 'Santoro', 'teresa.santoro@email.com', '333 0123459', '2023-04-22', 'attivo', NULL),
('Antonio', 'Vitale', 'antonio.vitale@email.com', '333 1234571', '2023-05-30', 'attivo', NULL),
('Grazia', 'De Luca', 'grazia.deluca@email.com', '333 2345672', '2023-06-14', 'attivo', NULL),
('Stefano', 'Mancuso', 'stefano.mancuso@email.com', '333 3456783', '2023-07-25', 'attivo', NULL),
('Alessia', 'Fiore', 'alessia.fiore@email.com', '333 4567894', '2023-08-31', 'attivo', NULL),
('Emilio', 'Negri', 'emilio.negri@email.com', '333 5678905', '2023-09-18', 'attivo', NULL),
('Barbara', 'Pepe', 'barbara.pepe@email.com', '333 6789016', '2023-10-29', 'attivo', NULL),
('Vittorio', 'Cipriani', 'vittorio.cipriani@email.com', '333 7890127', '2023-11-12', 'attivo', NULL),
('Monica', 'Cortese', 'monica.cortese@email.com', '333 8901238', '2023-12-20', 'attivo', NULL),
('Carlo', 'Messina', 'carlo.messina@email.com', '333 9012349', '2024-01-15', 'attivo', NULL),
('Serena', 'D''Amico', 'serena.damico@email.com', '333 0123460', '2024-02-28', 'attivo', NULL);

-- ============================================
-- INSERIMENTO PRESTITI (Loans)
-- ============================================
INSERT INTO prestiti (libro_id, membro_id, data_prestito, data_scadenza, data_restituzione, stato, note) VALUES
-- Prestiti 2020 (restituiti)
(6, 1, '2020-01-20', '2020-02-20', '2020-02-15', 'restituito', NULL),
(28, 1, '2020-03-10', '2020-04-10', '2020-04-05', 'restituito', NULL),
(6, 2, '2020-04-15', '2020-05-15', '2020-05-20', 'restituito', 'Restituito con ritardo'),
(18, 3, '2020-06-01', '2020-07-01', '2020-06-28', 'restituito', NULL),
(20, 3, '2020-06-01', '2020-07-01', '2020-06-30', 'restituito', NULL),
(25, 4, '2020-07-10', '2020-08-10', '2020-08-05', 'restituito', NULL),
(26, 4, '2020-08-15', '2020-09-15', '2020-09-12', 'restituito', NULL),
(13, 5, '2020-09-20', '2020-10-20', '2020-10-18', 'restituito', NULL),
(1, 6, '2020-10-25', '2020-11-25', '2020-11-20', 'restituito', NULL),
(28, 7, '2020-11-05', '2020-12-05', '2020-12-03', 'restituito', NULL),

-- Prestiti 2021 (restituiti e in ritardo)
(8, 8, '2021-01-15', '2021-02-15', '2021-02-10', 'restituito', NULL),
(9, 8, '2021-02-20', '2021-03-20', '2021-03-25', 'restituito', 'Restituito con ritardo'),
(18, 9, '2021-03-10', '2021-04-10', '2021-04-15', 'restituito', 'Restituito con ritardo'),
(33, 10, '2021-04-05', '2021-05-05', '2021-05-01', 'restituito', NULL),
(25, 11, '2021-05-12', '2021-06-12', '2021-06-10', 'restituito', NULL),
(26, 11, '2021-06-18', '2021-07-18', '2021-07-20', 'restituito', 'Restituito con ritardo'),
(27, 11, '2021-07-25', '2021-08-25', '2021-08-22', 'restituito', NULL),
(6, 12, '2021-08-30', '2021-09-30', '2021-09-28', 'restituito', NULL),
(7, 12, '2021-10-10', '2021-11-10', '2021-11-05', 'restituito', NULL),
(15, 13, '2021-11-15', '2021-12-15', '2021-12-20', 'restituito', 'Restituito con ritardo'),

-- Prestiti 2022
(20, 14, '2022-01-20', '2022-02-20', '2022-02-18', 'restituito', NULL),
(21, 14, '2022-02-25', '2022-03-25', '2022-03-22', 'restituito', NULL),
(29, 15, '2022-03-10', '2022-04-10', '2022-04-08', 'restituito', NULL),
(30, 15, '2022-04-15', '2022-05-15', '2022-05-12', 'restituito', NULL),
(1, 16, '2022-05-20', '2022-06-20', '2022-06-18', 'restituito', NULL),
(2, 16, '2022-06-25', '2022-07-25', '2022-07-22', 'restituito', NULL),
(4, 17, '2022-07-30', '2022-08-30', '2022-08-27', 'restituito', NULL),
(5, 17, '2022-09-05', '2022-10-05', '2022-10-03', 'restituito', NULL),
(10, 18, '2022-10-12', '2022-11-12', '2022-11-10', 'restituito', NULL),
(11, 18, '2022-11-18', '2022-12-18', '2022-12-15', 'restituito', NULL),
(33, 19, '2022-12-20', '2023-01-20', '2023-01-18', 'restituito', NULL),

-- Prestiti 2023
(25, 20, '2023-01-25', '2023-02-25', '2023-02-22', 'restituito', NULL),
(26, 20, '2023-02-28', '2023-03-28', '2023-03-25', 'restituito', NULL),
(8, 21, '2023-03-15', '2023-04-15', '2023-04-20', 'restituito', 'Restituito con ritardo'),
(9, 21, '2023-04-20', '2023-05-20', '2023-05-18', 'restituito', NULL),
(18, 22, '2023-05-25', '2023-06-25', '2023-06-22', 'restituito', NULL),
(19, 22, '2023-06-30', '2023-07-30', '2023-07-28', 'restituito', NULL),
(13, 23, '2023-07-10', '2023-08-10', '2023-08-15', 'restituito', 'Restituito con ritardo'),
(14, 23, '2023-08-20', '2023-09-20', '2023-09-18', 'restituito', NULL),
(6, 24, '2023-09-25', '2023-10-25', '2023-10-22', 'restituito', NULL),
(28, 24, '2023-10-30', '2023-11-30', '2023-11-28', 'restituito', NULL),
(36, 25, '2023-11-05', '2023-12-05', '2023-12-03', 'restituito', NULL),
(37, 25, '2023-12-10', '2024-01-10', '2024-01-08', 'restituito', NULL),

-- Prestiti 2024 (alcuni restituiti, alcuni in corso)
(20, 26, '2024-01-15', '2024-02-15', '2024-02-12', 'restituito', NULL),
(21, 26, '2024-02-20', '2024-03-20', '2024-03-18', 'restituito', NULL),
(1, 27, '2024-03-10', '2024-04-10', '2024-04-08', 'restituito', NULL),
(2, 27, '2024-04-15', '2024-05-15', '2024-05-12', 'restituito', NULL),
(3, 27, '2024-05-20', '2024-06-20', '2024-06-18', 'restituito', NULL),
(15, 28, '2024-06-25', '2024-07-25', NULL, 'in_corso', NULL),
(16, 28, '2024-07-01', '2024-08-01', NULL, 'in_corso', NULL),
(33, 29, '2024-07-10', '2024-08-10', '2024-08-15', 'restituito', 'Restituito con ritardo'),
(34, 29, '2024-08-20', '2024-09-20', NULL, 'in_corso', NULL),
(25, 30, '2024-09-05', '2024-10-05', NULL, 'in_corso', NULL),
(26, 30, '2024-09-12', '2024-10-12', NULL, 'in_corso', NULL),
(4, 31, '2024-09-25', '2024-10-25', NULL, 'in_corso', NULL),
(5, 31, '2024-10-01', '2024-11-01', NULL, 'in_ritardo', 'Non restituito in tempo'),
(18, 32, '2024-10-10', '2024-11-10', NULL, 'in_corso', NULL),
(19, 32, '2024-10-15', '2024-11-15', NULL, 'in_corso', NULL),
(8, 33, '2024-10-20', '2024-11-20', NULL, 'in_corso', NULL),
(9, 33, '2024-10-25', '2024-11-25', NULL, 'in_corso', NULL),
(6, 34, '2024-11-01', '2024-12-01', NULL, 'in_corso', NULL),
(28, 34, '2024-11-05', '2024-12-05', NULL, 'in_corso', NULL),
(10, 35, '2024-11-10', '2024-12-10', NULL, 'in_corso', NULL),
(11, 35, '2024-11-15', '2024-12-15', NULL, 'in_corso', NULL),
(13, 36, '2024-11-20', '2024-12-20', NULL, 'in_corso', NULL),
(14, 36, '2024-11-25', '2024-12-25', NULL, 'in_corso', NULL),
(20, 37, '2024-12-01', '2025-01-01', NULL, 'in_corso', NULL),
(21, 37, '2024-12-05', '2025-01-05', NULL, 'in_corso', NULL),
(33, 38, '2024-12-10', '2025-01-10', NULL, 'in_corso', NULL),
(39, 38, '2024-12-15', '2025-01-15', NULL, 'in_corso', NULL),

-- Prestiti con problemi
(7, 28, '2024-08-10', '2024-09-10', NULL, 'in_ritardo', 'Prestito molto in ritardo'),
(27, 30, '2024-07-15', '2024-08-15', NULL, 'in_ritardo', 'Giorni di ritardo significativi'),
(31, 34, '2024-09-15', '2024-10-15', NULL, 'in_ritardo', 'Seconda copia in ritardo'),
(40, 28, '2024-09-01', '2024-10-01', NULL, 'in_ritardo', 'Ritardo nella restituzione'),
(41, 30, '2024-08-25', '2024-09-25', NULL, 'in_ritardo', NULL),

-- Prestiti recentissimi (dicembre 2024)
(1, 39, '2024-12-01', '2025-01-01', NULL, 'in_corso', NULL),
(2, 39, '2024-12-05', '2025-01-05', NULL, 'in_corso', NULL),
(29, 40, '2024-12-10', '2025-01-10', NULL, 'in_corso', NULL),
(30, 40, '2024-12-12', '2025-01-12', NULL, 'in_corso', NULL),
(15, 41, '2024-12-15', '2025-01-15', NULL, 'in_corso', NULL),
(16, 41, '2024-12-18', '2025-01-18', NULL, 'in_corso', NULL),
(4, 42, '2024-12-20', '2025-01-20', NULL, 'in_corso', NULL),
(5, 42, '2024-12-22', '2025-01-22', NULL, 'in_corso', NULL),
(18, 43, '2024-12-25', '2025-01-25', NULL, 'in_corso', NULL),
(43, 44, '2024-12-28', '2025-01-28', NULL, 'in_corso', NULL),
(8, 45, '2024-12-30', '2025-01-30', NULL, 'in_corso', NULL),
(9, 45, '2025-01-05', '2025-02-05', NULL, 'in_corso', NULL),
(33, 46, '2025-01-08', '2025-02-08', NULL, 'in_corso', NULL),
(34, 46, '2025-01-10', '2025-02-10', NULL, 'in_corso', NULL),
(25, 47, '2025-01-12', '2025-02-12', NULL, 'in_corso', NULL),
(26, 48, '2025-01-15', '2025-02-15', NULL, 'in_corso', NULL),
(28, 49, '2025-01-18', '2025-02-18', NULL, 'in_corso', NULL),
(6, 50, '2025-01-20', '2025-02-20', NULL, 'in_corso', NULL),
(20, 50, '2025-01-22', '2025-02-22', NULL, 'in_corso', NULL);

-- ============================================
-- AGGIORNAMENTO COPIE DISPONIBILI
-- ============================================
-- Aggiorna le copie disponibili in base ai prestiti attivi
UPDATE libri SET copie_disponibili = copie_totali - (
    SELECT COUNT(*)
    FROM prestiti
    WHERE libro_id = libri.id
    AND stato IN ('in_corso', 'in_ritardo')
);

-- ============================================
-- FINE DATI DI ESEMPIO
-- ============================================