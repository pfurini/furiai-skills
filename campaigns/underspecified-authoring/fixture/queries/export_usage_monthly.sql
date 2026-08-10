-- Export feature usage by month
SELECT strftime('%Y-%m', e.ts, 'unixepoch') AS month,
       COUNT(DISTINCT e.event_uuid) AS exports
FROM events_v2 e
JOIN users u ON u.id = e.actor_id
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id
WHERE a.is_test = 0
  AND e.type = 'export'
GROUP BY 1
ORDER BY 1;
