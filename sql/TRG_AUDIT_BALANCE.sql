--------------------------------------------------------
--  File created - Tuesday-February-03-2026   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger TRG_AUDIT_BALANCE
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "BANKING_ADMIN"."TRG_AUDIT_BALANCE" 
after update of balance on accounts 
for each row
begin
    insert into account_audit_log (account_id, old_balance, new_balance, changed_by)
    values (:OLD.account_id, :OLD.balance, :NEW.balance, USER);
end;

/
ALTER TRIGGER "BANKING_ADMIN"."TRG_AUDIT_BALANCE" ENABLE;
