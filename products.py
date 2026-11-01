"""Handle product operations and product analytics."""

import json

import psycopg2
import redis

from redis_connection import redis_client
from schemas.products import CREATE_PRODUCTS_TABLE


def create_product(cursor):
    """Create a product after validating its details."""

    # Ensure the products table exists.
    try:
        cursor.execute(CREATE_PRODUCTS_TABLE)
    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Could not prepare products table: {error}")
        return

    product_name = input("Enter the product's name: ").strip()

    if not product_name:
        print("Product name cannot be empty.")
        return

    # Validate that both prices are valid positive numbers.
    try:
        selling_price = round(
            float(input("Enter the selling price: ")), 2
        )
        buying_price = round(
            float(input("Enter the buying price: ")), 2
        )

        if selling_price <= 0 or buying_price <= 0:
            print("Prices must be greater than zero.")
            return

    except ValueError:
        print("Please enter valid numbers for the prices.")
        return

    query = """
        INSERT INTO products (product_name, selling_price, buying_price)
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(
            query,
            (product_name, selling_price, buying_price),
        )
        cursor.connection.commit()
        print("Product created successfully.")

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Product creation failed: {error}")


def read_products(cursor):
    """Retrieve and display all products."""

    query = """
        SELECT product_id, product_name, selling_price, details
        FROM products
        ORDER BY product_id
    """

    try:
        cursor.execute(query)
        products = cursor.fetchall()

        if not products:
            print("No products found.")
            return

        print("\n---------- PRODUCTS ----------")

        for product in products:
            print(
                f"\nID: {product[0]} | "
                f"Name: {product[1]} | "
                f"Selling Price: {product[2]}"
            )

            # PostgreSQL JSONB data is returned as a Python dictionary.
            if product[3]:
                print("Product Details:")

                for key, value in product[3].items():
                    print(f"  {key}: {value}")

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Could not retrieve products: {error}")


def search_products_by_brand(cursor):
    """Find products using the brand stored in their JSONB details."""

    brand = input("Enter brand: ").strip()

    if not brand:
        print("Brand cannot be empty.")
        return

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

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Product search failed: {error}")


def update_product(cursor):
    """Update the selling price of an existing product."""

    read_products(cursor)

    try:
        product_id = int(input("Enter the product ID to update: "))
        new_selling_price = round(
            float(input("Enter the new selling price: ")), 2
        )

        if product_id <= 0:
            print("Product ID must be greater than zero.")
            return

        if new_selling_price <= 0:
            print("Selling price must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid product ID and price.")
        return

    query = """
        UPDATE products
        SET selling_price = %s
        WHERE product_id = %s
    """

    try:
        cursor.execute(query, (new_selling_price, product_id))

        if cursor.rowcount == 0:
            print("Product not found.")
            return

        cursor.connection.commit()
        print("Product updated successfully.")

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Product update failed: {error}")


def delete_product(cursor):
    """Delete a product using its ID."""

    read_products(cursor)

    try:
        product_id = int(input("Enter the product ID to delete: "))

        if product_id <= 0:
            print("Product ID must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid product ID.")
        return

    query = """
        DELETE FROM products
        WHERE product_id = %s
    """

    try:
        cursor.execute(query, (product_id,))

        if cursor.rowcount == 0:
            print("Product not found.")
            return

        cursor.connection.commit()
        print("Product deleted successfully.")

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Product deletion failed: {error}")


def generate_product_ranking(cursor):
    """Retrieve the top-selling products using Redis caching."""

    cache_key = "top_products"

    # First, try to retrieve the ranking from Redis.
    try:
        cached_products = redis_client.get(cache_key)

    except redis.RedisError as error:
        print(f"Redis unavailable. Retrieving from PostgreSQL: {error}")
        cached_products = None

    if cached_products:
        try:
            rankings = json.loads(cached_products)
            print("\nRetrieved top products from Redis (cache hit).")

        except json.JSONDecodeError:
            print("\nInvalid cached data. Retrieving from PostgreSQL.")
            rankings = None

    else:
        rankings = None

    # If the cache is empty or unavailable, query PostgreSQL.
    if rankings is None:
        print("\nRetrieving top products from PostgreSQL (cache miss).")

        query = """
            SELECT
                product_id,
                SUM(quantity) AS total_sold,
                RANK() OVER (
                    ORDER BY SUM(quantity) DESC
                ) AS product_rank
            FROM order_items
            GROUP BY product_id
            ORDER BY total_sold DESC
            LIMIT 10
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            # Convert query results into JSON-serializable dictionaries.
            rankings = [
                {
                    "product_id": int(product[0]),
                    "total_sold": int(product[1]),
                    "product_rank": int(product[2]),
                }
                for product in results
            ]

        except psycopg2.Error as error:
            cursor.connection.rollback()
            print(f"Could not generate product ranking: {error}")
            return

        # Cache the results for five minutes.
        try:
            redis_client.setex(
                cache_key,
                300,
                json.dumps(rankings),
            )
        except redis.RedisError as error:
            print(f"Could not cache product ranking: {error}")

    # Display the ranking regardless of whether it came from Redis or PostgreSQL.
    print("\n---------- TOP 10 PRODUCTS ----------")

    if not rankings:
        print("No product sales found.")
        return

    for product in rankings:
        print(
            f"Rank: {product['product_rank']} | "
            f"Product ID: {product['product_id']} | "
            f"Units Sold: {product['total_sold']}"
        )