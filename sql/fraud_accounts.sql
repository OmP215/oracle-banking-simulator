select t.sender_account_id, t.amount, f.reason, f.alert_date
from transactions t
join fraud_alerts f on t.tx_id = f.tx_id
order by t.amount desc;