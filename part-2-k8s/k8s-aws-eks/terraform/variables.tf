variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "cicd-terraform"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "eks-terraform-interview"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.123.0.0/16"
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-west-2a", "eu-west-2b"]
}

variable "public_subnets" {
  description = "Public subnet CIDRs"
  type        = list(string)
  default     = ["10.123.1.0/24", "10.123.2.0/24"]
}

variable "private_subnets" {
  description = "Private subnet CIDRs"
  type        = list(string)
  default     = ["10.123.3.0/24", "10.123.4.0/24"]
}

variable "intra_subnets" {
  description = "Intra subnet CIDRs"
  type        = list(string)
  default     = ["10.123.5.0/24", "10.123.6.0/24"]
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Example     = "eks-terraform-test-2"
    Environment = "dev"
  }
} 