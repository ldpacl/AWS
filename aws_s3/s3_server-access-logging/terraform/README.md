# S3 Server Access Logging - Terraform Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: S3 full access
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
- **main.tf**: Main Terraform configuration with S3 resources
- **variables.tf**: Variable definitions for bucket names and region
- **terraform.tfvars**: Variable values (customize this file)

### What This Configuration Creates
1. **Hosting Bucket 1** with public access and static website hosting
2. **Hosting Bucket 2** with public access and static website hosting
3. **Private Logging Bucket** with restricted access
4. **Bucket Policies** for public access and logging permissions
5. **Server Access Logging** configuration for both hosting buckets

## Implementation Steps

### Step 1: Prepare Configuration

1. **Navigate to terraform folder**:
```bash
cd /path/to/aws_s3/S3_server-access-logging/terraform/
```

2. **Update terraform.tfvars** with your values:
```hcl
region = "us-east-1"

# Bucket names must be globally unique
host-bucket-1 = "my-store-a-20240902"
host-bucket-2 = "my-store-b-20240902"
log-bucket = "my-logging-bucket-20240902"
```

**Important Notes:**
- **Bucket names must be globally unique** across all AWS accounts
- **Use descriptive names** with timestamps for uniqueness
- **Choose appropriate region** for your deployment

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
- Correct bucket names and region
- Bucket policies and configurations
- Server access logging setup

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
Apply complete! Resources: 9 added, 0 changed, 0 destroyed.
```

## Testing the Setup via AWS Console

### Step 1: Upload Test Content to Hosting Buckets

**Upload to Hosting Bucket 1:**
1. **Navigate to S3** in AWS Console
2. **Click on your first hosting bucket** (e.g., my-store-a-20240902)
3. **Click Upload**
4. **Create index.html**:
   - Click "Create file"
   - Name: `index.html`
   - Content: `<html><body><h1>Welcome to Store A</h1></body></html>`
5. **Click Upload**

**Upload to Hosting Bucket 2:**
1. **Click on your second hosting bucket** (e.g., my-store-b-20240902)
2. **Click Upload**
3. **Create index.html**:
   - Click "Create file"
   - Name: `index.html`
   - Content: `<html><body><h1>Welcome to Store B</h1></body></html>`
4. **Click Upload**

### Step 2: Get Website Endpoints

**For Both Hosting Buckets:**
1. **Click on hosting bucket**
2. **Go to Properties tab**
3. **Scroll to Static website hosting**
4. **Copy the Bucket website endpoint**

### Step 3: Access Websites to Generate Logs

**Generate Access Logs:**
1. **Open both website endpoints** in your browser
2. **Refresh pages multiple times** to generate access logs
3. **Try accessing non-existent pages** to generate 404 logs
4. **Access from different browsers/devices** for varied log entries

### Step 4: Verify Logging Configuration via Console

**Check Logging Settings:**
1. **Navigate to S3** in AWS Console
2. **Click on first hosting bucket**
3. **Go to Properties tab**
4. **Scroll to Server access logging**
5. **Verify**: Target bucket and prefix are configured correctly
6. **Repeat for second hosting bucket**

### Step 5: Monitor Log Files via Console

**Check Logging Bucket:**
1. **Navigate to your logging bucket**
2. **Look for logs folder structure**:
   - `logs/my-store-a-20240902/` (for hosting bucket 1 logs)
   - `logs/my-store-b-20240902/` (for hosting bucket 2 logs)
3. **Note**: Log files may take 2-24 hours to appear
4. **Refresh periodically** to check for new log files

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
# Get details of specific resources
terraform state show aws_s3_bucket.host-bucket-1
terraform state show aws_s3_bucket.log-bucket
terraform state show aws_s3_bucket_policy.host1-policy
```

## Cleanup Process

### Step 1: Empty S3 Buckets (Required Before Destroy)

**Via AWS Console:**

**Hosting Buckets:**
1. **Navigate to S3** in AWS Console
2. **Select first hosting bucket**
3. **Click Empty**
4. **Type bucket name** to confirm
5. **Click Empty**
6. **Repeat for second hosting bucket**

**Logging Bucket:**
1. **Select logging bucket**
2. **Click Empty**
3. **Type bucket name** to confirm
4. **Click Empty**
5. **Note**: This removes all access logs

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
Destroy complete! Resources: 9 destroyed.
```

### Step 3: Verify Cleanup via AWS Console

**Check S3 Buckets:**
1. **Navigate to S3** in AWS Console
2. **Verify all three buckets are deleted**
3. **Check that no resources remain**

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
- Use timestamps: `my-bucket-20240902-123456`

**Provider Download Failed**
```bash
# Clear Terraform cache and reinitialize
rm -rf .terraform/
terraform init
```

**Bucket Not Empty Error During Destroy**
- Empty buckets via AWS Console before running `terraform destroy`
- Terraform cannot delete non-empty S3 buckets

**Invalid Bucket Name Error**
- Bucket names must be 3-63 characters
- Use lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen

## Best Practices

### Naming Conventions
- **Include environment** in resource names (dev, staging, prod)
- **Use consistent naming** across all resources
- **Add timestamps** for uniqueness

### Security Considerations
- **Review bucket policies** before deployment
- **Monitor access logs** regularly for suspicious activity
- **Use least privilege** principle for IAM permissions

### Cost Optimization
- **Set lifecycle policies** for log retention
- **Monitor storage costs** for logging bucket
- **Consider log analysis tools** for better insights

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

## Files in This Directory

- **`main.tf`**: Main Terraform configuration with S3 resources and policies
- **`variables.tf`**: Variable definitions for bucket names and region
- **`terraform.tfvars`**: Variable values (customize with your bucket names)
- **`README.md`**: This documentation file

Remember to use globally unique bucket names and ensure your AWS credentials have appropriate S3 permissions before deployment.
