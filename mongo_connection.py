"""Provide access to the MongoDB database and carts collection."""

from pymongo import MongoClient


# Connect to the local MongoDB server.
# MongoClient establishes the connection lazily when the database is accessed.
client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000,
)

# Select the e-commerce database and its carts collection.
db = client["ecommerce_db"]
carts = db["carts"]