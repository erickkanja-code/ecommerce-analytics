"""Manage the PostgreSQL connection pool."""

import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import pool


# Load database credentials from the .env file.
load_dotenv()

# Database connection settings.
DB_USER = "ecommerce_user"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "ecommerce_db"

# The pool is created when the application first requests a connection.
_connection_pool = None


def create_connection_pool():
    """Create the PostgreSQL connection pool if it does not exist."""
    global _connection_pool

    if _connection_pool is not None:
        return

    password = os.getenv("POSTGRES_PASSWORD")

    if not password:
        raise ValueError(
            "POSTGRES_PASSWORD is missing from the environment."
        )

    try:
        _connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=20,
            user=DB_USER,
            password=password,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        print("PostgreSQL connection pool created successfully.")

    except psycopg2.Error as error:
        raise RuntimeError(
            f"Could not create PostgreSQL connection pool: {error}"
        ) from error


def get_connection():
    """Get an available connection from the pool."""
    if _connection_pool is None:
        create_connection_pool()

    return _connection_pool.getconn()


def return_connection_to_pool(connection):
    """Return a connection to the pool after use."""
    if _connection_pool is not None and connection is not None:
        _connection_pool.putconn(connection)


def close_pool():
    """Close all connections in the pool."""
    global _connection_pool

    if _connection_pool is not None:
        _connection_pool.closeall()
        _connection_pool = None