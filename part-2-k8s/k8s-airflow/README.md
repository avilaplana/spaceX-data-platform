## Apache Airflow SpaceX ETL – Helm Chart Deployment

This section demonstrates the deployment of Apache Airflow in a Kubernetes cluster, running SpaceX
ETL DAGs.

Initially, I attempted to deploy both the [Apache Airflow on Kubernetes Operator](https://github.com/apache/airflow-on-k8s-operator)
and the [Community Airflow Helm Chart](https://github.com/airflow-helm/charts). However, due to
deployment challenges and time constraints, I opted to build a custom Helm chart tailored to this
use case.

## Overview

This deployment consists of Apache Airflow components for orchestrating SpaceX data ETL processes:

1. **Airflow Init**: Creates the Airflow database, users, and initial setup.
2. **Airflow Webserver**: Provides the web UI for monitoring and managing DAGs.
2. **Airflow Scheduler**: Orchestrates and schedules the execution of DAGs.
3. **SpaceX ETL DAG**: A Pyton ETL pipeline that extracts, transforms, and loads SpaceX data from
the SpaceX API into the PostgreSQL database

Note: Start minikube and build the image `etl-airflow` with the following command:
```bash
 cd ../../part-3-etl-pipeline/with-airflow/ && \
 eval $(minikube docker-env) && \
 docker build --no-cache -t etl-airflow:latest -f Dockerfile .. && \
 cd ../../part-2-k8s/k8s-airflow 
```

## Prerequisites

- Kubectl v1.29.1
- Minikube v1.32.0 with the following configuration:
  ```
  - memory: 32Gb
  - cpus: 8
  ```
- Helm v3.14.0
- PostgreSQL client (`psql`) for database connectivity
- K9s 0.31.7 (Recommended to navigate K8s resources)
- PostgreSQL database running (from k8s-postgres deployment)

## Project Structure

```
k8s-airflow/
├── Chart.yaml                 # Helm chart metadata
├── values.yaml               # Default configuration values
├── Makefile                  # Build and deployment commands
├── README.md                 # This documentation
├── scripts/
│   └── spacex_etl_dag.py    # SpaceX ETL DAG definition
└── templates/
    ├── configmap.yaml        # Airflow configuration
    ├── dags-configmap.yaml   # DAGs configuration
    ├── init-job.yaml         # Airflow initialization job
    ├── pvc.yaml             # Persistent volume claims
    ├── scheduler-deployment.yaml  # Airflow scheduler
    ├── webserver-deployment.yaml  # Airflow webserver
    ├── webserver-service.yaml     # Webserver service
    └── NOTES.txt            # Post-installation notes
```

## Helm Configuration

The following table lists the configurable parameters of the airflow chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Airflow image repository | `"etl-airflow"` |
| `image.tag` | Airflow image tag | `"latest"` |
| `image.pullPolicy` | Image pull policy | `"Never"` |
| `database.host` | PostgreSQL host | `"my-postgres"` |
| `database.port` | PostgreSQL port | `5432` |
| `database.name` | Database name | `"spacex_data"` |
| `database.user` | Database user | `"postgres"` |
| `database.password` | Database password | `"mysecretpassword"` |
| `airflow.webserver.port` | Webserver port | `8080` |
| `airflow.webserver.replicas` | Webserver replicas | `1` |
| `airflow.scheduler.replicas` | Scheduler replicas | `1` |
| `admin.username` | Admin username | `"admin"` |
| `admin.password` | Admin password | `"password"` |

## Quick Start

### Using Makefile
```bash
# Install the Airflow Helm chart
make install-airflow-helm-chart

# Check Airflow pods and services
make check-airflow

# Uninstall the Airflow Helm chart
make uninstall
```
