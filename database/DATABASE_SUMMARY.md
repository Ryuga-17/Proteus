# Database Structure Summary

## Overview

This database schema is designed to support all agents in the Retail Agent System with a complete, production-ready structure.

## Entity Relationship Diagram (Simplified)

```
┌─────────────┐
│  locations  │
└──────┬──────┘
       │
       ├──────────────┐
       │              │
┌──────▼──────┐  ┌────▼─────────┐
│  inventory  │  │ reservations │
└──────┬──────┘  └──────────────┘
       │
       │
┌──────▼──────┐
│    skus     │
└──────┬──────┘
       │
       ├──────────────┐
       │              │
┌──────▼──────┐  ┌────▼──────────┐
│  products   │  │ order_items   │
└─────────────┘  └────┬──────────┘
                      │
                ┌─────▼─────┐
                │   orders  │
                └─────┬─────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
    ┌────▼────┐  ┌───▼────┐  ┌────▼──────┐
    │transact │  │shipment│  │  returns  │
    │  -ions  │  │    s   │  │           │
    └────┬────┘  └────────┘  └───────────┘
         │
    ┌────▼──────────┐
    │   customers   │
    └────┬──────────┘
         │
    ┌────▼──────────────┐
    │customer_preferences│
    └───────────────────┘
```

## Core Tables by Agent

### Inventory Agent
- **locations** - Stores, warehouses, godowns
- **inventory** - Stock levels by SKU and location
- **skus** - Product variants (size, color)
- **products** - Product catalog
- **sales_history** - For velocity calculations
- **inventory_transfers** - Transfer logs
- **supplier_orders** - Procurement orders

### Fulfillment Agent
- **orders** - Order headers
- **order_items** - Order line items
- **shipments** - Shipping information
- **reservations** - In-store pickup reservations

### Payment Agent
- **transactions** - All payment transactions
- **payment_methods** - Saved payment methods
- **orders** - Links to orders

### Loyalty Agent
- **customers** - Customer data with loyalty points/tier
- **loyalty_tier_rules** - Tier discount rules
- **coupons** - Discount codes
- **coupon_usage** - Usage tracking

### Support Agent
- **orders** - Order information
- **shipments** - Tracking information
- **returns** - Return/exchange tracking
- **transactions** - Payment/refund info

### Recommendation Agent
- **products** - Product catalog with tags
- **customers** - Customer information
- **customer_preferences** - Preference data
- **orders** - Purchase history for recommendations

## Key Features

### 1. Multi-Location Support
- Inventory tracked per location
- Supports transfers between locations
- Location-based reservations

### 2. Flexible Product Structure
- Products → SKUs (variants)
- JSONB for flexible metadata
- Array columns for tags/images

### 3. Complete Order Lifecycle
- Orders with status tracking
- Order items with pricing
- Shipments and reservations
- Returns and exchanges

### 4. Financial Tracking
- Transaction history
- Payment methods
- Refund tracking
- Cost/margin tracking

### 5. Customer Management
- Loyalty points and tiers
- Purchase history
- Preferences for recommendations
- Multiple addresses

### 6. Sales Analytics
- Sales history by SKU/date
- Sales velocity calculations (view)
- Customer order summaries (view)

## Data Flow Examples

### Purchase Flow
```
1. Check inventory (inventory table)
2. Create order (orders + order_items)
3. Reserve stock (update inventory.reserved_quantity)
4. Process payment (transactions)
5. Create shipment/reservation (shipments/reservations)
6. Update inventory (decrement quantity)
7. Update sales_history
8. Update customer loyalty points
```

### Return Flow
```
1. Find order (orders + order_items)
2. Create return record (returns)
3. Generate refund (transactions)
4. Update inventory (increment quantity)
5. Update customer if needed
```

### Inventory Transfer Flow
```
1. Check source stock (inventory)
2. Create transfer record (inventory_transfers)
3. Update source location (decrement inventory)
4. Update destination location (increment inventory)
```

## Important Constraints

### Business Rules Enforced

1. **No Negative Stock**
   - CHECK constraint: `quantity >= 0`
   - Available = quantity - reserved

2. **Reserved Stock Protection**
   - Reserved quantity tracked separately
   - Cannot oversell available stock

3. **Referential Integrity**
   - Foreign keys ensure data consistency
   - CASCADE deletes for related data

4. **Order Status Flow**
   - CHECK constraint enforces valid status transitions

5. **Unique Constraints**
   - SKU + Location (one inventory record per combination)
   - Order IDs, tracking numbers, coupon codes

## Indexing Strategy

### Primary Indexes
- All primary keys (automatic)
- Foreign keys for joins
- Unique constraints

### Performance Indexes
- Status columns (orders.status, shipments.status)
- Date columns (order_date, sale_date)
- Location/SKU combinations
- Customer lookups (email, customer_id)

### Special Indexes
- GIN indexes on arrays (tags, preferences)
- GIN indexes on JSONB (metadata)
- Composite indexes for common queries

## Scalability Considerations

### For Large Scale

1. **Partitioning**
   - Partition `sales_history` by date (monthly)
   - Partition `transactions` by date

2. **Archiving**
   - Archive orders > 2 years old
   - Archive sales_history > 1 year old

3. **Read Replicas**
   - Use for reporting queries
   - Reduce load on primary database

4. **Caching**
   - Cache product catalog
   - Cache customer profiles
   - Use Redis for hot data

## Security Considerations

1. **Data Encryption**
   - Encrypt payment details (payment_methods.encrypted_details)
   - Use encryption at rest in production

2. **Access Control**
   - Use database roles
   - Separate read/write users
   - Limit permissions per agent

3. **SQL Injection Prevention**
   - Use parameterized queries
   - SQLAlchemy ORM handles this

4. **Audit Trail**
   - created_at/updated_at on all tables
   - Consider adding audit tables for critical changes

## Maintenance

### Regular Tasks

1. **Vacuum/Analyze** (PostgreSQL)
   ```sql
   VACUUM ANALYZE;
   ```

2. **Backup**
   - Daily automated backups
   - Point-in-time recovery enabled

3. **Monitor**
   - Slow query log
   - Index usage
   - Table sizes

4. **Optimize**
   - Rebuild indexes periodically
   - Update statistics

## Migration from Mock Data

See `DATABASE_GUIDE.md` for step-by-step migration instructions.

## Files

- **schema.sql** - Complete database schema
- **seed_data.sql** - Sample data for testing
- **README.md** - Detailed documentation
- **DATABASE_GUIDE.md** - Integration guide
- **DATABASE_SUMMARY.md** - This file

