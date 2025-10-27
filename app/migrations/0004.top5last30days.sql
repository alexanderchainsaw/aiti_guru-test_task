CREATE OR REPLACE VIEW top5_most_sold_products_last_30_days AS
SELECT product_id, product_name, top_level_category, total_sold
FROM (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    COALESCE(top_cat.name, 'no category') AS top_level_category,
    SUM(oi.quantity) AS total_sold,
    ROW_NUMBER() OVER (ORDER BY SUM(oi.quantity) DESC) AS rn
  FROM order_items oi
  JOIN orders o ON o.id = oi.order_id
  JOIN products p ON p.id = oi.product_id
  LEFT JOIN categories prod_cat ON prod_cat.id = p.category_id
  LEFT JOIN category_closure cc ON cc.descendant = p.category_id
  -- найти верхнюю категорию через closure: ancestor у которого parent_id IS NULL
  LEFT JOIN categories top_cat ON top_cat.id = cc.ancestor AND top_cat.parent_id IS NULL
  WHERE o.created_timestamp >= (now() at time zone 'utc') - INTERVAL '30 days'
    AND o.status_id NOT IN (1, 2, 7) -- Статусы при которых товар не считается купленным
  GROUP BY p.id, p.name, top_cat.name
) t
WHERE rn <= 5;