import oracledb
from faker import Faker
import random
import re

fake = Faker()

DB_CONFIG =  {
    "user": "user",
    "password": "password",
    "dsn": "dns"
}

def clear_tables(cursor):
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
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        clear_tables(cursor)
        
        #create 200 customers
        customers = [(fake.first_name(), fake.last_name(), fake.email(), fake.msisdn()) for _ in range(200)]
        cursor.executemany("insert into customers (first_name, last_name, email, phone) values (:1, :2, :3, :4)", customers)

        #get ids and create accounts
        cursor.execute("select customer_id from customers")
        customer_ids = [row[0] for row in cursor.fetchall()]

        account_types = ['checking', 'savings']
        status = ['active', 'frozen', 'closed']
        weights = [85, 5, 10]
        accounts = [(cid, random.choice(account_types), round(random.uniform(1000, 50000), 2), random.choices(status, weights=weights)[0]) for cid in customer_ids]
        cursor.executemany("insert into accounts (customer_id, account_type, balance, status) values (:1, :2, :3, :4)", accounts)

        conn.commit()
        print(f"Success. Created {len(customers)} customers and accounts.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
     run_population()