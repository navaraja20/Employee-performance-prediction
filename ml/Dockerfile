
FROM python:3.9

WORKDIR /app

# Copy ML scripts and data
COPY . .
# Install required Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Run training script (optional)
CMD ["python", "train.py"]


