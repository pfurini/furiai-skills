-- 2026-01-08
-- Accounts<->users is many-to-many now (agencies, consultants, account moves).
-- users.account_id is kept for backward compatibility with old reports; do not
-- drop it yet. Source of truth for account membership is this table.
CREATE TABLE memberships (
    id         INTEGER PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    is_primary INTEGER NOT NULL DEFAULT 0,
    created_at INTEGER NOT NULL
);
