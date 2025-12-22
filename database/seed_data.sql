-- ============================================================================
-- Seed Data for Retail Agent System
-- ============================================================================
-- This file contains sample data to get started with the system
-- ============================================================================

-- ============================================================================
-- 1. LOCATIONS
-- ============================================================================

INSERT INTO locations (location_id, name, type, address, city, state, zip_code, phone) VALUES
('store_main_street', 'Main Street Store', 'store', '123 Main St', 'New York', 'NY', '10001', '555-0101'),
('store_westside_mall', 'Westside Mall Store', 'store', '456 Mall Blvd', 'Los Angeles', 'CA', '90001', '555-0102'),
('godown_central', 'Central Warehouse', 'godown', '789 Industrial Way', 'Chicago', 'IL', '60601', '555-0103'),
('warehouse_east', 'East Coast Warehouse', 'warehouse', '321 Distribution Dr', 'Boston', 'MA', '02101', '555-0104');

-- ============================================================================
-- 2. PRODUCTS & SKUs
-- ============================================================================

-- Sample Products
INSERT INTO products (product_id, title, description, category, brand, gender, base_price, tags) VALUES
('PROD-123', 'Classic White Sweatshirt', 'Comfortable and stylish white sweatshirt for casual wear', 'Tops', 'ComfortWear', 'Unisex', 39.99, ARRAY['sweatshirt', 'casual', 'comfortable', 'white']),
('PROD-456', 'Premium Denim Jeans', 'High-quality denim jeans with classic fit', 'Bottoms', 'DenimCraft', 'Male', 89.99, ARRAY['jeans', 'denim', 'classic', 'casual']),
('PROD-789', 'Elegant Floral Dress', 'Beautiful floral print dress perfect for any occasion', 'Dresses', 'StyleHaven', 'Female', 79.99, ARRAY['dress', 'floral', 'elegant', 'versatile']),
('PROD-101', 'Classic White Oxford Shirt', 'Versatile white shirt for office or casual wear', 'Tops', 'ClassicWear', 'Unisex', 49.99, ARRAY['shirt', 'formal', 'versatile', 'white']);

-- Sample SKUs
INSERT INTO skus (sku, product_id, size, color, variant_name, price, cost, margin) VALUES
-- PROD-123 SKUs
('sku_123_S_WHITE', 'PROD-123', 'S', 'White', 'White - Small', 39.99, 20.00, 19.99),
('sku_123_M_WHITE', 'PROD-123', 'M', 'White', 'White - Medium', 39.99, 20.00, 19.99),
('sku_123_L_WHITE', 'PROD-123', 'L', 'White', 'White - Large', 39.99, 20.00, 19.99),
('sku_123_XL_WHITE', 'PROD-123', 'XL', 'White', 'White - XLarge', 39.99, 20.00, 19.99),

-- PROD-456 SKUs
('sku_456_30_BLUE', 'PROD-456', '30', 'Blue', 'Blue - 30', 89.99, 45.00, 44.99),
('sku_456_32_BLUE', 'PROD-456', '32', 'Blue', 'Blue - 32', 89.99, 45.00, 44.99),
('sku_456_34_BLUE', 'PROD-456', '34', 'Blue', 'Blue - 34', 89.99, 45.00, 44.99),

-- PROD-789 SKUs
('sku_789_S_FLORAL', 'PROD-789', 'S', 'Floral', 'Floral - Small', 79.99, 35.00, 44.99),
('sku_789_M_FLORAL', 'PROD-789', 'M', 'Floral', 'Floral - Medium', 79.99, 35.00, 44.99),
('sku_789_L_FLORAL', 'PROD-789', 'L', 'Floral', 'Floral - Large', 79.99, 35.00, 44.99),

-- PROD-101 SKUs
('sku_101_S_WHITE', 'PROD-101', 'S', 'White', 'White - Small', 49.99, 25.00, 24.99),
('sku_101_M_WHITE', 'PROD-101', 'M', 'White', 'White - Medium', 49.99, 25.00, 24.99),
('sku_101_L_WHITE', 'PROD-101', 'L', 'White', 'White - Large', 49.99, 25.00, 24.99);

-- ============================================================================
-- 3. INVENTORY (Initial Stock Levels)
-- ============================================================================

-- Stock for store_main_street
INSERT INTO inventory (sku, location_id, quantity, reorder_point, safety_stock) VALUES
('sku_123_S_WHITE', 'store_main_street', 5, 3, 2),
('sku_123_M_WHITE', 'store_main_street', 8, 5, 3),
('sku_123_L_WHITE', 'store_main_street', 10, 5, 3),
('sku_456_30_BLUE', 'store_main_street', 15, 5, 3),
('sku_456_32_BLUE', 'store_main_street', 20, 5, 3),
('sku_789_S_FLORAL', 'store_main_street', 3, 2, 1),
('sku_789_M_FLORAL', 'store_main_street', 7, 3, 2);

-- Stock for store_westside_mall
INSERT INTO inventory (sku, location_id, quantity, reorder_point, safety_stock) VALUES
('sku_123_S_WHITE', 'store_westside_mall', 8, 5, 3),
('sku_123_M_WHITE', 'store_westside_mall', 12, 5, 3),
('sku_123_L_WHITE', 'store_westside_mall', 15, 5, 3),
('sku_456_32_BLUE', 'store_westside_mall', 25, 5, 3),
('sku_456_34_BLUE', 'store_westside_mall', 18, 5, 3),
('sku_789_M_FLORAL', 'store_westside_mall', 10, 5, 3),
('sku_789_L_FLORAL', 'store_westside_mall', 6, 3, 2);

-- Stock for godown_central (Warehouse)
INSERT INTO inventory (sku, location_id, quantity, reorder_point, safety_stock) VALUES
('sku_123_S_WHITE', 'godown_central', 500, 100, 50),
('sku_123_M_WHITE', 'godown_central', 600, 100, 50),
('sku_123_L_WHITE', 'godown_central', 550, 100, 50),
('sku_123_XL_WHITE', 'godown_central', 400, 100, 50),
('sku_456_30_BLUE', 'godown_central', 300, 50, 25),
('sku_456_32_BLUE', 'godown_central', 350, 50, 25),
('sku_456_34_BLUE', 'godown_central', 320, 50, 25),
('sku_789_S_FLORAL', 'godown_central', 200, 50, 25),
('sku_789_M_FLORAL', 'godown_central', 250, 50, 25),
('sku_789_L_FLORAL', 'godown_central', 220, 50, 25),
('sku_101_S_WHITE', 'godown_central', 400, 100, 50),
('sku_101_M_WHITE', 'godown_central', 450, 100, 50),
('sku_101_L_WHITE', 'godown_central', 420, 100, 50);

-- ============================================================================
-- 4. CUSTOMERS
-- ============================================================================

INSERT INTO customers (customer_id, email, name, phone, loyalty_points, loyalty_tier, total_spent, total_orders) VALUES
('c123', 'alex.johnson@email.com', 'Alex Johnson', '555-1001', 1250, 'gold', 1250.00, 15),
('c456', 'sarah.wilson@email.com', 'Sarah Wilson', '555-1002', 450, 'silver', 450.00, 8),
('c789', 'mike.chen@email.com', 'Mike Chen', '555-1003', 150, 'bronze', 150.00, 3),
('c999', 'emma.davis@email.com', 'Emma Davis', '555-1004', 2500, 'platinum', 2500.00, 30),
('default_user', 'user@example.com', 'Default User', '555-0000', 0, 'bronze', 0.00, 0),
('CUST001', 'cust001@example.com', 'Customer One', '555-2001', 100, 'bronze', 100.00, 2),
('CUST777', 'cust777@example.com', 'Customer 777', '555-2777', 500, 'silver', 500.00, 10),
('CUST888', 'cust888@example.com', 'Customer 888', '555-2888', 300, 'bronze', 300.00, 5);

-- Customer Preferences (for recommendations)
INSERT INTO customer_preferences (customer_id, category_preferences, brand_preferences, size_preferences, budget_min, budget_max) VALUES
('c123', ARRAY['Tops', 'Bottoms'], ARRAY['ComfortWear', 'DenimCraft'], ARRAY['M', 'L'], 20.00, 150.00),
('c456', ARRAY['Dresses', 'Tops'], ARRAY['StyleHaven'], ARRAY['S', 'M'], 30.00, 100.00),
('c999', ARRAY['Tops', 'Bottoms', 'Dresses'], ARRAY['StyleHaven', 'ComfortWear'], ARRAY['M', 'L', 'XL'], 50.00, 200.00);

-- ============================================================================
-- 5. LOYALTY TIER RULES
-- ============================================================================

INSERT INTO loyalty_tier_rules (tier, name, discount_percent, points_earn_rate, min_spend, benefits) VALUES
('bronze', 'Bronze Member Discount', 5.00, 1.00, 0.00, ARRAY['5% discount on all purchases', '1x points on purchases']),
('silver', 'Silver Member Discount', 10.00, 1.25, 100.00, ARRAY['10% discount', '1.25x points', 'Free shipping on orders $50+']),
('gold', 'Gold Member Discount', 15.00, 1.50, 500.00, ARRAY['15% discount', '1.5x points', 'Free shipping', 'Early access to sales']),
('platinum', 'Platinum Member Discount', 20.00, 2.00, 1000.00, ARRAY['20% discount', '2x points', 'Free shipping', 'VIP customer service', 'Exclusive events']);

-- ============================================================================
-- 6. COUPONS
-- ============================================================================

INSERT INTO coupons (coupon_code, name, description, discount_type, discount_value, min_purchase_amount, valid_from, valid_until, usage_limit, is_active) VALUES
('SAVE20', '20% Off Coupon', 'Save 20% on your purchase', 'percent_off', 20.00, 50.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year', 1000, TRUE),
('SAVE10', '10% Off Coupon', 'Save 10% on your purchase', 'percent_off', 10.00, 25.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year', 5000, TRUE),
('FLAT5', '$5 Off Coupon', 'Get $5 off your order', 'dollar_off', 5.00, 30.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '6 months', 2000, TRUE),
('WELCOME15', 'Welcome Discount', '15% off for new customers', 'percent_off', 15.00, 40.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '3 months', 10000, TRUE);

-- ============================================================================
-- 7. SAMPLE SALES HISTORY (Last 30 days)
-- ============================================================================

-- Generate some sample sales history for velocity calculations
INSERT INTO sales_history (sku, location_id, quantity, sale_date) VALUES
-- sku_123 (high demand)
('sku_123_M_WHITE', 'store_main_street', 10, CURRENT_DATE - INTERVAL '1 day'),
('sku_123_M_WHITE', 'store_main_street', 12, CURRENT_DATE - INTERVAL '2 days'),
('sku_123_M_WHITE', 'store_main_street', 15, CURRENT_DATE - INTERVAL '3 days'),
('sku_123_M_WHITE', 'store_main_street', 14, CURRENT_DATE - INTERVAL '4 days'),
('sku_123_M_WHITE', 'store_main_street', 20, CURRENT_DATE - INTERVAL '5 days'),
('sku_123_L_WHITE', 'store_main_street', 8, CURRENT_DATE - INTERVAL '1 day'),
('sku_123_L_WHITE', 'store_main_street', 10, CURRENT_DATE - INTERVAL '2 days'),

-- sku_456 (medium demand)
('sku_456_32_BLUE', 'store_main_street', 5, CURRENT_DATE - INTERVAL '1 day'),
('sku_456_32_BLUE', 'store_main_street', 6, CURRENT_DATE - INTERVAL '2 days'),
('sku_456_32_BLUE', 'store_main_street', 5, CURRENT_DATE - INTERVAL '3 days'),
('sku_456_32_BLUE', 'store_main_street', 7, CURRENT_DATE - INTERVAL '4 days'),
('sku_456_32_BLUE', 'store_main_street', 6, CURRENT_DATE - INTERVAL '5 days');

-- ============================================================================
-- Sample Orders (Optional - for testing)
-- ============================================================================

-- You can add sample orders here if needed for testing
-- INSERT INTO orders (order_id, customer_id, status, subtotal, total_amount, shipping_address) VALUES
-- ('ORD-12345', 'c123', 'delivered', 119.98, 119.98, '123 Customer St, City, State 12345');

-- ============================================================================
-- Verify Data
-- ============================================================================

-- Check counts
SELECT 'Locations' as table_name, COUNT(*) as count FROM locations
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'SKUs', COUNT(*) FROM skus
UNION ALL
SELECT 'Inventory Records', COUNT(*) FROM inventory
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers
UNION ALL
SELECT 'Coupons', COUNT(*) FROM coupons;

