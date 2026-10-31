CREATE_PRODUCTS_TABLE ="""
CREATE TABLE IF NOT EXISTS products (
    product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    selling_price NUMERIC(10,2) NOT NULL,
    buying_price NUMERIC(10,2) NOT NULL,
    details JSONB

    CONSTRAINT check_productname_is_not_empty CHECK (TRIM(product_name) <> ''), 
    CONSTRAINT check_sellingprice_is_valid CHECK (selling_price > 0), 
    CONSTRAINT check_buyingprice_is_valid CHECK (buying_price > 0)

);
"""