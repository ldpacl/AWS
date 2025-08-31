# Terraform IAM Setup Guide

## Prerequisites

### 1. Install Terraform

#### Windows
```bash
# Using Chocolatey
choco install terraform

# Or download from https://www.terraform.io/downloads
# Extract and add to PATH
```

#### macOS
```bash
# Using Homebrew
brew install terraform

# Or using tfenv for version management
brew install tfenv
tfenv install latest
tfenv use latest
```

#### Linux
```bash
# Ubuntu/Debian
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# CentOS/RHEL
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install terraform
```

### 2. Verify Installation
```bash
terraform --version
```

### 3. AWS Credentials Setup

#### Option A: AWS CLI Configuration
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
```

#### Option B: Environment Variables
```bash
# Linux/macOS
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Windows
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1
```

### 4. Required Permissions
Your AWS user needs:
- `IAMFullAccess` policy
- Or custom policy with permissions to create users, groups, roles, and attach policies

## Configuration Files Overview

### `main.tf`
Contains the main Terraform configuration:
- AWS provider configuration
- IAM users, groups, and roles
- Policy attachments and group memberships

### `variables.tf`
Defines input variables:
- `region`: AWS region for deployment
- `user-1`: Name for first IAM user
- `user-2`: Name for second IAM user

### `terraform.tfvars`
Contains variable values:
- Default region: `us-east-1`
- Default user names: `name1` and `name2`

## Setup and Deployment

### 1. Navigate to Terraform Directory
```bash
cd /path/to/AWS_IAM/terraform
```

### 2. Customize Variables (Optional)
Edit `terraform.tfvars`:
```hcl
region = "us-east-1"
user-1 = "sarah-db-admin"
user-2 = "mike-devops"
```

### 3. Initialize Terraform
```bash
terraform init
```
This command:
- Downloads the AWS provider
- Initializes the backend
- Prepares the working directory

### 4. Plan the Deployment
```bash
terraform plan
```
This command:
- Shows what resources will be created
- Validates the configuration
- Displays any errors before deployment

### 5. Apply the Configuration
```bash
terraform apply
```
- Review the planned changes
- Type `yes` to confirm deployment
- Wait for resources to be created

### 6. Verify Deployment
```bash
# Show current state
terraform show

# List created resources
terraform state list
```

## What Gets Created

### IAM Users
- **User 1**: Database Administrator with RDS full access
- **User 2**: DevOps Engineer with group-based permissions

### IAM Groups
- **EC2FullAccess**: Group with Amazon EC2 full access policy
- **S3FullAccess**: Group with Amazon S3 full access policy

### IAM Role
- **role1**: EC2 service role with S3 read-only access

### Access Keys and Login Profiles
- Console login profiles for both users (password reset required)
- Programmatic access keys for both users

## Managing the Infrastructure

### View Current State
```bash
terraform show
terraform state list
```

### Update Configuration
1. Modify `terraform.tfvars` or `main.tf`
2. Run `terraform plan` to preview changes
3. Run `terraform apply` to apply changes

## Cleanup

### Destroy All Resources
```bash
terraform destroy
```
- Review resources to be destroyed
- Type `yes` to confirm deletion
- All IAM resources will be removed

### Selective Resource Removal
```bash
# Remove specific resource
terraform destroy -target=aws_iam_user.user1
```

## Troubleshooting

### Common Issues

1. **Provider Download Failed**
   ```bash
   # Clear cache and reinitialize
   rm -rf .terraform
   terraform init
   ```

2. **AWS Credentials Not Found**
   ```bash
   # Verify credentials
   aws sts get-caller-identity
   ```

3. **Permission Denied**
   ```
   Error: AccessDenied: User is not authorized to perform iam:CreateUser
   Solution: Ensure your AWS user has IAM permissions
   ```

### Terraform State Issues
```bash
# Backup state file
cp terraform.tfstate terraform.tfstate.backup

# Remove resource from state (if needed)
terraform state rm aws_iam_user.user1
```

## Best Practices

- Always run `terraform plan` before `terraform apply`
- Keep `terraform.tfstate` file secure and backed up
- Use version control for Terraform configurations