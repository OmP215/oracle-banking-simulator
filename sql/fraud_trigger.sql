drop table account_audit_log;

create table account_audit_log (
    log_id      number generated always as identity primary key,
    account_id  number,
    old_balance number(15,2),
    new_balance number(15,2),
    changed_by  varchar(50),
    change_date timestamp default current_timestamp
);

create or replace trigger trg_audit_balance
after update of balance on accounts 
for each row
begin
    insert into account_audit_log (account_id, old_balance, new_balance, changed_by)
    values (:OLD.account_id, :OLD.balance, :NEW.balance, USER);
end;
/

create or replace trigger trg_detect_fraud
after insert on transactions
for each row
begin
    if :NEW.amount > 10000 then
        insert into fraud_alerts (tx_id, reason, alert_date, is_resolved)
        values (:NEW.tx_id, 'Transaction exceeds $10,000 threshold', SYSDATE,'N');
        end if;
    end;
/