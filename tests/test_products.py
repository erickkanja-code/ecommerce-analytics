
"""Tests for product CRUD operations and product ranking."""

from unittest.mock import MagicMock, patch

import products


@patch("builtins.input", side_effect=["Samsung TV", "500", "350"])
def test_create_product_success(mock_input):
    """A valid product should be inserted and committed."""

    cursor = MagicMock()

    products.create_product(cursor)

    assert cursor.execute.call_count == 2
    cursor.connection.commit.assert_called_once()


@patch("builtins.input", side_effect=["", "500", "350"])
def test_create_product_rejects_empty_name(mock_input):
    """A product with an empty name should not be inserted."""

    cursor = MagicMock()

    products.create_product(cursor)

    assert cursor.execute.call_count == 1
    cursor.connection.commit.assert_not_called()


@patch("builtins.input", side_effect=["Samsung TV", "-500", "350"])
def test_create_product_rejects_invalid_price(mock_input):
    """A product with a non-positive selling price should be rejected."""

    cursor = MagicMock()

    products.create_product(cursor)

    assert cursor.execute.call_count == 1
    cursor.connection.commit.assert_not_called()


def test_read_products_success():
    """Product records should be retrieved and displayed."""

    cursor = MagicMock()
    cursor.fetchall.return_value = [
        (1, "Samsung TV", 500, {"brand": "Samsung"}),
        (2, "iPhone", 900, {"brand": "Apple"}),
    ]

    products.read_products(cursor)

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()


def test_read_products_empty():
    """The application should handle an empty products table."""

    cursor = MagicMock()
    cursor.fetchall.return_value = []

    products.read_products(cursor)

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_called_once()


@patch("builtins.input", return_value="Samsung")
def test_search_products_by_brand(mock_input):
    """Brand search should return matching products."""

    cursor = MagicMock()
    cursor.fetchall.return_value = [
        (1, "Samsung TV", "Samsung"),
    ]

    products.search_products_by_brand(cursor)

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args.args[1] == ("Samsung",)


@patch("builtins.input", side_effect=["1", "600"])
def test_update_product_success(mock_input):
    """An existing product should have its selling price updated."""

    cursor = MagicMock()
    cursor.rowcount = 1

    products.update_product(cursor)

    # One SELECT for displaying products, one UPDATE.
    assert cursor.execute.call_count == 2
    cursor.connection.commit.assert_called_once()


@patch("builtins.input", side_effect=["1", "600"])
def test_update_product_not_found(mock_input):
    """Updating a nonexistent product should not commit."""

    cursor = MagicMock()
    cursor.rowcount = 0

    products.update_product(cursor)

    cursor.connection.commit.assert_not_called()


@patch("builtins.input", return_value="1")
def test_delete_product_success(mock_input):
    """An existing product should be deleted and committed."""

    cursor = MagicMock()
    cursor.rowcount = 1

    products.delete_product(cursor)

    assert cursor.execute.call_count == 2
    cursor.connection.commit.assert_called_once()


@patch("builtins.input", return_value="1")
def test_delete_product_not_found(mock_input):
    """Deleting a nonexistent product should not commit."""

    cursor = MagicMock()
    cursor.rowcount = 0

    products.delete_product(cursor)

    cursor.connection.commit.assert_not_called()


@patch("products.redis_client")
def test_generate_product_ranking_cache_hit(mock_redis):
    """Cached rankings should be displayed without querying PostgreSQL."""

    mock_redis.get.return_value = (
        '[{"product_id": 1, "total_sold": 10, "product_rank": 1}]'
    )

    cursor = MagicMock()

    products.generate_product_ranking(cursor)

    mock_redis.get.assert_called_once_with("top_products")
    cursor.execute.assert_not_called()


@patch("products.redis_client")
def test_generate_product_ranking_cache_miss(mock_redis):
    """A cache miss should retrieve rankings from PostgreSQL and cache them."""

    mock_redis.get.return_value = None

    cursor = MagicMock()
    cursor.fetchall.return_value = [
        (1, 10, 1),
        (2, 5, 2),
    ]

    products.generate_product_ranking(cursor)

    cursor.execute.assert_called_once()
    mock_redis.setex.assert_called_once()
