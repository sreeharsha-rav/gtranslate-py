# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies with pip
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8080

# Run the application directly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]