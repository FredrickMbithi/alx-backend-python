import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached results for query: {query}")
            return query_cache[query]
        else:
            results = func(conn, query, *args, **kwargs)
            query_cache[query] = results
            print(f"[CACHE MISS] Caching results for query: {query}")
            return results
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
