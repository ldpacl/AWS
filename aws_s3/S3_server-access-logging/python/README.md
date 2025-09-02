# S3 Server Access Logging - Python (Boto3) Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: S3 full access
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

The `s3-sal.py` script automates the complete S3 Server Access Logging setup:

### What the Script Does
1. **Creates hosting bucket 1** with public access and static website hosting
2. **Creates hosting bucket 2** with public access and static website hosting
3. **Creates private logging bucket** with restricted access
4. **Configures bucket policies** for public access and logging permissions
5. **Enables server access logging** for both hosting buckets
6. **Organizes logs** in separate folders within the logging bucket

### Input Requirements
- **Hosting bucket 1 name**: Must be globally unique
- **Hosting bucket 2 name**: Must be globally unique
- **Logging bucket name**: Must be globally unique
- **AWS Account ID**: Your 12-digit AWS account ID
- **Region**: AWS region for bucket creation

## Implementation Steps

### Step 1: Prepare for Execution

1. **Navigate to the python folder**:
```bash
cd /path/to/aws_s3/S3_server-access-logging/python/
```

2. **Verify script exists**:
```bash
ls -la s3-sal.py
```

3. **Check Python and boto3**:
```bash
python --version
python -c "import boto3; print('Boto3 ready')"
```

### Step 2: Run the Script

```bash
python s3-sal.py
```

### Step 3: Provide Input When Prompted

**Example interaction:**
```
Enter the name of the hosting bucket 1: my-store-a-20240902
Enter the name of the hosting bucket 2: my-store-b-20240902
Enter the name of the logging bucket: my-logging-bucket-20240902
Enter your account id: 123456789012
Enter the region: us-east-1
```

**Important Notes:**
- **Bucket names must be globally unique** across all AWS accounts
- **Use descriptive names** with timestamps for uniqueness
- **Account ID** can be found in AWS Console → Account settings
- **Region** should match your desired deployment region

### Step 4: Monitor Execution

The script will output progress messages:
```
Hosting bucket 1 created successfully
Host Bucket 1 policy added successfully
Hosting bucket 2 created successfully
Host Bucket 2 policy added successfully
Logging bucket created successfully
Log Bucket policy added successfully
```

## Testing the Setup via AWS Console

### Step 1: Upload Test Content to Hosting Buckets

**Upload to Hosting Bucket 1:**
1. **Navigate to S3** in AWS Console
2. **Click on your first hosting bucket** (e.g., my-store-a-20240902)
3. **Click Upload**
4. **Create a test file**: Click "Create folder" or upload an existing file
5. **Create index.html**: 
   - Click "Create file" 
   - Name: `index.html`
   - Content: `<html><body><h1>Welcome to Store A</h1></body></html>`
6. **Click Upload**

**Upload to Hosting Bucket 2:**
1. **Click on your second hosting bucket** (e.g., my-store-b-20240902)
2. **Click Upload**
3. **Create index.html**:
   - Click "Create file"
   - Name: `index.html` 
   - Content: `<html><body><h1>Welcome to Store B</h1></body></html>`
4. **Click Upload**

### Step 2: Get Website Endpoints

**For Hosting Bucket 1:**
1. **Click on your first hosting bucket**
2. **Go to Properties tab**
3. **Scroll to Static website hosting**
4. **Copy the Bucket website endpoint** (e.g., `http://my-store-a-20240902.s3-website-us-east-1.amazonaws.com`)

**For Hosting Bucket 2:**
1. **Click on your second hosting bucket**
2. **Go to Properties tab**
3. **Scroll to Static website hosting**
4. **Copy the Bucket website endpoint**

### Step 3: Access Websites to Generate Logs

**Generate Access Logs:**
1. **Open both website endpoints** in your browser
2. **Refresh pages multiple times** to generate access logs
3. **Try accessing non-existent pages** (e.g., add `/test.html` to URL) to generate 404 logs
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
1. **Navigate to your logging bucket** (e.g., my-logging-bucket-20240902)
2. **Look for logs folder structure**:
   - `logs/my-store-a-20240902/` (for hosting bucket 1 logs)
   - `logs/my-store-b-20240902/` (for hosting bucket 2 logs)
3. **Note**: Log files may take 2-24 hours to appear
4. **Refresh periodically** to check for new log files

## Cleanup Process

### Step 1: Run Cleanup Script

The repository includes a dedicated cleanup script `cleanup_s3_sal.py` that handles the complete removal of all resources.

```bash
python cleanup_s3_sal.py
```

### Step 2: Provide Input When Prompted

**Example interaction:**
```
Enter hosting bucket 1 name to delete: my-store-a-20240902
Enter hosting bucket 2 name to delete: my-store-b-20240902
Enter logging bucket name to delete: my-logging-bucket-20240902
```

### Step 3: Monitor Cleanup Progress

The cleanup script will output progress messages:
```
Disabling server access logging...
Logging disabled successfully
Emptying bucket: my-store-a-20240902
Bucket my-store-a-20240902 deleted successfully
Emptying bucket: my-store-b-20240902
Bucket my-store-b-20240902 deleted successfully
Emptying bucket: my-logging-bucket-20240902
Bucket my-logging-bucket-20240902 deleted successfully
Cleanup completed successfully!
```

### Step 4: Verify Cleanup via AWS Console

**Check S3 Buckets:**
1. **Navigate to S3** in AWS Console
2. **Verify all three buckets are deleted**
3. **Check that no resources remain**

**Optional CLI Verification:**
```bash
# Verify buckets are deleted (should return no results)
aws s3 ls | grep -E "(my-store-a|my-store-b|my-logging)"
```

## Files in This Directory

- **`s3-sal.py`**: Main script that creates the S3 server access logging infrastructure
- **`cleanup_s3_sal.py`**: Cleanup script that removes all created resources
- **`README.md`**: This documentation file

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
- Check if bucket exists via S3 Console

**AccessDenied Error**
- Ensure your AWS user has S3 permissions
- Check IAM policies in AWS Console

**InvalidBucketName Error**
- Bucket names must be 3-63 characters
- Use lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen

## Best Practices

### Naming Conventions
- **Include timestamps** in bucket names for uniqueness
- **Use descriptive prefixes** (e.g., company-project-store-a)
- **Avoid uppercase letters** in bucket names

### Security Considerations
- **Review bucket policies** before deployment
- **Monitor access logs** regularly for suspicious activity
- **Use least privilege** principle for IAM permissions

### Cost Optimization
- **Set lifecycle policies** for log retention
- **Monitor storage costs** for logging bucket
- **Consider log analysis tools** for better insights

### Error Handling
- **Always use try-except blocks** in production code
- **Log errors** for debugging purposes
- **Implement retry logic** for transient failures

## Script Customization

To modify the script for your specific needs:
1. **Edit bucket policies** in the JSON sections
2. **Change logging prefixes** for different folder structures
3. **Add error handling** for production use

Remember to use globally unique bucket names and ensure your AWS credentials have appropriate S3 permissions.