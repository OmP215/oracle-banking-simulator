# Oracle Banking Simulator

## Project Overview
An enterprise-grade **Oracle Database** project simulating a retail banking environment with automated fraud detection and audit logging.

##  Key Features
* **Automated Fraud Detection:** PL/SQL triggers monitor transactions in real-time, flagging transfers exceeding $10,000.
* **Full Audit Trail:** Automated logging of all balance changes to ensure financial integrity and compliance.
* **Synthetic Data Pipeline:** Python scripts utilizing `Faker` and `oracledb` to generate 1,000+ realistic, weighted transactions.

##  How to Run

### 1. Prerequisites
* **Oracle Database:** Instance of Oracle (e.g., Oracle 23ai Free).
* **Python 3.x**.
* **Libraries:** Install via `pip install oracledb faker`.

### 2. Database Setup
1. **Connect as Admin**.
2. **Run Schema Script:** Execute `banking_admin_tables.sql`.
3. **Deploy Logic:** Run your trigger scripts.

### 3. Configuration
* Update `DB_CONFIG` in the Python scripts to match your local environment (User/Password and DSN).

### 4. Execution Flow
1. **Populate Database:** `python populate_db.py` 
   *(Clears old data, resets identity sequences, and generates initial customers/accounts)*.
2. **Simulate Activity:** `python simulate_activity.py` 
   *(Generates 1,000+ transactions, tests balance constraints, and trips fraud triggers)*.

### 5. Result Verification
* **Check Alerts:** `SELECT * FROM fraud_alerts;` to see automated security results.
* **Check History:** `SELECT * FROM account_audit_log;` to verify the balance change paper trail.
