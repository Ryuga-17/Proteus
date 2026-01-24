-- Add test customer for WhatsApp testing
-- Run this in PostgreSQL: psql retail_agent_system -f add_customer.sql

-- Add your phone number as a customer
INSERT INTO customers (customer_id, name, phone, email, loyalty_points, loyalty_tier, total_spent, total_orders)
VALUES (
    'CUST-WHATSAPP-001',
    'Vivek',
    '+918850833367',
    'vivek@test.com',
    0,
    'bronze',
    0.00,
    0
)
ON CONFLICT (customer_id) DO UPDATE
SET phone = EXCLUDED.phone, name = EXCLUDED.name;

-- Verify it was added
SELECT customer_id, name, phone, email FROM customers WHERE phone = '+918850833367';
