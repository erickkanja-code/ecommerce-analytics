"
CREATE TABLE orders (
    order_id INT GENERATE ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total NUMERIC(10,2)
    FOREIGN KEY customer_id REFERENCES customers(customer_id)
);
"