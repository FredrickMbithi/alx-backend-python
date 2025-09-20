#!/usr/bin/env python3
"""
Task 2: Transaction Management Decorator

This script implements two decorators:
1. with_db_connection - automatically opens and closes a SQLite database connection.
2. transactional - wraps database operations in a transaction, committing changes
   if successful or rolling them back if an error occurs.
"""

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


def transactional(func):
    """
    Decorator to manage database transactions.

    Begins a transaction, commits if the wrapped function executes successfully,
    or rolls back if an exception occurs.

    Args:
        func (function): The database operation function.

    Returns:
        function: The wrapped function with automatic transaction handling.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update the email address of a user identified by their ID.

    Args:
        conn (sqlite3.Connection): The active database connection.
        user_id (int): The ID of the user to update.
        new_email (str): The new email address to set.

    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
