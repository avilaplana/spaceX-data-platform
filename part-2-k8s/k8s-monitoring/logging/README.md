## Introduction

I have used two different tech stacks to provide logging capabilities:
- ELK (Elasticsearch, Logstash, and Kibana)
- Promtail/Loki (part of the Grafana ecosystem)

Given that the Prometheus/Grafana stack has become the de facto standard for monitoring in recent
years, integrating Promtail and Loki was the better option. 

Several reliable resources are available for deploying Loki and Promtail. The next section includes
a tutorial outlining the deployment steps, along with reference links to the original documentation
and supporting material.

## Setting Up Logging in Kubernetes with Loki, Promtail

Assuming `kube-prometheus-stack` is used for monitoring, adding logging with `Loki` and `Promtail`
fits naturally. Unlike Prometheus, **Loki doesn’t have a Kubernetes operator—you deploy it via Helm
and configure it with values**.

### Step 1: Add the Grafana Helm repo

Add the Helm repo and update:

```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

More here:
[https://github.com/grafana/helm-charts](https://github.com/grafana/helm-charts)

### Step 2: Install Loki and Promtail

Install Loki and Promtail together with the `loki-stack` chart. Promtail runs as a DaemonSet on each
node and ships logs to Loki.

```
helm install loki grafana/loki-stack --set promtail.enabled=true --set grafana.enabled=false
```

**Project links:**

* Loki (log aggregation system): [https://grafana.com/oss/loki/](https://grafana.com/oss/loki/)
* Promtail (log shipper agent): [https://grafana.com/docs/loki/latest/clients/promtail/](https://grafana.com/docs/loki/latest/clients/promtail/)

Docs:
[https://github.com/grafana/helm-charts/tree/main/charts/loki-stack](https://github.com/grafana/helm-charts/tree/main/charts/loki-stack)
[https://grafana.com/docs/loki/latest/](https://grafana.com/docs/loki/latest/)

### Step 3: Verify the deployment

Check pods are running:

```
kubectl get pods -l app=loki
kubectl get pods -l app=promtail
```

Promtail collects logs from `/var/log/containers`.

### Step 4: Connect Loki to Grafana

Forward the Grafana service port:

```
kubectl port-forward svc/monitoring-grafana 3000:80
```

Open [http://localhost:3000](http://localhost:3000), log in (default `admin/prom-operator`), and add
Loki as a data source:

* URL: `http://loki:3100`

Grafana data source docs:
[https://grafana.com/docs/grafana/latest/datasources/loki/](https://grafana.com/docs/grafana/latest/datasources/loki/)

### Step 5: Explore logs

In Grafana’s Explore tab, select Loki and query logs, for example:

```
{job="kubernetes-pods", namespace="default"}
```

### Step 6: Customize Promtail config if needed

You can override Promtail’s config using Helm values, for example:

```
helm upgrade loki grafana/loki-stack --set promtail.config.snippets.pipelineStages='[{"docker": {"stream": "stdout"}}]'
```

Promtail config reference:
[https://grafana.com/docs/loki/latest/clients/promtail/configuration/](https://grafana.com/docs/loki/latest/clients/promtail/configuration/)


### A quick note on operators

Prometheus monitoring uses the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
via `kube-prometheus-stack`, which provides Kubernetes CRDs like `ServiceMonitor`. Loki does **not**
have an operator; it’s deployed via Helm with no CRDs.
