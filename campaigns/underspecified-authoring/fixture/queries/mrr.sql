-- Current MRR in dollars (exec dashboard headline)
SELECT ROUND(SUM(CASE p.billing_period
                     WHEN 'annual' THEN p.price_cents / 12.0
                     ELSE p.price_cents
                 END) / 100.0, 2) AS mrr_dollars
FROM subscriptions s
JOIN plans p ON p.id = s.plan_id
JOIN accounts a ON a.id = s.account_id AND a.is_test = 0
WHERE s.status = 'a';
