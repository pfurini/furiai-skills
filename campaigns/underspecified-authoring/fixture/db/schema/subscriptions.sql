CREATE TABLE subscriptions (
    id          INTEGER PRIMARY KEY,
    account_id  INTEGER NOT NULL REFERENCES accounts(id),
    plan_id     INTEGER NOT NULL REFERENCES plans(id),
    status      TEXT NOT NULL CHECK (status IN ('a', 'c', 't', 'p')),
    started_at  INTEGER NOT NULL,
    canceled_at INTEGER
);
