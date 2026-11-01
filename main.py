from customers import create_customer, read_customers
from products import create_product, read_products, update_product, delete_product
from connection import get_connection, return_connetcion_to_pool, close_pool


connection = get_connection()

with connection.cursor() as cursor:
    delete_product(cursor)













