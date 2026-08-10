CREATE TABLE accounts (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    is_test    INTEGER NOT NULL DEFAULT 0,
    created_at INTEGER NOT NULL
);
