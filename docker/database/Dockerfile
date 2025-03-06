# Use official PostgreSQL image
FROM postgres:13

# Set environment variables
ENV POSTGRES_USER=youruser
ENV POSTGRES_PASSWORD=yourpassword
ENV POSTGRES_DB=employee_db

# Copy initialization script
COPY ../database/init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
