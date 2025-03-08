# Use Python as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the FastAPI app code
COPY . .
# Copy the ML model folder

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
