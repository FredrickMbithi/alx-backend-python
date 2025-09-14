#!/usr/bin/env python3
"""
Task 4: Cache Database Queries Decorator

This script implements:
1. with_db_connection - Manages opening and closing the database connection.
2. cache_query - Caches query results to avoid redundant database calls.

Caching improves performance when the same query is executed multiple times.
"""

import sqlite3
import functools

# Global cache for storing query results
query_cache = {}


def with_db_connection(func):
    """
    Decorator to handle database connections.

    Opens a connection to 'users.db', passes it to the wrapped function,
    and ensures the connection is closed after use.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """
    Decorator to cache database query results based on the SQL query string.

    If the query has been executed before, returns the cached result instead of
    re-executing the database query.

    Returns:
        function: Wrapped function with caching logic.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        print(f"Executing and caching result for query: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database with caching.

    Args:
        conn (sqlite3.Connection): Active database connection.
        query (str): SQL query string.

    Returns:
        list: Query result set.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")

    print(users_again)
