-- ============================================
-- BIBLIOTECA - SCHEMA DEL DATABASE
-- Library Management System Database Schema
-- ============================================

-- Eliminazione delle tabelle se esistono (in ordine di dipendenza)
DROP TABLE IF EXISTS prestiti CASCADE;
DROP TABLE IF EXISTS libri_autori CASCADE;
DROP TABLE IF EXISTS libri CASCADE;
DROP TABLE IF EXISTS autori CASCADE;
DROP TABLE IF EXISTS categorie CASCADE;
DROP TABLE IF EXISTS editori CASCADE;
DROP TABLE IF EXISTS membri CASCADE;

-- ============================================
-- TABELLA: EDITORI (Publishers)
-- ============================================
CREATE TABLE editori (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    indirizzo VARCHAR(255),
    telefono VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE editori IS 'Tabella delle case editrici che pubblicano i libri';
COMMENT ON COLUMN editori.id IS 'Identificativo univoco dell''editore';
COMMENT ON COLUMN editori.nome IS 'Nome della casa editrice';
COMMENT ON COLUMN editori.indirizzo IS 'Indirizzo fisico dell''editore';
COMMENT ON COLUMN editori.telefono IS 'Numero di telefono di contatto';
COMMENT ON COLUMN editori.email IS 'Email di contatto';

-- Indice per ricerca rapida per nome
CREATE INDEX idx_editori_nome ON editori(nome);

-- ============================================
-- TABELLA: CATEGORIE (Categories)
-- ============================================
CREATE TABLE categorie (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descrizione TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE categorie IS 'Tabella delle categorie/geni letterari dei libri';
COMMENT ON COLUMN categorie.id IS 'Identificativo univoco della categoria';
COMMENT ON COLUMN categorie.nome IS 'Nome della categoria (es. Romanzo, Thriller, etc.)';
COMMENT ON COLUMN categorie.descrizione IS 'Descrizione dettagliata della categoria';

-- Indice per ricerca rapida
CREATE INDEX idx_categorie_nome ON categorie(nome);

-- ============================================
-- TABELLA: AUTORI (Authors)
-- ============================================
CREATE TABLE autori (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    anno_nascita INTEGER,
    anno_morte INTEGER,
    biografia TEXT,
    nazionalita VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_anni CHECK (anno_morte IS NULL OR anno_morte >= anno_nascita)
);

COMMENT ON TABLE autori IS 'Tabella degli autori dei libri';
COMMENT ON COLUMN autori.id IS 'Identificativo univoco dell''autore';
COMMENT ON COLUMN autori.nome IS 'Nome completo dell''autore';
COMMENT ON COLUMN autori.anno_nascita IS 'Anno di nascita dell''autore';
COMMENT ON COLUMN autori.anno_morte IS 'Anno di morte (NULL se ancora in vita)';
COMMENT ON COLUMN autori.biografia IS 'Biografia breve dell''autore';
COMMENT ON COLUMN autori.nazionalita IS 'Nazionalità dell''autore';

-- Indici per ricerche comuni
CREATE INDEX idx_autori_nome ON autori(nome);
CREATE INDEX idx_autori_nazionalita ON autori(nazionalita);

-- ============================================
-- TABELLA: MEMBRI (Members)
-- ============================================
CREATE TABLE membri (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    data_iscrizione DATE NOT NULL DEFAULT CURRENT_DATE,
    stato VARCHAR(20) NOT NULL DEFAULT 'attivo'
        CHECK (stato IN ('attivo', 'sospeso', 'inattivo')),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

COMMENT ON TABLE membri IS 'Tabella dei membri registrati alla biblioteca';
COMMENT ON COLUMN membri.id IS 'Identificativo univoco del membro';
COMMENT ON COLUMN membri.nome IS 'Nome del membro';
COMMENT ON COLUMN membri.cognome IS 'Cognome del membro';
COMMENT ON COLUMN membri.email IS 'Email univoca del membro';
COMMENT ON COLUMN membri.telefono IS 'Numero di telefono';
COMMENT ON COLUMN membri.data_iscrizione IS 'Data di iscrizione alla biblioteca';
COMMENT ON COLUMN membri.stato IS 'Stato del membro: attivo, sospeso, inattivo';
COMMENT ON COLUMN membri.note IS 'Note aggiuntive sul membro';

-- Indici per ricerche comuni
CREATE INDEX idx_membri_cognome ON membri(cognome);
CREATE INDEX idx_membri_email ON membri(email);
CREATE INDEX idx_membri_stato ON membri(stato);
CREATE INDEX idx_membri_nome_completo ON membri(nome, cognome);

-- ============================================
-- TABELLA: LIBRI (Books)
-- ============================================
CREATE TABLE libri (
    id SERIAL PRIMARY KEY,
    titolo VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    anno_pubblicazione INTEGER NOT NULL,
    editore_id INTEGER NOT NULL REFERENCES editori(id) ON DELETE RESTRICT,
    categoria_id INTEGER NOT NULL REFERENCES categorie(id) ON DELETE RESTRICT,
    copie_totali INTEGER NOT NULL DEFAULT 1 CHECK (copie_totali >= 0),
    copie_disponibili INTEGER NOT NULL DEFAULT 1 CHECK (copie_disponibili >= 0),
    descrizione TEXT,
    lingua VARCHAR(20) DEFAULT 'Italiano',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_copie CHECK (copie_disponibili <= copie_totali),
    CONSTRAINT check_anno_pubblicazione CHECK (anno_pubblicazione >= 1000 AND anno_pubblicazione <= EXTRACT(YEAR FROM CURRENT_DATE) + 1)
);

COMMENT ON TABLE libri IS 'Tabella principale dei libri della biblioteca';
COMMENT ON COLUMN libri.id IS 'Identificativo univoco del libro';
COMMENT ON COLUMN libri.titolo IS 'Titolo del libro';
COMMENT ON COLUMN libri.isbn IS 'ISBN (International Standard Book Number)';
COMMENT ON COLUMN libri.anno_pubblicazione IS 'Anno di pubblicazione';
COMMENT ON COLUMN libri.editore_id IS 'Chiave esterna verso la tabella editori';
COMMENT ON COLUMN libri.categoria_id IS 'Chiave esterna verso la tabella categorie';
COMMENT ON COLUMN libri.copie_totali IS 'Numero totale di copie possedute';
COMMENT ON COLUMN libri.copie_disponibili IS 'Numero di copie attualmente disponibili';
COMMENT ON COLUMN libri.descrizione IS 'Descrizione o sinossi del libro';
COMMENT ON COLUMN libri.lingua IS 'Lingua del libro';

-- Indici per ricerche comuni
CREATE INDEX idx_libri_titolo ON libri(titolo);
CREATE INDEX idx_libri_isbn ON libri(isbn);
CREATE INDEX idx_libri_categoria ON libri(categoria_id);
CREATE INDEX idx_libri_editore ON libri(editore_id);
CREATE INDEX idx_libri_anno_pubblicazione ON libri(anno_pubblicazione);
CREATE INDEX idx_libri_disponibili ON libri(copie_disponibili) WHERE copie_disponibili > 0;

-- Full text search index
CREATE INDEX idx_libri_titolo_fts ON libri USING gin(to_tsvector('italian', titolo));

-- ============================================
-- TABELLA: LIBRI_AUTORI (Book_Authors)
-- Tabella di giunzione per relazione molti-a-molti
-- ============================================
CREATE TABLE libri_autori (
    libro_id INTEGER NOT NULL REFERENCES libri(id) ON DELETE CASCADE,
    autore_id INTEGER NOT NULL REFERENCES autori(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (libro_id, autore_id)
);

COMMENT ON TABLE libri_autori IS 'Tabella di giunzione per la relazione molti-a-molti tra libri e autori';
COMMENT ON COLUMN libri_autori.libro_id IS 'Chiave esterna verso la tabella libri';
COMMENT ON COLUMN libri_autori.autore_id IS 'Chiave esterna verso la tabella autori';

-- ============================================
-- TABELLA: PRESTITI (Loans)
-- ============================================
CREATE TABLE prestiti (
    id SERIAL PRIMARY KEY,
    libro_id INTEGER NOT NULL REFERENCES libri(id) ON DELETE RESTRICT,
    membro_id INTEGER NOT NULL REFERENCES membri(id) ON DELETE RESTRICT,
    data_prestito DATE NOT NULL DEFAULT CURRENT_DATE,
    data_scadenza DATE NOT NULL,
    data_restituzione DATE,
    stato VARCHAR(20) NOT NULL DEFAULT 'in_corso'
        CHECK (stato IN ('in_corso', 'restituito', 'in_ritardo', 'perduto')),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_date_restituzione CHECK (
        data_restituzione IS NULL OR data_restituzione >= data_prestito
    ),
    CONSTRAINT check_date_scadenza CHECK (
        data_scadenza >= data_prestito
    )
);

COMMENT ON TABLE prestiti IS 'Tabella che traccia tutti i prestiti dei libri';
COMMENT ON COLUMN prestiti.id IS 'Identificativo univoco del prestito';
COMMENT ON COLUMN prestiti.libro_id IS 'Chiave esterna verso la tabella libri';
COMMENT ON COLUMN prestiti.membro_id IS 'Chiave esterna verso la tabella membri';
COMMENT ON COLUMN prestiti.data_prestito IS 'Data in cui il libro è stato preso in prestito';
COMMENT ON COLUMN prestiti.data_scadenza IS 'Data in cui il libro deve essere restituito';
COMMENT ON COLUMN prestiti.data_restituzione IS 'Data effettiva di restituzione (NULL se non ancora restituito)';
COMMENT ON COLUMN prestiti.stato IS 'Stato del prestito: in_corso, restituito, in_ritardo, perso';
COMMENT ON COLUMN prestiti.note IS 'Note aggiuntive sul prestito';

-- Indici per ricerche comuni
CREATE INDEX idx_prestiti_libro ON prestiti(libro_id);
CREATE INDEX idx_prestiti_membro ON prestiti(membro_id);
CREATE INDEX idx_prestiti_stato ON prestiti(stato);
CREATE INDEX idx_prestiti_data_prestito ON prestiti(data_prestito);
CREATE INDEX idx_prestiti_data_scadenza ON prestiti(data_scadenza);
CREATE INDEX idx_prestiti_data_restituzione ON prestiti(data_restituzione);
CREATE INDEX idx_prestiti_correnti ON prestiti(membro_id, stato) WHERE stato IN ('in_corso', 'in_ritardo');

-- ============================================
-- FUNZIONI E TRIGGER
-- ============================================

-- Funzione per aggiornare lo stato dei prestiti in ritardo
CREATE OR REPLACE FUNCTION aggiorna_stato_prestiti()
RETURNS VOID AS $$
BEGIN
    UPDATE prestiti
    SET stato = 'in_ritardo'
    WHERE stato = 'in_corso'
    AND data_scadenza < CURRENT_DATE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION aggiorna_stato_prestiti() IS 'Aggiorna automaticamente lo stato dei prestiti in ritardo';

-- Trigger per eseguire l'aggiornamento giornaliero
-- CREATE TRIGGER trigger_aggiorna_prestiti
-- AFTER INSERT ON prestiti
-- FOR EACH ROW
-- EXECUTE FUNCTION aggiorna_stato_prestiti();

-- ============================================
-- VISTE UTILI (Useful Views)
-- ============================================

-- Vista: Libri con dettagli completi
CREATE OR REPLACE VIEW vista_libri_dettagli AS
SELECT
    l.id AS libro_id,
    l.titolo,
    l.isbn,
    l.anno_pubblicazione,
    l.copie_totali,
    l.copie_disponibili,
    e.nome AS editore,
    c.nome AS categoria,
    STRING_AGG(a.nome, ', ') AS autori
FROM libri l
JOIN editori e ON l.editore_id = e.id
JOIN categorie c ON l.categoria_id = c.id
LEFT JOIN libri_autori la ON l.id = la.libro_id
LEFT JOIN autori a ON la.autore_id = a.id
GROUP BY l.id, l.titolo, l.isbn, l.anno_pubblicazione, l.copie_totali, l.copie_disponibili, e.nome, c.nome;

COMMENT ON VIEW vista_libri_dettagli IS 'Vista che mostra tutti i dettagli dei libri inclusi gli autori';

-- Vista: Prestiti attuali
CREATE OR REPLACE VIEW vista_prestiti_attuali AS
SELECT
    p.id AS prestito_id,
    l.titolo,
    m.nome AS membro_nome,
    m.cognome AS membro_cognome,
    p.data_prestito,
    p.data_scadenza,
    CASE
        WHEN p.data_scadenza < CURRENT_DATE THEN 'IN RITARDO'
        ELSE 'In corso'
    END AS stato_prestito,
    CURRENT_DATE - p.data_scadenza AS giorni_ritardo
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.stato IN ('in_corso', 'in_ritardo')
ORDER BY p.data_scadenza ASC;

COMMENT ON VIEW vista_prestiti_attuali IS 'Vista che mostra tutti i prestiti attualmente in corso';

-- Vista: Statistiche categorie
CREATE OR REPLACE VIEW vista_statistiche_categorie AS
SELECT
    c.id AS categoria_id,
    c.nome AS categoria,
    COUNT(DISTINCT l.id) AS num_libri,
    SUM(l.copie_totali) AS tot_copie,
    SUM(l.copie_disponibili) AS copie_disponibili,
    ROUND(AVG(l.anno_pubblicazione), 0) AS anno_medio_pubblicazione
FROM categorie c
LEFT JOIN libri l ON c.id = l.categoria_id
GROUP BY c.id, c.nome
ORDER BY num_libri DESC;

COMMENT ON VIEW vista_statistiche_categorie IS 'Statistiche aggregate per categoria';

-- ============================================
-- FINE DELLO SCHEMA
-- ============================================