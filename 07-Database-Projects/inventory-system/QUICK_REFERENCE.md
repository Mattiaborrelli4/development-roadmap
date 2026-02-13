# Quick Reference - Sistema Inventario

## Comandi Rapidi

### 1. Verifica Stato Database
```sql
-- Conta prodotti
SELECT COUNT(*) FROM products;

-- Conta vendite
SELECT COUNT(*) FROM sales WHERE status = 'COMPLETED';

-- Valore magazzino
SELECT ROUND(SUM(current_stock * cost_price), 2) AS valore_inventario
FROM products WHERE is_active = TRUE;
```

### 2. Prodotti da Riordinare
```sql
SELECT * FROM v_low_stock ORDER BY units_to_order DESC;
```

### 3. Vendite Oggi
```sql
SELECT COUNT(*), ROUND(SUM(total_amount), 2)
FROM sales
WHERE DATE(sale_date) = CURRENT_DATE
AND status = 'COMPLETED';
```

### 4. Top 5 Prodotti più Venduti
```sql
SELECT p.name, SUM(si.quantity) AS tot
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'COMPLETED'
GROUP BY p.name
ORDER BY tot DESC
LIMIT 5;
```

### 5. Margini per Categoria
```sql
SELECT * FROM v_category_performance
ORDER BY gross_profit DESC;
```

### 6. Movimenti Stock Recenti
```sql
SELECT p.name, sm.movement_type, sm.quantity, sm.movement_date
FROM stock_movements sm
JOIN products p ON sm.product_id = p.id
ORDER BY sm.movement_date DESC
LIMIT 20;
```

### 7. Fornitori Top
```sql
SELECT name, ROUND(SUM(total_cost), 2) AS totale
FROM suppliers s
JOIN purchase_orders po ON s.id = po.supplier_id
WHERE po.status = 'RECEIVED'
GROUP BY name
ORDER BY totale DESC;
```

### 8. Alert Inventario
```sql
SELECT * FROM check_stock_levels();
```

### 9. Report Riordini
```sql
SELECT * FROM generate_reorder_report();
```

### 10. Prodotti Overstock
```sql
SELECT p.name, current_stock, max_stock,
       (current_stock - max_stock) AS eccesso
FROM products
WHERE current_stock > max_stock;
```

## Query per Analisi

### Vendite Mensili 2024
```sql
SELECT
    EXTRACT(MONTH FROM sale_date) AS mese,
    COUNT(*) AS vendite,
    ROUND(SUM(total_amount), 2) AS fatturato
FROM sales
WHERE EXTRACT(YEAR FROM sale_date) = 2024
    AND status = 'COMPLETED'
GROUP BY EXTRACT(MONTH FROM sale_date)
ORDER BY mese;
```

### Prodotti mai venduti
```sql
SELECT p.name, p.current_stock, p.cost_price
FROM products p
LEFT JOIN sale_items si ON p.id = si.product_id
WHERE si.id IS NULL
ORDER BY p.current_stock DESC;
```

### Clienti VIP (spesa > 500)
```sql
SELECT customer_name, ROUND(SUM(total_amount), 2) AS totale
FROM sales
WHERE status = 'COMPLETED'
GROUP BY customer_name
HAVING SUM(total_amount) > 500
ORDER BY totale DESC;
```

### Giorni di copertura stock
```sql
SELECT
    p.name,
    p.current_stock,
    ROUND(COALESCE(SUM(si.quantity), 0) / 90.0, 2) AS vendite_giornaliere,
    CASE
        WHEN COALESCE(SUM(si.quantity), 0) > 0 THEN
            ROUND(p.current_stock / (SUM(si.quantity) / 90.0), 0)
        ELSE NULL
    END AS giorni_copertura
FROM products p
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id
    AND s.status = 'COMPLETED'
    AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days'
WHERE p.is_active = TRUE
GROUP BY p.id, p.name, p.current_stock
ORDER BY giorni_copertura ASC;
```

## Procedure Utili

### Processare Ricezione Ordine
```sql
CALL process_purchase_order_receipt(1);
```

### Creare Nuova Vendita
```sql
CALL create_sale_with_stock_update(
    'Mario Rossi',
    'CREDIT_CARD',
    '[{"product_id": 1, "quantity": 2}]'::JSONB
);
```

## Viste Principali

| Vista | Descrizione |
|-------|-------------|
| `v_product_summary` | Riepilogo prodotti con stato |
| `v_low_stock` | Prodotti da riordinare |
| `v_monthly_sales` | Vendite mensili |
| `v_supplier_performance` | Performance fornitori |
| `v_product_sales_summary` | Statistiche vendite prodotti |
| `v_daily_sales_report` | Report vendite giornaliero |
| `v_reorder_recommendations` | Suggerimenti riordino |

## Funzioni Utili

| Funzione | Uso |
|----------|-----|
| `calculate_reorder_quantity(id)` | Calcola quantità da ordinare |
| `get_product_sales_velocity(id)` | Velocità vendita |
| `check_stock_levels()` | Alert inventario |
| `generate_reorder_report()` | Report completo riordini |
| `calculate_product_profit_margin(id)` | Margini prodotto |
