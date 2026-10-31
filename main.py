from customers import create_customer, read_customers
from connection import get_connection, return_connetcion_to_pool, close_pool


connection = get_connection()

with connection.cursor() as cursor:
    create_customer(cursor)
    read_customers(cursor)













