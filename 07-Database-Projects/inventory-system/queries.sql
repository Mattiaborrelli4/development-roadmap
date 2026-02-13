-- ============================================
-- SISTEMA DI GESTIONE INVENTARIO
-- Query Avanzate
-- PostgreSQL
-- ============================================

-- ============================================
-- 1. PRODOTTI CON STOCK BASSO (Alert)
-- ============================================
-- Mostra tutti i prodotti che necessitano di essere riordinati
SELECT
    p.id,
    p.name AS prodotto,
    p.sku,
    p.current_stock AS stock_attuale,
    p.min_stock AS stock_minimo,
    p.reorder_point AS punto_riordino,
    c.name AS categoria,
    (p.reorder_point - p.current_stock) AS quantita_da_ordinare,
    ROUND((p.reorder_point - p.current_stock) * p.cost_price, 2) AS costo_stimato_riordino,
    s.name AS fornitore_preferred,
    s.email AS contatto_fornitore
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN suppliers s ON p.supplier_id = s.id
WHERE p.current_stock <= p.reorder_point
    AND p.is_active = TRUE
ORDER BY (p.reorder_point - p.current_stock) DESC;

-- ============================================
-- 2. VENDITE PER CATEGORIA (GROUP BY)
-- ============================================
-- Analisi delle vendite aggregate per categoria
SELECT
    c.name AS categoria,
    c.description,
    COUNT(DISTINCT si.sale_id) AS numero_vendite,
    SUM(si.quantity) AS totale_pezzi_venduti,
    SUM(si.subtotal) AS fatturato_totale,
    ROUND(AVG(si.subtotal), 2) AS valore_medio_vendita,
    ROUND(SUM(si.subtotal) * 100.0 / SUM(SUM(si.subtotal)) OVER (), 2) AS percentuale_fatturato
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'COMPLETED'
GROUP BY c.id, c.name, c.description
ORDER BY fatturato_totale DESC;

-- ============================================
-- 3. VENDITE MESE PER MESE (GROUP BY con DATE)
-- ============================================
-- Trend delle vendite mensili con confronto anno precedente
SELECT
    EXTRACT(YEAR FROM s.sale_date) AS anno,
    EXTRACT(MONTH FROM s.sale_date) AS mese,
    TO_CHAR(s.sale_date, 'TMmonth') AS nome_mese,
    COUNT(*) AS numero_vendite,
    ROUND(SUM(s.total_amount), 2) AS fatturato_totale,
    ROUND(AVG(s.total_amount), 2) AS valore_medio_ordine,
    COUNT(DISTINCT s.customer_name) AS clienti_unici,
    SUM(si.quantity) AS totale_pezzi_venduti
FROM sales s
JOIN sale_items si ON s.id = si.sale_id
WHERE s.status = 'COMPLETED'
    AND s.sale_date >= '2024-01-01'
GROUP BY EXTRACT(YEAR FROM s.sale_date),
         EXTRACT(MONTH FROM s.sale_date),
         TO_CHAR(s.sale_date, 'TMmonth')
ORDER BY anno DESC, mese DESC;

-- ============================================
-- 4. PERFORMANCE FORNITORI (GROUP BY + HAVING)
-- ============================================
-- Analisi dei fornitori con filtri con HAVING
SELECT
    s.id,
    s.name AS fornitore,
    s.contact_person,
    s.email,
    s.phone,
    COUNT(DISTINCT po.id) AS numero_ordini,
    ROUND(SUM(po.total_cost), 2) AS totale_acquisti,
    ROUND(AVG(po.total_cost), 2) AS valore_medio_ordini,
    COUNT(DISTINCT p.id) AS numero_prodotti_forniti,
    ROUND(AVG(po.total_cost / NULLIF((SELECT COUNT(*) FROM purchase_items WHERE order_id = po.id), 0)), 2) AS costo_medio_per_linea
FROM suppliers s
LEFT JOIN purchase_orders po ON s.id = po.supplier_id
LEFT JOIN purchase_items poi ON po.id = poi.order_id
LEFT JOIN products p ON poi.product_id = p.id
GROUP BY s.id, s.name, s.contact_person, s.email, s.phone
HAVING COUNT(DISTINCT po.id) >= 2  -- Solo fornitori con almeno 2 ordini
    AND SUM(po.total_cost) > 1000  -- Con volume acquisti > 1000
ORDER BY totale_acquisti DESC;

-- ============================================
-- 5. RENTABILITÀ PRODOTTI (Margin Analysis)
-- ============================================
-- Analisi di profitto e margin per prodotto
SELECT
    p.id,
    p.name AS prodotto,
    p.sku,
    c.name AS categoria,
    p.cost_price AS costo_acquisto,
    p.sell_price AS prezzo_vendita,
    ROUND(p.sell_price - p.cost_price, 2) AS profitto_unitario,
    ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2) AS margine_percentuale,
    COALESCE(SUM(si.quantity), 0) AS pezzi_venduti,
    ROUND(COALESCE(SUM(si.quantity), 0) * (p.sell_price - p.cost_price), 2) AS profitto_totale_generato,
    p.current_stock,
    s.name AS fornitore
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN suppliers s ON p.supplier_id = s.id
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales sl ON si.sale_id = sl.id AND sl.status = 'COMPLETED'
GROUP BY p.id, p.name, p.sku, c.name, p.cost_price, p.sell_price, p.current_stock, s.name
ORDER BY profitto_totale_generato DESC;

-- ============================================
-- 6. PRODOTTI CON ALTA ROTAZIONE (Top Selling)
-- ============================================
-- Prodotti più venduti con GROUP BY e HAVING
SELECT
    p.id,
    p.name AS prodotto,
    p.sku,
    c.name AS categoria,
    COUNT(DISTINCT si.sale_id) AS numero_vendite,
    SUM(si.quantity) AS totale_quantita_venduta,
    ROUND(SUM(si.subtotal), 2) AS fatturato_totale,
    ROUND(AVG(si.unit_price), 2) AS prezzo_medio_vendita,
    p.current_stock AS stock_attuale,
    p.min_stock AS stock_minimo
FROM products p
JOIN sale_items si ON p.id = si.product_id
JOIN sales s ON si.sale_id = s.id
JOIN categories c ON p.category_id = c.id
WHERE s.status = 'COMPLETED'
    AND s.sale_date >= '2024-01-01'
GROUP BY p.id, p.name, p.sku, c.name, p.current_stock, p.min_stock
HAVING SUM(si.quantity) >= 10  -- Almeno 10 pezzi venduti
ORDER BY totale_quantita_venduta DESC
LIMIT 20;

-- ============================================
-- 7. STORICO MOVIMENTI MAGAZZINO
-- ============================================
-- Analisi completa dei movimenti di stock
SELECT
    p.id,
    p.name AS prodotto,
    p.sku,
    sm.movement_type AS tipo_movimento,
    SUM(sm.quantity) AS quantita_totale,
    COUNT(*) AS numero_movimenti,
    MIN(sm.movement_date) AS primo_movimento,
    MAX(sm.movement_date) AS ultimo_movimento,
    ROUND(AVG(ABS(sm.quantity)), 2) AS media_quantita
FROM stock_movements sm
JOIN products p ON sm.product_id = p.id
WHERE sm.movement_date >= '2024-01-01'
GROUP BY p.id, p.name, p.sku, sm.movement_type
ORDER BY prodotto, sm.movement_type;

-- ============================================
-- 8. SUGGERIMENTI DI RIORDINO (Reorder Suggestions)
-- ============================================
-- Query complessa per suggerire cosa riordinare
WITH product_sales AS (
    SELECT
        p.id,
        p.name,
        p.current_stock,
        p.min_stock,
        p.reorder_point,
        p.cost_price,
        p.supplier_id,
        COALESCE(SUM(si.quantity), 0) AS vendite_ultimi_30_giorni
    FROM products p
    LEFT JOIN sale_items si ON p.id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.id
        AND s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - INTERVAL '30 days'
    WHERE p.is_active = TRUE
    GROUP BY p.id, p.name, p.current_stock, p.min_stock, p.reorder_point, p.cost_price, p.supplier_id
)
SELECT
    ps.name AS prodotto,
    ps.current_stock AS stock_attuale,
    ps.reorder_point AS punto_riordino,
    ps.vendite_ultimi_30_giorni AS vendite_30gg,
    GREATEST(
        (ps.reorder_point - ps.current_stock),
        CEIL(ps.vendite_ultimi_30_giorni / 30 * 30)  -- 30 giorni di stock
    ) AS quantita_suggerita,
    ROUND(GREATEST(
        (ps.reorder_point - ps.current_stock),
        CEIL(ps.vendite_ultimi_30_giorni / 30 * 30)
    ) * ps.cost_price, 2) AS costo_stimato,
    s.name AS fornitore,
    s.email AS contatto,
    s.phone AS telefono,
    CASE
        WHEN ps.current_stock <= 0 THEN 'URGENTE - Esaurito'
        WHEN ps.current_stock < ps.min_stock THEN 'URGENTE - Stock basso'
        WHEN ps.current_stock <= ps.reorder_point THEN 'CONSIGLIATO - Avvicinamento al riordino'
        ELSE 'OK'
    END AS priorita
FROM product_sales ps
JOIN suppliers s ON ps.supplier_id = s.id
WHERE ps.current_stock <= ps.reorder_point
    OR ps.vendite_ultimi_30_giorni > 0
ORDER BY
    CASE
        WHEN ps.current_stock <= 0 THEN 1
        WHEN ps.current_stock < ps.min_stock THEN 2
        WHEN ps.current_stock <= ps.reorder_point THEN 3
        ELSE 4
    END,
    (ps.reorder_point - ps.current_stock) DESC;

-- ============================================
-- 9. ANALISI VENDITE PER METODO DI PAGAMENTO
-- ============================================
-- Distribuzione delle vendite per metodo di pagamento
SELECT
    s.payment_method AS metodo_pagamento,
    COUNT(*) AS numero_transazioni,
    ROUND(SUM(s.total_amount), 2) AS fatturato_totale,
    ROUND(AVG(s.total_amount), 2) AS valore_medio_transazione,
    ROUND(SUM(s.total_amount) * 100.0 / SUM(SUM(s.total_amount)) OVER (), 2) AS percentuale_fatturato,
    COUNT(DISTINCT s.customer_name) AS clienti_unici
FROM sales s
WHERE s.status = 'COMPLETED'
    AND s.sale_date >= '2024-01-01'
GROUP BY s.payment_method
ORDER BY fatturato_totale DESC;

-- ============================================
-- 10. PRODOTTI CON OVERSTOCK (Eccesso di magazzino)
-- ============================================
-- Prodotti con stock troppo elevato
SELECT
    p.id,
    p.name AS prodotto,
    p.sku,
    c.name AS categoria,
    p.current_stock AS stock_attuale,
    p.max_stock AS stock_massimo,
    (p.current_stock - p.max_stock) AS eccesso_stock,
    ROUND((p.current_stock - p.max_stock) * p.cost_price, 2) AS valore_capitale_investito,
    COALESCE(SUM(si.quantity), 0) AS pezzi_venduti_ultimi_90gg,
    ROUND(COALESCE(SUM(si.quantity), 0) / 90.0, 2) AS vendite_medie_giornaliere,
    CASE
        WHEN COALESCE(SUM(si.quantity), 0) > 0 THEN
            ROUND((p.current_stock - p.max_stock)::numeric / NULLIF(SUM(si.quantity) / 90.0, 0), 0)
        ELSE NULL
    END AS giorni_per_smaltire_eccesso
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id
    AND s.status = 'COMPLETED'
    AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days'
WHERE p.current_stock > p.max_stock
    AND p.is_active = TRUE
GROUP BY p.id, p.name, p.sku, c.name, p.current_stock, p.max_stock, p.cost_price
ORDER BY valore_capitale_investito DESC;

-- ============================================
-- 11. CLIENTI TOP (Migliori clienti)
-- ============================================
-- Analisi dei clienti che spendono di più
SELECT
    s.customer_name AS cliente,
    COUNT(*) AS numero_ordini,
    ROUND(SUM(s.total_amount), 2) AS spesa_totale,
    ROUND(AVG(s.total_amount), 2) AS spesa_media,
    ROUND(MIN(s.total_amount), 2) AS ordine_minimo,
    ROUND(MAX(s.total_amount), 2) AS ordine_massimo,
    MIN(s.sale_date) AS primo_acquisto,
    MAX(s.sale_date) AS ultimo_acquisto,
    EXTRACT(DAY FROM MAX(s.sale_date) - MIN(s.sale_date)) AS giorni_tra_primo_ultimo
FROM sales s
WHERE s.status = 'COMPLETED'
    AND s.customer_name IS NOT NULL
GROUP BY s.customer_name
HAVING COUNT(*) >= 2  -- Almeno 2 ordini
ORDER BY spesa_totale DESC
LIMIT 30;

-- ============================================
-- 12. CONFRONTO VENDITE ACQUISTI (Margin Analysis)
-- ============================================
-- Analisi globale del business
SELECT
    'Fatturato Vendite' AS tipo,
    ROUND(SUM(s.total_amount), 2) AS totale
FROM sales s
WHERE s.status = 'COMPLETED'
UNION ALL
SELECT
    'Costo Vendite' AS tipo,
    ROUND(SUM(si.quantity * p.cost_price), 2) AS totale
FROM sale_items si
JOIN sales s ON si.sale_id = s.id
JOIN products p ON si.product_id = p.id
WHERE s.status = 'COMPLETED'
UNION ALL
SELECT
    'Profitto Lordo' AS tipo,
    ROUND(SUM(s.total_amount) - SUM(si.quantity * p.cost_price), 2) AS totale
FROM sales s
JOIN sale_items si ON s.id = si.sale_id
JOIN products p ON si.product_id = p.id
WHERE s.status = 'COMPLETED'
UNION ALL
SELECT
    'Valore Magazzino' AS tipo,
    ROUND(SUM(p.current_stock * p.cost_price), 2) AS totale
FROM products p
WHERE p.is_active = TRUE
UNION ALL
SELECT
    'Totale Acquisti' AS tipo,
    ROUND(SUM(po.total_cost), 2) AS totale
FROM purchase_orders po
WHERE po.status = 'RECEIVED';

-- ============================================
-- 13. PRODOTTI IN CALO (Declining Products)
-- ============================================
-- Prodotti con vendite in diminuzione nel tempo
WITH monthly_sales AS (
    SELECT
        p.id,
        p.name,
        EXTRACT(YEAR FROM s.sale_date) AS anno,
        EXTRACT(MONTH FROM s.sale_date) AS mese,
        SUM(si.quantity) AS quantita_venduta
    FROM products p
    JOIN sale_items si ON p.id = si.product_id
    JOIN sales s ON si.sale_id = s.id
    WHERE s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY p.id, p.name, EXTRACT(YEAR FROM s.sale_date), EXTRACT(MONTH FROM s.sale_date)
)
SELECT
    id,
    name AS prodotto,
    ROUND(AVG(quantita_venduta), 2) AS media_vendite_mensili,
    ROUND(MAX(quantita_venduta), 2) AS max_vendite_mese,
    ROUND(MIN(quantita_venduta), 2) AS min_vendite_mese,
    ROUND((MAX(quantita_venduta) - MIN(quantita_venduta)) / NULLIF(MAX(quantita_venduta), 0) * 100, 2) AS variazione_percentuale,
    CASE
        WHEN MAX(quantita_venduta) > 0 AND MIN(quantita_venduta) < MAX(quantita_venduta) * 0.5 THEN 'CALO SIGNIFICATIVO'
        WHEN MAX(quantita_venduta) > 0 AND MIN(quantita_venduta) < MAX(quantita_venduta) * 0.7 THEN 'CALO MODERATO'
        ELSE 'STABILE'
    END AS trend
FROM monthly_sales
GROUP BY id, name
HAVING COUNT(*) >= 4  -- Almeno 4 mesi di dati
ORDER BY variazione_percentuale DESC;

-- ============================================
-- 14. VALUTAZIONE FORNITORI (Supplier Rating)
-- ============================================
-- Valutazione complessiva dei fornitori
SELECT
    s.id,
    s.name AS fornitore,
    COUNT(DISTINCT po.id) AS numero_ordini,
    ROUND(SUM(po.total_cost), 2) AS volume_acquisti,
    COUNT(DISTINCT CASE WHEN po.status = 'RECEIVED' THEN po.id END) AS ordini_ricevuti,
    COUNT(DISTINCT CASE WHEN po.status = 'PENDING' THEN po.id END) AS ordini_in_attesa,
    ROUND(AVG(CASE WHEN po.status = 'RECEIVED' THEN
        EXTRACT(DAY FROM po.expected_date - po.order_date)
    END), 1) AS giorni_medi_consegna,
    COUNT(DISTINCT p.id) AS varietà_prodotti,
    CASE
        WHEN COUNT(DISTINCT po.id) >= 5 AND SUM(po.total_cost) > 5000 THEN 'GOLD'
        WHEN COUNT(DISTINCT po.id) >= 3 AND SUM(po.total_cost) > 2000 THEN 'SILVER'
        WHEN COUNT(DISTINCT po.id) >= 1 THEN 'BRONZE'
        ELSE 'NEW'
    END AS livello_fornitore
FROM suppliers s
LEFT JOIN purchase_orders po ON s.id = po.supplier_id
LEFT JOIN purchase_items poi ON po.id = poi.order_id
LEFT JOIN products p ON poi.product_id = p.id
GROUP BY s.id, s.name
ORDER BY volume_acquisti DESC;

-- ============================================
-- 15. PREVISIONE DOMANDA (Demand Forecasting)
-- ============================================
-- Previsione semplice basata su vendite storiche
WITH product_forecast AS (
    SELECT
        p.id,
        p.name,
        p.current_stock,
        COALESCE(SUM(CASE
            WHEN s.sale_date >= CURRENT_DATE - INTERVAL '30 days' THEN si.quantity
            ELSE 0
        END), 0) AS vendite_ultimi_30_gg,
        COALESCE(SUM(CASE
            WHEN s.sale_date >= CURRENT_DATE - INTERVAL '60 days'
                AND s.sale_date < CURRENT_DATE - INTERVAL '30 days' THEN si.quantity
            ELSE 0
        END), 0) AS vendite_30_60_gg_fa,
        COALESCE(SUM(CASE
            WHEN s.sale_date >= CURRENT_DATE - INTERVAL '90 days'
                AND s.sale_date < CURRENT_DATE - INTERVAL '60 days' THEN si.quantity
            ELSE 0
        END), 0) AS vendite_60_90_gg_fa
    FROM products p
    LEFT JOIN sale_items si ON p.id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
    WHERE p.is_active = TRUE
    GROUP BY p.id, p.name, p.current_stock
)
SELECT
    name AS prodotto,
    current_stock AS stock_attuale,
    vendite_ultimi_30_gg,
    vendite_30_60_gg_fa,
    vendite_60_90_gg_fa,
    ROUND((vendite_ultimi_30_gg + vendite_30_60_gg_fa + vendite_60_90_gg_fa) / 90.0, 2) AS media_vendite_giornaliere,
    ROUND(current_stock / NULLIF((vendite_ultimi_30_gg + vendite_30_60_gg_fa + vendite_60_90_gg_fa) / 90.0, 0), 0) AS giorni_di_rimanenza,
    CASE
        WHEN current_stock / NULLIF((vendite_ultimi_30_gg + vendite_30_60_gg_fa + vendite_60_90_gg_fa) / 90.0, 0) < 15 THEN 'SCORTA BASSA'
        WHEN current_stock / NULLIF((vendite_ultimi_30_gg + vendite_30_60_gg_fa + vendite_60_90_gg_fa) / 90.0, 0) > 90 THEN 'SCORTA ECCESSIVA'
        ELSE 'SCORTA OK'
    END AS stato
FROM product_forecast
WHERE (vendite_ultimi_30_gg + vendite_30_60_gg_fa + vendite_60_90_gg_fa) > 0
ORDER BY giorni_di_rimanenza ASC;

-- ============================================
-- 16. ANALISI GIACENZA MEDIA
-- ============================================
-- Calcolo giacenza media e rotazione stock
WITH inventory_days AS (
    SELECT
        p.id,
        p.name,
        p.current_stock,
        COALESCE(SUM(si.quantity), 0) AS vendite_totali,
        COALESCE(SUM(si.quantity) / 365.0, 0) AS vendite_medie_giornaliere,
        p.cost_price * p.current_stock AS valore_giacenza
    FROM products p
    LEFT JOIN sale_items si ON p.id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - INTERVAL '12 months'
    WHERE p.is_active = TRUE
    GROUP BY p.id, p.name, p.current_stock, p.cost_price
)
SELECT
    name AS prodotto,
    current_stock AS giacenza_attuale,
    vendite_totali AS pezzi_venduti_anno,
    ROUND(vendite_medie_giornaliere, 2) AS vendite_medie_giornaliere,
    ROUND(valore_giacenza, 2) AS valore_in_magazzino,
    CASE
        WHEN vendite_medie_giornaliere > 0 THEN
            ROUND(current_stock / vendite_medie_giornaliere, 0)
        ELSE 0
    END AS giorni_di_copertura,
    CASE
        WHEN vendite_medie_giornaliere > 0 THEN
            ROUND(365.0 / (current_stock / NULLIF(vendite_medie_giornaliere, 0)), 2)
        ELSE 0
    END AS rotazione_stock_volte_anno
FROM inventory_days
ORDER BY valore_giacenza DESC;

-- ============================================
-- 17. ANALISI RENTABILITÀ PER CATEGORIA
-- ============================================
-- Margini e profitto per categoria
SELECT
    c.name AS categoria,
    COUNT(DISTINCT p.id) AS numero_prodotti,
    COUNT(DISTINCT si.sale_id) AS numero_vendite,
    SUM(si.quantity) AS totale_pezzi_venduti,
    ROUND(SUM(si.subtotal), 2) AS fatturato_totale,
    ROUND(SUM(si.quantity * p.cost_price), 2) AS costo_totale_merci,
    ROUND(SUM(si.subtotal) - SUM(si.quantity * p.cost_price), 2) AS profitto_lordo,
    ROUND((SUM(si.subtotal) - SUM(si.quantity * p.cost_price)) / SUM(si.subtotal) * 100, 2) AS margine_percentuale,
    ROUND(AVG(p.sell_price - p.cost_price), 2) AS profitto_medio_unitario
FROM categories c
JOIN products p ON c.id = p.category_id
JOIN sale_items si ON p.id = si.product_id
JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
GROUP BY c.name
ORDER BY profitto_lordo DESC;

-- ============================================
-- 18. PRODOTTI CON MARGINE BASSO
-- ============================================
-- Identifica prodotti con margini insufficienti
SELECT
    p.id,
    p.name AS prodotto,
    p.sku,
    c.name AS categoria,
    p.cost_price AS costo,
    p.sell_price AS prezzo_vendita,
    ROUND(p.sell_price - p.cost_price, 2) AS profitto_unitario,
    ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2) AS margine_percentuale,
    p.current_stock AS stock,
    COALESCE(SUM(si.quantity), 0) AS quantita_venduta
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
WHERE (p.sell_price - p.cost_price) / p.sell_price * 100 < 20  -- Margine < 20%
    AND p.is_active = TRUE
GROUP BY p.id, p.name, p.sku, c.name, p.cost_price, p.sell_price, p.current_stock
ORDER BY margine_percentuale ASC;

-- ============================================
-- FINE QUERY AVANZATE
-- ============================================
