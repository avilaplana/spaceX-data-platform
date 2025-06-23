## Introduction

Over time, I have worked with different monitoring tools, but I keep coming back to Prometheus and
Grafana. They’re reliable, flexible, and work especially well in dynamic environments like
Kubernetes.

- Prometheus handles metrics collection and alerting. It uses a pull-based model, which fits nicely
in modern infrastructures, and PromQL gives you a lot of power to slice and analyze data.

- Grafana takes care of the visualization side. It connects easily to Prometheus (and many other
sources), letting you build custom dashboards and set up alerts without much overhead.

At this point, Prometheus and Grafana have become the go-to stack for monitoring in many
organizations. In the next section, I will walk through how to set them up, with links to official
docs and other useful resources.

## Kubernetes Monitoring Setup Using Prometheus Operator (`kube-prometheus-stack`)

### 1. Add and Update the Helm Repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 2. Install `kube-prometheus-stack` with Helm

```bash
helm install monitoring prometheus-community/kube-prometheus-stack
```

This chart installs:

* Prometheus Operator
* Prometheus
* Grafana
* Alertmanager
* All required CustomResourceDefinitions (CRDs)

Helm chart source:
[https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)

Prometheus Operator documentation:
[https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)

### 3. Verify Installation

Check if the required CRDs are installed:

```bash
kubectl get crds | grep monitoring.coreos.com
```

You should see (among others):

* `servicemonitors.monitoring.coreos.com`
* `podmonitors.monitoring.coreos.com`
* `prometheusrules.monitoring.coreos.com`

And check the Prometheus and Grafana pods:

```bash
kubectl get pods -l "release=monitoring"
```

### 4. Scraping Application Metrics (Native Prometheus Operator Way)

Prometheus Operator **does not use annotations like `prometheus.io/scrape: true`**.

Instead, it uses:

* `ServiceMonitor` — to scrape metrics via a Kubernetes Service.
* `PodMonitor` — to scrape metrics directly from pods.

#### Example: Using `ServiceMonitor`

**1. App Deployment and Service:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:latest
          ports:
            - containerPort: 8080
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  selector:
    app: my-app
  ports:
    - name: http
      port: 8080
      targetPort: 8080
```

**2. ServiceMonitor:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app-sm
  labels:
    release: monitoring  # Must match the Prometheus release label
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

ServiceMonitor docs:
[https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#servicemonitor](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#servicemonitor)

#### Example: Using `PodMonitor`

If you don’t have a service, and metrics are exposed directly on the pod:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: my-app-pm
  labels:
    release: monitoring
spec:
  selector:
    matchLabels:
      app: my-app
  podMetricsEndpoints:
    - path: /metrics
      port: metrics
      interval: 15s
```

PodMonitor docs:
[https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#podmonitor](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#podmonitor)

### 5. Access Prometheus and Grafana

Use port forwarding for local access:

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090
kubectl port-forward svc/monitoring-grafana 3000:80
```

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)

  * Default credentials: `admin/prom-operator`


### 6. Adding Custom Alert Rules (Optional)

You can define alerts with the `PrometheusRule` CRD:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: my-app-rules
  labels:
    release: monitoring
spec:
  groups:
    - name: my.rules
      rules:
        - alert: HighLatency
          expr: http_request_duration_seconds_bucket{le="1"} > 0.8
          for: 2m
          labels:
            severity: warning
          annotations:
            summary: "High request latency"
```

PrometheusRule docs:
[https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#prometheusrule](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#prometheusrule)

