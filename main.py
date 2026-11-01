
from customers import create_customer, read_customers
from products import (
    create_product,
    read_products,
    update_product,
    delete_product,
    generate_product_ranking
)
from connection import (
    get_connection,
    return_connection_to_pool,
    close_pool
)
from orders import make_order, read_orders, generate_customer_revenue

connection = get_connection()

try:
    with connection.cursor() as cursor:
        while True:
            print("\n===== E-COMMERCE SYSTEM =====")
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
            print("0. Exit")

            choice = input("Choose an option: ")

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
                make_order(cursor)
            elif choice == "8":
                read_orders(cursor)
            elif choice == "9":
                generate_product_ranking(cursor)
            elif choice == "0":
                break
            elif choice == "10":
                generate_customer_revenue(cursor)
            else:
                print("Invalid option. Try again.")

finally:
    return_connection_to_pool(connection)
    close_pool()
