terraform {
  required_version = ">= 0.14.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = ">=2.7.1"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.2.2"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.1.0"
    }
  }
}
# configure provider
provider "aws" {
  region     = var.aws_region
}
