
"""Tests for order processing and customer revenue reports."""

from unittest.mock import MagicMock, patch

import orders


@patch("orders.read_products")
@patch("builtins.input", side_effect=["1", "2", "0"])
def test_make_order_success(mock_input, mock_read_products):
    """A valid order should insert items, update the total, and commit."""

    cursor = MagicMock()

    # First fetchone() returns the generated order ID.
    # Second fetchone() returns the product's selling price.
    cursor.fetchone.side_effect = [
        (101,),
        (50.00,),
    ]

    orders.make_order(cursor, customer_id=5)

    # The order should belong to customer 5.
    order_insert = cursor.execute.call_args_list[1]
    assert order_insert.args[1] == (5,)

    # The order should be committed after successful processing.
    cursor.connection.commit.assert_called_once()
    cursor.connection.rollback.assert_not_called()


@patch("orders.read_products")
@patch("builtins.input", side_effect=["0"])
def test_make_order_empty_cart(mock_input, mock_read_products):
    """An empty cart should not create an order."""

    cursor = MagicMock()

    orders.make_order(cursor, customer_id=5)

    # Only the two table definitions should execute.
    assert cursor.execute.call_count == 2

    cursor.connection.commit.assert_not_called()


@patch("orders.read_products")
@patch("builtins.input", side_effect=["1", "2", "0"])
def test_make_order_product_not_found(mock_input, mock_read_products):
    """A missing product should cause the order transaction to roll back."""

    cursor = MagicMock()

    cursor.fetchone.side_effect = [
        (101,),  # Generated order ID.
        None,    # Product does not exist.
    ]

    orders.make_order(cursor, customer_id=5)

    cursor.connection.rollback.assert_called_once()
    cursor.connection.commit.assert_not_called()


@patch("orders.read_products")
@patch("builtins.input", side_effect=["1", "abc"])
def test_make_order_invalid_quantity_input(mock_input, mock_read_products):
    """Invalid numeric input should be rejected without crashing."""

    cursor = MagicMock()

    orders.make_order(cursor, customer_id=5)

    # Invalid input ends the current order attempt.
    cursor.connection.commit.assert_not_called()
    cursor.connection.rollback.assert_not_called()


def test_read_orders_success():
    """Existing orders should be retrieved."""

    cursor = MagicMock()
    cursor.fetchall.return_value = [
        (101, 5, "2026-11-01", 100.00),
    ]

    orders.read_orders(cursor)

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()


def test_generate_customer_revenue_success():
    """Customer revenue should be retrieved and displayed."""

    cursor = MagicMock()
    cursor.fetchall.return_value = [
        (5, 500.00),
        (7, 250.00),
    ]

    orders.generate_customer_revenue(cursor)

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()
