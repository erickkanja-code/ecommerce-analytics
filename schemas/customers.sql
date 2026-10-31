"
CREATE TABLE customers (
    customer_id INT GENERATE ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,

    CONSTRAINT check_name_is_valid CHECK (first_name <> ''), 
    CONSTRAINT check_name_is_valid CHECK (last_name <> ''), 
);
"