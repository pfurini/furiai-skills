CREATE TABLE events_v2 (
    id         INTEGER PRIMARY KEY,
    event_uuid TEXT NOT NULL,
    actor_id   INTEGER NOT NULL REFERENCES users(id),
    type       TEXT NOT NULL,
    ts         INTEGER NOT NULL
);
CREATE INDEX idx_events_v2_ts ON events_v2(ts);
CREATE INDEX idx_events_v2_actor ON events_v2(actor_id);
