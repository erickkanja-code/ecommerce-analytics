"""Handle customer creation and retrieval."""

import psycopg2

from schemas.customers import CREATE_CUSTOMERS_TABLE


def create_customer(cursor):
    """Create a customer record in PostgreSQL."""

    # Ensure the customers table exists before inserting a record.
    try:
        cursor.execute(CREATE_CUSTOMERS_TABLE)
    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Could not prepare customers table: {error}")
        return

    first_name = input("Enter your first name: ").strip()
    last_name = input("Enter your last name: ").strip()

    # Basic validation: names must not be empty.
    if not first_name or not last_name:
        print("First name and last name cannot be empty.")
        return

    query = """
        INSERT INTO customers (first_name, last_name)
        VALUES (%s, %s)
    """

    try:
        cursor.execute(query, (first_name, last_name))
        cursor.connection.commit()
        print("Customer created successfully.")

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Customer creation failed: {error}")


def read_customers(cursor):
    """Retrieve and display all customers."""

    query = """
        SELECT customer_id, first_name, last_name
        FROM customers
        ORDER BY customer_id
    """

    try:
        cursor.execute(query)
        customers = cursor.fetchall()

        if not customers:
            print("No customers found.")
            return

        print("\n---------- CUSTOMERS ----------")

        for customer in customers:
            print(
                f"ID: {customer[0]} | "
                f"Name: {customer[1]} {customer[2]}"
            )

    except psycopg2.Error as error:
        cursor.connection.rollback()
        print(f"Could not retrieve customers: {error}")