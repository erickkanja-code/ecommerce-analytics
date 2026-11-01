
import psycopg2
from schemas.products import CREATE_PRODUCTS_TABLE
import math


def create_product(cursor):
    try:
        cursor.execute(CREATE_PRODUCTS_TABLE)
    except psycopg2.Error as e:
        print(f"{e}")

    product_name = input("Enter the product's name:")
    selling_price = round(float(input("Enter the selling price:")), 2)
    buying_price = round(float(input("Enter the buying price:")), 2)

    query = """
        INSERT INTO products (product_name, selling_price, buying_price)
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(query, (product_name, selling_price, buying_price))
        cursor.connection.commit()
        print("Product created successfully")
    except psycopg2.Error as e:
        print(f"Product creation failed: {e}")


def read_products(cursor):
    query = "SELECT * FROM products"

    try:
        cursor.execute(query)
        products = cursor.fetchall()

        for product in products:
            print(
                f"\n{product[0]}: {product[1]} "
                f"| Selling Price: {product[2]}"
            )

            if product[5]:
                print("Product Details:")
                for key, value in product[5].items():
                    print(f"  {key}: {value}")

    except psycopg2.Error as e:
        print(e)


def search_products_by_brand(cursor):
    brand = input("Enter brand: ")

    query = """
        SELECT product_id, product_name, details ->> 'brand'
        FROM products
        WHERE details ->> 'brand' = %s
    """

    try:
        cursor.execute(query, (brand,))
        products = cursor.fetchall()

        if not products:
            print("No products found for that brand.")
            return

        print("\n---------- SEARCH RESULTS ----------")
        for product in products:
            print(
                f"ID: {product[0]} | "
                f"Name: {product[1]} | "
                f"Brand: {product[2]}"
            )

    except psycopg2.Error as e:
        print(f"Product search failed: {e}")


def update_product(cursor):
    read_products(cursor)

    product_id = int(
        input("Select one of the products above. Enter a number 1, 2 or 3 etc...")
    )

    new_selling_price = round(
        float(input("Enter the new selling price for this product")), 2
    )

    update_selling_price_query = """
        UPDATE products
        SET selling_price = %s
        WHERE product_id = %s
    """

    try:
        cursor.execute(
            update_selling_price_query,
            (new_selling_price, product_id)
        )

        print("Product updated successfully")

        cursor.execute(
            "SELECT * FROM products WHERE product_id = %s",
            (product_id,)
        )

        print(cursor.fetchall())
        cursor.connection.commit()

    except psycopg2.Error as e:
        print(e)


def delete_product(cursor):
    read_products(cursor)

    product_id = int(
        input("Select one of the products above. Enter a number 1, 2 or 3 etc...")
    )

    query = """
        DELETE FROM products
        WHERE product_id = %s
    """

    try:
        cursor.execute(query, (product_id,))
        cursor.connection.commit()
        print("Product deleted successfully")

    except psycopg2.Error as e:
        print(e)


def generate_product_ranking(cursor):
    query = """
        SELECT
            product_id,
            SUM(quantity) AS total_sold,
            RANK() OVER (
                ORDER BY SUM(quantity) DESC
            ) AS product_rank
        FROM order_items
        GROUP BY product_id
    """

    try:
        cursor.execute(query)
        rankings = cursor.fetchall()

        print("\n---------- PRODUCT RANKING ----------")

        for product in rankings:
            print(
                f"Rank: {product[2]} | "
                f"Product ID: {product[0]} | "
                f"Units Sold: {product[1]}"
            )

    except psycopg2.Error as e:
        print(f"Could not generate product ranking: {e}")
