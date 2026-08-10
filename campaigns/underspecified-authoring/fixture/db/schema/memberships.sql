CREATE TABLE memberships (
    id         INTEGER PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    is_primary INTEGER NOT NULL DEFAULT 0,
    created_at INTEGER NOT NULL
);
