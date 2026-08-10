#!/usr/bin/env python3
"""Compute and freeze the expected answers for the consumer questions.

The "correct" SQL for each question replicates the production convention
exactly as embodied in fixture/queries/*.sql. Variants are the predicted
single-miss wrong answers (diagnostic only; scoring is right/wrong against
the correct value). Asserts every variant differs from the correct value.

Writes key/expected-answers.json.
"""

import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "fixture" / "db" / "analytics.sqlite"
OUT = HERE.parent / "key" / "expected-answers.json"

JUL = "e.ts >= strftime('%s','2026-07-01') AND e.ts < strftime('%s','2026-08-01')"
JUN = "e.ts >= strftime('%s','2026-06-01') AND e.ts < strftime('%s','2026-07-01')"

REAL = """JOIN users u ON u.id = e.actor_id
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0"""

con = sqlite3.connect(DB)


def q(sql):
    return con.execute(sql).fetchone()[0]


answers = {}


def reg(qid, correct, variants, tolerance=0):
    for name, v in variants.items():
        assert v != correct, f"{qid}: variant {name} equals correct answer ({v})"
        if tolerance and isinstance(v, (int, float)):
            assert abs(v - correct) > 2 * tolerance, \
                f"{qid}: variant {name} ({v}) within tolerance of correct ({correct})"
    answers[qid] = {"correct": correct, "tolerance": tolerance, "variants": variants}
    print(f"{qid}: correct={correct}  variants={variants}")


# Q-B1: events recorded in July 2026 (convention: events_v2, distinct uuid,
# test accounts excluded — per daily_event_volume.sql)
reg("QB1",
    q(f"SELECT COUNT(DISTINCT e.event_uuid) FROM events_v2 e {REAL} WHERE {JUL}"),
    {
        "legacy_table": q("SELECT COUNT(*) FROM events e WHERE "
                          "e.ts >= strftime('%s','2026-07-01') AND e.ts < strftime('%s','2026-08-01')"),
        "with_test_accounts": q(f"SELECT COUNT(DISTINCT e.event_uuid) FROM events_v2 e WHERE {JUL}"),
        "no_dedup": q(f"SELECT COUNT(*) FROM events_v2 e {REAL} WHERE {JUL}"),
    })

# Q-B2: top account by events, June 2026 (per events_by_account_monthly.sql)
top = con.execute(f"""SELECT a.name, COUNT(DISTINCT e.event_uuid) AS n
FROM events_v2 e {REAL} WHERE {JUN} GROUP BY a.name ORDER BY n DESC LIMIT 2""").fetchall()
legacy_top = con.execute(f"""SELECT a.name, COUNT(DISTINCT e.event_uuid) AS n
FROM events_v2 e JOIN users u ON u.id = e.actor_id
JOIN accounts a ON a.id = u.account_id AND a.is_test = 0
WHERE {JUN} GROUP BY a.name ORDER BY n DESC LIMIT 2""").fetchall()
print(f"  QB2 detail: correct top2={top}  legacy top2={legacy_top}")
assert top[0][1] > 1.3 * top[1][1], "QB2: correct top account not a clear winner"
assert legacy_top[0][1] > 1.3 * legacy_top[1][1], "QB2: legacy top account not a clear winner"
reg("QB2", top[0][0], {"legacy_account_id_join": legacy_top[0][0]})

# Q-B3: average July session length in minutes (per avg_session_minutes.sql)
b3_correct = q("""SELECT ROUND(AVG(s.duration) / 60000.0, 1) FROM sessions s
JOIN users u ON u.id = s.user_id AND u.deleted_at IS NULL
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE s.started_at >= strftime('%s','2026-07-01') AND s.started_at < strftime('%s','2026-08-01')""")
b3_seconds = q("""SELECT ROUND(AVG(s.duration) / 60.0, 1) FROM sessions s
JOIN users u ON u.id = s.user_id AND u.deleted_at IS NULL
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE s.started_at >= strftime('%s','2026-07-01') AND s.started_at < strftime('%s','2026-08-01')""")
b3_with_test = q("""SELECT ROUND(AVG(s.duration) / 60000.0, 1) FROM sessions s
JOIN users u ON u.id = s.user_id AND u.deleted_at IS NULL
WHERE s.started_at >= strftime('%s','2026-07-01') AND s.started_at < strftime('%s','2026-08-01')""")
reg("QB3", b3_correct,
    {"seconds_interpretation": b3_seconds, "with_test_accounts": b3_with_test},
    tolerance=0.2)

# Q-B4: current MRR in dollars (per mrr.sql)
b4 = q("""SELECT ROUND(SUM(CASE p.billing_period WHEN 'annual' THEN p.price_cents/12.0
ELSE p.price_cents END)/100.0, 2) FROM subscriptions s
JOIN plans p ON p.id = s.plan_id
JOIN accounts a ON a.id = s.account_id AND a.is_test = 0 WHERE s.status='a'""")
reg("QB4", b4, {
    "no_annual_normalization": q("""SELECT ROUND(SUM(p.price_cents)/100.0, 2) FROM subscriptions s
JOIN plans p ON p.id = s.plan_id
JOIN accounts a ON a.id = s.account_id AND a.is_test = 0 WHERE s.status='a'"""),
    "with_test_accounts": q("""SELECT ROUND(SUM(CASE p.billing_period WHEN 'annual'
THEN p.price_cents/12.0 ELSE p.price_cents END)/100.0, 2) FROM subscriptions s
JOIN plans p ON p.id = s.plan_id JOIN accounts a ON a.id = s.account_id
WHERE s.status='a'"""),
    "cents_confusion": round(b4 * 100, 2),
}, tolerance=1.0)

# Q-C1: accounts signed up Q2 2026 (per signups_by_quarter.sql)
reg("QC1",
    q("""SELECT COUNT(*) FROM accounts WHERE is_test = 0
AND created_at >= strftime('%s','2026-04-01') AND created_at < strftime('%s','2026-07-01')"""),
    {"with_test_accounts": q("""SELECT COUNT(*) FROM accounts
AND_PLACEHOLDER""".replace("AND_PLACEHOLDER",
        "WHERE created_at >= strftime('%s','2026-04-01') AND created_at < strftime('%s','2026-07-01')"))})

# Q-C2: MAU July 2026 (per monthly_active_users.sql)
c2 = q(f"""SELECT COUNT(DISTINCT e.actor_id) FROM events_v2 e
JOIN users u ON u.id = e.actor_id AND u.deleted_at IS NULL
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE e.type != 'heartbeat' AND {JUL}""")
reg("QC2", c2, {
    "with_heartbeats": q(f"""SELECT COUNT(DISTINCT e.actor_id) FROM events_v2 e
JOIN users u ON u.id = e.actor_id AND u.deleted_at IS NULL
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0 WHERE {JUL}"""),
    "with_deleted_users": q(f"""SELECT COUNT(DISTINCT e.actor_id) FROM events_v2 e
JOIN users u ON u.id = e.actor_id
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE e.type != 'heartbeat' AND {JUL}"""),
    "with_test_accounts": q(f"""SELECT COUNT(DISTINCT e.actor_id) FROM events_v2 e
JOIN users u ON u.id = e.actor_id AND u.deleted_at IS NULL
WHERE e.type != 'heartbeat' AND {JUL}"""),
})

# Q-C3: registered users now (per registered_users.sql)
reg("QC3",
    q("""SELECT COUNT(*) FROM users u
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE u.deleted_at IS NULL"""),
    {
        "raw_count": q("SELECT COUNT(*) FROM users"),
        "only_deleted_filter": q("SELECT COUNT(*) FROM users WHERE deleted_at IS NULL"),
        "only_test_filter": q("""SELECT COUNT(*) FROM users u
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0"""),
    })

# Q-C4: export events July 2026 (per export_usage_monthly.sql)
reg("QC4",
    q(f"SELECT COUNT(DISTINCT e.event_uuid) FROM events_v2 e {REAL} WHERE e.type='export' AND {JUL}"),
    {
        "no_dedup": q(f"SELECT COUNT(*) FROM events_v2 e {REAL} WHERE e.type='export' AND {JUL}"),
        "with_test_accounts": q(f"SELECT COUNT(DISTINCT e.event_uuid) FROM events_v2 e WHERE e.type='export' AND {JUL}"),
    })

# Sanity questions
reg("QS1", q("SELECT COUNT(*) FROM plans"), {})
answers["QS2"] = {
    "correct": ["accounts", "users", "memberships", "plans", "subscriptions",
                "events", "events_v2", "sessions"],
    "tolerance": 0,
    "variants": {},
}
print(f"QS2: correct={answers['QS2']['correct']}")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(answers, indent=2))
print(f"\nwrote {OUT}")
