# Database Schema Documentation

## Overview

This database schema supports the entire Retail Agent System, including all agents:
- **Inventory Agent** - Stock management, transfers, procurement
- **Fulfillment Agent** - Shipments and in-store reservations
- **Payment Agent** - Transactions and payment processing
- **Loyalty Agent** - Points, discounts, and tier management
- **Support Agent** - Order tracking, returns, exchanges
- **Recommendation Agent** - Product recommendations and customer preferences

## Database Choice

### Recommended: PostgreSQL

**Why PostgreSQL?**
- ✅ Native support for JSON/JSONB (for flexible metadata)
- ✅ Array types (for tags, preferences)
- ✅ Excellent indexing capabilities
- ✅ Full ACID compliance
- ✅ Rich feature set (triggers, views, functions)
- ✅ Strong performance for complex queries
- ✅ Widely used and well-documented

### Alternative Options

1. **MySQL/MariaDB**
   - Can work but lacks some features (limited JSON support in older versions)
   - Would need schema adaptations

2. **MongoDB (NoSQL)**
   - Good for flexible schemas
   - Better for recommendation data (product embeddings)
   - Would need hybrid approach (SQL for transactions, NoSQL for products)
   - Not recommended for financial/transaction data

3. **Hybrid Approach**
   - PostgreSQL for transactional data (orders, payments, inventory)
   - MongoDB/Elasticsearch for product catalog and recommendations
   - Qdrant (already used) for vector search

## Schema Structure

### Core Tables

1. **locations** - Stores, warehouses, godowns
2. **products** - Product catalog
3. **skus** - Product variants (size, color)
4. **inventory** - Stock levels by location
5. **customers** - Customer information and loyalty
6. **orders** - Order headers
7. **order_items** - Order line items
8. **transactions** - Payment transactions
9. **shipments** - Shipping information
10. **reservations** - In-store pickup reservations

### Supporting Tables

- **sales_history** - For velocity calculations
- **customer_preferences** - For recommendations
- **payment_methods** - Saved payment methods
- **coupons** - Discount codes
- **returns** - Return/exchange tracking
- **supplier_orders** - Procurement orders
- **inventory_transfers** - Transfer logs

### Views

- **v_current_inventory** - Enhanced inventory view with product info
- **v_sales_velocity** - Sales velocity calculations
- **v_customer_orders** - Customer order summaries

## Key Design Decisions

### 1. SKU-Based Inventory

- **SKU** = Stock Keeping Unit (specific product variant)
- One product can have multiple SKUs (different sizes/colors)
- Inventory tracked at SKU level for accuracy

### 2. Location-Based Inventory

- Stock tracked per location (store/warehouse)
- Enables multi-location operations
- Supports transfers between locations

### 3. Reserved Quantity

- `reserved_quantity` tracks items reserved for orders/pickups
- `available_quantity = quantity - reserved_quantity`
- Prevents overselling

### 4. Sales Velocity Tracking

- `sales_history` table tracks daily sales by SKU
- Enables demand forecasting
- Supports reorder point calculations

### 5. Flexible Metadata

- JSONB columns for extensible data:
  - `products.metadata` - Size charts, care instructions, etc.
  - `customers.preferences.metadata` - Additional preferences
  - `transactions.gateway_response` - Payment gateway responses

### 6. Array Columns

- PostgreSQL arrays for:
  - `products.tags` - Searchable tags
  - `products.images` - Image URLs
  - `customer_preferences.category_preferences` - Preferred categories

## Indexes

Strategic indexes created for:
- Foreign keys (for joins)
- Common query patterns (status, dates)
- Search fields (tags, categories)
- Unique constraints (SKUs, order IDs)

## Data Types

- **VARCHAR** - IDs, codes, short text
- **TEXT** - Long text, descriptions
- **DECIMAL(10,2)** - Money amounts (prevents floating point errors)
- **INTEGER** - Quantities, counts
- **TIMESTAMP** - Dates and times
- **JSONB** - Flexible structured data
- **TEXT[]** - Arrays (tags, preferences)
- **UUID** - Auto-generated IDs where appropriate

## Relationships

```
customers
  ├── orders
  │   ├── order_items
  │   ├── transactions
  │   ├── shipments
  │   └── reservations
  ├── payment_methods
  ├── customer_preferences
  └── coupon_usage

products
  └── skus
      ├── inventory (by location)
      ├── order_items
      ├── sales_history
      ├── inventory_transfers
      └── supplier_order_items

locations
  ├── inventory
  ├── reservations
  └── inventory_transfers

coupons
  └── coupon_usage
```

## Setup Instructions

### 1. Install PostgreSQL

```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download from https://www.postgresql.org/download/windows/
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE retail_agent_db;
CREATE USER retail_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE retail_agent_db TO retail_user;
\q
```

### 3. Run Schema

```bash
# Connect to the new database
psql -U retail_user -d retail_agent_db -f schema.sql
```

### 4. Seed Initial Data

```bash
psql -U retail_user -d retail_agent_db -f seed_data.sql
```

## Connection Configuration

### Environment Variables

```env
# .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_agent_db
DB_USER=retail_user
DB_PASSWORD=your_password
DB_SSL_MODE=disable  # Use 'require' for production
```

### Python Connection (using psycopg2)

```python
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
```

### Using SQLAlchemy ORM

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

## Migration Strategy

### From Mock Data to Real Database

1. **Phase 1: Setup**
   - Create database and schema
   - Seed initial data (locations, products)

2. **Phase 2: Inventory Migration**
   - Migrate inventory data from MockDB
   - Update inventory tools to use database

3. **Phase 3: Customer Data**
   - Migrate customer profiles
   - Set up loyalty points system

4. **Phase 4: Orders & Transactions**
   - Migrate order data
   - Update payment processing

5. **Phase 5: Full Integration**
   - Update all agents to use database
   - Remove mock data classes

## Performance Considerations

### 1. Indexing
- Indexes on frequently queried columns
- Composite indexes for common query patterns
- GIN indexes for array/JSONB columns

### 2. Partitioning (for large datasets)
- Consider partitioning `sales_history` by date
- Partition `transactions` by date for large volumes

### 3. Caching
- Cache frequently accessed data (product catalog, customer profiles)
- Use Redis for session data and hot data

### 4. Read Replicas
- Use read replicas for reporting queries
- Keep master for writes

## Security

### Best Practices

1. **Use Connection Pooling**
   ```python
   from sqlalchemy.pool import QueuePool
   engine = create_engine(DATABASE_URL, poolclass=QueuePool, pool_size=10)
   ```

2. **Parameterized Queries**
   - Always use parameterized queries to prevent SQL injection
   - SQLAlchemy ORM handles this automatically

3. **Encrypt Sensitive Data**
   - Encrypt payment details before storing
   - Use encryption at rest for production

4. **Access Control**
   - Use database roles and permissions
   - Separate read/write users

5. **Backup Strategy**
   - Regular automated backups
   - Point-in-time recovery enabled

## Maintenance

### Regular Tasks

1. **Vacuum/Analyze** (PostgreSQL)
   ```sql
   VACUUM ANALYZE;
   ```

2. **Index Maintenance**
   - Monitor index usage
   - Rebuild indexes if needed

3. **Data Archiving**
   - Archive old orders (>2 years)
   - Archive old sales_history (>1 year)

4. **Monitor Performance**
   - Use EXPLAIN ANALYZE for slow queries
   - Monitor database metrics

## Next Steps

1. Review and customize schema for your needs
2. Run schema creation script
3. Seed initial data
4. Update agent tools to use database
5. Test thoroughly before production deployment

