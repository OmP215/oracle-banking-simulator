import oracledb
import random

DB_CONFIG =  {
    "user": "user",
    "password": "password",
    "dsn": "dns"
}

def simulate_activity():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()

        #fetch all valid account ids
        cursor.execute("select account_id from accounts where status = 'active'")
        account_ids = [row[0] for row in cursor.fetchall()]

        print(f"Simulating activity for {len(account_ids)} accounts...")

        for i in range(1000):
            sender, reciever = random.sample(account_ids, 2)

             # 5% chance of sus transaction
            if random.random() <0.05:
                amount = round(random.uniform(10001, 25000), 2)
                desc = "Large Asset Transfer"
            else:
                amount = round(random.uniform(5,500), 2)
                desc = "standard payment"
            
            #check if sender has enough money
            cursor.execute("select balance from accounts where account_id = :1", [sender])
            current_balance = cursor.fetchone()[0]

            if current_balance >= amount:
                # step 1: record the ledgar entry
                cursor.execute("""
                       insert into transactions (sender_account_id, receiver_account_id, amount, tx_type, description)
                       values (:1, :2, :3, 'transfer', :4)""", [sender, reciever, amount, desc])

                # step 2: update balances
                cursor.execute("update accounts set balance = balance - :1 where account_id = :2", [amount, sender])
                cursor.execute("update accounts set balance = balance + :1 where account_id = :2", [amount, reciever])
            else:
                print(f"Skipping transaction: Sender {sender} has insufficient funds.")
                
            if i % 50 == 0:
                conn.commit()

        conn.commit()
        print("1000 transaction completed")
    except Exception as e:
        print(f"error suring simulations: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    simulate_activity()