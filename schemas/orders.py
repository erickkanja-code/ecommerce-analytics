CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INT GENERATE ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total NUMERIC(10,2),

    FOREIGN KEY customer_id REFERENCES customers(customer_id),

    CONSTRAINT check_total_is_valid CHECK (total > 0)

);
"""