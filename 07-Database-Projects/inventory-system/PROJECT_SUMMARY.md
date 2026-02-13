# 📦 Sistema Gestione Inventario - Riepilogo Progetto

## Panoramica

Sistema completo di gestione inventario realizzato con **PostgreSQL** per gestire prodotti, fornitori, vendite, acquisti e movimenti di magazzino.

---

## 📁 File del Progetto

| File | Dimensione | Descrizione |
|------|-----------|-------------|
| **schema.sql** | 13 KB | Schema database completo con tutte le tabelle, vincoli, indici e trigger |
| **sample_data.sql** | 29 KB | Dati di esempio: 50+ prodotti, 100+ vendite, 200+ movimenti |
| **queries.sql** | 21 KB | 18 query avanzate con GROUP BY, HAVING, CTE |
| **views.sql** | 19 KB | 11 viste ottimizzate per analisi comuni |
| **procedures.sql** | 20 KB | Stored procedures e functions per automazione |
| **README.md** | 11 KB | Documentazione completa in italiano |
| **QUICK_REFERENCE.md** | 4.2 KB | Guida rapida comandi SQL più usati |
| **DATABASE_STRUCTURE.txt** | 11 KB | Diagramma ER e struttura relazioni |

**Totale:** 8 file, ~128 KB di codice SQL, 909 righe di documentazione

---

## 🗄️ Struttura Database

### Tabelle (8 totali)

1. **categories** - Categorie di prodotti
2. **suppliers** - Fornitori
3. **products** - Catalogo prodotti con stock
4. **sales** - Vendite
5. **sale_items** - Dettagli vendite
6. **purchase_orders** - Ordini di acquisto
7. **purchase_items** - Dettagli ordini acquisto
8. **stock_movements** - Movimenti magazzino

### Relazioni

```
suppliers ──┬── purchase_orders ── purchase_items
            └── products ──┬── sale_items ── sales
                          │
                          └── stock_movements

categories ── products
```

---

## 📊 Dataset

| Entità | Quantità | Note |
|--------|----------|------|
| Categorie | 12 | Elettronica, Informatica, Telefonia, etc. |
| Fornitori | 9 | Internazionali e locali |
| Prodotti | 50 | Con SKU univoci, prezzi, stock |
| Vendite | 100+ | Con date, clienti, metodi pagamento |
| Righe Vendita | 150+ | Items multipli per vendita |
| Ordini Acquisto | 21 | Con stati diversi |
| Movimenti Stock | 250+ | IN, OUT, ADJUSTMENT, RETURN, DAMAGE |

---

## 🔧 Funzionalità SQL Dimostrate

### Fundamentals
- ✅ CREATE TABLE con vincoli
- ✅ Foreign Keys con CASCADE
- ✅ CHECK constraints
- ✅ UNIQUE constraints
- ✅ INDEX ottimizzati

### Advanced SQL
- ✅ INNER JOIN, LEFT JOIN
- ✅ GROUP BY multi-colonna
- ✅ HAVING per filtri aggregati
- ✅ Subquery e CTE
- ✅ Window Functions
- ✅ UNION e UNION ALL

### Aggregation Functions
- ✅ COUNT(), SUM(), AVG()
- ✅ MIN(), MAX()
- ✅ ROUND() per arrotondamenti
- ✅ COALESCE per valori NULL

### Database Objects
- ✅ VIEWS (11 viste utili)
- ✅ FUNCTIONS (8 funzioni)
- ✅ PROCEDURES (3 procedure)
- ✅ TRIGGERS (5 trigger)
- ✅ Indici per performance

---

## 📈 Query Avanzate Incluse

1. **Prodotti con stock basso** - Alert riordini
2. **Vendite per categoria** - GROUP BY aggregato
3. **Vendite mensili** - Analisi temporale
4. **Performance fornitori** - Con HAVING
5. **Redditività prodotti** - Margin analysis
6. **Top prodotti venduti** - Ranking
7. **Storico movimenti** - Movimenti magazzino
8. **Suggerimenti riordino** - CTE complesso
9. **Metodi pagamento** - Analisi vendite
10. **Prodotti overstock** - Eccesso stock
11. **Clienti top** - Segmentazione
12. **Confronto vendite/acquisti** - Profit analysis
13. **Prodotti in calo** - Trend analysis
14. **Valutazione fornitori** - Rating
15. **Previsione domanda** - Forecasting
16. **Giacenza media** - Rotazione stock
17. **Redditività categoria** - Margini
18. **Prodotti poco redditizi** - Low margins

---

## 🎯 Viste Utili

### Core Views (in schema.sql)
- `v_product_summary` - Riepilogo prodotti con stato stock
- `v_supplier_performance` - Metriche fornitori
- `v_monthly_sales` - Vendite mensili
- `v_low_stock` - Prodotti da riordinare

### Extended Views (in views.sql)
- `v_product_sales_summary` - Statistiche vendite
- `v_daily_sales_report` - Report giornaliero
- `v_category_performance` - Performance categorie
- `v_inventory_valuation` - Valutazione magazzino
- `v_reorder_recommendations` - Suggerimenti intelligenti
- `v_product_profitability` - Redditività prodotti
- `v_purchase_order_status` - Stato ordini
- `v_customer_insights` - Analisi clienti
- `v_slow_moving_products` - Prodotti lenti
- `v_stock_movement_summary` - Movimenti
- `v_alerts_summary` - Panoramica alert

---

## ⚡ Stored Procedures & Functions

### Functions
1. `calculate_reorder_quantity(product_id)` - Calcola quantità riordino
2. `update_stock_after_sale(sale_id)` - Aggiorna stock post-vendita
3. `process_purchase_order_receipt(order_id)` - Processa ricezione
4. `get_product_sales_velocity(product_id, days)` - Velocità vendita
5. `get_inventory_turnover(days)` - Rotazione inventario
6. `generate_reorder_report()` - Report completo riordini
7. `calculate_product_profit_margin(product_id)` - Margini
8. `get_sales_analytics(start_date, end_date)` - Analytics vendite
9. `check_stock_levels()` - Verifica stock e genera alert

### Procedures
1. `create_sale_with_stock_update(...)` - Crea vendita transazionale
2. `bulk_update_products_category(...)` - Aggiornamento massivo

---

## 🚀 Come Utilizzare

### 1. Setup Database
```bash
psql -U postgres -c "CREATE DATABASE inventory_system;"
psql -U postgres -d inventory_system -f schema.sql
psql -U postgres -d inventory_system -f sample_data.sql
psql -U postgres -d inventory_system -f views.sql
psql -U postgres -d inventory_system -f procedures.sql
```

### 2. Query Rapide
```sql
-- Prodotti da riordinare
SELECT * FROM v_low_stock;

-- Vendite oggi
SELECT COUNT(*), SUM(total_amount)
FROM sales
WHERE DATE(sale_date) = CURRENT_DATE;

-- Report riordini
SELECT * FROM generate_reorder_report();
```

### 3. Analisi Avanzate
```sql
-- Leggi queries.sql per 18 query avanzate
-- Ogni query è commentata e pronta all'uso
```

---

## 📚 Concetti Chiave

### GROUP BY & HAVING
```sql
-- Raggruppa per categoria
SELECT c.name, SUM(si.subtotal)
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN categories c ON p.category_id = c.id
GROUP BY c.name
HAVING SUM(si.subtotal) > 1000;
```

### CTE (Common Table Expressions)
```sql
WITH sales_data AS (
    SELECT product_id, SUM(quantity) as qty
    FROM sale_items
    GROUP BY product_id
)
SELECT * FROM sales_data WHERE qty > 50;
```

### Window Functions
```sql
SELECT
    name,
    SUM(total_amount) OVER (PARTITION BY customer_id) as customer_total
FROM sales;
```

---

## 🎓 Cosa Imparerai

- ✅ Design database relazionale
- ✅ Normalizzazione e relazioni
- ✅ Vincoli e integrità dati
- ✅ Query ottimizzate con indici
- ✅ Viste per sicurezza e performance
- ✅ Stored procedures per automazione
- ✅ Trigger per aggiornamento automatico
- ✅ Funzioni di aggregazione
- ✅ GROUP BY e HAVING avanzati
- ✅ CTE e query complesse

---

## 📊 Statistiche Progetto

| Metrica | Valore |
|---------|--------|
| Righe SQL totali | ~2,400 |
| Query incluse | 18 |
| Viste create | 11 |
| Functions | 9 |
| Procedures | 2 |
| Triggers | 5 |
| Indici | 20+ |
| Documentazione righe | 909 |

---

## 🎯 Casi d'Uso

### Gestione Magazzino
- Monitoraggio stock in tempo reale
- Alert automatici per riordini
- Tracciamento movimenti
- Valutazione inventario

### Analisi Vendite
- Report giornalieri/settimanali/mensili
- Trend e previsioni
- Segmentazione clienti
- Analisi per categoria/prodotto

### Gestione Fornitori
- Valutazione performance
- Tracking ordini
- Analisi costi
- Rating fornitori

### Business Intelligence
- Margini di profitto
- Redditività prodotti
- Rotazione inventario
- Previsione domanda

---

## 🔄 Workflow Esempio

### 1. Nuovo Prodotto
```sql
INSERT INTO products (name, sku, category_id, supplier_id,
                     cost_price, sell_price, current_stock,
                     min_stock, max_stock, reorder_point)
VALUES ('Nuovo Prodotto', 'SKU-001', 1, 1, 50.00, 99.99, 100, 10, 150, 20);
```

### 2. Registra Vendita
```sql
CALL create_sale_with_stock_update(
    'Mario Rossi',
    'CREDIT_CARD',
    '[{"product_id": 1, "quantity": 2}]'::JSONB
);
```

### 3. Controlla Riordini
```sql
SELECT * FROM generate_reorder_report()
WHERE priority LIKE '%URGENT%';
```

### 4. Ricevi Merce
```sql
CALL process_purchase_order_receipt(5);
```

---

## 🌟 Punti di Forza

- ✅ **Schema normalizzato** - 3NF con relazioni corrette
- ✅ **Vincoli robusti** - CHECK, FOREIGN KEY, UNIQUE
- ✅ **Indici ottimizzati** - Performance su query comuni
- ✅ **Dati realistici** - 50+ prodotti, vendite realistiche
- ✅ **Query avanzate** - GROUP BY, HAVING, CTE, Window Functions
- ✅ **Automazione** - Trigger, procedures, functions
- ✅ **Viste utili** - 11 viste per analisi comuni
- ✅ **Documentazione completa** - README, quick reference, struttura

---

## 📖 Percorso di Studio Consigliato

1. **Prima lettura**: `README.md` - Panoramica completa
2. **Schema**: `schema.sql` - Capire struttura tabelle
3. **Dati**: `sample_data.sql` - Vedere dati inseriti
4. **Query**: `queries.sql` - Studiare query avanzate
5. **Viste**: `views.sql` - Capire utility viste
6. **Procedure**: `procedures.sql` - Automazioni
7. **Quick Ref**: `QUICK_REFERENCE.md` - Comandi rapidi

---

## 🎯 Progetti Simili

Questo è il progetto #07 del portfolio. Altri progetti database:
- E-commerce Database
- Library Management System
- Hospital Management
- HR Management System
- Social Media Database
- Banking System

---

## 📝 Note

- **Database**: PostgreSQL 12+
- **Linguaggio**: SQL puro + PL/pgSQL
- **Livello**: Intermedio/Avanzato
- **Focus**: Aggregazione, GROUP BY, HAVING, Viste
- **Documentazione**: Italiano

---

## ✅ Checklist

- [x] Schema completo con 8 tabelle
- [x] Relazioni e foreign keys
- [x] CHECK constraints
- [x] Indici ottimizzati
- [x] Trigger automatici
- [x] 50+ prodotti
- [x] 100+ vendite
- [x] 200+ movimenti
- [x] 18 query avanzate
- [x] 11 viste utili
- [x] 9 functions
- [x] 2 procedures
- [x] README in italiano
- [x] Quick reference guide
- [x] Database structure doc

---

**Progetto completato!** 🎉

Tutti i file sono pronti per l'uso. Segui le istruzioni nel README.md per iniziare.
