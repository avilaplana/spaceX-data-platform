## Problem - Part 2: Orchestration and Container Management with Kubernetes

- Describe the steps to deploy a Kubernetes cluster containing an orchestrator and database and the
ingestion script/tool containers.
- Describe how you would configure monitoring and logging for the Kubernetes cluster using tools like
Prometheus or Grafana.

## Solution

To address the requirements above, I made pragmatic decisions about the components used to build
the data platform. The stack consists of:

- `K8s cluster: resource manager`.
- `PostgresSQL: Database`.
- `Apache Airflow: ETL orchestrator: `.
- `Python APIs: ETL DAG`

I discarded DBT because of time.If included, the architecture would have remained largely the same
as in `Part 1`

### Kubernetes Resource Deployment Preference

The technologies I prefer for deploying resources in Kubernetes are, in order of preference:
- Official Kubernetes Operator
- Official Helm Chart
- Custom Operator + Helm Chart
- Custom Helm Chart

This `Part 2` is organized into the following sections:

- [Provision a EKS Kubernetes cluster with Terraform](k8s-aws-eks/terraform/README.md).
- [Deploy PostgresSQL in Kubernetes cluster](k8s-postgres/README.md)
- [Deploy Airflow cluster in Kubernetes cluster](k8s-postgres/README.md)
- [Metrics/Alerting with Prometheus/Grafana in Kubernetes cluster](k8s-monitoring/metrics/README.md)
- [Logging with Loki/Promtail in Kubernetes cluster](k8s-monitoring/logging/README.md)
