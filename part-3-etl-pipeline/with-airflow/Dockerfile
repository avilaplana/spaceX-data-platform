FROM apache/airflow:2.9.1-python3.10

USER root

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY with-airflow/requirements.txt /opt/airflow/requirements.txt

COPY with-airflow/wait-for-it.sh /opt/airflow/wait-for-it.sh

RUN chmod +x /opt/airflow/wait-for-it.sh

# Now switch to airflow user
USER airflow

# Install dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy the ETL files
COPY etl/ /opt/airflow/etl/

ENV PYTHONPATH=/opt/airflow:$PYTHONPATH
