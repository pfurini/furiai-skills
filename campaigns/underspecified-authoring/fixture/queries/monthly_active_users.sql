-- MAU by month (exec dashboard)
SELECT strftime('%Y-%m', e.ts, 'unixepoch') AS month,
       COUNT(DISTINCT e.actor_id) AS mau
FROM events_v2 e
JOIN users u ON u.id = e.actor_id AND u.deleted_at IS NULL
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE e.type != 'heartbeat'
GROUP BY 1
ORDER BY 1;
