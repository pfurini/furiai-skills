CREATE TABLE events (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    type    TEXT NOT NULL,
    ts      INTEGER NOT NULL
);
CREATE INDEX idx_events_ts ON events(ts);
