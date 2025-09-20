#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator

This script implements a decorator `with_db_connection` that automatically
opens a SQLite database connection, passes it to the wrapped function,
and ensures the connection is closed afterward.

This approach avoids repetitive connection setup and cleanup in each function.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator to manage database connections.

    It opens a connection to `users.db`, injects it as the first argument
    to the decorated function, and ensures the connection is closed
    after the function execution — even if an error occurs.

    Args:
        func (function): The target database function.

    Returns:
        function: The wrapped function with automatic DB connection handling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Inject the connection as the first argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a single user from the database by their ID.

    Args:
        conn (sqlite3.Connection): The active database connection.
        user_id (int): The ID of the user to retrieve.

    Returns:
        tuple or None: User record if found, otherwise None.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
