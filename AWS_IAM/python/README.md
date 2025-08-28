# Python Boto3 IAM Setup Guide

## Prerequisites

### 1. Python Installation
```bash
# Check Python version (3.6+ required)
python --version
# or
python3 --version

# Install Python if not available
# Windows: Download from https://python.org
# macOS: brew install python3
# Linux: sudo apt install python3 python3-pip
```

### 2. Install Required Packages
```bash
# Install boto3 AWS SDK
pip install boto3

# Or using pip3
pip3 install boto3

# Verify installation
python -c "import boto3; print(boto3.__version__)"
```

### 3. AWS Credentials Setup

#### Option A: AWS CLI Configuration
```bash
# Install AWS CLI first
pip install awscli

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format
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

#### Option C: AWS Credentials File
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
region = us-east-1
```

### 4. Required Permissions
Your AWS user needs:
- `IAMFullAccess` policy
- Or custom policy with permissions to create users, groups, roles, and attach policies

## Script Overview

The `iam.py` script creates:
- **2 IAM Groups**: `ec2fullaccess` and `s3fullaccess`
- **2 IAM Users**: Database Administrator and DevOps Engineer
- **1 IAM Role**: EC2 service role with S3 read-only access
- **Policy Attachments**: Appropriate permissions for each resource

## Running the Script

### 1. Navigate to Python Directory
```bash
cd /path/to/AWS_IAM/python
```

### 2. Execute the Script
```bash
python iam.py
# or
python3 iam.py
```

### 3. Provide Input When Prompted
```
Enter the name of the user1: sarah-db-admin
Enter the password of the user1: TempPassword123!
Enter the name of the user2: mike-devops
Enter the password of the user2: TempPassword456!
```

### 4. Expected Output
```
Group1 created successfully
Group2 created successfully
Policy1 attached successfully
Policy2 attached successfully
User1 created successfully
User2 created successfully
User2 added to group1 successfully
User1 added to group2 successfully
Role created successfully
```

## Script Functionality

### Groups Created
- **ec2fullaccess**: Group with `AmazonEC2FullAccess` policy
- **s3fullaccess**: Group with `AmazonS3FullAccess` policy

### Users Created
- **User1** (Database Admin): 
  - Added to `s3fullaccess` group
  - Direct `AmazonRDSFullAccess` policy attachment
- **User2** (DevOps Engineer):
  - Added to `ec2fullaccess` group

### Role Created
- **role1**: EC2 service role with `AmazonS3ReadOnlyAccess` policy

## Verification

### Check Created Resources
```python
import boto3

iam = boto3.client('iam')

# List users
users = iam.list_users()
print("Users:", [user['UserName'] for user in users['Users']])

# List groups
groups = iam.list_groups()
print("Groups:", [group['GroupName'] for group in groups['Groups']])

# List roles
roles = iam.list_roles()
print("Roles:", [role['RoleName'] for role in roles['Roles']])
```

### Test User Login
1. Go to AWS Console sign-in page
2. Use Account ID and created user credentials
3. Verify appropriate service access

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'boto3'**
   ```bash
   pip install boto3
   ```

2. **NoCredentialsError**
   ```
   Solution: Configure AWS credentials using one of the methods above
   ```

3. **AccessDenied Error**
   ```
   Solution: Ensure your AWS user has IAM permissions
   ```

4. **EntityAlreadyExists Error**
   ```python
   # Add this check before creating resources
   try:
       iam.get_user(UserName='existing-user')
       print("User already exists")
   except iam.exceptions.NoSuchEntityException:
       # User doesn't exist, safe to create
       pass
   ```

## Cleanup

### Steps to Run Cleanup Script

1. **Navigate to Python Directory**
   ```bash
   cd /path/to/AWS_IAM/python
   ```

2. **Execute the Cleanup Script**
   ```bash
   python cleanup.py
   # or
   python3 cleanup.py
   ```

3. **Provide Input When Prompted**
   ```
   Enter the name of user1 to delete: sarah-db-admin
   Enter the name of user2 to delete: mike-devops
   ```

4. **Expected Cleanup Output**
   ```
   Cleaning up User1...
   User1 deleted successfully
   Cleaning up User2...
   User2 deleted successfully
   Cleaning up Groups...
   Groups deleted successfully
   Cleaning up Role...
   Role deleted successfully
   All resources cleaned up successfully!
   ```

### What Gets Cleaned Up
- Detaches all policies from users and groups
- Removes users from groups
- Deletes login profiles
- Deletes IAM users
- Deletes IAM groups
- Deletes IAM role
