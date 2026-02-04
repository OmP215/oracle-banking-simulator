--------------------------------------------------------
--  File created - Tuesday-February-03-2026   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger TRG_DETECT_FRAUD
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "BANKING_ADMIN"."TRG_DETECT_FRAUD" 
after insert on transactions
for each row
begin
    if :NEW.amount > 10000 then
        insert into fraud_alerts (tx_id, reason, alert_date, is_resolved)
        values (:NEW.tx_id, 'Transaction exceeds $10,000 threshold', SYSDATE,'N');
        end if;
    end;

/
ALTER TRIGGER "BANKING_ADMIN"."TRG_DETECT_FRAUD" ENABLE;
