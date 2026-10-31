"
CREATE TABLE products (
    product_id INT GENERATE ALWAYS AS IDENTITY PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    selling_price NUMERIC(10,2) NOT NULL,
    buying_price NUMERIC(10,2) NOT NULL,
    details JSONB
);
"