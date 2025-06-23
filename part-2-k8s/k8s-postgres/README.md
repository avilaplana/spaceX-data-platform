# PostgreSQL SpaceX Helm Chart

This section demonstrates the deployment of a `PostgresSQL database` with SpaceX SQL schema. I have
used the **[Kubegres](https://kubegres.io/)** operator. 

## Overview

This deployment consists of two main components:

1. **Kubegres Operator**: A Kubernetes operator that manages PostgreSQL clusters. The operator is
deployed first to provide the necessary Custom Resource Definitions (CRDs) and operator logic for
managing PostgreSQL instances.

2. **PostgreSQL Helm Chart**: A custom Helm chart that deploys:
   - A **Kubegres Kind** resource that creates and manages the PostgreSQL database cluster
   - A **one-off initialization job** that creates the `spacex_data` database and sets up the
   complete SpaceX data model schema with dimension tables, fact tables, and bridge tables

## Prerequisites

- Kubectl v1.29.1
- Minikube v1.32.0 with the following configuration:
  ```
  - memory: 32Gb
  - cpus: 8
  ```
- Helm v3.14.0
- Kubegres Operator v1.17
- PostgreSQL client (`psql`) for database connectivity
- K9s 0.31.7 (Recommended to navigate K8s resources)

## Project Structure

```
k8s-postgres/
├── Chart.yaml                 # Helm chart metadata
├── values.yaml               # Default configuration values
├── Makefile                  # Build and deployment commands
├── README.md                 # This documentation
├── files/
│   └── init-sql.sh          # Database initialization script
└── templates/
    ├── _helpers.tpl         # Helm template helpers
    ├── configmap.yaml       # Database configuration
    ├── init-job.yaml        # Database initialization job
    ├── kubegres.yaml        # Kubegres PostgreSQL cluster
    └── NOTES.txt            # Post-installation notes
```

## Helm Configuration

The following table lists the configurable parameters of the postgres-spacex chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `namespace.create` | Create a new namespace | `false` (use --create-namespace flag) |
| `namespace.name` | Name of the namespace | `"interview"` |
| `postgresql.image` | PostgreSQL image | `"postgres:15"` |
| `postgresql.replicas` | Number of PostgreSQL replicas | `1` |
| `postgresql.port` | PostgreSQL port | `5432` |
| `postgresql.database.size` | Database storage size | `"1Gi"` |
| `postgresql.database.storageClassName` | Storage class name | `"standard"` |
| `postgresql.env.POSTGRES_PASSWORD` | PostgreSQL password | `"mysecretpassword"` |
| `postgresql.env.POSTGRES_REPLICATION_PASSWORD` | Replication password | `"replicationSecret"` |
| `init.enabled` | Enable database initialization | `true` |
| `init.database.name` | Database name to create | `"spacex_data"` |
| `init.database.host` | Database host | `"my-postgres"` |
| `init.database.port` | Database port | `5432` |
| `init.database.user` | Database user | `"postgres"` |
| `resources.limits.cpu` | CPU limit | `1000m` |
| `resources.limits.memory` | Memory limit | `1Gi` |
| `resources.requests.cpu` | CPU request | `500m` |
| `resources.requests.memory` | Memory request | `512Mi` |

## Quick Start

### Using Makefile
```bash
# Deploy the CRDs and operator
make deploy-operator

# Check if the operator to be ready
make check-operator

# Install the PostgreSQL Helm chart
make install-postgres-helm-chart

# Check job and pods
make check-postgres

# Uninstall the PostgreSQL Helm chart
make uninstall
```