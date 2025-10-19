# 0-stream_users.py
import seed

def stream_users():
    """
    Generator that yields rows from user_data one by one as dicts.
    Must use at most one loop.
    """
    conn = seed.connect_to_prodev()
    if not conn:
        return
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT user_id, name, email, age FROM user_data")
        for row in cur:   # one loop
            yield {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "age": int(row["age"]),
            }
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()
