# ----------------------------
# 1️⃣ Base image
# ----------------------------
FROM python:3.10-slim

# ----------------------------
# 2️⃣ Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# 3️⃣ Copy requirements
# ----------------------------
COPY requirements.txt .

# ----------------------------
# 4️⃣ Install system dependencies (for mysqlclient)
# ----------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 5️⃣ Install Python dependencies
# ----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# 6️⃣ Copy app source
# ----------------------------
COPY . .

# ----------------------------
# 7️⃣ Expose port and run
# ----------------------------
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

