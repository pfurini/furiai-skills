#!/usr/bin/env python3
"""Deterministic seed-data generator for the underspecified-authoring fixture.

This file lives OUTSIDE the fixture on purpose: it encodes the planted
conventions (test-account activity, heartbeat-only users, duplicate event
rows, the Acme->Zenith migration, ms durations) and must never be visible to
test subjects. Subjects only ever see staged copies of fixture/.

Writes CSVs into fixture/seed/ and rebuilds fixture/db/analytics.sqlite via
the fixture's own build script.
"""

import csv
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / "fixture"
SEED = FIXTURE / "seed"

rng = random.Random(20260801)


def epoch(y, m, d, h=0, mi=0, s=0):
    return int(datetime(y, m, d, h, mi, s, tzinfo=timezone.utc).timestamp())


NOW = epoch(2026, 8, 1)  # frozen "as of" instant for the fixture snapshot

JUL_START, JUL_END = epoch(2026, 7, 1), epoch(2026, 8, 1)
JUN_START, JUN_END = epoch(2026, 6, 1), epoch(2026, 7, 1)

MONTHS_2026 = {  # generation window for events_v2
    3: (epoch(2026, 3, 1), epoch(2026, 4, 1)),
    4: (epoch(2026, 4, 1), epoch(2026, 5, 1)),
    5: (epoch(2026, 5, 1), epoch(2026, 6, 1)),
    6: (JUN_START, JUN_END),
    7: (JUL_START, JUL_END),
}

REAL_ACCOUNT_NAMES = [
    "Acme Analytics", "Zenith Robotics", "Blue Harbor Media", "Cobalt Systems",
    "Driftwood Labs", "Everfield Health", "Fjord Logistics", "Gable & Sons",
    "Halcyon Grid", "Ironvale Mining", "Juniper Retail", "Kestrel Aero",
    "Lumen Payments", "Maplewright Co", "Northbeam Energy", "Opal Textiles",
    "Pinecrest Foods", "Quarry Digital", "Riverstone Legal", "Saltbrook Travel",
    "Tidewater Marine", "Umbra Security", "Vantage Realty", "Willow & Birch",
    "Xylo Instruments", "Yarrow Biotech", "Zephyr Couriers", "Arcline CAD",
    "Basalt Cloud", "Cinder Games", "Dockside Brewing", "Elmspring Schools",
    "Foxglove Beauty", "Granite Ledger", "Hollowell Farms", "Indigo Press",
    "Jetty Insurance", "Kilnworks Pottery", "Larkspur Events", "Mistral Wines",
    "Nook Furniture", "Orchard Dental", "Pillar Finance", "Quill Publishing",
]
TEST_ACCOUNT_NAMES = [
    "QA Sandbox", "Internal Test", "Staging Smoke", "Loadtest Rig",
    "Demo Test Org", "E2E Bot Farm",
]

ACME, ZENITH = 1, 2
N_REAL_ACCOUNTS = 44
N_ACCOUNTS = 50
MIGRATED = list(range(1, 19))       # users 1-18: Acme -> Zenith
ACME_STAY = list(range(19, 29))     # users 19-28 remain on Acme
ZENITH_NATIVE = list(range(29, 35))  # users 29-34
FIRST_OTHER_USER, LAST_OTHER_USER = 35, 388
FIRST_TEST_USER, LAST_TEST_USER = 389, 412


def rand_ts(lo, hi):
    return rng.randint(lo, hi - 1)


def build_accounts():
    rows = []
    for i in range(1, N_ACCOUNTS + 1):
        if i <= N_REAL_ACCOUNTS:
            name, is_test = REAL_ACCOUNT_NAMES[i - 1], 0
            if i <= 20:
                created = rand_ts(epoch(2024, 1, 1), epoch(2025, 1, 1))
            elif i <= 30:
                created = rand_ts(epoch(2025, 1, 1), epoch(2026, 1, 1))
            elif i <= 35:
                created = rand_ts(epoch(2026, 1, 1), epoch(2026, 4, 1))
            else:  # 36-44: the 9 real Q2-2026 signups
                created = rand_ts(epoch(2026, 4, 1), epoch(2026, 7, 1))
        else:
            name, is_test = TEST_ACCOUNT_NAMES[i - 45], 1
            if i in (45, 46, 47):  # 3 test accounts created in Q2 2026
                created = rand_ts(epoch(2026, 4, 1), epoch(2026, 7, 1))
            else:
                created = rand_ts(epoch(2025, 6, 1), epoch(2026, 3, 1))
        rows.append({"id": i, "name": name, "is_test": is_test, "created_at": created})
    return rows


def user_home_account(uid):
    """Current true account (primary membership)."""
    if uid in MIGRATED or uid in ZENITH_NATIVE:
        return ZENITH if uid in MIGRATED or uid in ZENITH_NATIVE else ACME
    if uid in ACME_STAY:
        return ACME
    if FIRST_OTHER_USER <= uid <= LAST_OTHER_USER:
        return 3 + (uid - FIRST_OTHER_USER) % 42
    return 45 + (uid - FIRST_TEST_USER) % 6


def legacy_account(uid):
    """Stale users.account_id: migrated users still point at Acme."""
    return ACME if uid in MIGRATED else user_home_account(uid)


def build_users(accounts):
    acct_created = {a["id"]: a["created_at"] for a in accounts}
    deletable = [u for u in range(FIRST_OTHER_USER, LAST_OTHER_USER + 1)]
    deleted = rng.sample(deletable, 40)
    late_deleted = deleted[:8]  # deleted mid/late July, with early-July activity
    rows = []
    for uid in range(1, LAST_TEST_USER + 1):
        home = user_home_account(uid)
        created = rand_ts(max(acct_created[home], epoch(2024, 1, 1)), epoch(2026, 3, 1)) \
            if acct_created[home] < epoch(2026, 3, 1) else rand_ts(acct_created[home], NOW)
        if uid in late_deleted:
            deleted_at = rand_ts(epoch(2026, 7, 15), epoch(2026, 8, 1))
        elif uid in deleted:
            deleted_at = rand_ts(epoch(2026, 1, 1), epoch(2026, 7, 10))
        else:
            deleted_at = ""
        domain = "example-test.dev" if home >= 45 else f"corp{home}.example"
        rows.append({
            "id": uid,
            "email": f"user{uid}@{domain}" if home < 45 else f"bot{uid}@{domain}",
            "account_id": legacy_account(uid),
            "created_at": created,
            "deleted_at": deleted_at,
        })
    return rows, set(deleted), set(late_deleted)


def build_memberships():
    rows = []
    mid = 0
    for uid in range(1, LAST_TEST_USER + 1):
        home = user_home_account(uid)
        mid += 1
        rows.append({"id": mid, "user_id": uid, "account_id": home,
                     "is_primary": 1, "created_at": rand_ts(epoch(2026, 1, 5), epoch(2026, 2, 1))})
        if uid in MIGRATED:  # old Acme membership kept, non-primary
            mid += 1
            rows.append({"id": mid, "user_id": uid, "account_id": ACME,
                         "is_primary": 0, "created_at": rand_ts(epoch(2026, 1, 5), epoch(2026, 2, 1))})
    for uid in (100, 120, 140, 160, 180, 200):  # consultants with a second account
        mid += 1
        rows.append({"id": mid, "user_id": uid,
                     "account_id": 3 + (uid - FIRST_OTHER_USER + 5) % 42,
                     "is_primary": 0, "created_at": rand_ts(epoch(2026, 2, 1), epoch(2026, 6, 1))})
    return rows


def build_plans_subs(accounts):
    plans = [
        {"id": 1, "name": "starter", "price_cents": 2900, "billing_period": "monthly"},
        {"id": 2, "name": "growth", "price_cents": 9900, "billing_period": "monthly"},
        {"id": 3, "name": "scale", "price_cents": 24900, "billing_period": "monthly"},
        {"id": 4, "name": "enterprise", "price_cents": 588000, "billing_period": "annual"},
    ]
    # status codes: a=active c=canceled t=trial p=past_due (mapping surfaces only
    # in the CHECK constraint and account_health.sql)
    status = {}
    for a in range(1, 31):
        status[a] = "a"
    for a in (31, 32, 33, 34, 41, 42):
        status[a] = "c"
    for a in (36, 37, 38, 39, 40):
        status[a] = "t"
    for a in (35, 43, 44):
        status[a] = "p"
    for a in (45, 46, 47):  # test accounts with live starter subs (naive-MRR trap)
        status[a] = "a"
    plan_of = {}
    for a in range(1, 31):
        if a in (1, 2):
            plan_of[a] = 4          # enterprise annual: Acme, Zenith
        elif a <= 8:
            plan_of[a] = 3          # scale x6
        elif a <= 18:
            plan_of[a] = 2          # growth x10
        else:
            plan_of[a] = 1          # starter x12
    acct_created = {a["id"]: a["created_at"] for a in accounts}
    subs = []
    sid = 0
    for a, st in sorted(status.items()):
        sid += 1
        started = rand_ts(acct_created[a], min(acct_created[a] + 90 * 86400, NOW - 1))
        subs.append({
            "id": sid, "account_id": a,
            "plan_id": plan_of.get(a, rng.choice([1, 2])),
            "status": st, "started_at": started,
            "canceled_at": rand_ts(min(started + 30 * 86400, NOW - 86400), NOW) if st == "c" else "",
        })
    return plans, subs


class EventGen:
    def __init__(self):
        self.rows = []
        self.next_id = 0
        self.next_uuid = 0

    def add(self, actor, etype, ts):
        self.next_id += 1
        self.next_uuid += 1
        self.rows.append({"id": self.next_id, "event_uuid": f"evt-{self.next_uuid:07d}",
                          "actor_id": actor, "type": etype, "ts": ts})

    def duplicate_some(self):
        """Ingest double-writes: same event_uuid, new row id. Exports dup harder."""
        dups = []
        for r in self.rows:
            p = 0.25 if r["type"] == "export" else 0.08
            if rng.random() < p:
                self.next_id += 1
                dups.append({**r, "id": self.next_id})
        self.rows.extend(dups)


NONHB_TYPES = ["session_start", "page_view", "action", "export"]
NONHB_W = [0.30, 0.35, 0.25, 0.10]


def build_events(users, deleted, late_deleted):
    ev = EventGen()
    user_created = {u["id"]: u["created_at"] for u in users}
    user_deleted_at = {u["id"]: u["deleted_at"] for u in users if u["deleted_at"] != ""}
    real_users = [u["id"] for u in users if user_home_account(u["id"]) < 45]
    test_users = [u["id"] for u in users if user_home_account(u["id"]) >= 45]

    def alive_window(uid, lo, hi):
        lo = max(lo, user_created[uid])
        if uid in user_deleted_at:
            hi = min(hi, user_deleted_at[uid])
        return (lo, hi) if lo < hi - 3600 else None

    hb_users = {u for u in real_users if u % 5 in (0, 1)}
    hb_only_july = set(rng.sample(
        [u for u in real_users if u not in deleted
         and u not in MIGRATED and u not in ACME_STAY and u not in ZENITH_NATIVE], 25))

    crafted_june = set(MIGRATED) | set(ACME_STAY) | set(ZENITH_NATIVE)
    for uid in MIGRATED:
        for _ in range(rng.randint(25, 40)):
            ev.add(uid, rng.choices(NONHB_TYPES, NONHB_W)[0], rand_ts(JUN_START, JUN_END))
    for uid in ACME_STAY:
        for _ in range(rng.randint(15, 25)):
            ev.add(uid, rng.choices(NONHB_TYPES, NONHB_W)[0], rand_ts(JUN_START, JUN_END))
    for uid in ZENITH_NATIVE:
        for _ in range(rng.randint(10, 20)):
            ev.add(uid, rng.choices(NONHB_TYPES, NONHB_W)[0], rand_ts(JUN_START, JUN_END))

    for month, (lo, hi) in MONTHS_2026.items():
        for uid in real_users:
            w = alive_window(uid, lo, hi)
            if w is None:
                continue
            if month == 6 and uid in crafted_june:
                pass  # june volume already crafted above
            elif month == 7 and uid in hb_only_july:
                pass  # heartbeats only (below): inflates naive MAU
            elif rng.random() < 0.55:
                for _ in range(rng.randint(3, 12)):
                    ev.add(uid, rng.choices(NONHB_TYPES, NONHB_W)[0], rand_ts(*w))
            if uid in hb_users or (month == 7 and uid in hb_only_july):
                for _ in range(rng.randint(10, 30)):
                    ev.add(uid, "heartbeat", rand_ts(*w))
        for uid in test_users:  # QA bots: heavy, every month
            w = alive_window(uid, lo, hi)
            if w is None:
                continue
            for _ in range(rng.randint(30, 60)):
                ev.add(uid, rng.choices(NONHB_TYPES, NONHB_W)[0], rand_ts(*w))
            for _ in range(rng.randint(40, 80)):
                ev.add(uid, "heartbeat", rand_ts(*w))

    # late-July-deleted users: guaranteed early-July activity (visible only if
    # the deleted_at filter is dropped -- their deleted_at postdates the events)
    for uid in late_deleted:
        for _ in range(rng.randint(3, 6)):
            ev.add(uid, rng.choices(NONHB_TYPES, NONHB_W)[0],
                   rand_ts(JUL_START, epoch(2026, 7, 14)))

    ev.duplicate_some()
    return ev.rows


def build_legacy_events(users, events_v2):
    """Deprecated `events` table: historical rows, plus the legacy tracker still
    mirroring session_start/page_view after the v2 cutover (so recent-month
    counts on it are plausible but wrong)."""
    rows = []
    nid = 0
    user_created = {u["id"]: u["created_at"] for u in users}
    uids = [u["id"] for u in users]
    lo, hi = epoch(2025, 6, 1), epoch(2026, 3, 1)
    for _ in range(2500):
        uid = rng.choice(uids)
        ts = rand_ts(max(lo, user_created[uid]), hi) if user_created[uid] < hi - 3600 else rand_ts(lo, hi)
        nid += 1
        rows.append({"id": nid, "user_id": uid,
                     "type": rng.choices(["session_start", "page_view", "action"], [0.35, 0.45, 0.2])[0],
                     "ts": ts})
    for r in events_v2:
        if r["type"] in ("session_start", "page_view") and rng.random() < 0.7:
            nid += 1
            rows.append({"id": nid, "user_id": r["actor_id"], "type": r["type"], "ts": r["ts"]})
    return rows


def build_sessions(users, deleted):
    rows = []
    sid = 0
    user_created = {u["id"]: u["created_at"] for u in users}
    user_deleted_at = {u["id"]: u["deleted_at"] for u in users if u["deleted_at"] != ""}
    for lo, hi in [(epoch(2026, 5, 1), epoch(2026, 6, 1)),
                   (JUN_START, JUN_END), (JUL_START, JUL_END)]:
        for u in users:
            uid = u["id"]
            wlo = max(lo, user_created[uid])
            whi = min(hi, user_deleted_at.get(uid, hi))
            if wlo >= whi - 3600:
                continue
            test = user_home_account(uid) >= 45
            if test:
                for _ in range(rng.randint(2, 8)):  # bot sessions: very short
                    sid += 1
                    rows.append({"id": sid, "user_id": uid,
                                 "started_at": rand_ts(wlo, whi),
                                 "duration": rng.randint(20000, 90000)})
            elif rng.random() < 0.5:
                for _ in range(rng.randint(1, 6)):
                    sid += 1
                    rows.append({"id": sid, "user_id": uid,
                                 "started_at": rand_ts(wlo, whi),
                                 "duration": rng.randint(180000, 2100000)})  # ms
    return rows


def write_csv(name, rows, fields):
    SEED.mkdir(parents=True, exist_ok=True)
    with open(SEED / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  seed/{name}: {len(rows)} rows")


def main():
    accounts = build_accounts()
    users, deleted, late_deleted = build_users(accounts)
    memberships = build_memberships()
    plans, subs = build_plans_subs(accounts)
    events_v2 = build_events(users, deleted, late_deleted)
    events = build_legacy_events(users, events_v2)
    sessions = build_sessions(users, deleted)

    write_csv("accounts.csv", accounts, ["id", "name", "is_test", "created_at"])
    write_csv("users.csv", users, ["id", "email", "account_id", "created_at", "deleted_at"])
    write_csv("memberships.csv", memberships, ["id", "user_id", "account_id", "is_primary", "created_at"])
    write_csv("plans.csv", plans, ["id", "name", "price_cents", "billing_period"])
    write_csv("subscriptions.csv", subs, ["id", "account_id", "plan_id", "status", "started_at", "canceled_at"])
    write_csv("events.csv", events, ["id", "user_id", "type", "ts"])
    write_csv("events_v2.csv", events_v2, ["id", "event_uuid", "actor_id", "type", "ts"])
    write_csv("sessions.csv", sessions, ["id", "user_id", "started_at", "duration"])

    print("building sqlite...")
    subprocess.run([sys.executable, str(FIXTURE / "db" / "build_db.py")], check=True)
    print("done")


if __name__ == "__main__":
    main()
