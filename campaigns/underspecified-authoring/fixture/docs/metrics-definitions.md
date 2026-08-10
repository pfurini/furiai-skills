# Metric definitions

_Last updated: February 2026_

The definitions below are the ones the exec dashboard uses. When a number you
compute disagrees with the dashboard, the dashboard is right and your query is
wrong; the canonical implementations live in `queries/`.

## MRR (monthly recurring revenue)

Sum of the monthly price of every **active** subscription. Annual plans are
normalized to a monthly figure: divide the annual price by 12. Reported in
dollars.

## Active user

A user who was active in the product during the period.

## Signups

New accounts created in the period.

## Session length

Average session duration over the period, reported in minutes.

## Event volume

Number of events recorded in the period.
