# EKS Cluster POC Makefile

# Default cluster name (can be overridden with CLUSTER_NAME=my-cluster)
CLUSTER_NAME ?= eks-terraform-test-2

.PHONY: help init validate plan apply destroy kubeconfig test clean status deploy quick-test outputs

# Default target
help:
	@echo "EKS Cluster POC - Available commands:"
	@echo "  init      - Initialize Terraform"
	@echo "  validate  - Validate Terraform configuration"
	@echo "  plan      - Show Terraform plan"
	@echo "  apply     - Deploy EKS cluster (use: make apply CLUSTER_NAME=my-cluster)"
	@echo "  kubeconfig- Update kubeconfig for cluster access"
	@echo "  test      - Test cluster with nginx pod"
	@echo "  status    - Check cluster and node status"
	@echo "  destroy   - Destroy EKS cluster"
	@echo "  clean     - Clean up local files"
	@echo "  deploy    - Full deployment workflow (use: make deploy CLUSTER_NAME=my-cluster)"
	@echo "  quick-test- Quick test (assumes cluster is running)"
	@echo "  outputs   - Show Terraform outputs"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make apply CLUSTER_NAME=my-prod-cluster"
	@echo "  make deploy CLUSTER_NAME=my-dev-cluster"

# Initialize Terraform
init:
	@echo "Initializing Terraform..."
	terraform init

# Validate configuration
validate:
	@echo "Validating Terraform configuration..."
	terraform validate

# Show plan
plan:
	@echo "Showing Terraform plan for cluster: $(CLUSTER_NAME)..."
	terraform plan -var="cluster_name=$(CLUSTER_NAME)"

# Deploy cluster
apply:
	@echo "Deploying EKS cluster: $(CLUSTER_NAME)..."
	terraform apply -auto-approve -var="cluster_name=$(CLUSTER_NAME)"

# Update kubeconfig
kubeconfig:
	@echo "Updating kubeconfig for cluster: $(CLUSTER_NAME)..."
	aws eks update-kubeconfig --region eu-west-2 --name $(CLUSTER_NAME) --profile cicd-terraform
	@echo "Kubeconfig updated successfully!"

# Test cluster
test:
	@echo "Testing cluster with nginx pod..."
	kubectl run testpod --image=nginx
	@echo "Waiting for pod to be ready..."
	kubectl wait --for=condition=ready pod/testpod --timeout=60s
	@echo "Pod status:"
	kubectl get pods
	@echo "Pod logs:"
	kubectl logs testpod

# Check status
status:
	@echo "Cluster Status for: $(CLUSTER_NAME)"
	@echo "=================="
	@echo "Checking cluster status..."
	aws eks describe-cluster --name $(CLUSTER_NAME) --region eu-west-2 --profile cicd-terraform --query 'cluster.status' --output text
	@echo ""
	@echo "Node Status:"
	@echo "==============="
	kubectl get nodes
	@echo ""
	@echo "Pod Status:"
	@echo "============="
	kubectl get pods --all-namespaces

# Destroy cluster
destroy:
	@echo "Destroying EKS cluster: $(CLUSTER_NAME)..."
	terraform destroy -auto-approve -var="cluster_name=$(CLUSTER_NAME)"

# Clean up local files
clean:
	@echo "Cleaning up local files..."
	rm -rf .terraform
	rm -f terraform.tfstate*
	rm -f .terraform.lock.hcl
	@echo "Cleanup complete!"

# Full deployment workflow
deploy: init validate plan apply kubeconfig test
	@echo "Deployment complete! Cluster $(CLUSTER_NAME) is ready."

# Quick test (assumes cluster is already running)
quick-test: kubeconfig test

# Show outputs
outputs:
	@echo "Terraform outputs:"
	terraform output 