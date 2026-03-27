# Oracle Banking Simulator

## Project Overview
An enterprise-grade **Oracle Database** project simulating a retail banking environment with automated fraud detection and comprehensive audit logging.

## Key Features
* **Automated Fraud Detection:** PL/SQL triggers monitor transactions in real-time, flagging transfers exceeding $10,000
* **Full Audit Trail:** Automated logging of all balance changes to ensure financial integrity and compliance
* **Synthetic Data Pipeline:** Python scripts utilizing `Faker` and `oracledb` to generate 1,000+ realistic, weighted transactions
* **Environment-Based Configuration:** Secure credential management using environment variables
* **Comprehensive Error Handling:** Robust error handling and validation throughout the application

## Architecture

### Database Components
- **Tables:** customers, accounts, transactions, fraud_alerts, account_audit_log
- **Triggers:** TRG_DETECT_FRAUD, TRG_AUDIT_BALANCE
- **Sequences:** tx_seq for transaction IDs

### Python Scripts
- **populate_db.py:** Database initialization with synthetic data
- **simulate_activity.py:** Transaction simulation with fraud patterns

## How to Run

### 1. Prerequisites
* **Oracle Database:** Oracle 12c or newer (e.g., Oracle 23ai Free, Oracle XE)
* **Python:** Version 3.7 or higher
* **Git:** For cloning the repository

### 2. Installation

#### Clone the Repository
```bash
git clone https://github.com/OmP215/oracle-banking-simulator.git
cd oracle-banking-simulator
```

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

The requirements.txt includes:
- `oracledb` - Oracle Database driver
- `Faker` - Synthetic data generation
- `python-dotenv` - Environment variable management

### 3. Database Setup

#### Connect as Admin
Connect to your Oracle database with appropriate privileges:
```sql
sqlplus sys/password@localhost:1521/XEPDB1 as sysdba
```

#### Create Database User (Optional)
If you need a dedicated user for the simulator:
```sql
CREATE USER banking_admin IDENTIFIED BY your_password;
GRANT CONNECT, RESOURCE TO banking_admin;
GRANT UNLIMITED TABLESPACE TO banking_admin;
```

#### Run Schema Script
Execute the main schema script to create all tables:
```bash
sqlplus banking_admin/password@localhost:1521/XEPDB1 @sql/banking_admin_tables.sql
```

#### Deploy Triggers
Install the fraud detection and audit triggers:
```bash
sqlplus banking_admin/password@localhost:1521/XEPDB1 @sql/TRG_DETECT_FRAUD.sql
sqlplus banking_admin/password@localhost:1521/XEPDB1 @sql/TRG_AUDIT_BALANCE.sql
```

### 4. Configuration

#### Create Environment File
Copy the example configuration and update with your credentials:
```bash
cp .env.example .env
```

#### Edit .env File
Update the `.env` file with your database credentials:
```bash
DB_USER=banking_admin
DB_PASSWORD=your_password
DB_DSN=localhost:1521/XEPDB1
```

**DSN Format Examples:**
- Local Oracle XE: `localhost:1521/XEPDB1`
- Remote database: `hostname:1521/servicename`
- Easy Connect: `host:port/service_name`

**Security Note:** Never commit the `.env` file to version control. It's already listed in `.gitignore`.

### 5. Execution Flow

#### Populate Database
Initialize the database with synthetic customers and accounts:
```bash
python scripts/populate_db.py
```

**What it does:**
- Clears existing data and resets identity sequences
- Generates 200 customers with realistic personal information
- Creates accounts with random balances ($1,000 - $50,000)
- Distributes account statuses (85% active, 5% frozen, 10% closed)

#### Simulate Activity
Generate realistic transaction patterns:
```bash
python scripts/simulate_activity.py
```

**What it does:**
- Generates 1,000 transactions between active accounts
- 95% normal transactions ($5 - $500)
- 5% suspicious transactions ($10,001 - $25,000) that trigger fraud alerts
- Validates sender balance before processing
- Commits in batches of 50 for performance

### 6. Result Verification

#### Check Fraud Alerts
View all detected suspicious transactions:
```sql
SELECT * FROM fraud_alerts ORDER BY alert_date DESC;
```

Expected columns:
- `alert_id`: Unique alert identifier
- `tx_id`: Related transaction ID
- `reason`: Why the alert was triggered
- `alert_date`: When the alert was created
- `is_resolved`: 'N' for new, 'Y' for resolved

#### Check Audit Log
Verify the balance change audit trail:
```sql
SELECT * FROM account_audit_log ORDER BY changed_at DESC;
```

Expected columns:
- `audit_id`: Unique audit log entry
- `account_id`: Account that was modified
- `old_balance`: Balance before change
- `new_balance`: Balance after change
- `changed_by`: Database user who made the change
- `changed_at`: Timestamp of the change

#### View Transaction Summary
Get transaction statistics:
```sql
SELECT
    COUNT(*) as total_transactions,
    SUM(amount) as total_volume,
    AVG(amount) as avg_transaction,
    MAX(amount) as largest_transaction
FROM transactions;
```

#### Find High-Value Transactions
View all transactions that triggered fraud alerts:
```sql
SELECT t.*, fa.reason, fa.alert_date
FROM transactions t
JOIN fraud_alerts fa ON t.tx_id = fa.tx_id
ORDER BY t.amount DESC;
```

## Project Structure
```
oracle-banking-simulator/
├── sql/
│   ├── banking_admin_tables.sql    # Main schema definition
│   ├── TRG_AUDIT_BALANCE.sql      # Balance audit trigger
│   └── TRG_DETECT_FRAUD.sql       # Fraud detection trigger
├── scripts/
│   ├── populate_db.py             # Database initialization
│   └── simulate_activity.py       # Transaction simulation
├── .env.example                    # Configuration template
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Troubleshooting

### Connection Issues
**Error:** `DPI-1047: Cannot locate an Oracle Client library`
- **Solution:** Install Oracle Instant Client or use Oracle Database with built-in client

**Error:** `ORA-12541: TNS:no listener`
- **Solution:** Verify Oracle listener is running: `lsnrctl status`

### Authentication Issues
**Error:** `ORA-01017: invalid username/password`
- **Solution:** Verify credentials in `.env` file match your database user

### Schema Issues
**Error:** `ORA-00942: table or view does not exist`
- **Solution:** Run the schema script first: `@sql/banking_admin_tables.sql`

**Error:** Missing account_audit_log table
- **Solution:** This has been fixed in the latest version. Re-run `banking_admin_tables.sql`

## Development

### Running in Development Mode
For testing, you can use the default credentials by skipping the `.env` file (not recommended for production):
```bash
python scripts/populate_db.py  # Will warn about default credentials
```

### Customizing Transaction Patterns
Edit `simulate_activity.py` to adjust:
- Number of transactions (line 73: `range(1000)`)
- Fraud threshold percentage (line 77: `random.random() < 0.05`)
- Transaction amount ranges (lines 78-82)

### Customizing Fraud Detection
Edit `sql/TRG_DETECT_FRAUD.sql` to modify:
- Fraud threshold amount (line 26: `IF :NEW.amount > 10000`)
- Add additional detection rules

## Future Enhancements
- Multiple fraud detection rules (velocity checks, pattern analysis)
- Customer credit limits and account types
- Interest calculation for savings accounts
- Monthly statement generation
- Multi-currency support
- RESTful API for transaction processing
- Web dashboard for monitoring

## License
This project is available for educational and demonstration purposes.

## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests.

## Contact
For questions or feedback, please open an issue on the GitHub repository.
