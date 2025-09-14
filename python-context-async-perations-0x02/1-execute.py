#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager.

This script defines an ExecuteQuery context manager class
to handle database connections and query execution.

Usage:
    with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
        print("Users older than 25:", results)
"""

import sqlite3


class ExecuteQuery:
    """Context manager for executing queries with automatic connection handling."""

    def __init__(self, db_name, query, params=None):
        """
        Initialize with database name, query, and optional parameters.
        
        Args:
            db_name (str): The SQLite database file.
            query (str): The SQL query to execute.
            params (tuple): Parameters for the SQL query (default: None).
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        """Open the connection, execute the query, and return results."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection after use."""
        if self.conn:
            self.conn.close()


# Example usage
if __name__ == "__main__":
    with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
        print("Users older than 25:", results)
