# EN: Terraform provider and backend configuration for StrataRAG Orchestrator
# FR: Configuration du provider et du backend Terraform pour StrataRAG Orchestrator

terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # EN: Uncomment and configure for remote state storage
  # FR: Décommenter et configurer pour le stockage d'état distant
  # backend "s3" {
  #   bucket = "strata-rag-tf-state"
  #   key    = "terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region / Région AWS"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming / Nom du projet"
  type        = string
  default     = "strata-rag"
}

variable "environment" {
  description = "Deployment environment / Environnement de déploiement"
  type        = string
  default     = "dev"
}