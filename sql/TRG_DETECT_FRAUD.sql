/*
 * TRG_DETECT_FRAUD - Automated Fraud Detection Trigger
 *
 * Purpose:
 *   Automatically detects and flags suspicious transactions in real-time.
 *   Creates fraud alerts for transactions exceeding defined thresholds.
 *
 * Trigger Type: AFTER INSERT
 * Table: transactions
 *
 * Detection Rules:
 *   - Transactions over $10,000 are flagged as potentially fraudulent
 *   - Alert is created with status 'N' (unresolved)
 *
 * Future Enhancements:
 *   - Multiple threshold levels
 *   - Time-based pattern detection
 *   - Account velocity checks
 */

CREATE OR REPLACE TRIGGER TRG_DETECT_FRAUD
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    -- Check if transaction exceeds fraud threshold
    IF :NEW.amount > 10000 THEN
        INSERT INTO fraud_alerts (tx_id, reason, alert_date, is_resolved)
        VALUES (:NEW.tx_id, 'Transaction exceeds $10,000 threshold', SYSDATE, 'N');
    END IF;
END;
/

-- Enable the trigger
ALTER TRIGGER TRG_DETECT_FRAUD ENABLE;
/
