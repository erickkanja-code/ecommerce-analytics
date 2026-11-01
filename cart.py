"""Handle customer cart storage and retrieval using MongoDB."""

from mongo_connection import carts


def save_cart(customer_id, items):
    """Save or update a customer's cart in MongoDB."""

    # Basic validation of the customer ID.
    if not isinstance(customer_id, int) or customer_id <= 0:
        print("Invalid customer ID.")
        return

    # Ensure the cart contains valid items.
    if not isinstance(items, list) or not items:
        print("Cart must contain at least one item.")
        return

    for item in items:
        if not isinstance(item, dict):
            print("Each cart item must be a dictionary.")
            return

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not isinstance(product_id, int) or product_id <= 0:
            print("Each item must have a valid product ID.")
            return

        if not isinstance(quantity, int) or quantity <= 0:
            print("Each item must have a valid positive quantity.")
            return

    cart = {
        "customer_id": customer_id,
        "items": items,
    }

    try:
        # Update the customer's existing cart or create a new one.
        carts.update_one(
            {"customer_id": customer_id},
            {"$set": cart},
            upsert=True,
        )

        print("Cart saved successfully!")

    except Exception as error:
        print(f"Could not save cart: {error}")


def read_cart(customer_id):
    """Retrieve and display a customer's cart from MongoDB."""

    if not isinstance(customer_id, int) or customer_id <= 0:
        print("Invalid customer ID.")
        return

    try:
        cart = carts.find_one({"customer_id": customer_id})

        if not cart:
            print("No cart found for this customer.")
            return

        print("\n---------- CUSTOMER CART ----------")

        for item in cart.get("items", []):
            print(
                f"Product ID: {item['product_id']} | "
                f"Quantity: {item['quantity']}"
            )

    except Exception as error:
        print(f"Could not retrieve cart: {error}")