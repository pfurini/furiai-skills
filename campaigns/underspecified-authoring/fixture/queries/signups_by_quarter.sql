-- New accounts per quarter
SELECT strftime('%Y', created_at, 'unixepoch') || '-Q' ||
       ((strftime('%m', created_at, 'unixepoch') + 2) / 3) AS quarter,
       COUNT(*) AS new_accounts
FROM accounts
WHERE is_test = 0
GROUP BY 1
ORDER BY 1;
