CREATE TABLE users (
    id         INTEGER PRIMARY KEY,
    email      TEXT NOT NULL,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at INTEGER NOT NULL,
    deleted_at INTEGER
);
