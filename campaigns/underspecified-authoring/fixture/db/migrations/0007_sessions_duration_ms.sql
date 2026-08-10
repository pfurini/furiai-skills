-- 2025-12-02
-- Tracker v2 reports session duration in milliseconds. Existing rows were
-- recorded in seconds by tracker v1; backfill multiplies them by 1000 so the
-- column is uniformly milliseconds from here on.
UPDATE sessions SET duration = duration * 1000 WHERE started_at < 1764633600;
