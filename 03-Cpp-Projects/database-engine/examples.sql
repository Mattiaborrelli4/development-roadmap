-- Esempi di SQL per il Database Engine
-- Puoi copiare e incollare questi comandi nel menu interattivo

-- ============================================
-- ESEMPIO 1: Gestione Dipendenti
-- ============================================

-- Crea tabella dipendenti
CREATE TABLE dipendenti (id, nome, ruolo, stipendio)

-- Inserisci dipendenti
INSERT INTO dipendenti (1, Mario Rossi, Sviluppatore, 50000)
INSERT INTO dipendenti (2, Luigi Verdi, Designer, 45000)
INSERT INTO dipendenti (3, Anna Bianchi, Project Manager, 60000)
INSERT INTO dipendenti (4, Paolo Neri, Sviluppatore, 55000)
INSERT INTO dipendenti (5, Laura Gialli, QA Engineer, 42000)

-- Visualizza tutti
SELECT * FROM dipendenti

-- Trova sviluppatori
SELECT * FROM dipendenti WHERE ruolo == Sviluppatore

-- Trova chi guadagna più di 50000
SELECT * FROM dipendenti WHERE stipendio > 50000

-- Aggiorna stipendio
UPDATE dipendenti SET stipendio = 58000 WHERE id == 2

-- Verifica aggiornamento
SELECT * FROM dipendenti WHERE id == 2

-- Elimina un dipendente
DELETE FROM dipendenti WHERE id == 5

-- Verifica eliminazione
SELECT * FROM dipendenti

-- ============================================
-- ESEMPIO 2: Gestione Studenti
-- ============================================

-- Crea tabella studenti
CREATE TABLE studenti (matricola, nome, corso, media_voti)

-- Inserisci studenti
INSERT INTO studenti (1001, Marco Ferrari, Informatica, 28)
INSERT INTO studenti (1002, Giulia Esposito, Matematica, 30)
INSERT INTO studenti (1003, Andrea Romano, Fisica, 27)
INSERT INTO studenti (1004, Sara Conti, Informatica, 29)

-- Visualizza tutti
SELECT * FROM studenti

-- Trova studenti di Informatica
SELECT * FROM studenti WHERE corso == Informatica

-- Trova studenti con media >= 28
SELECT * FROM studenti WHERE media_voti >= 28

-- Aggiorna media
UPDATE studenti SET media_voti = 29 WHERE matricola == 1003

-- Elimina studente
DELETE FROM studenti WHERE matricola == 1004

-- ============================================
-- ESEMPIO 3: Gestione Prodotti
-- ============================================

-- Crea tabella prodotti
CREATE TABLE prodotti (codice, nome, prezzo, quantita)

-- Inserisci prodotti
INSERT INTO prodotti (101, Laptop, 1200, 50)
INSERT INTO prodotti (102, Mouse, 25, 200)
INSERT INTO prodotti (103, Tastiera, 45, 150)
INSERT INTO prodotti (104, Monitor, 350, 80)

-- Visualizza tutti
SELECT * FROM prodotti

-- Trova prodotti con prezzo < 100
SELECT * FROM prodotti WHERE prezzo < 100

-- Aggiorna quantità
UPDATE prodotti SET quantita = 180 WHERE codice == 102

-- Elimina prodotto
DELETE FROM prodotti WHERE codice == 104

-- ============================================
-- ESEMPIO 4: Test B-tree Split
-- ============================================

-- Crea tabella per test split
CREATE TABLE test_split (id, valore)

-- Inserisci molti valori per testare split
INSERT INTO test_split (1, a)
INSERT INTO test_split (2, b)
INSERT INTO test_split (3, c)
INSERT INTO test_split (4, d)
INSERT INTO test_split (5, e)
INSERT INTO test_split (6, f)
INSERT INTO test_split (7, g)
INSERT INTO test_split (8, h)
INSERT INTO test_split (9, i)
INSERT INTO test_split (10, j)

-- Visualizza struttura B-tree dal menu (opzione 6)
SELECT * FROM test_split

-- ============================================
-- TEST QUERY COMPLESSE
-- ============================================

-- Query di unione implicita (più INSERT + SELECT)
CREATE TABLE temp (id, valore)
INSERT INTO temp (1, test1)
INSERT INTO temp (2, test2)
SELECT * FROM temp

-- Test update condizionale
UPDATE temp SET valore = updated WHERE id == 1
SELECT * FROM temp

-- Test delete condizionale
DELETE FROM temp WHERE id == 2
SELECT * FROM temp
