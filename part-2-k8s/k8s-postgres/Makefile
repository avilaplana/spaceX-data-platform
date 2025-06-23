# PostgresSQL Helm Chart Makefile

.PHONY: help deploy-operator check-operator install-postgres-helm-chart check-postgres uninstall

# Default target
help:
	@echo "PostgresSQL Helm Chart - Available commands:"
	@echo "  deploy-operator      			- Deploy Kubegres CRD's and operator"
	@echo "  check-operator       			- Check the operator is up and running"
	@echo "  install-postgres-helm-chart    - Install PostgresSQL Helm Chart"
	@echo "  check-postgres					- Check job and pods are running"
	@echo "  uninstall      				- Uninstall PostgresSQL Helm Chart"

# Deploy Kubegres CRD's and operator
deploy-operator:
	@echo "Installing Kubegres operator..."
	kubectl apply -f https://raw.githubusercontent.com/reactive-tech/kubegres/v1.17/kubegres.yaml

# Check the operator is up and running
check-operator:
	@echo "Checking if Kubegres operator is ready..."
	kubectl wait --for=condition=ready pod -l control-plane=controller-manager -n kubegres-system --timeout=300s
	@echo "Kubegres operator is ready!"

# Install PostgresSQL Helm Chart
install-postgres-helm-chart:
	@echo "Installing PostgreSQL Helm chart..."
	helm install postgres-spacex ./ --namespace interview --create-namespace

# Check job and pods are running
check-postgres:
	@echo "Checking PostgreSQL deployment status..."
	@echo "=== Kubegres status ==="
	kubectl get kubegres -n interview
	@echo ""
	@echo "=== Pods status ==="
	kubectl get pods -n interview
	@echo ""
	@echo "=== Jobs status ==="
	kubectl get jobs -n interview
	@echo ""
	@echo "=== Services status ==="
	kubectl get svc -n interview

# Uninstall PostgresSQL Helm Chart
uninstall:
	@echo "Uninstalling PostgreSQL Helm chart..."
	helm uninstall postgres-spacex --namespace interview
	@echo "Removing namespace..."
	kubectl delete namespace interview --ignore-not-found=true
	@echo "PostgreSQL Helm chart uninstalled successfully!"
	
