
from products import read_products
import psycopg2
from schemas.orders import CREATE_ORDERS_TABLE
from schemas.order_items import CREATE_ORDER_ITEMS_TABLE

def make_order(cursor):
    cursor.execute(CREATE_ORDERS_TABLE)
    cursor.execute(CREATE_ORDER_ITEMS_TABLE)
    
    order_items = {}
    order_status = "ongoing"
    connection = cursor.connection

    try:
        while order_status == "ongoing":
            read_products(cursor)

            selected_product_id = int(
                input("Select a product ID (0 to finish): ")
            )

            if selected_product_id == 0:
                order_status = "complete"
            else:
                quantity = int(input("Quantity: "))
                order_items[selected_product_id] = quantity

        if not order_items:
            print("Your cart is empty.")
            return

        create_order_query = """
            INSERT INTO orders (customer_id)
            VALUES (%s)
            RETURNING order_id
        """

        cursor.execute(create_order_query, (1,))
        order_id = cursor.fetchone()[0]

        print("Order created.")

        for item in order_items:
            get_unit_price_query = """
                SELECT selling_price
                FROM products
                WHERE product_id = %s
            """

            cursor.execute(get_unit_price_query, (item,))
            result = cursor.fetchone()

            if result is None:
                raise ValueError(f"Product {item} does not exist.")

            unit_price = result[0]

            create_order_item_query = """
                INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                create_order_item_query,
                (order_id, item, order_items[item], unit_price)
            )
        update_order_total_query = """
            UPDATE orders
            SET total = (
                SELECT SUM(quantity * unit_price)
                FROM order_items
                WHERE order_id = %s
            )
            WHERE order_id = %s
        """
        
        cursor.execute(
                        update_order_total_query,
                        (order_id, order_id)
        )
        connection.commit()
        print("Order completed successfully!")

    except (psycopg2.Error, ValueError) as e:
        connection.rollback()
        print(f"Order creation failed: {e}")

def read_orders(cursor):
    read_orders_query = """
        SELECT * 
        FROM orders
    """
    
    try:
        print("----------ORDERS---------")
        cursor.execute(read_orders_query)
        print(cursor.fetchall())
    except psycopg2.Error as e:
        print(e)        
    

def generate_customer_revenue(cursor):
    query = """
        WITH customer_revenue AS (
            SELECT
                customer_id,
                SUM(total) AS total_revenue
            FROM orders
            GROUP BY customer_id
        )

        SELECT *
        FROM customer_revenue
        ORDER BY total_revenue DESC;
    """

    try:
        cursor.execute(query)
        revenue = cursor.fetchall()

        print("\n---------- CUSTOMER REVENUE ----------")

        for customer in revenue:
            print(
                f"Customer ID: {customer[0]} | "
                f"Total Revenue: {customer[1]}"
            )

    except psycopg2.Error as e:
        print(f"Could not generate customer revenue: {e}")
