# Airflow Helm Chart Makefile

.PHONY: help install-airflow-helm-chart check-airflow uninstall

# Default target
help:
	@echo "Airflow Helm Chart - Available commands:"
	@echo "  install-airflow-helm-chart    - Install Airflow Helm Chart"
	@echo "  check-airflow					- Check Airflow pods and services are running"
	@echo "  uninstall      				- Uninstall Airflow Helm Chart"

# Install Airflow Helm Chart
install-airflow-helm-chart:
	@echo "Installing Airflow Helm chart..."
	helm install airflow-spacex ./ --namespace airflow --create-namespace

# Check Airflow pods and services are running
check-airflow:
	@echo "Checking Airflow deployment status..."
	@echo "=== Airflow pods status ==="
	kubectl get pods -n airflow -l app=airflow
	@echo ""
	@echo "=== Airflow services status ==="
	kubectl get svc -n airflow -l app=airflow
	@echo ""
	@echo "=== Airflow jobs status ==="
	kubectl get jobs -n airflow
	@echo ""
	@echo "=== Airflow ConfigMaps ==="
	kubectl get configmap -n airflow -l app=airflow

# Uninstall Airflow Helm Chart
uninstall:
	@echo "Uninstalling Airflow Helm chart..."
	helm uninstall airflow-spacex --namespace airflow
	@echo "Airflow Helm chart uninstalled successfully!" 