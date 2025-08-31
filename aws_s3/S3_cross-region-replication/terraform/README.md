# S3 Cross-Region Replication - Terraform Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: S3, IAM, and STS full access
- **Two AWS Regions**: Access to at least two different regions
- **AWS Credentials**: Configured via AWS CLI or environment variables

## Terraform Installation

### Step 1: Install Terraform

**Linux (Ubuntu/Debian):**
```bash
# Add HashiCorp GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

# Add HashiCorp repository
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

# Install Terraform
sudo apt-get update && sudo apt-get install terraform

# Verify installation
terraform --version
```

**macOS:**
```bash
# Using Homebrew
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Verify installation
terraform --version
```

**Windows:**
1. Download from https://www.terraform.io/downloads.html
2. Extract to a directory (e.g., C:\terraform)
3. Add to PATH environment variable
4. Verify: `terraform --version`

### Step 2: Configure AWS Credentials

**Option 1: AWS CLI (Recommended)**
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

**Option 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## Terraform Configuration Overview

### Files Structure
- **main.tf**: Main Terraform configuration with resources
- **variables.tf**: Variable definitions
- **terraform.tfvars**: Variable values (customize this file)

### What This Configuration Creates
1. **Source S3 bucket** in region-1 with versioning enabled
2. **Destination S3 bucket** in region-2 with versioning enabled
3. **IAM role** for S3 replication service
4. **IAM policy** with replication permissions
5. **Replication configuration** on source bucket

## Implementation Steps

### Step 1: Prepare Configuration

1. **Navigate to terraform folder**:
```bash
cd /path/to/aws_s3/S3_cross-region-replication/terraform/
```

2. **Update terraform.tfvars** with your values:
```hcl
region-1 = "us-east-1"
region-2 = "us-west-2"

# Bucket names must be globally unique
source-bucket = "my-source-bucket-20240829"
destination-bucket = "my-dest-bucket-20240829"
```

**Important Notes:**
- **Bucket names must be globally unique** across all AWS accounts
- **Use descriptive names** with timestamps for uniqueness
- **Choose different regions** for proper cross-region replication

### Step 2: Initialize Terraform

```bash
# Initialize Terraform (downloads AWS provider)
terraform init
```

**Expected output:**
```
Initializing the backend...
Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws...
Terraform has been successfully initialized!
```

### Step 3: Plan Deployment

```bash
# Review what Terraform will create
terraform plan
```

**Review the plan output** to ensure:
- Correct bucket names and regions
- IAM role and policy creation
- Replication configuration setup

### Step 4: Apply Configuration

```bash
# Deploy the infrastructure
terraform apply
```

**When prompted:**
- Type `yes` to confirm deployment
- Wait for completion (typically 2-5 minutes)

**Expected output:**
```
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.
```

## Testing Replication via AWS Console

### Step 1: Upload Test File to Source Bucket

1. **Navigate to S3** in AWS Console (region-1)
2. **Click on your source bucket**
3. **Click Upload**
4. **Add files**: Select or drag a test file
5. **Click Upload**

### Step 2: Verify Replication in Destination Bucket

1. **Switch to region-2** in AWS Console
2. **Navigate to S3** service
3. **Click on your destination bucket**
4. **Wait 5-15 minutes** for replication to complete
5. **Refresh the page**
6. **Verify the test file** appears in the destination bucket

### Step 3: Monitor Replication Status

1. **Navigate to S3** in region-1 (source region)
2. **Click on your source bucket**
3. **Go to Management tab**
4. **Click Replication**
5. **Check replication rules** and metrics


## Terraform State Management

### View Current State
```bash
# Show current Terraform state
terraform show

# List all resources in state
terraform state list
```

### Check Resource Status
```bash
# Get details of specific resource
terraform state show aws_s3_bucket.source-bucket
terraform state show aws_iam_role.replication-role
```

## Cleanup Process

### Step 1: Empty S3 Buckets (Required Before Destroy)

**Via AWS Console:**

**Source Bucket:**
1. **Navigate to S3** in region-1
2. **Select your source bucket**
3. **Click Empty**
4. **Type bucket name** to confirm
5. **Click Empty**

**Destination Bucket:**
1. **Navigate to S3** in region-2
2. **Select your destination bucket**
3. **Click Empty**
4. **Type bucket name** to confirm
5. **Click Empty**

### Step 2: Destroy Terraform Infrastructure

```bash
# Destroy all resources
terraform destroy
```

**When prompted:**
- **Review the destruction plan**
- Type `yes` to confirm destruction
- **Wait for completion** (typically 2-5 minutes)

**Expected output:**
```
Destroy complete! Resources: 6 destroyed.
```

### Step 3: Verify Cleanup via AWS Console

**Check S3 Buckets:**
1. **Navigate to S3** in both regions
2. **Verify buckets are deleted**

**Check IAM Resources:**
1. **Navigate to IAM** → **Roles**
2. **Verify replication-role is deleted**
3. **Navigate to IAM** → **Policies**
4. **Verify replication-policy is deleted**


## Troubleshooting

### Common Issues

**Terraform Not Found**
```bash
# Verify Terraform installation
terraform --version
# If not found, reinstall Terraform
```

**AWS Credentials Error**
```bash
# Verify AWS credentials
aws sts get-caller-identity
# If error, reconfigure: aws configure
```

**Bucket Already Exists Error**
- Update `terraform.tfvars` with unique bucket names
- Use timestamps: `my-bucket-20240829-123456`

**Provider Download Failed**
```bash
# Clear Terraform cache and reinitialize
rm -rf .terraform/
terraform init
```

**Bucket Not Empty Error During Destroy**
- Empty buckets via AWS Console before running `terraform destroy`
- Terraform cannot delete non-empty S3 buckets

## Best Practices

### Naming Conventions
- **Include environment** in resource names (dev, staging, prod)
- **Use consistent naming** across all resources
- **Add timestamps** for uniqueness

## Terraform Commands Reference

| Command | Purpose |
|---------|---------|
| `terraform init` | Initialize working directory |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy infrastructure |
| `terraform validate` | Validate configuration |
| `terraform fmt` | Format configuration files |
| `terraform show` | Show current state |
| `terraform state list` | List resources in state |
| `terraform refresh` | Update state from AWS |
