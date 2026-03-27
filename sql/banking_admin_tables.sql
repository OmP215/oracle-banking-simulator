/*
 * Oracle Banking Simulator - Database Schema
 *
 * This script creates the complete database schema for a banking simulation system.
 * It includes tables for customers, accounts, transactions, fraud detection, and audit logging.
 *
 * Tables:
 * - customers: Customer personal information
 * - accounts: Bank accounts with balances and status
 * - transactions: Transaction history
 * - fraud_alerts: Automated fraud detection alerts
 * - account_audit_log: Balance change audit trail
 *
 * Prerequisites:
 * - Oracle Database 12c or newer (for IDENTITY columns)
 * - Appropriate permissions to create tables and sequences
 */

-- Drop existing tables if they exist (cascade constraints to handle dependencies)
DROP TABLE account_audit_log CASCADE CONSTRAINTS;
DROP TABLE fraud_alerts CASCADE CONSTRAINTS;
DROP TABLE transactions CASCADE CONSTRAINTS;
DROP TABLE accounts CASCADE CONSTRAINTS;
DROP TABLE customers CASCADE CONSTRAINTS;

-- Drop existing sequence if it exists
BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE tx_seq';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -2289 THEN -- Ignore "sequence does not exist" error
            RAISE;
        END IF;
END;
/

-- Create specialized sequence for transaction IDs
-- Starting at 1000 to differentiate from auto-generated IDs
CREATE SEQUENCE tx_seq START WITH 1000 INCREMENT BY 1;

-- Customers table
-- Stores customer personal information and contact details
CREATE TABLE customers (
    customer_id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name          VARCHAR2(50) NOT NULL,
    last_name           VARCHAR2(50) NOT NULL,
    email               VARCHAR2(100) UNIQUE,
    phone               VARCHAR2(50), -- Sized for international formats from Faker
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_format CHECK (email LIKE '%@%.%')
);

-- Accounts table
-- Stores bank account information with balance and status tracking
CREATE TABLE accounts (
    account_id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id         NUMBER REFERENCES customers(customer_id),
    account_type        VARCHAR2(20) CHECK (account_type IN ('checking', 'savings')),
    balance             NUMBER(15,2) DEFAULT 0,
    status              VARCHAR2(20) DEFAULT 'active',
    CONSTRAINT chk_balance_non_negative CHECK (balance >= 0),
    CONSTRAINT chk_account_status CHECK (status IN ('active', 'frozen', 'closed'))
);

-- Transactions table
-- Records all financial transactions between accounts
CREATE TABLE transactions (
    tx_id               NUMBER DEFAULT tx_seq.NEXTVAL PRIMARY KEY,
    sender_account_id   NUMBER REFERENCES accounts(account_id),
    receiver_account_id NUMBER REFERENCES accounts(account_id),
    amount              NUMBER(15,2) NOT NULL,
    tx_type             VARCHAR2(20),
    description         VARCHAR2(255),
    tx_timestamp        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fraud alerts table
-- Stores automated fraud detection alerts triggered by suspicious transactions
CREATE TABLE fraud_alerts (
    alert_id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tx_id               NUMBER REFERENCES transactions(tx_id),
    reason              VARCHAR2(255),
    alert_date          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_resolved         CHAR(1) DEFAULT 'N' CHECK (is_resolved IN ('Y','N'))
);

-- Account audit log table
-- Maintains a complete audit trail of all balance changes
CREATE TABLE account_audit_log (
    audit_id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id          NUMBER REFERENCES accounts(account_id),
    old_balance         NUMBER(15,2),
    new_balance         NUMBER(15,2),
    changed_by          VARCHAR2(50),
    changed_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
