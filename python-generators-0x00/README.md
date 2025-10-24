# Python Generators – Streaming, Batching, Pagination, and Aggregation

This mini-project shows how to use Python **generators** to work with a MySQL table (`user_data`) efficiently: stream one row at a time, fetch in batches, lazy-load paginated results, and compute an average without loading everything into memory.

## What’s here

- `seed.py` – creates the `ALX_prodev` database, `user_data` table, and loads `user_data.csv`
- `0-stream_users.py` – `stream_users()` yields one user row at a time
- `1-batch_processing.py` – `stream_users_in_batches()` and `batch_processing()` (filters age > 25)
- `2-lazy_paginate.py` – `paginate_users()` helper + `lazy_paginate()` (also exported as `lazy_pagination`)
- `4-stream_ages.py` – `stream_user_ages()` + `print_average_age()` (memory-efficient average)

> Put `user_data.csv` in this same directory.

## Setup

1) Install connector:
```bash
pip install mysql-connector-python
