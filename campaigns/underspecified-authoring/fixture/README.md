# lumina-analytics

Analytics working repo for the growth team: the nightly SQLite snapshot, its
schema and migration history, and the reporting queries behind the exec
dashboard.

- `db/analytics.sqlite` — the data (snapshot as of 2026-08-01, UTC)
- `db/schema/` — current DDL, `db/migrations/` — how it got there
- `docs/` — overview and metric definitions
- `queries/` — the canonical reporting queries (run with `sqlite3`)
- `seed/` + `db/build_db.py` — rebuild the snapshot from the warehouse CSVs

Rebuild: `python3 db/build_db.py`

Questions about metric definitions go to #growth-analytics.
