#!/usr/bin/env python3
"""
Task 3: Retry Database Queries Decorator

This script implements:
1. with_db_connection - Automatically opens and closes a SQLite database connection.
2. retry_on_failure - Retries a database operation a set number of times if it fails.

The retry decorator adds resilience to database operations that may fail due to transient issues.
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator to handle database connections.

    Opens a connection to 'users.db', injects it into the wrapped function,
    and ensures the connection is closed after execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function multiple times upon failure.

    Args:
        retries (int): Number of times to retry before giving up.
        delay (int): Delay in seconds between retries.

    Returns:
        function: Wrapped function with retry mechanism.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries:
                        print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print(f"Attempt {attempt} failed: {e}. No more retries left.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the database.

    Args:
        conn (sqlite3.Connection): The active database connection.

    Returns:
        list: All rows from the users table.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
