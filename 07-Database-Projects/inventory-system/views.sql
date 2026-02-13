-- ============================================
-- SISTEMA DI GESTIONE INVENTARIO
-- Views del Database
-- PostgreSQL
-- ============================================

-- NOTA: Le view principali sono già incluse in schema.sql
-- Questo file contiene view aggiuntive e utility

-- ============================================
-- VIEW: v_product_sales_summary
-- ============================================
-- Riepilogo vendite per prodotto
CREATE OR REPLACE VIEW v_product_sales_summary AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.sku,
    c.name AS category_name,
    p.cost_price,
    p.sell_price,
    ROUND(p.sell_price - p.cost_price, 2) AS profit_per_unit,
    ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2) AS margin_percentage,
    p.current_stock,
    p.min_stock,
    p.max_stock,
    p.reorder_point,
    COUNT(DISTINCT si.sale_id) AS total_sales,
    SUM(si.quantity) AS total_quantity_sold,
    ROUND(SUM(si.subtotal), 2) AS total_revenue,
    ROUND(SUM(si.quantity) * p.cost_price, 2) AS total_cost,
    ROUND(SUM(si.subtotal) - SUM(si.quantity) * p.cost_price, 2) AS total_profit,
    ROUND(AVG(si.unit_price), 2) AS avg_selling_price,
    MIN(s.sale_date) AS first_sale_date,
    MAX(s.sale_date) AS last_sale_date
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
GROUP BY p.id, p.name, p.sku, c.name, p.cost_price, p.sell_price,
         p.current_stock, p.min_stock, p.max_stock, p.reorder_point
ORDER BY total_revenue DESC NULLS LAST;

-- ============================================
-- VIEW: v_daily_sales_report
-- ============================================
-- Report vendite giornaliere
CREATE OR REPLACE VIEW v_daily_sales_report AS
SELECT
    DATE(s.sale_date) AS sale_date,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT s.customer_name) AS unique_customers,
    ROUND(SUM(s.total_amount), 2) AS total_revenue,
    ROUND(AVG(s.total_amount), 2) AS avg_transaction_value,
    COUNT(DISTINCT si.product_id) AS products_sold,
    SUM(si.quantity) AS total_items_sold,
    ROUND(SUM(CASE WHEN s.payment_method = 'CASH' THEN s.total_amount ELSE 0 END), 2) AS cash_revenue,
    ROUND(SUM(CASE WHEN s.payment_method = 'CREDIT_CARD' THEN s.total_amount ELSE 0 END), 2) AS credit_card_revenue,
    ROUND(SUM(CASE WHEN s.payment_method = 'DEBIT_CARD' THEN s.total_amount ELSE 0 END), 2) AS debit_card_revenue,
    ROUND(SUM(CASE WHEN s.payment_method = 'PAYPAL' THEN s.total_amount ELSE 0 END), 2) AS paypal_revenue,
    ROUND(SUM(CASE WHEN s.payment_method = 'BANK_TRANSFER' THEN s.total_amount ELSE 0 END), 2) AS bank_transfer_revenue
FROM sales s
JOIN sale_items si ON s.id = si.sale_id
WHERE s.status = 'COMPLETED'
GROUP BY DATE(s.sale_date)
ORDER BY sale_date DESC;

-- ============================================
-- VIEW: v_category_performance
-- ============================================
-- Performance per categoria
CREATE OR REPLACE VIEW v_category_performance AS
SELECT
    c.id AS category_id,
    c.name AS category_name,
    c.description,
    COUNT(DISTINCT p.id) AS product_count,
    COUNT(DISTINCT CASE WHEN p.is_active = TRUE THEN p.id END) AS active_products,
    SUM(p.current_stock) AS total_stock,
    ROUND(SUM(p.current_stock * p.cost_price), 2) AS total_inventory_value,
    COUNT(DISTINCT si.sale_id) AS total_sales,
    SUM(si.quantity) AS total_items_sold,
    ROUND(SUM(si.subtotal), 2) AS total_revenue,
    ROUND(SUM(si.quantity * p.cost_price), 2) AS total_cost_of_goods,
    ROUND(SUM(si.subtotal) - SUM(si.quantity * p.cost_price), 2) AS gross_profit,
    ROUND((SUM(si.subtotal) - SUM(si.quantity * p.cost_price)) / NULLIF(SUM(si.subtotal), 0) * 100, 2) AS profit_margin_percentage
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
GROUP BY c.id, c.name, c.description
ORDER BY total_revenue DESC NULLS LAST;

-- ============================================
-- VIEW: v_supplier_purchase_history
-- ============================================
-- Storico acquisti per fornitore
CREATE OR REPLACE VIEW v_supplier_purchase_history AS
SELECT
    s.id AS supplier_id,
    s.name AS supplier_name,
    s.contact_person,
    s.email,
    s.phone,
    COUNT(DISTINCT po.id) AS total_orders,
    COUNT(DISTINCT CASE WHEN po.status = 'PENDING' THEN po.id END) AS pending_orders,
    COUNT(DISTINCT CASE WHEN po.status = 'ORDERED' THEN po.id END) AS ordered_orders,
    COUNT(DISTINCT CASE WHEN po.status = 'RECEIVED' THEN po.id END) AS received_orders,
    COUNT(DISTINCT CASE WHEN po.status = 'CANCELLED' THEN po.id END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN po.status = 'RECEIVED' THEN po.total_cost ELSE 0 END), 2) AS total_spent,
    ROUND(AVG(CASE WHEN po.status = 'RECEIVED' THEN po.total_cost ELSE NULL END), 2) AS avg_order_value,
    MIN(po.order_date) AS first_order_date,
    MAX(po.order_date) AS last_order_date,
    COUNT(DISTINCT p.id) AS distinct_products_supplied
FROM suppliers s
LEFT JOIN purchase_orders po ON s.id = po.supplier_id
LEFT JOIN purchase_items poi ON po.id = poi.order_id
LEFT JOIN products p ON poi.product_id = p.id
GROUP BY s.id, s.name, s.contact_person, s.email, s.phone
ORDER BY total_spent DESC NULLS LAST;

-- ============================================
-- VIEW: v_inventory_valuation
-- ============================================
-- Valutazione inventario
CREATE OR REPLACE VIEW v_inventory_valuation AS
SELECT
    c.id AS category_id,
    c.name AS category_name,
    COUNT(p.id) AS total_products,
    COUNT(CASE WHEN p.current_stock > 0 THEN p.id END) AS products_with_stock,
    SUM(p.current_stock) AS total_items_in_stock,
    ROUND(SUM(p.current_stock * p.cost_price), 2) AS total_cost_value,
    ROUND(SUM(p.current_stock * p.sell_price), 2) AS total_retail_value,
    ROUND(SUM(p.current_stock * (p.sell_price - p.cost_price)), 2) AS total_potential_profit,
    COUNT(CASE WHEN p.current_stock <= p.min_stock THEN p.id END) AS products_below_min_stock,
    COUNT(CASE WHEN p.current_stock >= p.max_stock THEN p.id END) AS products_overstocked,
    COUNT(CASE WHEN p.current_stock = 0 THEN p.id END) AS products_out_of_stock
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
WHERE p.is_active = TRUE
GROUP BY c.id, c.name
ORDER BY total_cost_value DESC;

-- ============================================
-- VIEW: v_stock_movement_summary
-- ============================================
-- Riepilogo movimenti stock
CREATE OR REPLACE VIEW v_stock_movement_summary AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.sku,
    c.name AS category_name,
    COUNT(*) AS total_movements,
    SUM(CASE WHEN sm.movement_type = 'IN' THEN sm.quantity ELSE 0 END) AS total_in,
    SUM(CASE WHEN sm.movement_type = 'OUT' THEN ABS(sm.quantity) ELSE 0 END) AS total_out,
    SUM(CASE WHEN sm.movement_type = 'ADJUSTMENT' THEN sm.quantity ELSE 0 END) AS total_adjustment,
    SUM(CASE WHEN sm.movement_type = 'RETURN' THEN sm.quantity ELSE 0 END) AS total_return,
    SUM(CASE WHEN sm.movement_type = 'DAMAGE' THEN ABS(sm.quantity) ELSE 0 END) AS total_damage,
    MIN(sm.movement_date) AS first_movement,
    MAX(sm.movement_date) AS last_movement,
    p.current_stock
FROM stock_movements sm
JOIN products p ON sm.product_id = p.id
LEFT JOIN categories c ON p.category_id = c.id
GROUP BY p.id, p.name, p.sku, c.name, p.current_stock
ORDER BY total_movements DESC;

-- ============================================
-- VIEW: v_reorder_recommendations
-- ============================================
-- Raccomandazioni riordino avanzate
CREATE OR REPLACE VIEW v_reorder_recommendations AS
WITH sales_velocity AS (
    SELECT
        p.id,
        COALESCE(SUM(si.quantity) / 90.0, 0) AS daily_sales_rate
    FROM products p
    LEFT JOIN sale_items si ON p.id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.id
        AND s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days'
    WHERE p.is_active = TRUE
    GROUP BY p.id
)
SELECT
    p.id,
    p.name AS product_name,
    p.sku,
    c.name AS category_name,
    p.current_stock,
    p.min_stock,
    p.reorder_point,
    sv.daily_sales_rate,
    CASE
        WHEN sv.daily_sales_rate > 0 THEN
            ROUND(p.current_stock / sv.daily_sales_rate, 0)
        ELSE 999
    END AS days_of_stock_remaining,
    GREATEST(
        p.reorder_point - p.current_stock,
        CEIL(sv.daily_sales_rate * 30)
    ) AS suggested_order_quantity,
    s.name AS preferred_supplier,
    s.email AS supplier_email,
    s.phone AS supplier_phone,
    ROUND(GREATEST(p.reorder_point - p.current_stock, CEIL(sv.daily_sales_rate * 30)) * p.cost_price, 2) AS estimated_cost,
    CASE
        WHEN p.current_stock <= 0 THEN 'URGENT - Out of Stock'
        WHEN p.current_stock < p.min_stock THEN 'URGENT - Below Minimum'
        WHEN p.current_stock <= p.reorder_point THEN 'ORDER - At Reorder Point'
        WHEN sv.daily_sales_rate > 0 AND p.current_stock / sv.daily_sales_rate < 30 THEN 'PLAN - Low Stock'
        ELSE 'OK - Sufficient Stock'
    END AS order_priority
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN suppliers s ON p.supplier_id = s.id
LEFT JOIN sales_velocity sv ON p.id = sv.id
WHERE p.is_active = TRUE
    AND (p.current_stock <= p.reorder_point OR sv.daily_sales_rate > 0)
ORDER BY
    CASE
        WHEN p.current_stock <= 0 THEN 1
        WHEN p.current_stock < p.min_stock THEN 2
        WHEN p.current_stock <= p.reorder_point THEN 3
        WHEN sv.daily_sales_rate > 0 AND p.current_stock / sv.daily_sales_rate < 30 THEN 4
        ELSE 5
    END,
    suggested_order_quantity DESC;

-- ============================================
-- VIEW: v_product_profitability
-- ============================================
-- Analisi redditività prodotti
CREATE OR REPLACE VIEW v_product_profitability AS
SELECT
    p.id,
    p.name AS product_name,
    p.sku,
    c.name AS category,
    p.cost_price,
    p.sell_price,
    ROUND(p.sell_price - p.cost_price, 2) AS profit_per_unit,
    ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2) AS profit_margin_pct,
    COALESCE(SUM(si.quantity), 0) AS units_sold,
    COALESCE(ROUND(SUM(si.subtotal), 2), 0) AS total_revenue,
    COALESCE(ROUND(SUM(si.quantity * p.cost_price), 2), 0) AS total_cost,
    COALESCE(ROUND(SUM(si.subtotal) - SUM(si.quantity * p.cost_price), 2), 0) AS gross_profit,
    COALESCE(ROUND((SUM(si.subtotal) - SUM(si.quantity * p.cost_price)) / NULLIF(SUM(si.subtotal), 0) * 100, 2), 0) AS actual_margin_pct,
    p.current_stock,
    ROUND(p.current_stock * p.cost_price, 2) AS inventory_value,
    CASE
        WHEN SUM(si.quantity) > 0 THEN
            ROUND(AVG(si.unit_price), 2)
        ELSE p.sell_price
    END AS avg_selling_price
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
WHERE p.is_active = TRUE
GROUP BY p.id, p.name, p.sku, c.name, p.cost_price, p.sell_price, p.current_stock
HAVING COALESCE(SUM(si.quantity), 0) > 0
ORDER BY gross_profit DESC;

-- ============================================
-- VIEW: v_purchase_order_status
-- ============================================
-- Stato ordini di acquisto
CREATE OR REPLACE VIEW v_purchase_order_status AS
SELECT
    po.id AS order_id,
    s.name AS supplier_name,
    po.order_date,
    po.expected_date,
    po.status,
    COUNT(DISTINCT poi.product_id) AS total_products,
    SUM(poi.quantity) AS total_items,
    ROUND(SUM(poi.quantity * poi.unit_cost), 2) AS total_cost,
    po.notes,
    CASE
        WHEN po.status = 'PENDING' THEN 'DA INVIARE'
        WHEN po.status = 'ORDERED' AND po.expected_date < CURRENT_DATE THEN 'IN RITARDO'
        WHEN po.status = 'ORDERED' THEN 'IN ATTESA CONSEGNA'
        WHEN po.status = 'RECEIVED' THEN 'RICEVUTO'
        WHEN po.status = 'CANCELLED' THEN 'CANCELLATO'
        ELSE 'SCONOSCIUTO'
    END AS status_description,
    EXTRACT(DAY FROM CURRENT_DATE - po.order_date) AS days_since_order,
    EXTRACT(DAY FROM COALESCE(po.expected_date, CURRENT_DATE) - CURRENT_DATE) AS days_until_expected
FROM purchase_orders po
JOIN suppliers s ON po.supplier_id = s.id
LEFT JOIN purchase_items poi ON po.id = poi.order_id
GROUP BY po.id, s.name, po.order_date, po.expected_date, po.status, po.notes
ORDER BY
    CASE po.status
        WHEN 'PENDING' THEN 1
        WHEN 'ORDERED' THEN 2
        WHEN 'RECEIVED' THEN 3
        WHEN 'CANCELLED' THEN 4
    END,
    po.expected_date ASC;

-- ============================================
-- VIEW: v_customer_insights
-- ============================================
-- Analisi clienti
CREATE OR REPLACE VIEW v_customer_insights AS
SELECT
    customer_name,
    COUNT(*) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_spent,
    ROUND(AVG(total_amount), 2) AS avg_order_value,
    ROUND(MIN(total_amount), 2) AS min_order_value,
    ROUND(MAX(total_amount), 2) AS max_order_value,
    MIN(sale_date) AS first_purchase,
    MAX(sale_date) AS last_purchase,
    EXTRACT(DAY FROM MAX(sale_date) - MIN(sale_date)) AS days_as_customer,
    COUNT(DISTINCT DATE(sale_date)) AS shopping_days,
    MODE() WITHIN GROUP (ORDER BY payment_method) AS preferred_payment_method,
    CASE
        WHEN COUNT(*) >= 10 THEN 'VIP - Gold'
        WHEN COUNT(*) >= 5 THEN 'Loyal - Silver'
        WHEN COUNT(*) >= 2 THEN 'Regular - Bronze'
        ELSE 'New'
    END AS customer_tier
FROM sales
WHERE status = 'COMPLETED'
    AND customer_name IS NOT NULL
GROUP BY customer_name
ORDER BY total_spent DESC;

-- ============================================
-- VIEW: v_slow_moving_products
-- ============================================
-- Prodotti a lenta movimentazione
CREATE OR REPLACE VIEW v_slow_moving_products AS
WITH product_metrics AS (
    SELECT
        p.id,
        p.name,
        p.sku,
        c.name AS category,
        p.current_stock,
        p.cost_price,
        p.sell_price,
        COALESCE(SUM(si.quantity), 0) AS total_sold_90days,
        COALESCE(SUM(si.quantity) / 90.0, 0) AS daily_sales_rate,
        MAX(s.sale_date) AS last_sale_date
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    LEFT JOIN sale_items si ON p.id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.id
        AND s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days'
    WHERE p.is_active = TRUE
    GROUP BY p.id, p.name, p.sku, c.name, p.current_stock, p.cost_price, p.sell_price
)
SELECT
    id,
    name AS product_name,
    sku,
    category,
    current_stock,
    total_sold_90days,
    daily_sales_rate,
    ROUND(current_stock * cost_price, 2) AS inventory_investment,
    ROUND(current_stock / NULLIF(daily_sales_rate, 0), 0) AS days_to_sell,
    ROUND((CURRENT_DATE - last_sale_date)::numeric) AS days_since_last_sale,
    CASE
        WHEN total_sold_90days = 0 AND current_stock > 0 THEN 'CRITICO - Nessuna vendita'
        WHEN daily_sales_rate > 0 AND current_stock / daily_sales_rate > 180 THEN 'ATTENZIONE - Più di 6 mesi'
        WHEN daily_sales_rate > 0 AND current_stock / daily_sales_rate > 90 THEN 'ATTENZIONE - Più di 3 mesi'
        WHEN daily_sales_rate > 0 AND current_stock / daily_sales_rate > 60 THEN 'MONITORAGGIO - Più di 2 mesi'
        ELSE 'OK'
    END AS status
FROM product_metrics
WHERE current_stock > 0
ORDER BY
    CASE
        WHEN total_sold_90days = 0 THEN 1
        WHEN daily_sales_rate > 0 THEN 2
        ELSE 3
    END,
    days_since_last_sale DESC,
    inventory_investment DESC;

-- ============================================
-- VIEW: v_alerts_summary
-- ============================================
-- Riepilogo allarmi inventario
CREATE OR REPLACE VIEW v_alerts_summary AS
SELECT
    'Out of Stock' AS alert_type,
    COUNT(*) AS alert_count,
    ROUND(SUM(cost_price * current_stock), 2) AS potential_revenue_lost
FROM products
WHERE current_stock = 0 AND is_active = TRUE
UNION ALL
SELECT
    'Below Minimum' AS alert_type,
    COUNT(*) AS alert_count,
    0 AS potential_revenue_lost
FROM products
WHERE current_stock > 0 AND current_stock < min_stock AND is_active = TRUE
UNION ALL
SELECT
    'Overstocked' AS alert_type,
    COUNT(*) AS alert_count,
    ROUND(SUM(cost_price * (current_stock - max_stock)), 2) AS potential_revenue_lost
FROM products
WHERE current_stock > max_stock AND is_active = TRUE
UNION ALL
SELECT
    'Pending Orders' AS alert_type,
    COUNT(*) AS alert_count,
    ROUND(SUM(total_cost), 2) AS potential_revenue_lost
FROM purchase_orders
WHERE status IN ('PENDING', 'ORDERED');

-- ============================================
-- COMMENTI
-- ============================================
COMMENT ON VIEW v_product_sales_summary IS 'Riepilogo vendite e metriche per prodotto';
COMMENT ON VIEW v_daily_sales_report IS 'Report vendite giornaliere con dettaglio metodi pagamento';
COMMENT ON VIEW v_category_performance IS 'Performance vendite e profitto per categoria';
COMMENT ON VIEW v_supplier_purchase_history IS 'Storico acquisti e statistiche fornitori';
COMMENT ON VIEW v_inventory_valuation IS 'Valutazione inventario e stato stock per categoria';
COMMENT ON VIEW v_stock_movement_summary IS 'Riepilogo movimenti di magazzino per prodotto';
COMMENT ON VIEW v_reorder_recommendations IS 'Raccomandazioni intelligenti di riordino';
COMMENT ON VIEW v_product_profitability IS 'Analisi redditività dettagliata prodotti';
COMMENT ON VIEW v_purchase_order_status IS 'Stato e tracking ordini di acquisto';
COMMENT ON VIEW v_customer_insights IS 'Analisi comportamento clienti';
COMMENT ON VIEW v_slow_moving_products IS 'Identifica prodotti a rotazione lenta';
COMMENT ON VIEW v_alerts_summary IS 'Panoramica allarmi e problemi inventario';

-- ============================================
-- FINE VIEWS
-- ============================================
