
"""Main entry point for the e-commerce analytics application."""

from customers import create_customer, read_customers
from products import (
    create_product,
    read_products,
    update_product,
    delete_product,
    generate_product_ranking,
    search_products_by_brand,
)
from connection import (
    get_connection,
    return_connection_to_pool,
    close_pool,
)
from orders import (
    make_order,
    read_orders,
    generate_customer_revenue,
)
from cart import save_cart, read_cart


def select_customer(cursor):
    """Display customers and return the ID of a selected customer."""

    read_customers(cursor)

    try:
        selected_id = int(input("Enter customer ID: "))

        if selected_id <= 0:
            print("Customer ID must be greater than zero.")
            return None

        # Verify that the selected customer exists.
        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_id = %s",
            (selected_id,),
        )

        if cursor.fetchone():
            print(f"Customer {selected_id} selected successfully.")
            return selected_id

        print("Customer not found.")
        return None

    except ValueError:
        print("Please enter a valid customer ID.")
        return None

    except Exception as error:
        print(f"Could not select customer: {error}")
        return None


def main():
    """Run the application's menu and coordinate its operations."""

    connection = get_connection()

    # Tracks the customer currently using the application.
    current_customer_id = None

    try:
        with connection.cursor() as cursor:
            while True:
                print("\n===== E-COMMERCE SYSTEM =====")

                if current_customer_id is not None:
                    print(f"Current customer ID: {current_customer_id}")
                else:
                    print("No customer selected")

                print("1. Create customer")
                print("2. View customers")
                print("3. Create product")
                print("4. View products")
                print("5. Update product")
                print("6. Delete product")
                print("7. Make an order")
                print("8. View orders")
                print("9. Generate product ranking")
                print("10. Generate customer revenue report")
                print("11. Search products by brand")
                print("12. Save customer cart")
                print("13. View customer cart")
                print("14. Select customer")
                print("0. Exit")

                choice = input("Choose an option: ").strip()

                if choice == "1":
                    create_customer(cursor)

                elif choice == "2":
                    read_customers(cursor)

                elif choice == "3":
                    create_product(cursor)

                elif choice == "4":
                    read_products(cursor)

                elif choice == "5":
                    update_product(cursor)

                elif choice == "6":
                    delete_product(cursor)

                elif choice == "7":
                    if current_customer_id is None:
                        print("Please select a customer first.")
                    else:
                        make_order(cursor, current_customer_id)

                elif choice == "8":
                    read_orders(cursor)

                elif choice == "9":
                    generate_product_ranking(cursor)

                elif choice == "10":
                    generate_customer_revenue(cursor)

                elif choice == "11":
                    search_products_by_brand(cursor)

                elif choice == "12":
                    if current_customer_id is None:
                        print("Please select a customer first.")
                    else:
                        # Sample cart items for demonstrating MongoDB storage.
                        items = [
                            {"product_id": 1, "quantity": 2},
                            {"product_id": 3, "quantity": 1},
                        ]
                        save_cart(current_customer_id, items)

                elif choice == "13":
                    if current_customer_id is None:
                        print("Please select a customer first.")
                    else:
                        read_cart(current_customer_id)

                elif choice == "14":
                    selected_id = select_customer(cursor)

                    # Keep the previous customer if selection fails.
                    if selected_id is not None:
                        current_customer_id = selected_id

                elif choice == "0":
                    print("Exiting application.")
                    break

                else:
                    print("Invalid option. Try again.")

    finally:
        # Always return the connection and close the pool on exit.
        return_connection_to_pool(connection)
        close_pool()


if __name__ == "__main__":
    main()
