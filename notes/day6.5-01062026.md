# Day 6.5 Learning - Terraform + AWS Integration

## Objective

Connect Terraform to a real AWS account and perform the first successful Terraform-to-AWS interaction.

---

## AWS Account Setup

### AWS CLI Installation

Verified installation:

```powershell
aws --version
```

Example Output:

```text
aws-cli/2.x.x
```

---

## AWS CLI Configuration

Configured AWS credentials using:

```powershell
aws configure
```

Configured:

```text
AWS Access Key
AWS Secret Access Key
Region: ap-south-1
Output Format: json
```

---

## AWS Authentication Verification

Verified identity using:

```powershell
aws sts get-caller-identity
```

Initial output:

```text
arn:aws:iam::<account-id>:root
```

Learned that root credentials should not be used for daily operations.

---

## IAM User Creation

Created IAM user:

```text
terraform-admin
```

Permissions assigned:

```text
AdministratorAccess
```

Generated:

* Access Key
* Secret Access Key

Updated AWS CLI credentials using:

```powershell
aws configure
```

Verified:

```powershell
aws sts get-caller-identity
```

Output:

```text
arn:aws:iam::<account-id>:user/terraform-admin
```

---

## Why IAM Users Matter

### Root Account

```text
Full unrestricted access
Billing access
Account deletion capability
```

### IAM User

```text
Controlled access
Daily administration
Best practice
```

Real-world environments use IAM users, groups, and roles instead of root accounts.

---

## Terraform AWS Provider

Created:

### provider.tf

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

---

### variables.tf

```hcl
variable "aws_region" {
  default = "ap-south-1"
}
```

---

## AWS Data Sources

Learned Terraform Data Sources.

Example:

```hcl
data "aws_availability_zones" "available" {}
```

Purpose:

* Reads AWS information
* Does not create infrastructure
* No AWS charges incurred

---

## Terraform Outputs

Created:

```hcl
output "availability_zones" {
  value = data.aws_availability_zones.available.names
}
```

---

## First Terraform-to-AWS Interaction

Executed:

```powershell
terraform init
terraform plan
terraform apply
```

Output:

```text
availability_zones = [
  "ap-south-1a",
  "ap-south-1b",
  "ap-south-1c"
]
```

Successfully retrieved real AWS Availability Zone information.

---

## Resource vs Data Source

### Data Source

```hcl
data "aws_availability_zones" "available" {}
```

Purpose:

```text
Read existing information
No infrastructure creation
```

Examples:

```text
Availability Zones
AMI IDs
VPC Information
Subnet Information
```

---

### Resource

```hcl
resource "aws_instance" "web" {
  ...
}
```

Purpose:

```text
Create infrastructure
Modify infrastructure
Delete infrastructure
```

Examples:

```text
EC2
Security Groups
VPC
Subnets
RDS
EKS
```

---

## AWS Concepts Introduced

Studied:

* Regions
* Availability Zones (AZ)
* VPC
* Subnets
* Security Groups
* EC2
* IAM

Mumbai Region:

```text
ap-south-1
```

Availability Zones:

```text
ap-south-1a
ap-south-1b
ap-south-1c
```

---

## Key Learnings

✅ AWS CLI Installation

✅ AWS CLI Configuration

✅ IAM User Creation

✅ AWS Authentication

✅ Terraform AWS Provider

✅ Terraform Data Sources

✅ Terraform Outputs

✅ Availability Zones Discovery

✅ First Terraform-to-AWS API Interaction

✅ IAM Security Best Practices

---

## Current Roadmap Progress

```text
Linux
 ↓
Python
 ↓
Git/GitHub
 ↓
FastAPI
 ↓
Docker
 ↓
Docker Compose
 ↓
PostgreSQL
 ↓
Terraform Fundamentals
 ↓
AWS CLI
 ↓
IAM
 ↓
Terraform + AWS
 ↓
Security Groups
 ↓
VPC
 ↓
EC2
 ↓
Kubernetes
 ↓
Monitoring
 ↓
AI Infrastructure & LLMOps
```

---

## Next Session

### Terraform + AWS Resources

Topics:

* Security Groups
* VPC
* Subnets
* Route Tables
* Internet Gateway
* EC2 Instances

Goal:

Create and manage real AWS infrastructure using Terraform while staying within AWS Free Tier limits.
