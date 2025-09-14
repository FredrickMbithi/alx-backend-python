# seed.py
import csv
import uuid
import os
import mysql.connector
from mysql.connector import Error

# --- Edit these or set via env vars ---
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
# --------------------------------------

def connect_db():
    """
    Connects to the MySQL server (no specific DB selected).
    Returns a live connection or None on failure.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            autocommit=True
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def create_database(connection):
    """
    Creates database ALX_prodev if it doesn't exist.
    """
    with connection.cursor() as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")

def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database="ALX_prodev",
            autocommit=True
        )
        return conn
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """
    Creates table user_data if it doesn't exist.
    user_id: Primary Key, UUID, Indexed
    name: VARCHAR NOT NULL
    email: VARCHAR NOT NULL
    age: DECIMAL NOT NULL  (we'll use DECIMAL(3,0) to match integer ages)
    """
    ddl = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL
    ) ENGINE=InnoDB;
    """
    with connection.cursor() as cur:
        cur.execute(ddl)
    print("Table user_data created successfully")

def insert_data(connection, csv_path):
    """
    Inserts CSV rows if they do not already exist.
    Expects CSV with headers: user_id (optional), name, email, age
    If user_id is missing/empty, a UUID is generated.
    Uses ON DUPLICATE KEY UPDATE to ignore duplicates.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    rows = []
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            uid = r.get("user_id") or str(uuid.uuid4())
            name = r.get("name", "").strip()
            email = r.get("email", "").strip()
            age = r.get("age", "").strip()
            if not name or not email or age == "":
                continue
            rows.append((uid, name, email, age))

    if not rows:
        print("No rows to insert.")
        return

    sql = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE user_id = user_data.user_id;
    """
    with connection.cursor() as cur:
        cur.executemany(sql, rows)
    print(f"Inserted/Skipped {len(rows)} rows from {csv_path}")
