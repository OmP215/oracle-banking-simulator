/*
 * TRG_AUDIT_BALANCE - Balance Change Audit Trigger
 *
 * Purpose:
 *   Automatically logs all balance changes to the account_audit_log table.
 *   This creates a complete audit trail for compliance and debugging.
 *
 * Trigger Type: AFTER UPDATE
 * Table: accounts
 * Column: balance
 *
 * Behavior:
 *   For each balance update, records:
 *   - Account ID
 *   - Old balance value
 *   - New balance value
 *   - User who made the change
 *   - Timestamp (automatic via DEFAULT)
 */

CREATE OR REPLACE TRIGGER TRG_AUDIT_BALANCE
AFTER UPDATE OF balance ON accounts
FOR EACH ROW
BEGIN
    INSERT INTO account_audit_log (account_id, old_balance, new_balance, changed_by)
    VALUES (:OLD.account_id, :OLD.balance, :NEW.balance, USER);
END;
/

-- Enable the trigger
ALTER TRIGGER TRG_AUDIT_BALANCE ENABLE;
/
