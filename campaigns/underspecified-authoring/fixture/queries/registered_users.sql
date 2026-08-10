-- Registered user count (investor update)
SELECT COUNT(*) AS registered_users
FROM users u
JOIN memberships m ON m.user_id = u.id AND m.is_primary = 1
JOIN accounts a ON a.id = m.account_id AND a.is_test = 0
WHERE u.deleted_at IS NULL;
