# 4-stream_ages.py
import seed

def stream_user_ages():
    """
    Generator that yields ages (as ints) one by one.
    Uses a single loop over the cursor.
    """
    conn = seed.connect_to_prodev()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT age FROM user_data")
        for (age,) in cur:   # loop #1
            # age may be Decimal -> cast to int
            yield int(age)
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

def print_average_age():
    """
    Consumes the generator and prints the average without loading all rows.
    Uses at most one loop here -> total ≤ 2 loops for the file.
    """
    total = 0
    count = 0
    for age in stream_user_ages():   # loop #2
        total += age
        count += 1
    avg = (total / count) if count else 0
    print(f"Average age of users: {avg:.2f}")

if __name__ == "__main__":
    print_average_age()
