
"""Tests for customer creation and retrieval."""

from unittest.mock import MagicMock, patch

import customers


@patch("builtins.input", side_effect=["John", "Doe"])
def test_create_customer_success(mock_input):
    """A valid customer should be inserted and committed."""

    cursor = MagicMock()

    customers.create_customer(cursor)

    # The table and customer INSERT statements should execute.
    assert cursor.execute.call_count == 2

    # A successful insert should commit the transaction.
    cursor.connection.commit.assert_called_once()


@patch("builtins.input", side_effect=["", "Doe"])
def test_create_customer_rejects_empty_name(mock_input):
    """Customer creation should stop when a name is empty."""

    cursor = MagicMock()

    customers.create_customer(cursor)

    # Only the table creation query should execute.
    assert cursor.execute.call_count == 1

    # No customer should be inserted or committed.
    cursor.connection.commit.assert_not_called()


def test_read_customers_success():
    """Existing customers should be retrieved and displayed."""

    cursor = MagicMock()

    cursor.fetchall.return_value = [
        (1, "John", "Doe"),
        (2, "Jane", "Smith"),
    ]

    customers.read_customers(cursor)

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()


def test_read_customers_empty():
    """The application should handle an empty customer table."""

    cursor = MagicMock()
    cursor.fetchall.return_value = []

    customers.read_customers(cursor)

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()
