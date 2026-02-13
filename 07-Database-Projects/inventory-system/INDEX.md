# 🔍 Indice del Progetto - Sistema Gestione Inventario

## 🚀 Inizia Qui

**Nuovo al progetto?** Leggi i file in questo ordine:

1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Panoramica completa del progetto
2. **[README.md](README.md)** - Guida utente dettagliata
3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Comandi SQL più usati
4. **[DATABASE_STRUCTURE.txt](DATABASE_STRUCTURE.txt)** - Schema e relazioni

---

## 📁 File SQL

### 1. [schema.sql](schema.sql) ⭐ PRIMA PARTE
**Cosa contiene:**
- 8 tabelle complete con vincoli
- Foreign keys con CASCADE
- CHECK constraints per validazione
- 20+ indici ottimizzati
- 4 trigger automatici
- 4 viste core

**Quando usarlo:**
- Prima di tutto! Crea la struttura del database
- Capire relazioni tra tabelle
- Vedere esempi di CHECK constraints

**Comando:**
```bash
psql -U postgres -d inventory_system -f schema.sql
```

---

### 2. [sample_data.sql](sample_data.sql) ⭐ SECONDA PARTE
**Cosa contiene:**
- 12 categorie
- 9 fornitori
- 50 prodotti realistici
- 100+ vendite con items
- 21 ordini di acquisto
- 250+ movimenti di stock

**Quando usarlo:**
- Dopo lo schema
- Popola il database con dati di test
- Esempi di INSERT complessi

**Comando:**
```bash
psql -U postgres -d inventory_system -f sample_data.sql
```

---

### 3. [queries.sql](queries.sql) 📚 STUDIO
**Cosa contiene:**
- 18 query avanzate
- GROUP BY multi-livello
- HAVING con aggregazioni
- CTE complesse
- Window functions
- Analisi business

**Query principali:**
1. Prodotti con stock basso (alert)
2. Vendite per categoria (GROUP BY)
3. Vendite mensili (date grouping)
4. Performance fornitori (HAVING)
5. Redditività prodotti (margin analysis)
6. Top prodotti venduti (ranking)
7. Storico movimenti
8. Suggerimenti riordino (CTE)
9. Metodi pagamento
10. Prodotti overstock
11. Clienti top
12. Confronto vendite/acquisti
13. Prodotti in calo (trend)
14. Valutazione fornitori
15. Previsione domanda
16. Giacenza media
17. Redditività categoria
18. Prodotti poco redditizi

**Quando usarlo:**
- Studiare SQL avanzato
- Esempi di GROUP BY/HAVING
- Analisi business reali

---

### 4. [views.sql](views.sql) 👁️ ANALISI
**Cosa contiene:**
- 11 viste ottimizzate
- Query complesse preimpacchettate
- Analytics ready

**Viste incluse:**
1. `v_product_sales_summary` - Statistiche vendite
2. `v_daily_sales_report` - Report giornaliero
3. `v_category_performance` - Performance categorie
4. `v_supplier_purchase_history` - Storico fornitori
5. `v_inventory_valuation` - Valutazione magazzino
6. `v_stock_movement_summary` - Movimenti
7. `v_reorder_recommendations` - Suggerimenti intelligenti
8. `v_product_profitability` - Redditività
9. `v_purchase_order_status` - Stato ordini
10. `v_customer_insights` - Analisi clienti
11. `v_slow_moving_products` - Prodotti lenti
12. `v_alerts_summary` - Panoramica alert

**Quando usarlo:**
- Semplificare query complesse
- Creare report standard
- Ottimizzare performance

---

### 5. [procedures.sql](procedures.sql) ⚡ AUTOMAZIONE
**Cosa contiene:**
- 9 functions utili
- 2 stored procedures
- 1 trigger aggiuntivo
- Automazione business logic

**Functions principali:**
- `calculate_reorder_quantity()` - Calcola riordini
- `update_stock_after_sale()` - Aggiorna stock
- `process_purchase_order_receipt()` - Ricevi ordine
- `get_product_sales_velocity()` - Velocità vendita
- `get_inventory_turnover()` - Rotazione
- `generate_reorder_report()` - Report riordini
- `calculate_product_profit_margin()` - Margini
- `get_sales_analytics()` - Analytics vendite
- `check_stock_levels()` - Alert stock

**Procedures:**
- `create_sale_with_stock_update()` - Crea vendita
- `bulk_update_products_category()` - Aggiornamento bulk

**Quando usarlo:**
- Automatizzare processi
- Incapsulare logica business
- Ridurre errori umani

---

## 📚 Documentazione

### [README.md](README.md) 📖
**Guida completa del progetto:**
- Descrizione dettagliata
- Struttura tabelle
- Come installare
- Query di esempio
- Estensioni future

**Per chi:** Tutti

### [QUICK_REFERENCE.md](QUICK_REFERENCE.md) ⚡
**Riferimento rapido:**
- Comandi essenziali
- Query più usate
- Procedure comuni
- Viste principali

**Per chi:** Utenti esperti

### [DATABASE_STRUCTURE.txt](DATABASE_STRUCTURE.txt) 🏗️
**Struttura tecnica:**
- Diagramma ER (ASCII art)
- Relazioni tabelle
- Vincoli e indici
- Data flow

**Per chi:** Sviluppatori, DBA

### [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 📊
**Overview progetto:**
- Statistiche complete
- Cosa imparare
- Casi d'uso
- Checklist

**Per chi:** Nuovi utenti, recruiter

---

## 🎯 Percorsi di Apprendimento

### 🟢 Principiante Assoluto
1. Leggi `PROJECT_SUMMARY.md`
2. Leggi `README.md` sezione "Schema del Database"
3. Esegui `schema.sql`
4. Esegui `sample_data.sql`
5. Prova query da `QUICK_REFERENCE.md`

### 🟡 Intermedio
1. Studia `queries.sql` prime 5 query
2. Capisci GROUP BY e HAVING
3. Studia viste in `views.sql`
4. Usa `QUICK_REFERENCE.md`
5. Prova a modificare query

### 🔴 Avanzato
1. Tutto `queries.sql` (18 query)
2. Studia CTE e Window Functions
3. `procedures.sql` - functions
4. Crea tue custom viste
5. Ottimizza con EXPLAIN ANALYZE

---

## 📋 Cheat Sheet

### Setup Rapido
```bash
# 1. Crea database
createdb inventory_system

# 2. Esegui in ordine
psql -d inventory_system -f schema.sql
psql -d inventory_system -f sample_data.sql
psql -d inventory_system -f views.sql
psql -d inventory_system -f procedures.sql
```

### Query Essenziali
```sql
-- Stock basso
SELECT * FROM v_low_stock;

-- Vendite oggi
SELECT COUNT(*), SUM(total_amount)
FROM sales
WHERE DATE(sale_date) = CURRENT_DATE;

-- Report riordini
SELECT * FROM generate_reorder_report();
```

---

## 🔗 Referenze Rapide

| Vuoi... | Vai a... |
|---------|---------|
| Capire lo schema | DATABASE_STRUCTURE.txt |
| Installare | README.md - Come Iniziare |
| Query veloci | QUICK_REFERENCE.md |
| Studiare SQL | queries.sql |
| Creare automazioni | procedures.sql |
| Panoramica | PROJECT_SUMMARY.md |

---

## ✅ Checklist Progetto

- [ ] Letto PROJECT_SUMMARY.md
- [ ] Capita struttura database
- [ ] Eseguito schema.sql
- [ ] Eseguito sample_data.sql
- [ ] Provate 5 query da queries.sql
- [ ] Capito GROUP BY
- [ ] Capito HAVING
- [ ] Usate viste
- [ ] Provate procedure
- [ ] Creato 1 query personalizzata

---

## 🎓 Concetti Chiave

### GROUP BY
```sql
SELECT category, SUM(amount)
FROM sales
GROUP BY category;
```

### HAVING
```sql
SELECT category, SUM(amount)
FROM sales
GROUP BY category
HAVING SUM(amount) > 1000;
```

### CTE
```sql
WITH totals AS (
    SELECT product_id, SUM(qty)
    FROM items
    GROUP BY product_id
)
SELECT * FROM totals WHERE sum > 50;
```

---

## 📞 Supporto

**Problemi?**
1. Controlla README.md - Troubleshooting
2. Verifica ordine esecuzione file
3. Controlla version PostgreSQL (12+)

**Tips:**
- Usa `\d table_name` per vedere struttura tabella
- Usa `EXPLAIN` prima di query complesse
- UsaBEGIN/COMMIT per operazioni multiple

---

**Progetto completato e pronto per l'uso! 🎉**
