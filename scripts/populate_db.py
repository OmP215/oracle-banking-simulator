"""
Oracle Banking Simulator - Database Population Script

This script initializes the banking database with synthetic customer and account data.
It uses the Faker library to generate realistic test data.

Features:
- Clears existing data and resets sequences
- Creates 200 customers with random personal information
- Creates accounts for each customer with weighted status distribution
"""

import oracledb
from faker import Faker
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

fake = Faker()

# Database configuration from environment variables
DB_CONFIG = {
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "dsn": os.getenv("DB_DSN", "localhost:1521/XEPDB1")
}

def clear_tables(cursor):
    """
    Clear all existing data and reset identity sequences.

    Args:
        cursor: Oracle database cursor
    """
    print("🧹 Cleaning up existing data and resetting IDs...")

    # Tables to clear in order of dependency
    tables_to_clear = [
        "account_audit_log", 
        "fraud_alerts", 
        "transactions", 
        "accounts", 
        "customers"
    ]
    
    for table in tables_to_clear:
        try:
            # The 'RESTART IDENTITY' clause is the key for Oracle 12c and newer
            cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY")
        except oracledb.Error:
            # Fallback for older setups: Delete and manually reset
            cursor.execute(f"DELETE FROM {table}")
            if table == "customers":
                cursor.execute("ALTER TABLE customers MODIFY customer_id GENERATED ALWAYS AS IDENTITY (START WITH 1)")
            elif table == "accounts":
                cursor.execute("ALTER TABLE accounts MODIFY account_id GENERATED ALWAYS AS IDENTITY (START WITH 1)")

    # Reset your custom transaction sequence
    try:
        cursor.execute("DROP SEQUENCE tx_seq")
        cursor.execute("CREATE SEQUENCE tx_seq START WITH 1000 INCREMENT BY 1")
    except oracledb.Error:
        pass
        
    print("✨ All IDs and sequences have been reset to 1.")

def run_population():
    """
    Main function to populate the database with synthetic banking data.

    Process:
    1. Clear existing data and reset sequences
    2. Generate 200 customers with fake personal information
    3. Create accounts for each customer with random balances and types
    """
    conn = None
    try:
        # Validate configuration
        if DB_CONFIG["user"] == "user" or DB_CONFIG["password"] == "password":
            print("⚠️  Warning: Using default database credentials!")
            print("   Please create a .env file with your actual database credentials.")
            print("   See .env.example for the template.")
            return

        print(f"🔌 Connecting to database at {DB_CONFIG['dsn']}...")
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()

        clear_tables(cursor)

        # Create 200 customers with realistic data
        print("👥 Creating customers...")
        customers = [
            (fake.first_name(), fake.last_name(), fake.email(), fake.msisdn())
            for _ in range(200)
        ]
        cursor.executemany(
            "INSERT INTO customers (first_name, last_name, email, phone) VALUES (:1, :2, :3, :4)",
            customers
        )

        # Get customer IDs and create accounts
        print("💰 Creating accounts...")
        cursor.execute("SELECT customer_id FROM customers")
        customer_ids = [row[0] for row in cursor.fetchall()]

        account_types = ['checking', 'savings']
        status_options = ['active', 'frozen', 'closed']
        status_weights = [85, 5, 10]  # 85% active, 5% frozen, 10% closed

        accounts = [
            (
                cid,
                random.choice(account_types),
                round(random.uniform(1000, 50000), 2),
                random.choices(status_options, weights=status_weights)[0]
            )
            for cid in customer_ids
        ]
        cursor.executemany(
            "INSERT INTO accounts (customer_id, account_type, balance, status) VALUES (:1, :2, :3, :4)",
            accounts
        )

        conn.commit()
        print(f"✅ Success! Created {len(customers)} customers and {len(accounts)} accounts.")

    except oracledb.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
     run_population()