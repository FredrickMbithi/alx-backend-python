# 1-batch_processing.py
import seed

def stream_users_in_batches(batch_size):
    """
    Generator that yields lists (batches) of users as dicts.
    Uses one loop over pages and stops when a page is empty.
    """
    conn = seed.connect_to_prodev()
    if not conn:
        return
    try:
        offset = 0
        while True:  # loop #1
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            page = cur.fetchall()
            cur.close()
            if not page:
                break
            # normalize ages to int
            batch = [
                {
                    "user_id": r["user_id"],
                    "name": r["name"],
                    "email": r["email"],
                    "age": int(r["age"]),
                }
                for r in page
            ]
            yield batch
            offset += batch_size
    finally:
        conn.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over age 25 and prints them.
    Total loops:
      - for batch in generator (loop #2)
      - for user in filtered list (loop #3)
    """
    for batch in stream_users_in_batches(batch_size):      # loop #2
        filtered = [u for u in batch if u["age"] > 25]
        for user in filtered:                              # loop #3
            print(user)
