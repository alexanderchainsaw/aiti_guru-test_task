CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id INTEGER REFERENCES categories(id) ON DELETE SET NULL DEFAULT NULL ,
    created_timestamp TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- оптимизация поиска по вложенным категориям
CREATE TABLE category_closure (
    ancestor INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    descendant INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    depth INTEGER NOT NULL,
    PRIMARY KEY (ancestor, descendant)
);

CREATE INDEX idx_category_closure_descendant ON category_closure(descendant);
CREATE INDEX idx_category_closure_ancestor ON category_closure(ancestor);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    price NUMERIC(12,2) NOT NULL, -- Актуальная цена товара
    created_timestamp TIMESTAMP DEFAULT (now() at time zone 'utc')
);

CREATE INDEX idx_products_category_id ON products(category_id);

CREATE TABLE order_statuses(
    id SERIAL PRIMARY KEY,
    status_name VARCHAR(20),
    description TEXT DEFAULT NULL
);

-- еще можно так

--CREATE TYPE order_status AS ENUM (
--  'draft', 'awaiting_payment', 'payment_success', 'processing',
--  'in_delivery', 'delivered', 'canceled'
--);

INSERT INTO order_statuses(status_name) VALUES ('draft'); -- id 1
INSERT INTO order_statuses(status_name) VALUES ('awaiting_payment'); -- id 2
INSERT INTO order_statuses(status_name) VALUES ('payment_success'); -- id 3
INSERT INTO order_statuses(status_name) VALUES ('processing'); -- id 4
INSERT INTO order_statuses(status_name) VALUES ('in_delivery'); -- id 5
INSERT INTO order_statuses(status_name) VALUES ('delivered'); -- id 6
INSERT INTO order_statuses(status_name) VALUES ('canceled'); -- id 7

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    created_timestamp TIMESTAMP DEFAULT (now() at time zone 'utc'),
    status_id INTEGER REFERENCES order_statuses(id) ON DELETE SET NULL
);

CREATE TABLE order_status_changes(
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    old_status_id INTEGER REFERENCES order_statuses(id) ON DELETE RESTRICT,
    new_status_id INTEGER REFERENCES order_statuses(id) ON DELETE RESTRICT,
    created_timestamp TIMESTAMP DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY(order_id, old_status_id, new_status_id)
);


CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order NUMERIC(12,2) NOT NULL, -- Цена товара на момент совершения заказа
    PRIMARY KEY (order_id, product_id)
);

CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);


