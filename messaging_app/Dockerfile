# messaging_app/Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory first
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy project code
COPY . /app/

# Create a non-root user and use it
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the port Django will run on (default is 8000)
# Using -p flag in EXPOSE or docker run -p 8000:8000
EXPOSE 8000

# Default command - run migrations and start server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
