-- ============================================
-- SISTEMA DI GESTIONE INVENTARIO
-- Schema del Database Completo
-- PostgreSQL
-- ============================================

-- Eliminazione delle tabelle se esistono (in ordine di dipendenza)
DROP TABLE IF EXISTS stock_movements CASCADE;
DROP TABLE IF EXISTS purchase_items CASCADE;
DROP TABLE IF EXISTS purchase_orders CASCADE;
DROP TABLE IF EXISTS sale_items CASCADE;
DROP TABLE IF EXISTS sales CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- ============================================
-- TABELLA CATEGORIES
-- ============================================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABELLA SUPPLIERS
-- ============================================
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- ============================================
-- TABELLA PRODUCTS
-- ============================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    sell_price DECIMAL(10, 2) NOT NULL,
    current_stock INTEGER DEFAULT 0,
    min_stock INTEGER DEFAULT 10,
    max_stock INTEGER DEFAULT 100,
    reorder_point INTEGER DEFAULT 15,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_cost_price CHECK (cost_price > 0),
    CONSTRAINT check_sell_price CHECK (sell_price > 0),
    CONSTRAINT check_stock_positive CHECK (current_stock >= 0),
    CONSTRAINT check_min_stock CHECK (min_stock >= 0),
    CONSTRAINT check_max_stock CHECK (max_stock > min_stock),
    CONSTRAINT check_reorder_point CHECK (reorder_point >= min_stock)
);

-- Index per queries frequenti
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_supplier ON products(supplier_id);
CREATE INDEX idx_products_stock ON products(current_stock);
CREATE INDEX idx_products_active ON products(is_active);

-- ============================================
-- TABELLA SALES
-- ============================================
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR(200),
    total_amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'COMPLETED',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_total_amount CHECK (total_amount >= 0),
    CONSTRAINT check_payment_method CHECK (payment_method IN ('CASH', 'CREDIT_CARD', 'DEBIT_CARD', 'BANK_TRANSFER', 'PAYPAL'))
);

-- Index per queries frequenti
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sales_customer ON sales(customer_name);
CREATE INDEX idx_sales_status ON sales(status);

-- ============================================
-- TABELLA SALE_ITEMS
-- ============================================
CREATE TABLE sale_items (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT check_quantity CHECK (quantity > 0),
    CONSTRAINT check_unit_price CHECK (unit_price > 0),
    CONSTRAINT check_subtotal CHECK (subtotal >= 0)
);

-- Index per queries frequenti
CREATE INDEX idx_sale_items_sale ON sale_items(sale_id);
CREATE INDEX idx_sale_items_product ON sale_items(product_id);

-- ============================================
-- TABELLA PURCHASE_ORDERS
-- ============================================
CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    order_date DATE NOT NULL,
    expected_date DATE,
    status VARCHAR(20) DEFAULT 'PENDING',
    total_cost DECIMAL(12, 2) DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_status CHECK (status IN ('PENDING', 'ORDERED', 'RECEIVED', 'CANCELLED')),
    CONSTRAINT check_total_cost CHECK (total_cost >= 0)
);

-- Index per queries frequenti
CREATE INDEX idx_purchase_orders_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_purchase_orders_date ON purchase_orders(order_date);
CREATE INDEX idx_purchase_orders_status ON purchase_orders(status);

-- ============================================
-- TABELLA PURCHASE_ITEMS
-- ============================================
CREATE TABLE purchase_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    CONSTRAINT check_quantity_po CHECK (quantity > 0),
    CONSTRAINT check_unit_cost CHECK (unit_cost > 0)
);

-- Index per queries frequenti
CREATE INDEX idx_purchase_items_order ON purchase_items(order_id);
CREATE INDEX idx_purchase_items_product ON purchase_items(product_id);

-- ============================================
-- TABELLA STOCK_MOVEMENTS
-- ============================================
CREATE TABLE stock_movements (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    movement_type VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    reference_id INTEGER,
    movement_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    CONSTRAINT check_movement_type CHECK (movement_type IN ('IN', 'OUT', 'ADJUSTMENT', 'TRANSFER', 'RETURN', 'DAMAGE')),
    CONSTRAINT check_movement_quantity CHECK (quantity != 0)
);

-- Index per queries frequenti
CREATE INDEX idx_stock_movements_product ON stock_movements(product_id);
CREATE INDEX idx_stock_movements_type ON stock_movements(movement_type);
CREATE INDEX idx_stock_movements_date ON stock_movements(movement_date);
CREATE INDEX idx_stock_movements_reference ON stock_movements(reference_id);

-- ============================================
-- VIEWS UTILI
-- ============================================

-- View: Riepilogo prodotti con stato stock
CREATE OR REPLACE VIEW v_product_summary AS
SELECT
    p.id,
    p.name,
    p.sku,
    p.cost_price,
    p.sell_price,
    p.current_stock,
    p.min_stock,
    p.max_stock,
    p.reorder_point,
    c.name AS category_name,
    s.name AS supplier_name,
    ROUND((p.sell_price - p.cost_price) / p.sell_price * 100, 2) AS margin_percentage,
    ROUND(p.sell_price - p.cost_price, 2) AS profit_per_unit,
    CASE
        WHEN p.current_stock <= 0 THEN 'OUT_OF_STOCK'
        WHEN p.current_stock <= p.min_stock THEN 'LOW_STOCK'
        WHEN p.current_stock >= p.max_stock THEN 'OVERSTOCK'
        ELSE 'IN_STOCK'
    END AS stock_status,
    CASE
        WHEN p.current_stock <= p.reorder_point THEN TRUE
        ELSE FALSE
    END AS needs_reorder,
    p.is_active
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN suppliers s ON p.supplier_id = s.id;

-- View: Performance fornitori
CREATE OR REPLACE VIEW v_supplier_performance AS
SELECT
    s.id,
    s.name,
    s.contact_person,
    s.email,
    s.phone,
    COUNT(DISTINCT po.id) AS total_orders,
    SUM(po.total_cost) AS total_purchased,
    ROUND(AVG(po.total_cost), 2) AS avg_order_value,
    COUNT(DISTINCT p.id) AS products_supplied,
    ROUND(SUM(po.total_cost) * 100.0 / NULLIF(SUM(SUM(po.total_cost)) OVER (), 0), 2) AS purchase_percentage
FROM suppliers s
LEFT JOIN purchase_orders po ON s.id = po.supplier_id AND po.status = 'RECEIVED'
LEFT JOIN purchase_items poi ON po.id = poi.order_id
LEFT JOIN products p ON poi.product_id = p.id
GROUP BY s.id, s.name, s.contact_person, s.email, s.phone;

-- View: Vendite mensili
CREATE OR REPLACE VIEW v_monthly_sales AS
SELECT
    EXTRACT(YEAR FROM sale_date) AS year,
    EXTRACT(MONTH FROM sale_date) AS month,
    TO_CHAR(sale_date, 'Month') AS month_name,
    COUNT(*) AS total_sales,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_sale_value,
    COUNT(DISTINCT customer_name) AS unique_customers
FROM sales
WHERE status = 'COMPLETED'
GROUP BY EXTRACT(YEAR FROM sale_date), EXTRACT(MONTH FROM sale_date), TO_CHAR(sale_date, 'Month')
ORDER BY year DESC, month DESC;

-- View: Prodotti con stock basso
CREATE OR REPLACE VIEW v_low_stock AS
SELECT
    p.id,
    p.name,
    p.sku,
    p.current_stock,
    p.min_stock,
    p.reorder_point,
    c.name AS category_name,
    (p.reorder_point - p.current_stock) AS units_to_order,
    ROUND((p.reorder_point - p.current_stock) * p.cost_price, 2) AS estimated_cost
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.current_stock <= p.reorder_point
AND p.is_active = TRUE
ORDER BY (p.reorder_point - p.current_stock) DESC;

-- ============================================
-- FUNZIONI TRIGGER
-- ============================================

-- Funzione per aggiornare updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger per categories
CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger per suppliers
CREATE TRIGGER update_suppliers_updated_at
    BEFORE UPDATE ON suppliers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger per products
CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Funzione per aggiornare il totale degli ordini di acquisto
CREATE OR REPLACE FUNCTION update_purchase_order_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE purchase_orders
    SET total_cost = (
        SELECT SUM(quantity * unit_cost)
        FROM purchase_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_purchase_total
    AFTER INSERT OR UPDATE OR DELETE ON purchase_items
    FOR EACH ROW
    EXECUTE FUNCTION update_purchase_order_total();

-- ============================================
-- COMMENTI
-- ============================================

COMMENT ON TABLE categories IS 'Categorie di prodotti';
COMMENT ON TABLE suppliers IS 'Fornitori di prodotti';
COMMENT ON TABLE products IS 'Catalogo prodotti con informazioni su prezzi e stock';
COMMENT ON TABLE sales IS 'Vendite effettuate';
COMMENT ON TABLE sale_items IS 'Dettagli prodotti venduti';
COMMENT ON TABLE purchase_orders IS 'Ordini di acquisto ai fornitori';
COMMENT ON TABLE purchase_items IS 'Dettagli ordini di acquisto';
COMMENT ON TABLE stock_movements IS 'Movimenti di magazzino (entrata/uscita/ajuste)';

COMMENT ON VIEW v_product_summary IS 'Riepilogo prodotti con stato stock e margini';
COMMENT ON VIEW v_supplier_performance IS 'Analisi performance fornitori';
COMMENT ON VIEW v_monthly_sales IS 'Vendite aggregate per mese';
COMMENT ON VIEW v_low_stock IS 'Prodotti che necessitano riordino';

-- ============================================
-- FINE SCHEMA
-- ============================================
