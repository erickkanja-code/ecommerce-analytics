
"""Tests for saving and retrieving customer carts."""

from unittest.mock import patch

import cart


@patch("cart.carts")
def test_save_cart_success(mock_carts):
    """A valid cart should be saved using MongoDB upsert."""

    items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1},
    ]

    cart.save_cart(customer_id=5, items=items)

    mock_carts.update_one.assert_called_once_with(
        {"customer_id": 5},
        {
            "$set": {
                "customer_id": 5,
                "items": items,
            }
        },
        upsert=True,
    )


@patch("cart.carts")
def test_save_cart_rejects_invalid_customer_id(mock_carts):
    """A non-positive customer ID should be rejected."""

    cart.save_cart(customer_id=0, items=[
        {"product_id": 1, "quantity": 2}
    ])

    mock_carts.update_one.assert_not_called()


@patch("cart.carts")
def test_save_cart_rejects_empty_items(mock_carts):
    """An empty cart should not be saved."""

    cart.save_cart(customer_id=5, items=[])

    mock_carts.update_one.assert_not_called()


@patch("cart.carts")
def test_save_cart_rejects_invalid_product_id(mock_carts):
    """A cart item with an invalid product ID should be rejected."""

    items = [
        {"product_id": 0, "quantity": 2}
    ]

    cart.save_cart(customer_id=5, items=items)

    mock_carts.update_one.assert_not_called()


@patch("cart.carts")
def test_save_cart_rejects_invalid_quantity(mock_carts):
    """A cart item with a non-positive quantity should be rejected."""

    items = [
        {"product_id": 1, "quantity": -2}
    ]

    cart.save_cart(customer_id=5, items=items)

    mock_carts.update_one.assert_not_called()


@patch("cart.carts")
def test_read_cart_success(mock_carts):
    """An existing cart should be retrieved from MongoDB."""

    mock_carts.find_one.return_value = {
        "customer_id": 5,
        "items": [
            {"product_id": 1, "quantity": 2},
        ],
    }

    cart.read_cart(customer_id=5)

    mock_carts.find_one.assert_called_once_with(
        {"customer_id": 5}
    )


@patch("cart.carts")
def test_read_cart_not_found(mock_carts):
    """A missing cart should be handled without an error."""

    mock_carts.find_one.return_value = None

    cart.read_cart(customer_id=5)

    mock_carts.find_one.assert_called_once_with(
        {"customer_id": 5}
    )
