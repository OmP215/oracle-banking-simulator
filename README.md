PROJECT OVERVIEW
    An enterprise grade Oracle Database project simulating a retail banking environment with automated fraud detection and audit logging.

KEY FEATURES
    Automated Fraud Detection: PL/SQL triggers monitor transactions in real-time, flagging trafser exceeding $10,000.
    Full Audit Trail: Automated logging of all balance changed to ensure financial integrity and compliance.
    Synthetic Data Pipeline: Python scripts utilizing Faker and oracledb to generate 1,000+ realistic, weighted transactions.

HOW TO RUN
    1. Prerequisites
       a. Instance of Oracle (Oracle 23ai Free)
       b. Python 3.x
       c. Faker and oracledb libraries (pip install oracledb faker)
    2. Database Setup
       a. Connect as admin
       b. Run the schema script (banking_admin_tables.sql)
       c. Deploy the logic (trigger scripts)
    3. Configuration
       a. Update DB_CONFIG in python script to match local environment (User/Password and DNS)
    4. Execution Flow
       a. python populate_db.py (clears old data, resets identity sequences, and generates initial customers and accounts)
       b. python simulate_activoty.py (generates 1000+ transactions, tests balance constraints, and trips fraud trigger)
    5. Result Verification
       a. Check the alerts: select * from fraud_alerts; to see the results of the automated security logic
       b. Check the history: select * from account_audit_log; tp verify the paper trail of balance changes# oracle-banking-simulator
