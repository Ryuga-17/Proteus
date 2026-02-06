"""
Add test customer for WhatsApp testing
Run this script to add your phone number to the customers table
"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Get database config
db_user = os.getenv('DB_USER')
if not db_user:
    import getpass
    db_user = getpass.getuser()

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'retail_agent_system'),
    'user': db_user,
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

def add_test_customer(phone_number: str, name: str = "Test User", email: str = None):
    """Add a test customer to the database"""
    try:
        # Remove password if empty
        config = {k: v for k, v in db_config.items() if v or k != 'password'}
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Check if customer already exists
        cursor.execute("SELECT customer_id FROM customers WHERE phone = %s", (phone_number,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ Customer already exists with phone {phone_number}")
            print(f"   Customer ID: {existing[0]}")
            cursor.close()
            conn.close()
            return existing[0]
        
        # Generate customer ID
        import uuid
        customer_id = f"CUST-{str(uuid.uuid4())[:8].upper()}"
        
        # Check what columns exist in customers table
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'customers'
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        # Build INSERT statement based on available columns
        if 'phone' in columns:
            if 'email' in columns and email:
                cursor.execute("""
                    INSERT INTO customers (customer_id, name, phone, email, loyalty_tier)
                    VALUES (%s, %s, %s, %s, 'bronze')
                    ON CONFLICT (customer_id) DO UPDATE
                    SET phone = EXCLUDED.phone, name = EXCLUDED.name
                    RETURNING customer_id
                """, (customer_id, name, phone_number, email or f"{phone_number}@test.com"))
            else:
                cursor.execute("""
                    INSERT INTO customers (customer_id, name, phone, loyalty_tier)
                    VALUES (%s, %s, %s, 'bronze')
                    ON CONFLICT (customer_id) DO UPDATE
                    SET phone = EXCLUDED.phone, name = EXCLUDED.name
                    RETURNING customer_id
                """, (customer_id, name, phone_number))
        elif 'phone_number' in columns:
            if 'email' in columns and email:
                cursor.execute("""
                    INSERT INTO customers (customer_id, name, phone_number, email, loyalty_tier)
                    VALUES (%s, %s, %s, %s, 'bronze')
                    ON CONFLICT (customer_id) DO UPDATE
                    SET phone_number = EXCLUDED.phone_number, name = EXCLUDED.name
                    RETURNING customer_id
                """, (customer_id, name, phone_number, email or f"{phone_number}@test.com"))
            else:
                cursor.execute("""
                    INSERT INTO customers (customer_id, name, phone_number, loyalty_tier)
                    VALUES (%s, %s, %s, 'bronze')
                    ON CONFLICT (customer_id) DO UPDATE
                    SET phone_number = EXCLUDED.phone_number, name = EXCLUDED.name
                    RETURNING customer_id
                """, (customer_id, name, phone_number))
        else:
            print("❌ Error: Could not find 'phone' or 'phone_number' column in customers table")
            print(f"   Available columns: {columns}")
            cursor.close()
            conn.close()
            return None
        
        customer_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Test customer added successfully!")
        print(f"   Customer ID: {customer_id}")
        print(f"   Phone: {phone_number}")
        print(f"   Name: {name}")
        return customer_id
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection error: {e}")
        print("   Using in-memory database - customer will be auto-created for testing")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Default test phone number
    test_phone = "+918850833367"
    
    if len(sys.argv) > 1:
        test_phone = sys.argv[1]
    
    print(f"Adding test customer with phone: {test_phone}")
    print("-" * 60)
    
    customer_id = add_test_customer(test_phone, "Vivek")
    
    if customer_id:
        print("\n✅ You can now test WhatsApp authentication!")
        print("   Send 'Hi' to +1 415 523 8886 from WhatsApp")
    else:
        print("\n⚠️  Could not add to database, but in-memory database will work for testing")
