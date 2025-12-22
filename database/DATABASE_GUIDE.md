# Database Integration Guide

## Quick Start

### 1. Setup Database

```bash
# Create database
createdb retail_agent_db

# Run schema
psql -d retail_agent_db -f schema.sql

# Seed initial data
psql -d retail_agent_db -f seed_data.sql
```

### 2. Install Python Dependencies

```bash
pip install psycopg2-binary sqlalchemy python-dotenv
```

### 3. Configure Environment

Add to `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_agent_db
DB_USER=your_username
DB_PASSWORD=your_password
```

## Database Abstraction Layer

### Option 1: SQLAlchemy ORM (Recommended)

Create `database/db_session.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Option 2: Direct psycopg2

Create `database/db_connection.py`:

```python
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor():
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
```

## Updating Agent Tools

### Example: Inventory Tools with Database

Replace `Inventory agent/inventory_tools.py` MockDB with:

```python
from database.db_session import SessionLocal
from sqlalchemy import text

class InventoryDB:
    """Database-backed inventory operations."""
    
    def get_stock(self, sku: str) -> dict:
        """Get stock levels for SKU across all locations."""
        with SessionLocal() as db:
            result = db.execute(
                text("""
                    SELECT location_id, quantity, reserved_quantity, available_quantity
                    FROM inventory
                    WHERE sku = :sku
                """),
                {"sku": sku}
            ).fetchall()
            
            return {
                row.location_id: {
                    "quantity": row.quantity,
                    "reserved": row.reserved_quantity,
                    "available": row.available_quantity
                }
                for row in result
            }
    
    def update_stock(self, location_id: str, sku: str, quantity_change: int) -> bool:
        """Update stock level (atomic operation)."""
        with SessionLocal() as db:
            try:
                db.execute(
                    text("""
                        UPDATE inventory
                        SET quantity = quantity + :change
                        WHERE sku = :sku AND location_id = :location_id
                        AND (quantity + :change) >= 0
                        RETURNING inventory_id
                    """),
                    {
                        "sku": sku,
                        "location_id": location_id,
                        "change": quantity_change
                    }
                )
                
                if db.rowcount == 0:
                    return False
                
                db.commit()
                return True
            except Exception:
                db.rollback()
                return False
    
    def get_sales_velocity(self, sku: str) -> float:
        """Calculate average daily sales velocity."""
        with SessionLocal() as db:
            result = db.execute(
                text("SELECT avg_daily_sales FROM v_sales_velocity WHERE sku = :sku"),
                {"sku": sku}
            ).fetchone()
            
            return float(result.avg_daily_sales) if result else 0.0

# Replace MockDB() with InventoryDB()
db = InventoryDB()
```

### Example: Customer/Loyalty Tools

```python
from database.db_session import SessionLocal
from sqlalchemy import text

def get_customer_profile(customer_id: str) -> dict:
    """Get customer profile with loyalty info."""
    with SessionLocal() as db:
        result = db.execute(
            text("""
                SELECT c.*, ltr.discount_percent, ltr.points_earn_rate
                FROM customers c
                LEFT JOIN loyalty_tier_rules ltr ON c.loyalty_tier = ltr.tier
                WHERE c.customer_id = :customer_id
            """),
            {"customer_id": customer_id}
        ).fetchone()
        
        if result:
            return dict(result)
        return None

def update_loyalty_points(customer_id: str, points_change: int) -> bool:
    """Update customer loyalty points."""
    with SessionLocal() as db:
        try:
            db.execute(
                text("""
                    UPDATE customers
                    SET loyalty_points = GREATEST(0, loyalty_points + :change)
                    WHERE customer_id = :customer_id
                """),
                {"customer_id": customer_id, "change": points_change}
            )
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
```

### Example: Order Creation

```python
from database.db_session import SessionLocal
from sqlalchemy import text
from datetime import datetime

def create_order(customer_id: str, items: list, shipping_address: str) -> str:
    """Create a new order with items."""
    order_id = f"ORD-{int(datetime.now().timestamp())}"
    
    with SessionLocal() as db:
        try:
            # Calculate totals
            subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
            total = subtotal  # Add tax/shipping later
            
            # Create order
            db.execute(
                text("""
                    INSERT INTO orders 
                    (order_id, customer_id, status, subtotal, total_amount, shipping_address)
                    VALUES (:order_id, :customer_id, 'pending', :subtotal, :total, :address)
                """),
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "subtotal": subtotal,
                    "total": total,
                    "address": shipping_address
                }
            )
            
            # Create order items
            for item in items:
                db.execute(
                    text("""
                        INSERT INTO order_items
                        (order_id, sku, quantity, unit_price, line_total)
                        VALUES (:order_id, :sku, :qty, :price, :total)
                    """),
                    {
                        "order_id": order_id,
                        "sku": item['sku'],
                        "qty": item['quantity'],
                        "price": item['unit_price'],
                        "total": item['quantity'] * item['unit_price']
                    }
                )
            
            db.commit()
            return order_id
        except Exception as e:
            db.rollback()
            raise
```

## Migration Checklist

- [ ] Database created and schema loaded
- [ ] Initial data seeded
- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] Inventory tools updated
- [ ] Customer/loyalty tools updated
- [ ] Order creation/retrieval updated
- [ ] Payment transaction logging added
- [ ] Fulfillment tracking added
- [ ] Returns processing added
- [ ] All mock data classes replaced
- [ ] Integration tests passed
- [ ] Performance tested

## Common Queries

### Get Current Inventory Status

```sql
SELECT * FROM v_current_inventory 
WHERE location_id = 'store_main_street' 
AND stock_status = 'low_stock';
```

### Get Customer Order History

```sql
SELECT o.*, COUNT(oi.order_item_id) as item_count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.customer_id = 'c123'
GROUP BY o.order_id
ORDER BY o.order_date DESC;
```

### Get Sales Velocity

```sql
SELECT sku, avg_daily_sales, total_30day_sales
FROM v_sales_velocity
WHERE avg_daily_sales > 10
ORDER BY avg_daily_sales DESC;
```

### Get Low Stock Items

```sql
SELECT * FROM v_current_inventory
WHERE available_quantity <= reorder_point
ORDER BY available_quantity ASC;
```

## Next Steps

1. Start with inventory tools (most critical)
2. Then customer/loyalty system
3. Then order management
4. Finally, payments and fulfillment
5. Test thoroughly at each stage

