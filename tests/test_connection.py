
"""Tests for PostgreSQL connection-pool management."""

from unittest.mock import MagicMock, patch

import pytest

import connection


def test_create_connection_pool_success():
    """The pool should be created using the configured database settings."""

    with (
        patch.object(connection, "_connection_pool", None),
        patch.object(connection.os, "getenv", return_value="test_password"),
        patch.object(connection.pool, "SimpleConnectionPool") as mock_pool,
    ):
        connection.create_connection_pool()

        mock_pool.assert_called_once()

        args = mock_pool.call_args.kwargs

        assert args["minconn"] == 1
        assert args["maxconn"] == 20
        assert args["user"] == connection.DB_USER
        assert args["password"] == "test_password"
        assert args["host"] == connection.DB_HOST
        assert args["port"] == connection.DB_PORT
        assert args["database"] == connection.DB_NAME


def test_create_connection_pool_missing_password():
    """Pool creation should fail if the database password is missing."""

    with (
        patch.object(connection, "_connection_pool", None),
        patch.object(connection.os, "getenv", return_value=None),
    ):
        with pytest.raises(ValueError, match="POSTGRES_PASSWORD"):
            connection.create_connection_pool()


def test_get_connection():
    """The application should receive a connection from the pool."""

    mock_pool = MagicMock()
    mock_connection = MagicMock()
    mock_pool.getconn.return_value = mock_connection

    with patch.object(connection, "_connection_pool", mock_pool):
        result = connection.get_connection()

    assert result is mock_connection
    mock_pool.getconn.assert_called_once()


def test_return_connection_to_pool():
    """A borrowed connection should be returned to the pool."""

    mock_pool = MagicMock()
    mock_connection = MagicMock()

    with patch.object(connection, "_connection_pool", mock_pool):
        connection.return_connection_to_pool(mock_connection)

    mock_pool.putconn.assert_called_once_with(mock_connection)


def test_close_pool():
    """Closing the pool should close all connections and reset it."""

    mock_pool = MagicMock()

    with patch.object(connection, "_connection_pool", mock_pool):
        connection.close_pool()

        mock_pool.closeall.assert_called_once()
        assert connection._connection_pool is None


def test_return_connection_when_pool_does_not_exist():
    """Returning a connection should do nothing if no pool exists."""

    mock_connection = MagicMock()

    with patch.object(connection, "_connection_pool", None):
        connection.return_connection_to_pool(mock_connection)
