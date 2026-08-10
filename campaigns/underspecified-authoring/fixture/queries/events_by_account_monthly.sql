-- Event volume per account per month (CS dashboard)
SELECT strftime('%Y-%m', e.ts, 'unixepoch') AS month,
       a.name AS account,
       COUNT(DISTINCT e.event_uuid) AS events
FROM events_v2 e
JOIN users u ON u.id = e.actor_id
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id
WHERE a.is_test = 0
GROUP BY 1, 2
ORDER BY 1, events DESC;
