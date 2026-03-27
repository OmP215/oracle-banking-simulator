"""
Oracle Banking Simulator - Transaction Activity Simulation Script

This script simulates realistic banking transaction activity including:
- Normal transactions between accounts
- High-value transactions that trigger fraud alerts
- Balance validation and insufficient funds checking

Features:
- Generates 1000+ transactions with weighted distribution
- 5% chance of suspicious high-value transactions (>$10,000)
- Validates sender has sufficient funds before processing
- Commits in batches for performance
"""

import oracledb
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DB_CONFIG = {
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "dsn": os.getenv("DB_DSN", "localhost:1521/XEPDB1")
}

def simulate_activity():
    """
    Simulate 1000 banking transactions with realistic patterns.

    Transaction patterns:
    - 95% normal transactions ($5-$500)
    - 5% suspicious transactions (>$10,000) that trigger fraud alerts

    The function:
    1. Fetches all active accounts
    2. Randomly selects sender/receiver pairs
    3. Validates sender has sufficient funds
    4. Records transaction and updates balances
    5. Commits in batches of 50 for performance
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

        # Fetch all valid account IDs
        print("📊 Fetching active accounts...")
        cursor.execute("SELECT account_id FROM accounts WHERE status = 'active'")
        account_ids = [row[0] for row in cursor.fetchall()]

        if len(account_ids) < 2:
            print("❌ Error: Need at least 2 active accounts to simulate transactions.")
            return

        print(f"💸 Simulating activity for {len(account_ids)} accounts...")

        transactions_completed = 0
        transactions_skipped = 0

        for i in range(1000):
            sender, receiver = random.sample(account_ids, 2)

            # 5% chance of suspicious transaction
            if random.random() < 0.05:
                amount = round(random.uniform(10001, 25000), 2)
                desc = "Large Asset Transfer"
            else:
                amount = round(random.uniform(5, 500), 2)
                desc = "Standard payment"

            # Check if sender has enough funds
            cursor.execute("SELECT balance FROM accounts WHERE account_id = :1", [sender])
            result = cursor.fetchone()
            if not result:
                continue
            current_balance = result[0]

            if current_balance >= amount:
                # Step 1: Record the ledger entry
                cursor.execute("""
                       INSERT INTO transactions (sender_account_id, receiver_account_id, amount, tx_type, description)
                       VALUES (:1, :2, :3, 'transfer', :4)""", [sender, receiver, amount, desc])

                # Step 2: Update balances
                cursor.execute("UPDATE accounts SET balance = balance - :1 WHERE account_id = :2", [amount, sender])
                cursor.execute("UPDATE accounts SET balance = balance + :1 WHERE account_id = :2", [amount, receiver])

                transactions_completed += 1
            else:
                transactions_skipped += 1

            # Commit every 50 transactions for performance
            if i % 50 == 0 and i > 0:
                conn.commit()
                print(f"   Processed {i} transactions...")

        conn.commit()
        print(f"✅ Simulation complete!")
        print(f"   Transactions completed: {transactions_completed}")
        print(f"   Transactions skipped (insufficient funds): {transactions_skipped}")

    except oracledb.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Unexpected error during simulation: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
    simulate_activity()