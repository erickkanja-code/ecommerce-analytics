import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

load_dotenv()
try:
    postgreSQL_pool = pool.SimpleConnectionPool(
        1, 20, user='ecommerce_user', password=os.getenv("POSTGRES_PASSWORD"), host="localhost", port="5433", database="ecommerce_db"
    )
    print("Postgres pool created successfully")
except psycopg2.OperationalError as e:
    print(f"Could not connect to PostgreSQL {e}")
    
def get_connection():
    return postgreSQL_pool.getconn()

def return_connection_to_pool(connection):
    return postgreSQL_pool.putconn(connection)

def close_pool():
    postgreSQL_pool.closeall()
    
    