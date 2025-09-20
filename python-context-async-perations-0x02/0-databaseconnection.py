#!/usr/bin/env python3
"""
Task 0: Custom class-based context manager for database connections.

This script defines a DatabaseConnection context manager class
to automatically handle opening and closing of SQLite connections.

Usage:
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
"""

import sqlite3


class DatabaseConnection:
    """Context manager for managing SQLite database connections."""

    def __init__(self, db_name):
        """Initialize with the database name."""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensure the connection is closed when exiting the context.
        If an exception occurs, it will still close the connection.
        """
        if self.conn:
            self.conn.close()


# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("All users:", results)
