-- ============================================
-- SISTEMA DI GESTIONE INVENTARIO
-- Stored Procedures e Functions
-- PostgreSQL
-- ============================================

-- ============================================
-- FUNCTION: calculate_reorder_quantity
-- Calcola quantità suggerita per riordino
-- ============================================
CREATE OR REPLACE FUNCTION calculate_reorder_quantity(p_product_id INTEGER)
RETURNS TABLE(quantity INTEGER, cost DECIMAL) AS $$
DECLARE
    v_current_stock INTEGER;
    v_reorder_point INTEGER;
    v_daily_sales DECIMAL;
    v_supplier_id INTEGER;
    v_cost_price DECIMAL;
    v_suggested_qty INTEGER;
BEGIN
    -- Ottieni dati prodotto
    SELECT
        current_stock,
        reorder_point,
        supplier_id,
        cost_price
    INTO v_current_stock, v_reorder_point, v_supplier_id, v_cost_price
    FROM products
    WHERE id = p_product_id;

    -- Calcola vendite medie giornaliere (ultimi 90 giorni)
    SELECT COALESCE(SUM(quantity) / 90.0, 0)
    INTO v_daily_sales
    FROM sale_items si
    JOIN sales s ON si.sale_id = s.id
    WHERE si.product_id = p_product_id
        AND s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days';

    -- Calcola quantità suggerita
    v_suggested_qty := GREATEST(
        v_reorder_point - v_current_stock,
        CEIL(v_daily_sales * 30)
    );

    RETURN QUERY SELECT v_suggested_qty, ROUND(v_suggested_qty * v_cost_price, 2);
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: update_stock_after_sale
-- Aggiorna stock dopo una vendita
-- ============================================
CREATE OR REPLACE FUNCTION update_stock_after_sale(p_sale_id INTEGER)
RETURNS VOID AS $$
DECLARE
    v_product_id INTEGER;
    v_quantity INTEGER;
BEGIN
    -- Per ogni item venduto
    FOR v_product_id, v_quantity IN
        SELECT product_id, quantity
        FROM sale_items
        WHERE sale_id = p_sale_id
    LOOP
        -- Aggiorna stock prodotto
        UPDATE products
        SET current_stock = current_stock - v_quantity
        WHERE id = v_product_id;

        -- Registra movimento di stock
        INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, notes)
        VALUES (v_product_id, 'OUT', v_quantity, p_sale_id, 'Vendita SA-' || p_sale_id);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: process_purchase_order_receipt
-- Processa ricezione ordine di acquisto
-- ============================================
CREATE OR REPLACE FUNCTION process_purchase_order_receipt(p_order_id INTEGER)
RETURNS VOID AS $$
DECLARE
    v_product_id INTEGER;
    v_quantity INTEGER;
BEGIN
    -- Aggiorna stato ordine
    UPDATE purchase_orders
    SET status = 'RECEIVED'
    WHERE id = p_order_id;

    -- Per ogni item dell'ordine
    FOR v_product_id, v_quantity IN
        SELECT product_id, quantity
        FROM purchase_items
        WHERE order_id = p_order_id
    LOOP
        -- Aggiorna stock prodotto
        UPDATE products
        SET current_stock = current_stock + v_quantity
        WHERE id = v_product_id;

        -- Registra movimento di stock
        INSERT INTO stock_movements (product_id, movement_type, quantity, reference_id, notes)
        VALUES (v_product_id, 'IN', v_quantity, p_order_id, 'Ricezione PO-' || p_order_id);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: get_product_sales_velocity
-- Calcola velocità di vendita prodotto
-- ============================================
CREATE OR REPLACE FUNCTION get_product_sales_velocity(p_product_id INTEGER, p_days INTEGER DEFAULT 30)
RETURNS TABLE(
    daily_avg DECIMAL,
    weekly_avg DECIMAL,
    monthly_avg DECIMAL,
    days_of_stock INTEGER
) AS $$
DECLARE
    v_current_stock INTEGER;
    v_total_sold INTEGER;
    v_daily_rate DECIMAL;
BEGIN
    -- Ottieni stock attuale
    SELECT current_stock INTO v_current_stock
    FROM products
    WHERE id = p_product_id;

    -- Calcola vendite nel periodo
    SELECT COALESCE(SUM(si.quantity), 0)
    INTO v_total_sold
    FROM sale_items si
    JOIN sales s ON si.sale_id = s.id
    WHERE si.product_id = p_product_id
        AND s.status = 'COMPLETED'
        AND s.sale_date >= CURRENT_DATE - (p_days || ' days')::INTERVAL;

    -- Calcola velocità
    v_daily_rate := v_total_sold::DECIMAL / p_days;

    RETURN QUERY
    SELECT
        v_daily_rate,
        v_daily_rate * 7,
        v_daily_rate * 30,
        CASE WHEN v_daily_rate > 0 THEN FLOOR(v_current_stock::DECIMAL / v_daily_rate) ELSE NULL END;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- PROCEDURE: create_sale_with_stock_update
-- Crea vendita e aggiorna stock in transazione
-- ============================================
CREATE OR REPLACE PROCEDURE create_sale_with_stock_update(
    p_customer_name VARCHAR,
    p_payment_method VARCHAR,
    p_items JSONB
) AS $$
DECLARE
    v_sale_id INTEGER;
    v_item JSON;
    v_product_id INTEGER;
    v_quantity INTEGER;
    v_unit_price DECIMAL;
    v_total_amount DECIMAL := 0;
BEGIN
    -- Crea vendita
    INSERT INTO sales (customer_name, payment_method, total_amount)
    VALUES (p_customer_name, p_payment_method, 0)
    RETURNING id INTO v_sale_id;

    -- Processa ogni item
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
        v_product_id := (v_item->>'product_id')::INTEGER;
        v_quantity := (v_item->>'quantity')::INTEGER;

        -- Ottieni prezzo di vendita
        SELECT sell_price INTO v_unit_price
        FROM products
        WHERE id = v_product_id;

        -- Verifica disponibilità stock
        IF NOT EXISTS (
            SELECT 1 FROM products
            WHERE id = v_product_id AND current_stock >= v_quantity
        ) THEN
            RAISE EXCEPTION 'Stock insufficiente per prodotto %', v_product_id;
        END IF;

        -- Crea sale_item
        INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal)
        VALUES (v_sale_id, v_product_id, v_quantity, v_unit_price, v_quantity * v_unit_price);

        v_total_amount := v_total_amount + (v_quantity * v_unit_price);
    END LOOP;

    -- Aggiorna totale vendita
    UPDATE sales
    SET total_amount = v_total_amount
    WHERE id = v_sale_id;

    -- Aggiorna stock
    PERFORM update_stock_after_sale(v_sale_id);

    RAISE NOTICE 'Vendita creata: ID=%, Totale=%', v_sale_id, v_total_amount;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: get_inventory_turnover
-- Calcola rotazione inventario
-- ============================================
CREATE OR REPLACE FUNCTION get_inventory_turnover(p_days INTEGER DEFAULT 90)
RETURNS TABLE(
    product_id INTEGER,
    product_name VARCHAR,
    turnover_rate DECIMAL,
    days_to_sell INTEGER,
    classification VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH sales_data AS (
        SELECT
            p.id,
            p.name,
            p.current_stock,
            COALESCE(SUM(si.quantity), 0) AS sold_qty
        FROM products p
        LEFT JOIN sale_items si ON p.id = si.product_id
        LEFT JOIN sales s ON si.sale_id = s.id
            AND s.status = 'COMPLETED'
            AND s.sale_date >= CURRENT_DATE - (p_days || ' days')::INTERVAL
        WHERE p.is_active = TRUE
        GROUP BY p.id, p.name, p.current_stock
    )
    SELECT
        id,
        name,
        CASE
            WHEN sold_qty > 0 THEN ROUND((sold_qty::DECIMAL / p_days) * 365, 2)
            ELSE 0
        END AS turnover_rate,
        CASE
            WHEN sold_qty > 0 THEN FLOOR(p_days::DECIMAL / (sold_qty::DECIMAL / p_days))
            ELSE NULL
        END AS days_to_sell,
        CASE
            WHEN sold_qty = 0 THEN 'NO SALES'
            WHEN current_stock = 0 THEN 'OUT OF STOCK'
            WHEN (sold_qty::DECIMAL / p_days) > 0 AND current_stock / (sold_qty::DECIMAL / p_days) < 30 THEN 'FAST MOVING'
            WHEN (sold_qty::DECIMAL / p_days) > 0 AND current_stock / (sold_qty::DECIMAL / p_days) < 90 THEN 'NORMAL MOVING'
            ELSE 'SLOW MOVING'
        END AS classification
    FROM sales_data;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: generate_reorder_report
-- Genera report riordini
-- ============================================
CREATE OR REPLACE FUNCTION generate_reorder_report()
RETURNS TABLE(
    product_name VARCHAR,
    current_stock INTEGER,
    reorder_point INTEGER,
    suggested_order_qty INTEGER,
    estimated_cost DECIMAL,
    priority VARCHAR,
    supplier_name VARCHAR,
    supplier_email VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH product_metrics AS (
        SELECT
            p.id,
            p.name,
            p.current_stock,
            p.reorder_point,
            p.cost_price,
            p.supplier_id,
            COALESCE(SUM(si.quantity) / 90.0, 0) AS daily_sales
        FROM products p
        LEFT JOIN sale_items si ON p.id = si.product_id
        LEFT JOIN sales s ON si.sale_id = s.id
            AND s.status = 'COMPLETED'
            AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days'
        WHERE p.is_active = TRUE
        GROUP BY p.id, p.name, p.current_stock, p.reorder_point, p.cost_price, p.supplier_id
    )
    SELECT
        pm.name,
        pm.current_stock,
        pm.reorder_point,
        GREATEST(
            (pm.reorder_point - pm.current_stock),
            CEIL(pm.daily_sales * 30)
        )::INTEGER,
        ROUND(GREATEST(
            (pm.reorder_point - pm.current_stock),
            CEIL(pm.daily_sales * 30)
        ) * pm.cost_price, 2),
        CASE
            WHEN pm.current_stock <= 0 THEN 'URGENT - Out of Stock'
            WHEN pm.current_stock < pm.reorder_point THEN 'URGENT - Below Reorder'
            WHEN pm.daily_sales > 0 AND pm.current_stock / pm.daily_sales < 30 THEN 'ORDER - Low Stock'
            ELSE 'OK'
        END,
        s.name,
        s.email
    FROM product_metrics pm
    LEFT JOIN suppliers s ON pm.supplier_id = s.id
    WHERE pm.current_stock <= pm.reorder_point
        OR pm.daily_sales > 0
    ORDER BY
        CASE
            WHEN pm.current_stock <= 0 THEN 1
            WHEN pm.current_stock < pm.reorder_point THEN 2
            ELSE 3
        END,
        GREATEST((pm.reorder_point - pm.current_stock), CEIL(pm.daily_sales * 30)) DESC;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: calculate_product_profit_margin
-- Calcola margine profitto prodotto
-- ============================================
CREATE OR REPLACE FUNCTION calculate_product_profit_margin(p_product_id INTEGER)
RETURNS TABLE(
    product_name VARCHAR,
    cost_price DECIMAL,
    sell_price DECIMAL,
    profit_per_unit DECIMAL,
    margin_percentage DECIMAL,
    total_sold INTEGER,
    total_revenue DECIMAL,
    total_cost DECIMAL,
    total_profit DECIMAL,
    actual_margin_percentage DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.name,
        p.cost_price,
        p.sell_price,
        ROUND(p.sell_price - p.cost_price, 2),
        ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2),
        COALESCE(SUM(si.quantity), 0),
        ROUND(COALESCE(SUM(si.subtotal), 0), 2),
        ROUND(COALESCE(SUM(si.quantity * p.cost_price), 0), 2),
        ROUND(COALESCE(SUM(si.subtotal - si.quantity * p.cost_price), 0), 2),
        ROUND(COALESCE(SUM(si.subtotal - si.quantity * p.cost_price), 0) * 100.0 /
              NULLIF(SUM(si.subtotal), 0), 2)
    FROM products p
    LEFT JOIN sale_items si ON p.id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.id AND s.status = 'COMPLETED'
    WHERE p.id = p_product_id
    GROUP BY p.id, p.name, p.cost_price, p.sell_price;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: get_sales_analytics
-- Analytics vendite per periodo
-- ============================================
CREATE OR REPLACE FUNCTION get_sales_analytics(p_start_date DATE, p_end_date DATE)
RETURNS TABLE(
    period VARCHAR,
    total_sales INTEGER,
    total_revenue DECIMAL,
    avg_order_value DECIMAL,
    total_items_sold INTEGER,
    unique_customers INTEGER,
    best_selling_product VARCHAR,
    top_category VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH period_data AS (
        SELECT
            TO_CHAR(s.sale_date, 'YYYY-MM') AS period,
            COUNT(*) AS sales_count,
            ROUND(SUM(s.total_amount), 2) AS revenue,
            ROUND(AVG(s.total_amount), 2) AS avg_order,
            SUM(si.quantity) AS items_sold,
            COUNT(DISTINCT s.customer_name) AS customers
        FROM sales s
        JOIN sale_items si ON s.id = si.sale_id
        WHERE s.status = 'COMPLETED'
            AND s.sale_date::DATE BETWEEN p_start_date AND p_end_date
        GROUP BY TO_CHAR(s.sale_date, 'YYYY-MM')
    ),
    best_products AS (
        SELECT
            p.name,
            SUM(si.quantity) AS qty
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        JOIN products p ON si.product_id = p.id
        WHERE s.status = 'COMPLETED'
            AND s.sale_date::DATE BETWEEN p_start_date AND p_end_date
        GROUP BY p.name
        ORDER BY qty DESC
        LIMIT 1
    ),
    top_categories AS (
        SELECT
            c.name,
            COUNT(DISTINCT si.sale_id) AS sales_count
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        JOIN products p ON si.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        WHERE s.status = 'COMPLETED'
            AND s.sale_date::DATE BETWEEN p_start_date AND p_end_date
        GROUP BY c.name
        ORDER BY sales_count DESC
        LIMIT 1
    )
    SELECT
        pd.period,
        pd.sales_count::INTEGER,
        pd.revenue,
        pd.avg_order,
        pd.items_sold::INTEGER,
        pd.customers::INTEGER,
        bp.name,
        tc.name
    FROM period_data pd
    CROSS JOIN best_products bp
    CROSS JOIN top_categories tc
    ORDER BY pd.period;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGER: auto_update_sale_total
-- Aggiorna totale vendita automaticamente
-- ============================================
CREATE OR REPLACE FUNCTION auto_update_sale_total()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        UPDATE sales
        SET total_amount = (
            SELECT SUM(subtotal)
            FROM sale_items
            WHERE sale_id = COALESCE(NEW.sale_id, OLD.sale_id)
        )
        WHERE id = COALESCE(NEW.sale_id, OLD.sale_id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE sales
        SET total_amount = (
            SELECT SUM(subtotal)
            FROM sale_items
            WHERE sale_id = OLD.sale_id
        )
        WHERE id = OLD.sale_id;
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Creazione trigger
DROP TRIGGER IF EXISTS trigger_auto_update_sale_total ON sale_items;
CREATE TRIGGER trigger_auto_update_sale_total
    AFTER INSERT OR UPDATE OR DELETE ON sale_items
    FOR EACH ROW
    EXECUTE FUNCTION auto_update_sale_total();

-- ============================================
-- PROCEDURE: bulk_update_products_category
-- Aggiornamento massivo categoria prodotti
-- ============================================
CREATE OR REPLACE PROCEDURE bulk_update_products_category(
    p_old_category_id INTEGER,
    p_new_category_id INTEGER
) AS $$
BEGIN
    -- Verifica esistenza categorie
    IF NOT EXISTS (SELECT 1 FROM categories WHERE id = p_new_category_id) THEN
        RAISE EXCEPTION 'Nuova categoria non trovata: %', p_new_category_id;
    END IF;

    -- Aggiorna prodotti
    UPDATE products
    SET category_id = p_new_category_id
    WHERE category_id = p_old_category_id;

    RAISE NOTICE 'Aggiornati % prodotti dalla categoria % alla %',
        (SELECT COUNT(*) FROM products WHERE category_id = p_new_category_id),
        p_old_category_id,
        p_new_category_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: check_stock_levels
-- Verifica livelli stock e restituisce alert
-- ============================================
CREATE OR REPLACE FUNCTION check_stock_levels()
RETURNS TABLE(
    alert_type VARCHAR,
    product_name VARCHAR,
    current_stock INTEGER,
    threshold_value INTEGER,
    message VARCHAR
) AS $$
BEGIN
    -- Prodotti esauriti
    RETURN QUERY
    SELECT
        'OUT_OF_STOCK',
        p.name,
        p.current_stock,
        0,
        'Prodotto esaurito - Riordino immediato necessario'
    FROM products p
    WHERE p.current_stock = 0 AND p.is_active = TRUE

    UNION ALL

    -- Prodotti sotto il minimo
    SELECT
        'BELOW_MINIMUM',
        p.name,
        p.current_stock,
        p.min_stock,
        'Stock sotto il minimo - Consigliato riordino'
    FROM products p
    WHERE p.current_stock > 0
        AND p.current_stock < p.min_stock
        AND p.is_active = TRUE

    UNION ALL

    -- Prodotti sovrastock
    SELECT
        'OVERSTOCKED',
        p.name,
        p.current_stock,
        p.max_stock,
        'Stock eccessivo - Valutare sconti o promozioni'
    FROM products p
    WHERE p.current_stock > p.max_stock
        AND p.is_active = TRUE

    ORDER BY alert_type, current_stock;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- COMMENTI
-- ============================================
COMMENT ON FUNCTION calculate_reorder_quantity IS 'Calcola quantità suggerita per riordino prodotto';
COMMENT ON FUNCTION update_stock_after_sale IS 'Aggiorna stock dopo vendita';
COMMENT ON FUNCTION process_purchase_order_receipt IS 'Processa ricezione ordine acquisto';
COMMENT ON FUNCTION get_product_sales_velocity IS 'Calcola velocità di vendita prodotto';
COMMENT ON PROCEDURE create_sale_with_stock_update IS 'Crea vendita e aggiorna stock in transazione';
COMMENT ON FUNCTION get_inventory_turnover IS 'Calcola rotazione inventario';
COMMENT ON FUNCTION generate_reorder_report IS 'Genera report riordini';
COMMENT ON FUNCTION calculate_product_profit_margin IS 'Calcola margine profitto prodotto';
COMMENT ON FUNCTION get_sales_analytics IS 'Analytics vendite per periodo';
COMMENT ON FUNCTION check_stock_levels IS 'Verifica livelli stock e genera alert';
COMMENT ON PROCEDURE bulk_update_products_category IS 'Aggiornamento massivo categoria prodotti';

-- ============================================
-- ESEMPI DI UTILIZZO
-- ============================================

-- Esempio 1: Ottenere quantità riordino
-- SELECT * FROM calculate_reorder_quantity(1);

-- Esempio 2: Ottenere velocità vendita
-- SELECT * FROM get_product_sales_velocity(1, 30);

-- Esempio 3: Generare report riordini
-- SELECT * FROM generate_reorder_report();

-- Esempio 4: Creare vendita con aggiornamento stock
-- CALL create_sale_with_stock_update(
--     'Mario Rossi',
--     'CREDIT_CARD',
--     '[{"product_id": 1, "quantity": 2}, {"product_id": 3, "quantity": 1}]'::JSONB
-- );

-- Esempio 5: Verificare livelli stock
-- SELECT * FROM check_stock_levels();

-- Esempio 6: Ottenere rotazione inventario
-- SELECT * FROM get_inventory_turnover(90);

-- Esempio 7: Calcolare margine profitto
-- SELECT * FROM calculate_product_profit_margin(1);

-- Esempio 8: Analytics vendite
-- SELECT * FROM get_sales_analytics('2024-01-01'::DATE, '2024-03-31'::DATE);

-- ============================================
-- FINE PROCEDURES E FUNCTIONS
-- ============================================
