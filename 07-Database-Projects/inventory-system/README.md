# Sistema di Gestione Inventario (Inventory System)

## Descrizione del Progetto

Sistema completo di gestione inventario realizzato con **PostgreSQL** per la gestione di prodotti, fornitori, vendite, acquisti e movimenti di magazzino.

Il progetto include:
- ✅ Schema database completo con relazioni e vincoli
- ✅ Dati di esempio realistici (50+ prodotti, 100+ vendite, 200+ movimenti)
- ✅ Query avanzate con funzioni di aggregazione e GROUP BY/HAVING
- ✅ Viste ottimizzate per analisi comuni
- ✅ Trigger per aggiornamento automatico dei dati

---

## Struttura del Progetto

```
inventory-system/
├── schema.sql           # Schema completo del database
├── sample_data.sql      # Dati di esempio
├── queries.sql          # Query avanzate
├── views.sql            # Viste utili
└── README.md            # Questa documentazione
```

---

## Come Iniziare

### Prerequisiti

- PostgreSQL 12 o superiore
- Client PostgreSQL (psql, pgAdmin, DBeaver, etc.)

### Installazione

1. **Creare il database**
```sql
CREATE DATABASE inventory_system;
\c inventory_system
```

2. **Eseguire lo schema**
```bash
psql -U postgres -d inventory_system -f schema.sql
```

3. **Inserire i dati di esempio**
```bash
psql -U postgres -d inventory_system -f sample_data.sql
```

4. **Creare le viste aggiuntive**
```bash
psql -U postgres -d inventory_system -f views.sql
```

---

## Schema del Database

### Tabelle Principali

#### 1. `categories`
Categorie di prodotti
- `id` - Chiave primaria
- `name` - Nome categoria (univoco)
- `description` - Descrizione

#### 2. `suppliers`
Fornitori di prodotti
- `id` - Chiave primaria
- `name` - Nome fornitore
- `contact_person` - Referente
- `email` - Email (con validazione)
- `phone` - Telefono
- `address` - Indirizzo

#### 3. `products`
Catalogo prodotti con informazioni stock
- `id` - Chiave primaria
- `name` - Nome prodotto
- `sku` - Codice SKU (univoco)
- `category_id` - Chiave esterna → categories
- `supplier_id` - Chiave esterna → suppliers
- `cost_price` - Prezzo di costo > 0
- `sell_price` - Prezzo di vendita > 0
- `current_stock` - Stock attuale ≥ 0
- `min_stock` - Stock minimo
- `max_stock` - Stock massimo
- `reorder_point` - Punto di riordino
- `is_active` - Prodotto attivo

#### 4. `sales`
Vendite effettuate
- `id` - Chiave primaria
- `sale_date` - Data vendita
- `customer_name` - Nome cliente
- `total_amount` - Totale vendita
- `payment_method` - Metodo di pagamento
- `status` - Stato vendita

#### 5. `sale_items`
Dettagli prodotti venduti
- `id` - Chiave primaria
- `sale_id` - Chiave esterna → sales
- `product_id` - Chiave esterna → products
- `quantity` - Quantità venduta
- `unit_price` - Prezzo unitario
- `subtotal` - Subtotale

#### 6. `purchase_orders`
Ordini di acquisto ai fornitori
- `id` - Chiave primaria
- `supplier_id` - Chiave esterna → suppliers
- `order_date` - Data ordine
- `expected_date` - Data prevista consegna
- `status` - Stato (PENDING/ORDERED/RECEIVED/CANCELLED)
- `total_cost` - Costo totale

#### 7. `purchase_items`
Dettagli ordini di acquisto
- `id` - Chiave primaria
- `order_id` - Chiave esterna → purchase_orders
- `product_id` - Chiave esterna → products
- `quantity` - Quantità
- `unit_cost` - Costo unitario

#### 8. `stock_movements`
Movimenti di magazzino
- `id` - Chiave primaria
- `product_id` - Chiave esterna → products
- `movement_type` - Tipo (IN/OUT/ADJUSTMENT/TRANSFER/RETURN/DAMAGE)
- `quantity` - Quantità
- `reference_id` - Riferimento documento
- `movement_date` - Data movimento
- `notes` - Note

### Vincoli e Indici

**CHECK Constraints:**
- `cost_price > 0` - Prezzo costo deve essere positivo
- `sell_price > 0` - Prezzo vendita deve essere positivo
- `current_stock >= 0` - Stock non può essere negativo
- `max_stock > min_stock` - Stock massimo > minimo
- `reorder_point >= min_stock` - Punto riordino ≥ minimo

**Indici ottimizzati:**
- Prodotti: SKU, categoria, fornitore, stock
- Vendite: data, cliente, stato
- Movimenti: prodotto, tipo, data

### Trigger

1. **update_updated_at_column** - Aggiorna automaticamente `updated_at`
2. **update_purchase_order_total** - Calcola totale ordini di acquisto

---

## Viste Disponibili

### 1. `v_product_summary`
Riepilogo prodotti con stato stock e margini

```sql
SELECT * FROM v_product_summary
WHERE needs_reorder = TRUE;
```

### 2. `v_supplier_performance`
Analisi performance fornitori

```sql
SELECT * FROM v_supplier_performance
WHERE total_orders > 0;
```

### 3. `v_monthly_sales`
Vendite aggregate per mese

```sql
SELECT * FROM v_monthly_sales
ORDER BY year DESC, month DESC;
```

### 4. `v_low_stock`
Prodotti che necessitano riordino

```sql
SELECT * FROM v_low_stock
ORDER BY units_to_order DESC;
```

### 5. `v_product_sales_summary`
Statistiche vendite per prodotto

### 6. `v_daily_sales_report`
Report vendite giornaliere

### 7. `v_category_performance`
Performance per categoria

### 8. `v_inventory_valuation`
Valutazione inventario

### 9. `v_reorder_recommendations`
Raccomandazioni riordino intelligenti

### 10. `v_product_profitability`
Redditività prodotti

---

## Query di Esempio

### Prodotti con Stock Basso (Alert)

```sql
SELECT
    p.name AS prodotto,
    p.current_stock AS stock_attuale,
    p.reorder_point AS punto_riordino,
    (p.reorder_point - p.current_stock) AS da_ordinare,
    c.name AS categoria,
    s.name AS fornitore
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN suppliers s ON p.supplier_id = s.id
WHERE p.current_stock <= p.reorder_point
ORDER BY (p.reorder_point - p.current_stock) DESC;
```

### Vendite per Categoria (GROUP BY)

```sql
SELECT
    c.name AS categoria,
    COUNT(DISTINCT si.sale_id) AS vendite,
    SUM(si.quantity) AS pezzi_venduti,
    ROUND(SUM(si.subtotal), 2) AS fatturato
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'COMPLETED'
GROUP BY c.name
ORDER BY fatturato DESC;
```

### Top 10 Prodotti Più Venduti

```sql
SELECT
    p.name AS prodotto,
    c.name AS categoria,
    SUM(si.quantity) AS totale_venduto,
    ROUND(SUM(si.subtotal), 2) AS fatturato
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'COMPLETED'
GROUP BY p.id, p.name, c.name
ORDER BY totale_venduto DESC
LIMIT 10;
```

### Margini di Profitto per Prodotto

```sql
SELECT
    p.name AS prodotto,
    p.cost_price AS costo,
    p.sell_price AS prezzo_vendita,
    ROUND(p.sell_price - p.cost_price, 2) AS profitto_unitario,
    ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2) AS margine_percentuale
FROM products p
WHERE p.is_active = TRUE
ORDER BY margine_percentuale DESC;
```

### Analisi Movimenti di Magazzino

```sql
SELECT
    p.name AS prodotto,
    sm.movement_type AS tipo_movimento,
    SUM(sm.quantity) AS quantita,
    COUNT(*) AS numero_movimenti
FROM stock_movements sm
JOIN products p ON sm.product_id = p.id
WHERE sm.movement_date >= '2024-01-01'
GROUP BY p.id, p.name, sm.movement_type
ORDER BY prodotto, sm.movement_type;
```

### Fornitori con Alti Volumi (HAVING)

```sql
SELECT
    s.name AS fornitore,
    COUNT(DISTINCT po.id) AS numero_ordini,
    ROUND(SUM(po.total_cost), 2) AS totale_acquisti
FROM suppliers s
JOIN purchase_orders po ON s.id = po.supplier_id
GROUP BY s.id, s.name
HAVING COUNT(DISTINCT po.id) >= 2
    AND SUM(po.total_cost) > 1000
ORDER BY totale_acquisti DESC;
```

---

## Funzionalità SQL Dimostrate

### Aggregation Functions
- `COUNT()` - Contare record
- `SUM()` - Sommare valori
- `AVG()` - Calcolare medie
- `MIN()` / `MAX()` - Valori minimi e massimi
- `ROUND()` - Arrotondamenti

### GROUP BY
- Raggruppamento per categoria
- Raggruppamento per mese
- Raggruppamento multi-colonna

### HAVING
- Filtrare gruppi di risultati
- Condizioni su aggregazioni

### JOINs
- `INNER JOIN` - Join interne
- `LEFT JOIN` - Join esterne sinistra
- Join multi-tabella

### Window Functions
- `SUM() OVER()` - Totali cumulativi
- `ROW_NUMBER()` - Numerazione righe

### CTE (Common Table Expressions)
- Query ricorsive
- Subquery ottimizzate

---

## Statistiche del Dataset

| Entità | Quantità |
|--------|----------|
| Categorie | 12 |
| Fornitori | 9 |
| Prodotti | 50 |
| Vendite | 100 |
| Righe vendita | 150+ |
| Ordini acquisto | 21 |
| Movimenti stock | 250+ |

---

## Caratteristiche Avanzate

### Trigger Automatici
1. Aggiornamento `updated_at` su modifiche
2. Calcolo automatico totale ordini acquisto

### Vincoli di Integrità
- Foreign Keys con CASCADE
- CHECK constraints per validazione dati
- UNIQUE constraints per SKU

### Ottimizzazioni
- Indici su colonne frequentemente query
- Viste materializzate per report
- Query ottimizzate con EXPLAIN ANALYZE

---

## Query Disponibili in `queries.sql`

1. **Prodotti con stock basso** - Alert riordini
2. **Vendite per categoria** - Analisi aggregata
3. **Vendite mensili** - Trend temporali
4. **Performance fornitori** - Valutazione fornitori
5. **Redditività prodotti** - Analisi margini
6. **Top prodotti** - Prodotti più venduti
7. **Storico movimenti** - Analisi magazzino
8. **Suggerimenti riordino** - CTE complesso
9. **Metodi pagamento** - Analisi vendite
10. **Prodotti overstock** - Eccesso magazzino
11. **Top clienti** - Migliori clienti
12. **Confronto vendite/acquisti** - ANALISI profitto
13. **Prodotti in calo** - Trend negativi
14. **Valutazione fornitori** - Rating fornitori
15. **Previsione domanda** - Forecasting
16. **Giacenza media** - Rotazione stock
17. **Redditività categoria** - Margin per categoria
18. **Margini bassi** - Prodotti poco redditizi

---

## Troubleshooting

### Errore: Relation does not exist
Verifica di aver eseguito i file nell'ordine corretto:
1. `schema.sql`
2. `sample_data.sql`
3. `views.sql`

### Trigger non funzionano
Verifica che i trigger siano abilitati:
```sql
SELECT * FROM information_schema.triggers
WHERE event_object_table = 'products';
```

### Performance lente
Analizza le query con EXPLAIN:
```sql
EXPLAIN ANALYZE
SELECT * FROM v_product_summary;
```

---

## Estensioni Possibili

- [ ] Implementare stored procedure per operazioni complesse
- [ ] Aggiungere reportistica con PgTalk
- [ ] Creare dashboard con Grafana
- [ ] Integrazione API REST
- [ ] Esportazione dati in Excel/CSV
- [ ] Notifiche automatiche per stock basso
- [ ] Multi-warehouse support
- [ ] Gestione lotti e scadenze

---

## Autore

Progetto realizzato per portfolio di database projects.

**Tecnologie utilizzate:**
- PostgreSQL 15+
- SQL Avanzato
- Database Design
- Query Optimization

---

## Licenza

Questo progetto è a scopo educativo e formativo.
