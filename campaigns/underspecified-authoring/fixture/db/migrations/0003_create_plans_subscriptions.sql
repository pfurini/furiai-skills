-- 2024-02-20
CREATE TABLE plans (
    id             INTEGER PRIMARY KEY,
    name           TEXT NOT NULL,
    price_cents    INTEGER NOT NULL,
    billing_period TEXT NOT NULL CHECK (billing_period IN ('monthly', 'annual'))
);

CREATE TABLE subscriptions (
    id          INTEGER PRIMARY KEY,
    account_id  INTEGER NOT NULL REFERENCES accounts(id),
    plan_id     INTEGER NOT NULL REFERENCES plans(id),
    status      TEXT NOT NULL CHECK (status IN ('a', 'c', 't', 'p')),
    started_at  INTEGER NOT NULL,
    canceled_at INTEGER
);
