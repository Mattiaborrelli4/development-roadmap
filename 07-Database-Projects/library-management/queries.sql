-- ============================================
-- BIBLIOTECA - QUERY DI ESEMPIO
-- Library Management System - Example Queries
-- ============================================

-- ============================================
-- 1. QUERY SEMPLICI CON SELECT E WHERE
-- ============================================

-- 1.1 Elenca tutti i libri disponibili (con copie disponibili > 0)
SELECT
    id,
    titolo,
    isbn,
    copie_totali,
    copie_disponibili
FROM libri
WHERE copie_disponibili > 0
ORDER BY titolo ASC;

-- 1.2 Trova tutti i libri di una specifica categoria (es. Thriller)
SELECT
    l.titolo,
    l.anno_pubblicazione,
    c.nome AS categoria,
    l.copie_disponibili
FROM libri l
JOIN categorie c ON l.categoria_id = c.id
WHERE c.nome = 'Thriller'
ORDER BY l.titolo;

-- 1.3 Trova membri con stato attivo
SELECT
    id,
    nome,
    cognome,
    email,
    data_iscrizione
FROM membri
WHERE stato = 'attivo'
ORDER BY cognome, nome;

-- 1.4 Trova libri pubblicati dopo il 2000
SELECT
    titolo,
    anno_pubblicazione,
    copie_disponibili
FROM libri
WHERE anno_pubblicazione > 2000
ORDER BY anno_pubblicazione DESC;

-- 1.5 Trova prestiti in ritardo
SELECT
    p.id AS prestito_id,
    l.titolo,
    m.nome AS membro_nome,
    m.cognome AS membro_cognome,
    p.data_prestito,
    p.data_scadenza,
    CURRENT_DATE - p.data_scadenza AS giorni_ritardo
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.stato = 'in_ritardo'
ORDER BY p.data_scadenza ASC;

-- ============================================
-- 2. JOIN (INNER, LEFT, RIGHT)
-- ============================================

-- 2.1 INNER JOIN: Libri con i loro autori
SELECT
    l.titolo,
    l.anno_pubblicazione,
    a.nome AS autore
FROM libri l
INNER JOIN libri_autori la ON l.id = la.libro_id
INNER JOIN autori a ON la.autore_id = a.id
ORDER BY l.titolo, a.nome;

-- 2.2 LEFT JOIN: Tutti i libri con le loro categorie (anche senza categoria)
SELECT
    l.titolo,
    c.nome AS categoria,
    l.copie_disponibili
FROM libri l
LEFT JOIN categorie c ON l.categoria_id = c.id
ORDER BY c.nome, l.titolo;

-- 2.3 LEFT JOIN: Tutti i membri e i loro prestiti (anche membri senza prestiti)
SELECT
    m.nome,
    m.cognome,
    m.email,
    COUNT(p.id) AS num_prestiti
FROM membri m
LEFT JOIN prestiti p ON m.id = p.membro_id
GROUP BY m.id, m.nome, m.cognome, m.email
ORDER BY num_prestiti DESC;

-- 2.4 LEFT JOIN: Libri senza autori (caso edge)
SELECT
    l.titolo,
    l.isbn
FROM libri l
LEFT JOIN libri_autori la ON l.id = la.libro_id
WHERE la.libro_id IS NULL;

-- 2.5 Multiple JOINs: Vista completa prestiti
SELECT
    p.id AS prestito_id,
    l.titolo,
    m.nome AS membro_nome,
    m.cognome AS membro_cognome,
    p.data_prestito,
    p.data_scadenza,
    p.data_restituzione,
    p.stato
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.stato IN ('in_corso', 'in_ritardo')
ORDER BY p.data_scadenza ASC;

-- ============================================
-- 3. FUNZIONI DI AGGREGAZIONE (COUNT, SUM, AVG, MAX, MIN)
-- ============================================

-- 3.1 COUNT: Conta il numero di libri per categoria
SELECT
    c.nome AS categoria,
    COUNT(l.id) AS numero_libri
FROM categorie c
LEFT JOIN libri l ON c.id = l.categoria_id
GROUP BY c.nome
ORDER BY numero_libri DESC;

-- 3.2 COUNT: Conta quanti autori ha scritto ogni libro
SELECT
    l.titolo,
    COUNT(a.id) AS numero_autori
FROM libri l
LEFT JOIN libri_autori la ON l.id = la.libro_id
LEFT JOIN autori a ON la.autore_id = a.id
GROUP BY l.id, l.titolo
HAVING COUNT(a.id) > 1
ORDER BY numero_autori DESC;

-- 3.3 SUM: Somma delle copie totali e disponibili per categoria
SELECT
    c.nome AS categoria,
    SUM(l.copie_totali) AS totale_copie,
    SUM(l.copie_disponibili) AS copie_disponibili,
    SUM(l.copie_totali) - SUM(l.copie_disponibili) AS copie_in_prestito
FROM categorie c
JOIN libri l ON c.id = l.categoria_id
GROUP BY c.nome
ORDER BY totale_copie DESC;

-- 3.4 AVG: Anno medio di pubblicazione per categoria
SELECT
    c.nome AS categoria,
    ROUND(AVG(l.anno_pubblicazione), 0) AS anno_medio_pubblicazione,
    COUNT(l.id) AS numero_libri
FROM categorie c
JOIN libri l ON c.id = l.categoria_id
GROUP BY c.nome
ORDER BY anno_medio_pubblicazione DESC;

-- 3.5 MAX, MIN: Anno più vecchio e più recente dei libri
SELECT
    MIN(anno_pubblicazione) AS libro_piu_antico,
    MAX(anno_pubblicazione) AS libro_piu_recente,
    COUNT(*) AS totale_libri
FROM libri;

-- 3.6 MAX, MIN per categoria
SELECT
    c.nome AS categoria,
    MIN(l.anno_pubblicazione) AS primo_anno,
    MAX(l.anno_pubblicazione) AS ultimo_anno,
    COUNT(l.id) AS num_libri
FROM categorie c
JOIN libri l ON c.id = l.categoria_id
GROUP BY c.nome
ORDER BY c.nome;

-- ============================================
-- 4. GROUP BY e HAVING
-- ============================================

-- 4.1 GROUP BY: Numero di libri per editore
SELECT
    e.nome AS editore,
    COUNT(l.id) AS numero_libri
FROM editori e
LEFT JOIN libri l ON e.id = l.editore_id
GROUP BY e.id, e.nome
ORDER BY numero_libri DESC;

-- 4.2 GROUP BY: Numero di prestiti per membro (solo membri attivi)
SELECT
    m.nome,
    m.cognome,
    COUNT(p.id) AS numero_prestiti
FROM membri m
JOIN prestiti p ON m.id = p.membro_id
WHERE m.stato = 'attivo'
GROUP BY m.id, m.nome, m.cognome
ORDER BY numero_prestiti DESC;

-- 4.3 GROUP BY con HAVING: Membri con più di 3 prestiti totali
SELECT
    m.nome,
    m.cognome,
    m.email,
    COUNT(p.id) AS numero_prestiti
FROM membri m
JOIN prestiti p ON m.id = p.membro_id
GROUP BY m.id, m.nome, m.cognome, m.email
HAVING COUNT(p.id) > 3
ORDER BY numero_prestiti DESC;

-- 4.4 HAVING: Categorie con più di 5 libri
SELECT
    c.nome AS categoria,
    COUNT(l.id) AS numero_libri
FROM categorie c
JOIN libri l ON c.id = l.categoria_id
GROUP BY c.id, c.nome
HAVING COUNT(l.id) >= 5
ORDER BY numero_libri DESC;

-- 4.5 GROUP BY: Prestiti per stato
SELECT
    stato,
    COUNT(*) AS numero_prestiti,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM prestiti), 2) AS percentuale
FROM prestiti
GROUP BY stato
ORDER BY numero_prestiti DESC;

-- 4.6 GROUP BY con MONTH: Prestiti per mese (ultimo anno)
SELECT
    EXTRACT(MONTH FROM data_prestito) AS mese,
    EXTRACT(YEAR FROM data_prestito) AS anno,
    COUNT(*) AS numero_prestiti
FROM prestiti
WHERE EXTRACT(YEAR FROM data_prestito) = 2024
GROUP BY EXTRACT(MONTH FROM data_prestito), EXTRACT(YEAR FROM data_prestito)
ORDER BY mese;

-- ============================================
-- 5. SUBQUERY (SOTTOPERCHIERE)
-- ============================================

-- 5.1 Subquery: Libri con più prestiti della media
SELECT
    l.titolo,
    COUNT(p.id) AS numero_prestiti
FROM libri l
JOIN prestiti p ON l.id = p.libro_id
GROUP BY l.id, l.titolo
HAVING COUNT(p.id) > (
    SELECT AVG(num_prestiti)
    FROM (
        SELECT COUNT(*) AS num_prestiti
        FROM prestiti
        GROUP BY libro_id
    ) AS subquery
)
ORDER BY numero_prestiti DESC;

-- 5.2 Subquery: Membri che hanno preso in prestito più di 5 libri
SELECT
    nome,
    cognome,
    email
FROM membri
WHERE id IN (
    SELECT membro_id
    FROM prestiti
    GROUP BY membro_id
    HAVING COUNT(*) >= 5
)
ORDER BY cognome, nome;

-- 5.3 Subquery: Libri mai presi in prestito
SELECT
    titolo,
    isbn,
    anno_pubblicazione
FROM libri
WHERE id NOT IN (
    SELECT DISTINCT libro_id
    FROM prestiti
)
ORDER BY titolo;

-- 5.4 Subquery correlata: Ultimo prestito di ogni libro
SELECT
    l.titolo,
    p.data_prestito,
    p.stato
FROM libri l
JOIN prestiti p ON l.id = p.libro_id
WHERE p.data_prestito = (
    SELECT MAX(data_prestito)
    FROM prestiti
    WHERE libro_id = l.id
)
ORDER BY p.data_prestito DESC;

-- 5.5 Subquery: Libri con copie totali superiori alla media
SELECT
    titolo,
    copie_totali,
    copie_disponibili,
    (
        SELECT ROUND(AVG(copie_totali))
        FROM libri
    ) AS media_copie_totali
FROM libri
WHERE copie_totali > (
    SELECT AVG(copie_totali)
    FROM libri
)
ORDER BY copie_totali DESC;

-- ============================================
-- 6. FUNZIONI DI DATA (Date Functions)
-- ============================================

-- 6.1 Libri da restituire questa settimana (prossimi 7 giorni)
SELECT
    l.titolo,
    m.nome AS membro_nome,
    m.cognome AS membro_cognome,
    p.data_scadenza,
    p.data_scadenza - CURRENT_DATE AS giorni_mancanti
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.data_scadenza BETWEEN CURRENT_DATE AND CURRENT_DATE + 7
    AND p.stato IN ('in_corso', 'in_ritardo')
ORDER BY p.data_scadenza ASC;

-- 6.2 Prestiti scaduti da più di 30 giorni
SELECT
    l.titolo,
    m.nome AS membro_nome,
    m.cognome AS membro_cognome,
    p.data_scadenza,
    CURRENT_DATE - p.data_scadenza AS giorni_ritardo,
    m.telefono
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.stato = 'in_ritardo'
    AND CURRENT_DATE - p.data_scadenza > 30
ORDER BY giorni_ritardo DESC;

-- 6.3 Prestiti effettuati nell''ultimo mese
SELECT
    l.titolo,
    m.nome AS membro_nome,
    m.cognome AS membro_cognome,
    p.data_prestito
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.data_prestito >= CURRENT_DATE - INTERVAL '1 month'
ORDER BY p.data_prestito DESC;

-- 6.4 Membri iscritti nell''ultimo anno
SELECT
    nome,
    cognome,
    email,
    data_iscrizione,
    CURRENT_DATE - data_iscrizione AS giorni_da_iscrizione
FROM membri
WHERE data_iscrizione >= CURRENT_DATE - INTERVAL '1 year'
ORDER BY data_iscrizione DESC;

-- 6.5 Prestiti per anno con statistiche
SELECT
    EXTRACT(YEAR FROM data_prestito) AS anno,
    COUNT(*) AS numero_prestiti,
    COUNT(*) FILTER (WHERE stato = 'restituito') AS restituiti,
    COUNT(*) FILTER (WHERE stato IN ('in_corso', 'in_ritardo')) AS attivi,
    COUNT(*) FILTER (WHERE stato = 'in_ritardo') AS in_ritardo
FROM prestiti
GROUP BY EXTRACT(YEAR FROM data_prestito)
ORDER BY anno DESC;

-- 6.6 Tempo medio di prestito per libro (in giorni)
SELECT
    l.titolo,
    COUNT(p.id) AS numero_prestiti,
    ROUND(AVG(p.data_restituzione - p.data_prestito), 1) AS giorni_medi_prestito
FROM libri l
JOIN prestiti p ON l.id = p.libro_id
WHERE p.data_restituzione IS NOT NULL
GROUP BY l.id, l.titolo
HAVING COUNT(p.id) >= 3
ORDER BY giorni_medi_prestito DESC;

-- ============================================
-- 7. QUERY AVANZATE
-- ============================================

-- 7.1 RANK: Libri più popolari (più prestati)
SELECT
    l.titolo,
    COUNT(p.id) AS numero_prestiti,
    RANK() OVER (ORDER BY COUNT(p.id) DESC) AS classifica
FROM libri l
JOIN prestiti p ON l.id = p.libro_id
GROUP BY l.id, l.titolo
ORDER BY numero_prestiti DESC
LIMIT 10;

-- 7.2 DENSE_RANK: Top 10 membri per numero di prestiti
WITH ranking_membri AS (
    SELECT
        m.nome,
        m.cognome,
        COUNT(p.id) AS numero_prestiti,
        DENSE_RANK() OVER (ORDER BY COUNT(p.id) DESC) AS posizione
    FROM membri m
    JOIN prestiti p ON m.id = p.membro_id
    GROUP BY m.id, m.nome, m.cognome
)
SELECT *
FROM ranking_membri
WHERE posizione <= 10
ORDER BY posizione;

-- 7.3 CTE: Membri con prestiti attivi e dettagli
WITH membri_con_prestiti AS (
    SELECT
        m.id,
        m.nome,
        m.cognome,
        m.email,
        COUNT(p.id) AS num_prestiti_attivi
    FROM membri m
    JOIN prestiti p ON m.id = p.membro_id
    WHERE p.stato IN ('in_corso', 'in_ritardo')
    GROUP BY m.id, m.nome, m.cognome, m.email
)
SELECT *
FROM membri_con_prestiti
WHERE num_prestiti_attivi > 0
ORDER BY num_prestiti_attivi DESC;

-- 7.4 CTE con JOIN: Libri con tutti i dettagli
WITH dettagli_autori AS (
    SELECT
        la.libro_id,
        STRING_AGG(a.nome, ', ') AS autori
    FROM libri_autori la
    JOIN autori a ON la.autore_id = a.id
    GROUP BY la.libro_id
)
SELECT
    l.titolo,
    l.isbn,
    l.anno_pubblicazione,
    e.nome AS editore,
    c.nome AS categoria,
    da.autori,
    l.copie_totali,
    l.copie_disponibili
FROM libri l
JOIN editori e ON l.editore_id = e.id
JOIN categorie c ON l.categoria_id = c.id
LEFT JOIN dettagli_autori da ON l.id = da.libro_id
ORDER BY l.titolo;

-- 7.5 WINDOW FUNCTION: Prestiti cumulativi per membro
SELECT
    m.nome,
    m.cognome,
    p.data_prestito,
    l.titolo,
    COUNT(*) OVER (
        PARTITION BY m.id
        ORDER BY p.data_prestito
    ) AS prestito_numero,
    p.stato
FROM membri m
JOIN prestiti p ON m.id = p.membro_id
JOIN libri l ON p.libro_id = l.id
WHERE m.id IN (1, 2, 3)
ORDER BY m.cognome, m.nome, p.data_prestito;

-- 7.6 CASE: Categorizzazione dei membri in base ai prestiti
SELECT
    m.nome,
    m.cognome,
    COUNT(p.id) AS numero_prestiti,
    CASE
        WHEN COUNT(p.id) = 0 THEN 'Nessun prestito'
        WHEN COUNT(p.id) BETWEEN 1 AND 3 THEN 'Lettore occasionale'
        WHEN COUNT(p.id) BETWEEN 4 AND 7 THEN 'Lettore regolare'
        WHEN COUNT(p.id) BETWEEN 8 AND 12 THEN 'Lettore assiduo'
        ELSE 'Grande lettore'
    END AS categoria_lettore
FROM membri m
LEFT JOIN prestiti p ON m.id = p.membro_id
GROUP BY m.id, m.nome, m.cognome
ORDER BY numero_prestiti DESC;

-- ============================================
-- 8. REPORTISTICHE
-- ============================================

-- 8.1 Report generale: Stato della biblioteca
SELECT
    'Totale Libri' AS metrica,
    COUNT(*) AS valore
FROM libri
UNION ALL
SELECT 'Totale Copie', SUM(copie_totali) FROM libri
UNION ALL
SELECT 'Copie Disponibili', SUM(copie_disponibili) FROM libri
UNION ALL
SELECT 'Copie in Prestito', SUM(copie_totali - copie_disponibili) FROM libri
UNION ALL
SELECT 'Totale Membri', COUNT(*) FROM membri
UNION ALL
SELECT 'Membri Attivi', COUNT(*) FROM membri WHERE stato = 'attivo'
UNION ALL
SELECT 'Totale Prestiti', COUNT(*) FROM prestiti
UNION ALL
SELECT 'Prestiti Attivi', COUNT(*) FROM prestiti WHERE stato IN ('in_corso', 'in_ritardo')
UNION ALL
SELECT 'Prestiti in Ritardo', COUNT(*) FROM prestiti WHERE stato = 'in_ritardo';

-- 8.2 Report: Libri più prestati con dettagli
SELECT
    l.titolo,
    l.isbn,
    e.nome AS editore,
    c.nome AS categoria,
    STRING_AGG(a.nome, ', ') AS autori,
    COUNT(p.id) AS numero_prestiti,
    l.copie_totali,
    ROUND(COUNT(p.id)::NUMERIC / l.copie_totali, 2) AS prestiti_per_copia
FROM libri l
JOIN editori e ON l.editore_id = e.id
JOIN categorie c ON l.categoria_id = c.id
LEFT JOIN libri_autori la ON l.id = la.libro_id
LEFT JOIN autori a ON la.autore_id = a.id
LEFT JOIN prestiti p ON l.id = p.libro_id
GROUP BY l.id, l.titolo, l.isbn, e.nome, c.nome, l.copie_totali
ORDER BY numero_prestiti DESC
LIMIT 10;

-- 8.3 Report: Prestiti per categoria (ultimo anno)
SELECT
    c.nome AS categoria,
    COUNT(p.id) AS numero_prestiti,
    COUNT(*) FILTER (WHERE p.stato = 'restituito') AS restituiti,
    COUNT(*) FILTER (WHERE p.stato IN ('in_corso', 'in_ritardo')) AS attivi,
    COUNT(*) FILTER (WHERE p.stato = 'in_ritardo') AS in_ritardo,
    ROUND(COUNT(*) FILTER (WHERE p.stato = 'in_ritardo')::NUMERIC / COUNT(p.id) * 100, 2) AS percentuale_ritardo
FROM categorie c
JOIN libri l ON c.id = l.categoria_id
JOIN prestiti p ON l.id = p.libro_id
WHERE EXTRACT(YEAR FROM p.data_prestito) = 2024
GROUP BY c.id, c.nome
ORDER BY numero_prestiti DESC;

-- 8.4 Report: Attività mensile della biblioteca
SELECT
    EXTRACT(YEAR FROM data_prestito) AS anno,
    EXTRACT(MONTH FROM data_prestito) AS mese,
    COUNT(*) AS nuovi_prestiti,
    COUNT(*) FILTER (WHERE stato = 'restituito' AND EXTRACT(MONTH FROM data_restituzione) = EXTRACT(MONTH FROM data_prestito)) AS restituiti_nello_stesso_mese,
    COUNT(DISTINCT membro_id) AS membri_attivi
FROM prestiti
WHERE EXTRACT(YEAR FROM data_prestito) >= 2023
GROUP BY EXTRACT(YEAR FROM data_prestito), EXTRACT(MONTH FROM data_prestito)
ORDER BY anno DESC, mese;

-- ============================================
-- FINE QUERY DI ESEMPIO
-- ============================================