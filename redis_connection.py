"""Provide access to the Redis cache."""

import redis


# Connect to the local Redis server.
# decode_responses=True returns strings instead of bytes.
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5,
)