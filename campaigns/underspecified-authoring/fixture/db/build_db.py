#!/usr/bin/env python3
"""Rebuild db/analytics.sqlite from db/schema/*.sql and seed/*.csv."""

import csv
import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
ROOT = DB_DIR.parent
DB = DB_DIR / "analytics.sqlite"

TABLES = [
    ("accounts", ["id", "name", "is_test", "created_at"]),
    ("users", ["id", "email", "account_id", "created_at", "deleted_at"]),
    ("memberships", ["id", "user_id", "account_id", "is_primary", "created_at"]),
    ("plans", ["id", "name", "price_cents", "billing_period"]),
    ("subscriptions", ["id", "account_id", "plan_id", "status", "started_at", "canceled_at"]),
    ("events", ["id", "user_id", "type", "ts"]),
    ("events_v2", ["id", "event_uuid", "actor_id", "type", "ts"]),
    ("sessions", ["id", "user_id", "started_at", "duration"]),
]


def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    for name, _ in TABLES:
        con.executescript((DB_DIR / "schema" / f"{name}.sql").read_text())
    for name, cols in TABLES:
        with open(ROOT / "seed" / f"{name}.csv", newline="") as f:
            rows = [tuple(r[c] if r[c] != "" else None for c in cols)
                    for r in csv.DictReader(f)]
        con.executemany(
            f"INSERT INTO {name} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
            rows,
        )
        print(f"  {name}: {len(rows)} rows")
    con.commit()
    con.close()
    print(f"built {DB}")


if __name__ == "__main__":
    main()
