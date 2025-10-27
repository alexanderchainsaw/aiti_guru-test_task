INSERT INTO clients (name, address) VALUES
('Acme Corp', '123 Industrial Ave'),
('Global Traders', '89 Commerce St'),
('Sunrise Market', '42 Hill Road'),
('Nova Retail', '5 Ocean Drive'),
('ByteShop', '17 Silicon Blvd');

-- Root categories
INSERT INTO categories (name, parent_id) VALUES
('Electronics', NULL),
('Home Appliances', NULL),
('Groceries', NULL);

-- Subcategories
INSERT INTO categories (name, parent_id) VALUES
('Phones', 1),
('Laptops', 1),
('TVs', 1),
('Refrigerators', 2),
('Washing Machines', 2),
('Fruits', 3),
('Vegetables', 3);

INSERT INTO products (name, category_id, quantity, price) VALUES
('iPhone 17', 4, 5, 999.99),
('Samsung Galaxy S24', 4, 70, 899.99),
('MacBook Pro 14"', 5, 30, 1999.00),
('Dell XPS 13', 5, 40, 1499.00),
('Sony Bravia 55"', 6, 20, 1299.00),
('LG OLED 65"', 6, 15, 1799.00),
('Bosch Refrigerator', 7, 25, 899.00),
('Samsung Washer', 8, 25, 749.00),
('Apples', 9, 200, 1.50),
('Carrots', 10, 180, 1.20);

INSERT INTO orders (client_id, status_id) VALUES
(1, 3), -- payment_success
(2, 4), -- processing
(3, 6), -- delivered
(4, 1), -- draft
(5, 3); -- payment_success