-- Per-account subscription snapshot for the CS dashboard
SELECT a.name AS account,
       CASE s.status
            WHEN 'a' THEN 'active'
            WHEN 't' THEN 'trial'
            WHEN 'p' THEN 'past_due'
            WHEN 'c' THEN 'canceled'
       END AS status,
       p.name AS plan,
       p.price_cents / 100.0 AS price_dollars
FROM accounts a
JOIN subscriptions s ON s.account_id = a.id
JOIN plans p ON p.id = s.plan_id
WHERE a.is_test = 0
ORDER BY a.name;
