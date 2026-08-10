# Analytics database overview

_Last updated: November 2025_

Our product analytics live in a single SQLite database at `db/analytics.sqlite`,
rebuilt nightly from the warehouse export. Schema DDL is under `db/schema/`,
history under `db/migrations/`, and the reporting queries the growth team runs
are collected in `queries/`.

All timestamps everywhere are **unix epoch seconds, UTC**. Convert calendar
dates with `strftime('%s', '2026-07-01')` when filtering.

## Tables

| Table | What it holds |
|---|---|
| `accounts` | One row per customer organization |
| `users` | People. `users.account_id` links each user to their account |
| `plans` | Our price book |
| `subscriptions` | One row per account subscription with its status |
| `events` | The product event stream (one row per tracked action) |
| `sessions` | App sessions per user: `started_at` and `duration` (seconds) |

## Relationships

```
accounts 1--n users 1--n events
accounts 1--n subscriptions n--1 plans
users 1--n sessions
```

Join events to accounts through `users.account_id`.

## Event types

`session_start`, `page_view`, `action`, `export`, plus internal housekeeping
types emitted by the clients.
