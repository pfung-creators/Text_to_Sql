CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    signup_date DATE,
    country TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10,2)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    status TEXT
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2)
);

INSERT INTO customers (name, email, signup_date, country) VALUES
('Alice Kumar', 'alice@example.com', '2024-01-15', 'India'),
('Bob Smith', 'bob@example.com', '2024-03-02', 'USA'),
('Chen Wei', 'chen@example.com', '2024-05-20', 'China');

INSERT INTO products (name, category, price) VALUES
('Wireless Mouse', 'Electronics', 25.00),
('Office Chair', 'Furniture', 150.00),
('Notebook', 'Stationery', 3.50);

INSERT INTO orders (customer_id, order_date, status) VALUES
(1, '2024-06-01', 'completed'),
(2, '2024-06-05', 'completed'),
(1, '2024-07-10', 'pending');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 25.00),
(1, 3, 5, 3.50),
(2, 2, 1, 150.00),
(3, 1, 1, 25.00);
