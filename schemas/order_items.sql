"
CREATE TABLE order_items (
    item_id INT GENERATE ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2)
    FOREIGN KEY order_id REFERENCES orders(order_id)
    FOREIGN KEY product_id REFERENCES products(product_id)
);
"