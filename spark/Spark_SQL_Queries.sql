-- Inspect transactions
SELECT transaction_id, user_id, total, status
FROM transactions
LIMIT 10;

-- Logical representation of item normalization
SELECT item.product_id, item.subtotal
FROM transactions
LATERAL VIEW explode(items) exploded_items AS item;

-- Revenue aggregation by category
SELECT category_id, SUM(subtotal) AS total_revenue
FROM transaction_items
GROUP BY category_id
ORDER BY total_revenue DESC;

-- Customer transaction summary
SELECT user_id,
       COUNT(transaction_id) AS num_transactions,
       SUM(total) AS total_spent
FROM transactions
GROUP BY user_id;
