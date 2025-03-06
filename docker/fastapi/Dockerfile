# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY ../backend/requirements.txt .
COPY ../backend/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
