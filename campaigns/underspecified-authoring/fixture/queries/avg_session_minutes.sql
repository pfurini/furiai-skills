-- Average session length in minutes, by month
SELECT strftime('%Y-%m', s.started_at, 'unixepoch') AS month,
       ROUND(AVG(s.duration) / 60000.0, 1) AS avg_minutes
FROM sessions s
JOIN users u ON u.id = s.user_id AND u.deleted_at IS NULL
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
GROUP BY 1
ORDER BY 1;
