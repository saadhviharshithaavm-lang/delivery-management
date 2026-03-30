"""
Quick test script to verify Oracle database connection and setup
Run this before starting the main application
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def test_connection():
    print("=" * 50)
    print("FreshDeliver Backend - Oracle Connection Test")
    print("=" * 50)
    print()

    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL not found in .env file")
        print("   Please create .env file and set DATABASE_URL")
        return False

    print(f"Database URL: {db_url.split('@')[1] if '@' in db_url else db_url}")
    print()

    try:
        # Create engine
        print("Connecting to Oracle database...")
        engine = create_engine(db_url)

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM DUAL"))
            result.fetchone()

        print("Database connection successful!")
        print()

        # Check if tables exist
        print("Checking tables...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name
                FROM user_tables
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]

        if tables:
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("WARNING: No tables found. Please run customer.sql to create tables.")

        print()

        # Check customers
        if 'CUSTOMERS' in tables:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM customers"))
                count = result.fetchone()[0]
            print(f"Customers table has {count} records")
        else:
            print("WARNING: Customers table not found")

        print()
        print("=" * 50)
        print("All checks passed! You can start the backend now.")
        print("   Run: python main.py")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check if Oracle is running")
        print("2. Verify credentials in .env file")
        print("3. Ensure the Oracle service/SID is correct")
        print("4. Check that the user/schema exists and has permissions")
        print("5. Install Oracle Instant Client if needed")
        return False

if __name__ == "__main__":
    test_connection()
