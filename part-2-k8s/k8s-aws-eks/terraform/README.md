# EKS Cluster POC with Terraform

The purpose of this section is to exercise the provision of a simple EKS Kubernetes cluster with
Terraform. 

These are the Terraform links that I have followed:

- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) 
- [VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)	
- [EKS Module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)

## Prerequisites

- Kubectl v1.29.1
- AWS CLI 2.11.19 configured with `cicd-terraform` profile
- Terraform v1.12.2

## Project Structure

```
k8s-aws-eks/
├── Makefile                  # Build and deployment commands
├── README.md                 # This documentation
└── terraform/
    ├── main.tf              # Main Terraform configuration
    ├── variables.tf         # Input variables
    ├── outputs.tf           # Output values
    ├── Makefile             # Terraform-specific commands
    └── README.md            # Terraform documentation
```

## Setup

### 1. Create AWS User and Attach IAM Policies

Create a user with the following policies:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:*",
                "ec2:*",
                "iam:*",
                "cloudformation:*",
                "autoscaling:*",
                "cloudwatch:*",
                "logs:*",
                "kms:*",
                "elasticloadbalancing:*",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:GetParametersByPath",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

### 2. Configure AWS CLI Profile

Configure the AWS CLI with the `cicd-terraform` profile using the access keys:

```bash
aws configure --profile cicd-terraform
```

Enter the following when prompted:
- AWS Access Key ID: [Your Access Key ID]
- AWS Secret Access Key: [Your Secret Access Key]
- Default region name: eu-west-2
- Default output format: json

Alternatively, you can manually edit `~/.aws/credentials`:

```ini
[cicd-terraform]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

And `~/.aws/config`:

```ini
[profile cicd-terraform]
region = eu-west-2
output = json
```

## Quick Start

### Using Makefile
```bash
# deploy (init, validate and apply)
make deploy

# Access the cluster (update kubeconfig for cluster access)
make kubeconfig 
make test

# Clean up
make destroy
```

## Configuration

### Variables
All configuration is in `variables.tf`. Key variables:

- `cluster_name`: EKS cluster name (default: "eks-terraform-test-2")
- `region`: AWS region (default: "eu-west-2")
- `profile`: AWS CLI profile (default: "cicd-terraform")
- `vpc_cidr`: VPC CIDR block (default: "10.123.0.0/16")

### Cluster Specifications
- **Node Type**: t3.medium (2 vCPU, 4GB RAM)
- **Capacity Type**: SPOT (cost-effective)
- **Node Count**: 1-3 nodes (desired: 2)
- **Kubernetes Version**: Latest EKS version
- **Networking**: Private subnets for nodes, public subnets for load balancers

## Architecture

```
VPC (10.123.0.0/16)
├── Public Subnets (10.123.1.0/24, 10.123.2.0/24)
├── Private Subnets (10.123.3.0/24, 10.123.4.0/24)
├── Intra Subnets (10.123.5.0/24, 10.123.6.0/24)
├── EKS Cluster
└── Node Group (t3.medium, SPOT)
```
