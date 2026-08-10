-- 2026-02-16
-- New ingest pipeline. All new instrumentation writes here. The legacy
-- tracker keeps writing session_start/page_view rows to `events` until the
-- SDK v3 rollout completes; treat `events` as legacy.
CREATE TABLE events_v2 (
    id         INTEGER PRIMARY KEY,
    event_uuid TEXT NOT NULL,
    actor_id   INTEGER NOT NULL REFERENCES users(id),
    type       TEXT NOT NULL,
    ts         INTEGER NOT NULL
);
CREATE INDEX idx_events_v2_ts ON events_v2(ts);
