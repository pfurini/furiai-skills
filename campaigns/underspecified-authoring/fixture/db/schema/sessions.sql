CREATE TABLE sessions (
    id         INTEGER PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    started_at INTEGER NOT NULL,
    duration   INTEGER NOT NULL
);
CREATE INDEX idx_sessions_started ON sessions(started_at);
