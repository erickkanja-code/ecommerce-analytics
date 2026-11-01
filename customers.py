import psycopg2
from schemas.customers import CREATE_CUSTOMERS_TABLE

def create_customer(cursor):
    try:
        cursor.execute(CREATE_CUSTOMERS_TABLE)
    except psycopg2.errors as e:
        print(f"{e}")
        
    first_name = input("Enter your first name:")
    last_name = input("Enter your last name:")
    query = "INSERT INTO customers (first_name, last_name) VALUES (%s, %s)"
    try:
        cursor.execute(query, (first_name, last_name))
        cursor.connection.commit()
        print("Customer created successfully")
    except psycopg2.Error as e:
        print(f"Customer creation failed: {e}")
        
def read_customers(cursor):
    query = "SELECT * FROM customers;"
    try:
        cursor.execute(query)
        customers = cursor.fetchall()
        print(customers)
    except psycopg2.Error as e:
        print(e)
        
