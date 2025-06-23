# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY without-airflow/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ETL files
COPY etl/entities/ etl/entities/
COPY etl/__init__.py etl/
COPY without-airflow/run_etl.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the ETL process
CMD ["python", "run_etl.py"] 