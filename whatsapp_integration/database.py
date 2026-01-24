"""
Database operations for WhatsApp integration
Handles OTP storage and session management
"""
import os
import sys
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import uuid

logger = logging.getLogger(__name__)

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from whatsapp_integration.models import AuthState, SessionInfo, AuthFlowContext


class WhatsAppDatabase:
    """Database handler for WhatsApp integration"""
    
    def __init__(self):
        """Initialize database connection"""
        # Try to load .env file if not already loaded
        try:
            from dotenv import load_dotenv
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env_path = os.path.join(project_root, '.env')
            if os.path.exists(env_path):
                load_dotenv(env_path, override=True)
        except ImportError:
            pass
        
        # Get database config from environment
        # Default user to current system user if not specified
        db_user = os.getenv('DB_USER')
        if not db_user:
            import getpass
            db_user = getpass.getuser()
        
        db_password = os.getenv('DB_PASSWORD', '')
        
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'retail_agent_system'),
            'user': db_user,
            'password': db_password,
            'port': os.getenv('DB_PORT', '5432')
        }
        
        logger.info(f"Database config: host={self.db_config['host']}, db={self.db_config['database']}, user={self.db_config['user']}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            # Remove password from config if empty to avoid auth issues
            config = {k: v for k, v in self.db_config.items() if v or k != 'password'}
            conn = psycopg2.connect(**config)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def initialize_tables(self):
        """Create necessary tables for WhatsApp integration"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Enable UUID extension if not already enabled
            try:
                cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
                conn.commit()
                logger.info("UUID extension enabled")
            except Exception as e:
                logger.warning(f"Could not enable UUID extension (may already exist): {e}")
            
            # Check if customers table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'customers'
                );
            """)
            customers_table_exists = cursor.fetchone()[0]
            
            # WhatsApp Sessions table
            # Use conditional foreign key - only if customers table exists
            if customers_table_exists:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS whatsapp_sessions (
                        session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        whatsapp_user_id VARCHAR(50) UNIQUE NOT NULL,
                        customer_id VARCHAR(50) REFERENCES customers(customer_id) ON DELETE SET NULL,
                        auth_state VARCHAR(50) NOT NULL DEFAULT 'unauthenticated',
                        phone_number VARCHAR(20),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        metadata JSONB DEFAULT '{}',
                        CONSTRAINT valid_auth_state CHECK (auth_state IN ('unauthenticated', 'waiting_for_phone', 'waiting_for_otp', 'authenticated', 'expired', 'waiting_for_stepup'))
                    )
                """)
            else:
                # Create without foreign key constraint if customers table doesn't exist
                logger.warning("customers table not found - creating whatsapp_sessions without foreign key constraint")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS whatsapp_sessions (
                        session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        whatsapp_user_id VARCHAR(50) UNIQUE NOT NULL,
                        customer_id VARCHAR(50),
                        auth_state VARCHAR(50) NOT NULL DEFAULT 'unauthenticated',
                        phone_number VARCHAR(20),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        metadata JSONB DEFAULT '{}',
                        CONSTRAINT valid_auth_state CHECK (auth_state IN ('unauthenticated', 'waiting_for_phone', 'waiting_for_otp', 'authenticated', 'expired', 'waiting_for_stepup'))
                    )
                """)
            
            # Create index on whatsapp_user_id for fast lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_user_id 
                ON whatsapp_sessions(whatsapp_user_id)
            """)
            
            # Create index on customer_id for reverse lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_customer_id 
                ON whatsapp_sessions(customer_id)
            """)
            
            # OTP storage table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS whatsapp_otps (
                    otp_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    whatsapp_user_id VARCHAR(50) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    otp_code VARCHAR(6) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    verified BOOLEAN DEFAULT FALSE,
                    verified_at TIMESTAMP,
                    attempts INTEGER DEFAULT 0,
                    max_attempts INTEGER DEFAULT 3,
                    metadata JSONB DEFAULT '{}'
                )
            """)
            
            # Create index on whatsapp_user_id and phone for OTP lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_whatsapp_otps_user_phone 
                ON whatsapp_otps(whatsapp_user_id, phone_number)
            """)
            
            # Create index on expires_at for cleanup jobs
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_whatsapp_otps_expires 
                ON whatsapp_otps(expires_at)
            """)
            
            cursor.close()
    
    def get_session(self, whatsapp_user_id: str) -> Optional[SessionInfo]:
        """Get session information for a WhatsApp user"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT whatsapp_user_id, customer_id, auth_state, phone_number, 
                       created_at, last_activity, expires_at, metadata
                FROM whatsapp_sessions
                WHERE whatsapp_user_id = %s
            """, (whatsapp_user_id,))
            
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                metadata = row['metadata'] if row['metadata'] else {}
                return SessionInfo(
                    whatsapp_user_id=row['whatsapp_user_id'],
                    customer_id=row['customer_id'],
                    auth_state=AuthState(row['auth_state']),
                    auth_level=metadata.get('auth_level', 'BASIC'),
                    phone_number=row['phone_number'],
                    created_at=row['created_at'],
                    last_activity=row['last_activity'],
                    expires_at=row['expires_at'],
                    metadata=metadata
                )
            return None
    
    def create_or_update_session(self, whatsapp_user_id: str, auth_state: AuthState, 
                                phone_number: Optional[str] = None,
                                customer_id: Optional[str] = None,
                                expires_at: Optional[datetime] = None,
                                metadata: Optional[Dict[str, Any]] = None) -> SessionInfo:
        """Create or update a WhatsApp session"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Check if session exists
            cursor.execute("""
                SELECT whatsapp_user_id FROM whatsapp_sessions 
                WHERE whatsapp_user_id = %s
            """, (whatsapp_user_id,))
            
            exists = cursor.fetchone()
            
            if exists:
                # Update existing session
                metadata_json = json.dumps(metadata) if metadata else None
                cursor.execute("""
                    UPDATE whatsapp_sessions
                    SET auth_state = %s, phone_number = COALESCE(%s, phone_number),
                        customer_id = COALESCE(%s, customer_id),
                        expires_at = COALESCE(%s, expires_at),
                        last_activity = CURRENT_TIMESTAMP,
                        metadata = COALESCE(%s::jsonb, metadata)
                    WHERE whatsapp_user_id = %s
                    RETURNING whatsapp_user_id, customer_id, auth_state, phone_number,
                              created_at, last_activity, expires_at, metadata
                """, (auth_state.value, phone_number, customer_id, expires_at, metadata_json, whatsapp_user_id))
            else:
                # Create new session
                metadata_json = json.dumps(metadata) if metadata else '{}'
                cursor.execute("""
                    INSERT INTO whatsapp_sessions 
                    (whatsapp_user_id, auth_state, phone_number, customer_id, expires_at, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s::jsonb)
                    RETURNING whatsapp_user_id, customer_id, auth_state, phone_number,
                              created_at, last_activity, expires_at, metadata
                """, (whatsapp_user_id, auth_state.value, phone_number, customer_id, expires_at, metadata_json))
            
            row = cursor.fetchone()
            cursor.close()
            
            metadata = row.get('metadata', {}) if row.get('metadata') else {}
            return SessionInfo(
                whatsapp_user_id=row['whatsapp_user_id'],
                customer_id=row['customer_id'],
                auth_state=AuthState(row['auth_state']),
                auth_level=metadata.get('auth_level', 'BASIC'),
                phone_number=row['phone_number'],
                created_at=row['created_at'],
                last_activity=row['last_activity'],
                expires_at=row.get('expires_at'),
                metadata=metadata
            )
    
    def store_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str, 
                  expiry_minutes: int = 10) -> str:
        """Store OTP in database"""
        expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
        otp_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO whatsapp_otps 
                (otp_id, whatsapp_user_id, phone_number, otp_code, expires_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (otp_id, whatsapp_user_id, phone_number, otp_code, expires_at))
            cursor.close()
        
        return otp_id
    
    def verify_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str) -> bool:
        """Verify OTP and mark as verified if valid"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get latest unverified OTP for this user/phone
            cursor.execute("""
                SELECT otp_id, otp_code, expires_at, attempts, max_attempts
                FROM whatsapp_otps
                WHERE whatsapp_user_id = %s 
                  AND phone_number = %s
                  AND verified = FALSE
                  AND expires_at > CURRENT_TIMESTAMP
                ORDER BY created_at DESC
                LIMIT 1
            """, (whatsapp_user_id, phone_number))
            
            otp_record = cursor.fetchone()
            
            if not otp_record:
                cursor.close()
                return False
            
            # Check attempts
            if otp_record['attempts'] >= otp_record['max_attempts']:
                cursor.close()
                return False
            
            # Increment attempts
            cursor.execute("""
                UPDATE whatsapp_otps
                SET attempts = attempts + 1
                WHERE otp_id = %s
            """, (otp_record['otp_id'],))
            
            # Verify OTP code
            if otp_record['otp_code'] == otp_code:
                cursor.execute("""
                    UPDATE whatsapp_otps
                    SET verified = TRUE, verified_at = CURRENT_TIMESTAMP
                    WHERE otp_id = %s
                """, (otp_record['otp_id'],))
                cursor.close()
                return True
            
            cursor.close()
            return False
    
    def get_customer_by_phone(self, phone_number: str) -> Optional[str]:
        """Get customer ID by phone number"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Try different phone column names
                for phone_col in ['phone', 'phone_number', 'mobile']:
                    try:
                        cursor.execute(f"""
                            SELECT customer_id FROM customers 
                            WHERE {phone_col} = %s OR {phone_col} = %s 
                            LIMIT 1
                        """, (phone_number, phone_number.replace('+', '')))
                        
                        row = cursor.fetchone()
                        if row:
                            cursor.close()
                            return row[0]
                    except Exception:
                        continue
                
                cursor.close()
                return None
        except Exception as e:
            logger.warning(f"Error looking up customer by phone: {e}")
            return None
    
    def cleanup_expired_otps(self):
        """Clean up expired OTPs (call periodically)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM whatsapp_otps 
                WHERE expires_at < CURRENT_TIMESTAMP - INTERVAL '1 day'
            """)
            deleted = cursor.rowcount
            cursor.close()
            return deleted
    
    def cleanup_expired_sessions(self, expiry_days: int = 30):
        """Clean up expired sessions (call periodically)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM whatsapp_sessions 
                WHERE auth_state = 'unauthenticated' 
                  AND last_activity < CURRENT_TIMESTAMP - INTERVAL '%s days'
            """, (expiry_days,))
            deleted = cursor.rowcount
            cursor.close()
            return deleted


# Global database instance
# Try to use PostgreSQL, fallback to in-memory if not available
db = None

try:
    # Try to create PostgreSQL connection
    test_db = WhatsAppDatabase()
    # Test connection (quick test)
    try:
        with test_db.get_connection():
            pass
        db = test_db
        logger.info("✅ Using PostgreSQL database")
    except Exception as conn_error:
        # Connection failed, use in-memory
        raise conn_error
except Exception as e:
    # Fallback to in-memory database
    logger.warning(f"⚠️  PostgreSQL not available ({str(e)[:100]}), using in-memory database")
    try:
        from whatsapp_integration.database_memory import WhatsAppDatabaseMemory
        db = WhatsAppDatabaseMemory()
        logger.info("✅ Using in-memory database (no PostgreSQL required)")
    except ImportError as import_error:
        # If memory module doesn't exist, create a simple fallback
        logger.error(f"❌ Could not load in-memory database fallback: {import_error}")
        # Create a minimal fallback
        class MinimalDB:
            def initialize_tables(self): return True
            def get_session(self, *args): return None
            def create_or_update_session(self, *args, **kwargs): return None
            def store_otp(self, *args, **kwargs): return "mock"
            def verify_otp(self, *args, **kwargs): return False
            def get_customer_by_phone(self, *args): return None
            def cleanup_expired_otps(self): return 0
            def cleanup_expired_sessions(self, *args): return 0
        db = MinimalDB()
        logger.warning("⚠️  Using minimal fallback database (limited functionality)")
