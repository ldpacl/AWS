# S3 Cross-Region Replication - Python (Boto3) Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: S3 and IAM full access
- **Two AWS Regions**: Access to at least two different regions
- **AWS Credentials**: Configured via AWS CLI, environment variables, or IAM roles

## Python Environment Setup

### Step 1: Install Python (if not already installed)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Windows:**
- Download from https://python.org/downloads/
- Ensure "Add Python to PATH" is checked during installation

### Step 2: Install Required Python Packages

```bash
# Install boto3 (AWS SDK for Python)
pip install boto3

# Verify installation
python -c "import boto3; print(boto3.__version__)"
```

### Step 3: Configure AWS Credentials

**Option 1: AWS CLI (Recommended)**
```bash
# Install AWS CLI first
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

## Script Overview

The `s3_crr.py` script automates the complete S3 Cross-Region Replication setup:

### What the Script Does
1. **Creates source bucket** in the default region
2. **Enables versioning** on source bucket
3. **Creates destination bucket** in specified region
4. **Enables versioning** on destination bucket
5. **Creates IAM policy** with replication permissions
6. **Creates IAM role** for S3 service
7. **Attaches policy to role**
8. **Configures replication rules** on source bucket

### Input Requirements
- **Source bucket name**: Must be globally unique
- **Destination bucket name**: Must be globally unique
- **Destination region**: Different from your default region

## Implementation Steps

### Step 1: Prepare for Execution

1. **Navigate to the python folder**:
```bash
cd /path/to/aws_s3/S3_cross-region-replication/python/
```

2. **Verify script exists**:
```bash
ls -la s3_crr.py
```

3. **Check Python and boto3**:
```bash
python --version
python -c "import boto3; print('Boto3 ready')"
```

### Step 2: Run the Script

```bash
python s3_crr.py
```

### Step 3: Provide Input When Prompted

**Example interaction:**
```
Enter the source bucket name: my-source-bucket-20240829
Enter the destination bucket name: my-dest-bucket-20240829
Enter the destination bucket region: us-west-2
```

**Important Notes:**
- **Bucket names must be globally unique** across all AWS accounts
- **Use descriptive names** with timestamps for uniqueness
- **Destination region** must be different from your default region
- **Script runs in your default region** (configured in AWS credentials)

### Step 4: Monitor Execution

The script will output progress messages:
```
Source bucket created successfully
Destination bucket created successfully
Replication policy created successfully
Replication role created successfully
Replication configuration set successfully
```

## Testing Replication

### Step 1: Upload Test File via AWS Console

1. **Navigate to S3** in AWS Console (source region)
2. **Click on your source bucket**
3. **Click Upload**
4. **Add files**: Select or drag a test file
5. **Click Upload**

### Step 2: Verify Replication via AWS Console

**Check Source Bucket:**
1. **Navigate to S3** in AWS Console (source region)
2. **Click on your source bucket**
3. **Verify the uploaded file** is present

**Check Destination Bucket:**
1. **Switch to destination region** in AWS Console
2. **Navigate to S3** service
3. **Click on your destination bucket**
4. **Wait 5-15 minutes** for replication to complete
5. **Refresh the page**
6. **Verify the test file** appears in the destination bucket

### Step 3: Monitor Replication Status

1. **Navigate to S3** in source region
2. **Click on your source bucket**
3. **Go to Management tab**
4. **Click Replication**
5. **Check replication metrics** and status

## Cleanup Process

### Step 1: Run Cleanup Script

```bash
python cleanup_s3_crr.py
```

### Step 2: Provide Input When Prompted

**Example interaction:**
```
Enter the source bucket name to delete: my-source-bucket-20240829
Enter the destination bucket name to delete: my-dest-bucket-20240829
Enter the destination bucket region: us-west-2
```

### Step 3: Monitor Cleanup Progress

The cleanup script will output progress messages:
```
Emptying source bucket...
Source bucket deleted successfully
Emptying destination bucket...
Destination bucket deleted successfully
Policy detached from role
Replication role deleted successfully
Replication policy deleted successfully
Cleanup completed successfully!
```

### Step 4: Verify Cleanup via AWS Console

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

**ImportError: No module named 'boto3'**
```bash
pip install boto3
# or
pip3 install boto3
```

**NoCredentialsError**
```bash
# Configure AWS credentials
aws configure
# or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**BucketAlreadyExists Error**
- Use unique bucket names with timestamps
- Check if bucket exists in another region via S3 Console

**AccessDenied Error**
- Ensure your AWS user has S3 and IAM permissions
- Check IAM policies attached to your user in IAM Console

**InvalidLocationConstraint Error**
- Verify the destination region name is correct
- Use standard region names (e.g., us-west-2, eu-west-1)

## Best Practices

### Naming Conventions
- **Include timestamps** in bucket names for uniqueness
- **Use descriptive prefixes** (e.g., company-project-source-bucket)
- **Avoid special characters** in bucket names