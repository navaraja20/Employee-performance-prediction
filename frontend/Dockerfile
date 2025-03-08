# Use official Python image as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy required files
COPY ./requirements.txt .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
