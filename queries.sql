--  Get users with purchases in the last 30 days
SELECT u.user_id, u.name, u.email
FROM users u
JOIN transactions t ON u.user_id = t.user_id
WHERE t.date >= NOW() - INTERVAL '30 days';

-- Get the top 3 products by purchase frequency
SELECT p.product_id, p.name, SUM(td.quantity) AS total_quantity
FROM products p
JOIN transaction_details td ON p.product_id = td.product_id
GROUP BY p.product_id
ORDER BY SUM(td.quantity) DESC
LIMIT 3;

-- Calculate revenue per product category
SELECT p.category, SUM(td.quantity * p.price) AS revenue
FROM products p
JOIN transaction_details td ON p.product_id = td.product_id
GROUP BY p.category;

--  Transaction summaries with item counts
SELECT t.transaction_id, COUNT(td.product_id) AS item_count, 
       SUM(td.quantity * p.price) AS total_amount
FROM transactions t
JOIN transaction_details td ON t.transaction_id = td.transaction_id
JOIN products p ON td.product_id = p.product_id
GROUP BY t.transaction_id;

--  Users exceeding $500 in total purchases
SELECT u.user_id, u.name, SUM(td.quantity * p.price) AS total_spent
FROM users u
JOIN transactions t ON u.user_id = t.user_id
JOIN transaction_details td ON t.transaction_id = td.transaction_id
JOIN products p ON td.product_id = p.product_id
GROUP BY u.user_id
HAVING SUM(td.quantity * p.price) > 500;

--  Remaining stock for a product
SELECT p.product_id, (p.stock - COALESCE(SUM(td.quantity), 0)) AS remaining_stock
FROM products p
LEFT JOIN transaction_details td ON p.product_id = td.product_id
WHERE p.product_id = :product_id
GROUP BY p.product_id;
