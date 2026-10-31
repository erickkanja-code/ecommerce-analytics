CREATE_CUSTOMERS_TABLE = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,

    CONSTRAINT check_firstname_is_not_empty CHECK (TRIM(first_name) <> ''), 
    CONSTRAINT check_lastname_is_not_empty CHECK (TRIM(last_name) <> '')
);
"""