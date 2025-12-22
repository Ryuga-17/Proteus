-- ============================================================================
-- Retail Agent System - Complete Database Schema
-- ============================================================================
-- This schema supports all agents: Inventory, Fulfillment, Payment, 
-- Loyalty, Support, and Recommendation agents.
-- 
-- Database: PostgreSQL (can be adapted for MySQL/MariaDB)
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. LOCATIONS (Stores, Warehouses, Godowns)
-- ============================================================================

CREATE TABLE locations (
    location_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('store', 'warehouse', 'godown')),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    phone VARCHAR(20),
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_type ON locations(type);
CREATE INDEX idx_locations_active ON locations(is_active);

-- ============================================================================
-- 2. PRODUCTS & SKUs
-- ============================================================================

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    brand VARCHAR(100),
    gender VARCHAR(20) CHECK (gender IN ('Male', 'Female', 'Unisex', 'Kids')),
    base_price DECIMAL(10, 2) NOT NULL,
    tags TEXT[], -- Array of tags for search/recommendations
    images TEXT[], -- Array of image URLs
    metadata JSONB, -- Additional flexible data (size chart, care instructions, etc.)
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_tags ON products USING GIN(tags);
CREATE INDEX idx_products_metadata ON products USING GIN(metadata);

-- SKUs represent specific product variants (size, color combinations)
CREATE TABLE skus (
    sku VARCHAR(100) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    size VARCHAR(20),
    color VARCHAR(50),
    variant_name VARCHAR(255), -- e.g., "Red - Large"
    price DECIMAL(10, 2), -- Override price if different from base
    cost DECIMAL(10, 2), -- Cost for margin calculations
    margin DECIMAL(10, 2), -- Profit margin
    barcode VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_skus_product ON skus(product_id);
CREATE INDEX idx_skus_active ON skus(is_active);

-- ============================================================================
-- 3. INVENTORY (Stock Levels by Location)
-- ============================================================================

CREATE TABLE inventory (
    inventory_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) NOT NULL REFERENCES skus(sku) ON DELETE CASCADE,
    location_id VARCHAR(50) NOT NULL REFERENCES locations(location_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reserved_quantity INTEGER DEFAULT 0 CHECK (reserved_quantity >= 0),
    available_quantity INTEGER GENERATED ALWAYS AS (quantity - reserved_quantity) STORED,
    reorder_point INTEGER DEFAULT 0,
    safety_stock INTEGER DEFAULT 5,
    last_restocked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sku, location_id)
);

CREATE INDEX idx_inventory_sku ON inventory(sku);
CREATE INDEX idx_inventory_location ON inventory(location_id);
CREATE INDEX idx_inventory_available ON inventory(available_quantity);
CREATE INDEX idx_inventory_low_stock ON inventory(reorder_point) WHERE available_quantity <= reorder_point;

-- ============================================================================
-- 4. SALES HISTORY (for velocity calculations)
-- ============================================================================

CREATE TABLE sales_history (
    sale_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) NOT NULL REFERENCES skus(sku) ON DELETE CASCADE,
    location_id VARCHAR(50) REFERENCES locations(location_id),
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL DEFAULT CURRENT_DATE,
    order_id VARCHAR(50), -- Reference to order if applicable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sales_sku_date ON sales_history(sku, sale_date);
CREATE INDEX idx_sales_location ON sales_history(location_id);
CREATE INDEX idx_sales_order ON sales_history(order_id);

-- ============================================================================
-- 5. CUSTOMERS
-- ============================================================================

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    loyalty_points INTEGER DEFAULT 0,
    loyalty_tier VARCHAR(20) DEFAULT 'bronze' CHECK (loyalty_tier IN ('bronze', 'silver', 'gold', 'platinum')),
    total_spent DECIMAL(10, 2) DEFAULT 0.00,
    total_orders INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_order_date TIMESTAMP
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_tier ON customers(loyalty_tier);
CREATE INDEX idx_customers_points ON customers(loyalty_points);

-- Customer preferences for recommendations
CREATE TABLE customer_preferences (
    preference_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    category_preferences TEXT[], -- Preferred categories
    brand_preferences TEXT[], -- Preferred brands
    size_preferences TEXT[], -- Preferred sizes
    style_preferences TEXT[], -- Style tags
    budget_min DECIMAL(10, 2),
    budget_max DECIMAL(10, 2),
    metadata JSONB, -- Additional preferences
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(customer_id)
);

CREATE INDEX idx_preferences_customer ON customer_preferences(customer_id);
CREATE INDEX idx_preferences_categories ON customer_preferences USING GIN(category_preferences);

-- ============================================================================
-- 6. ORDERS
-- ============================================================================

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'confirmed', 'processing', 'shipped', 'delivered', 
        'cancelled', 'returned', 'refunded'
    )),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
    shipping_cost DECIMAL(10, 2) DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Order items (products in each order)
CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(50) NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL REFERENCES skus(sku),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    line_total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_sku ON order_items(sku);

-- ============================================================================
-- 7. PAYMENTS & TRANSACTIONS
-- ============================================================================

CREATE TABLE payment_methods (
    payment_method_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('credit_card', 'debit_card', 'upi', 'paypal', 'wallet', 'bank_transfer')),
    provider VARCHAR(100), -- e.g., 'Visa', 'Mastercard', 'GPay'
    last_four VARCHAR(4), -- Last 4 digits for cards
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    encrypted_details JSONB, -- Encrypted payment details
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payment_methods_customer ON payment_methods(customer_id);
CREATE INDEX idx_payment_methods_active ON payment_methods(is_active);

CREATE TABLE transactions (
    transaction_id VARCHAR(100) PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES orders(order_id),
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id),
    payment_method_id UUID REFERENCES payment_methods(payment_method_id),
    type VARCHAR(50) NOT NULL CHECK (type IN ('payment', 'refund', 'loyalty_points', 'partial_refund')),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'success', 'failed', 'cancelled', 'refunded')),
    payment_method_type VARCHAR(50),
    gateway_response JSONB, -- Response from payment gateway
    loyalty_points_used INTEGER DEFAULT 0,
    loyalty_points_earned INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_order ON transactions(order_id);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_date ON transactions(created_at);

-- ============================================================================
-- 8. FULFILLMENT (Shipments & Reservations)
-- ============================================================================

CREATE TABLE shipments (
    shipment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(50) NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    tracking_number VARCHAR(100) UNIQUE,
    carrier VARCHAR(100), -- e.g., 'UPS', 'FedEx', 'DHL'
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'exception')),
    shipping_address TEXT NOT NULL,
    estimated_delivery_date DATE,
    actual_delivery_date DATE,
    current_location VARCHAR(255),
    tracking_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_shipments_order ON shipments(order_id);
CREATE INDEX idx_shipments_tracking ON shipments(tracking_number);
CREATE INDEX idx_shipments_status ON shipments(status);

-- In-store reservations (for pickup orders)
CREATE TABLE reservations (
    reservation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(50) NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    location_id VARCHAR(50) NOT NULL REFERENCES locations(location_id),
    pickup_code VARCHAR(50) UNIQUE,
    status VARCHAR(50) DEFAULT 'reserved' CHECK (status IN ('reserved', 'ready', 'picked_up', 'expired', 'cancelled')),
    reserved_until TIMESTAMP NOT NULL,
    picked_up_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reservations_order ON reservations(order_id);
CREATE INDEX idx_reservations_location ON reservations(location_id);
CREATE INDEX idx_reservations_code ON reservations(pickup_code);
CREATE INDEX idx_reservations_expiry ON reservations(reserved_until) WHERE status = 'reserved';

-- ============================================================================
-- 9. COUPONS & PROMOTIONS
-- ============================================================================

CREATE TABLE coupons (
    coupon_code VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    discount_type VARCHAR(50) NOT NULL CHECK (discount_type IN ('percent_off', 'dollar_off', 'free_shipping', 'buy_x_get_y')),
    discount_value DECIMAL(10, 2),
    min_purchase_amount DECIMAL(10, 2) DEFAULT 0.00,
    max_discount_amount DECIMAL(10, 2), -- For percent off, cap the discount
    applicable_categories TEXT[],
    applicable_products TEXT[], -- Product IDs
    applicable_brands TEXT[],
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP,
    usage_limit INTEGER, -- Total uses allowed
    usage_count INTEGER DEFAULT 0,
    customer_limit INTEGER DEFAULT 1, -- Uses per customer
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_coupons_active ON coupons(is_active);
CREATE INDEX idx_coupons_validity ON coupons(valid_from, valid_until);
CREATE INDEX idx_coupons_code ON coupons(coupon_code);

-- Coupon usage tracking
CREATE TABLE coupon_usage (
    usage_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coupon_code VARCHAR(50) NOT NULL REFERENCES coupons(coupon_code),
    order_id VARCHAR(50) NOT NULL REFERENCES orders(order_id),
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id),
    discount_amount DECIMAL(10, 2) NOT NULL,
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_coupon_usage_order ON coupon_usage(order_id);
CREATE INDEX idx_coupon_usage_customer ON coupon_usage(customer_id);
CREATE INDEX idx_coupon_usage_code ON coupon_usage(coupon_code);

-- Loyalty tier discounts (part of loyalty system)
CREATE TABLE loyalty_tier_rules (
    tier VARCHAR(20) PRIMARY KEY CHECK (tier IN ('bronze', 'silver', 'gold', 'platinum')),
    name VARCHAR(100) NOT NULL,
    discount_percent DECIMAL(5, 2) NOT NULL, -- e.g., 5.00 for 5%
    points_earn_rate DECIMAL(5, 2) DEFAULT 1.00, -- Multiplier for points
    min_spend DECIMAL(10, 2) DEFAULT 0.00,
    benefits TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 10. RETURNS & EXCHANGES
-- ============================================================================

CREATE TABLE returns (
    return_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(50) NOT NULL REFERENCES orders(order_id),
    order_item_id UUID NOT NULL REFERENCES order_items(order_item_id),
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id),
    return_type VARCHAR(50) NOT NULL CHECK (return_type IN ('refund', 'exchange')),
    reason TEXT,
    status VARCHAR(50) DEFAULT 'requested' CHECK (status IN ('requested', 'approved', 'in_transit', 'received', 'processed', 'rejected')),
    return_label_url TEXT,
    refund_amount DECIMAL(10, 2),
    refund_transaction_id VARCHAR(100),
    exchange_order_id VARCHAR(50), -- If exchange, reference to new order
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_returns_order ON returns(order_id);
CREATE INDEX idx_returns_customer ON returns(customer_id);
CREATE INDEX idx_returns_status ON returns(status);

-- ============================================================================
-- 11. SUPPLIER ORDERS (Procurement)
-- ============================================================================

CREATE TABLE supplier_orders (
    purchase_order_id VARCHAR(50) PRIMARY KEY,
    supplier_name VARCHAR(255),
    supplier_contact TEXT,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'ordered', 'partially_received', 'received', 'cancelled')),
    total_amount DECIMAL(10, 2),
    order_date DATE DEFAULT CURRENT_DATE,
    expected_delivery_date DATE,
    received_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE supplier_order_items (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    purchase_order_id VARCHAR(50) NOT NULL REFERENCES supplier_orders(purchase_order_id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL REFERENCES skus(sku),
    quantity INTEGER NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    line_total DECIMAL(10, 2) NOT NULL,
    received_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_supplier_orders_status ON supplier_orders(status);
CREATE INDEX idx_supplier_order_items_po ON supplier_order_items(purchase_order_id);

-- ============================================================================
-- 12. TRANSFER LOGS (Inventory Transfers between Locations)
-- ============================================================================

CREATE TABLE inventory_transfers (
    transfer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) NOT NULL REFERENCES skus(sku),
    from_location_id VARCHAR(50) NOT NULL REFERENCES locations(location_id),
    to_location_id VARCHAR(50) NOT NULL REFERENCES locations(location_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_transit', 'completed', 'cancelled')),
    logistics_cost DECIMAL(10, 2),
    reason TEXT,
    initiated_by VARCHAR(100), -- User/system that initiated
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (from_location_id != to_location_id)
);

CREATE INDEX idx_transfers_sku ON inventory_transfers(sku);
CREATE INDEX idx_transfers_from ON inventory_transfers(from_location_id);
CREATE INDEX idx_transfers_to ON inventory_transfers(to_location_id);
CREATE INDEX idx_transfers_status ON inventory_transfers(status);

-- ============================================================================
-- TRIGGERS for updated_at timestamps
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_locations_updated_at BEFORE UPDATE ON locations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_skus_updated_at BEFORE UPDATE ON skus FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_inventory_updated_at BEFORE UPDATE ON inventory FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_shipments_updated_at BEFORE UPDATE ON shipments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reservations_updated_at BEFORE UPDATE ON reservations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_coupons_updated_at BEFORE UPDATE ON coupons FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS for Common Queries
-- ============================================================================

-- View: Current stock levels with product info
CREATE OR REPLACE VIEW v_current_inventory AS
SELECT 
    i.inventory_id,
    i.sku,
    s.product_id,
    p.title AS product_title,
    p.category,
    p.brand,
    s.size,
    s.color,
    i.location_id,
    l.name AS location_name,
    l.type AS location_type,
    i.quantity,
    i.reserved_quantity,
    i.available_quantity,
    i.reorder_point,
    i.safety_stock,
    CASE 
        WHEN i.available_quantity <= 0 THEN 'out_of_stock'
        WHEN i.available_quantity <= i.reorder_point THEN 'low_stock'
        ELSE 'in_stock'
    END AS stock_status
FROM inventory i
JOIN skus s ON i.sku = s.sku
JOIN products p ON s.product_id = p.product_id
JOIN locations l ON i.location_id = l.location_id
WHERE s.is_active = TRUE AND p.is_active = TRUE AND l.is_active = TRUE;

-- View: Sales velocity (last 30 days average)
CREATE OR REPLACE VIEW v_sales_velocity AS
SELECT 
    sku,
    AVG(daily_quantity) AS avg_daily_sales,
    SUM(daily_quantity) AS total_30day_sales
FROM (
    SELECT 
        sku,
        sale_date,
        SUM(quantity) AS daily_quantity
    FROM sales_history
    WHERE sale_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY sku, sale_date
) daily_sales
GROUP BY sku;

-- View: Customer order summary
CREATE OR REPLACE VIEW v_customer_orders AS
SELECT 
    c.customer_id,
    c.name,
    c.loyalty_tier,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    MAX(o.order_date) AS last_order_date,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('cancelled')
GROUP BY c.customer_id, c.name, c.loyalty_tier;

