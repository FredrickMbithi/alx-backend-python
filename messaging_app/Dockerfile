FROM python:3.10-slim

# Prevent Python from writing pyc files and buffering issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for MySQL client build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory where the repo will be copied
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire project into the image at /app
COPY . .

# Create a non-root user and ensure /app is owned by that user
RUN useradd -m appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Django default port
EXPOSE 8000

# Default command: run migrations then start dev server.
# Note: in CI we run the same commands via docker compose run -w /app ...
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
