#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries

This script uses aiosqlite and asyncio.gather() to fetch data from a users.db
SQLite database concurrently.
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """
    Fetch all users asynchronously from the users table.
    """
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results


async def async_fetch_older_users():
    """
    Fetch all users older than 40 asynchronously from the users table.
    """
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        await cursor.close()
        return results


async def fetch_concurrently():
    """
    Run both queries concurrently using asyncio.gather.
    """
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
