drop table fraud_alerts cascade constraints;
drop table transactions cascade constraints;
drop table accounts cascade constraints;
drop table customers cascade constraints;
drop sequence tx_seq;
-- create specialized sequence for txn ids
create sequence tx_seq start with 1000 increment by 1;

-- customers table
create table customers (
    customer_id         number generated always as identity primary key,
    first_name          varchar2(50) not null,
    last_name           varchar2(50) not null,
    email               varchar2(100) unique,
    created_at          timestamp default current_timestamp,
    constraint chk_email_format check (email like '%@%.%'),
    phone               varchar2(50) --changed to 50 for faker library
);

-- accounts table
create table accounts(
    account_id          number generated always as identity primary key,
    customer_id         number references customers(customer_id),
    account_type        varchar2(20) check (account_type in ('checking', 'savings')),
    balance             number(15,2) default 0,
    status              varchar2(20) default 'active',
    constraint chk_balance_non_negative check (balance >= 0),
    constraint chk_count_status check (status in ('active', 'frozen', 'closed'))
);

-- transactions table
create table transactions(
    tx_id               number default tx_seq.nextval primary key,
    sender_account_id   number references accounts(account_id),
    receiver_account_id number references accounts(account_id),
    amount              number(15,2) not null,
    tx_type             varchar2(20),
    description         varchar2(255),
    tx_timestamp        timestamp default current_timestamp
);

-- fraud alerts table
create table fraud_alerts (
    alert_id            number generated always as identity primary key,
    tx_id               number references transactions(tx_id),
    reason              varchar2(255),
    alert_date          timestamp default current_timestamp,
    is_resolved         char(1) default 'N' check (is_resolved in ('Y','N'))
);
