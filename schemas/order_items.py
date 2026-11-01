CREATE_ORDER_ITEMS_TABLE ="""
CREATE TABLE IF NOT EXISTS order_items (
    item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),

    CONSTRAINT check_quantiy_is_valid CHECK (quantity > 0)
);
"""