
CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total NUMERIC(10,2) DEFAULT 0,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
"""

