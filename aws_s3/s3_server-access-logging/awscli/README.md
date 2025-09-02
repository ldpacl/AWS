# S3 Server Access Logging - AWS CLI Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: S3 full access
- **Unique Bucket Names**: S3 bucket names must be globally unique

## AWS CLI Installation

### Install AWS CLI v2

**Linux/macOS:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows:**
```powershell
# Download and run the MSI installer from:
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

**Verify Installation:**
```bash
aws --version
```

### Configure AWS CLI
```bash
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

## Implementation Steps

### Step 1: Create Hosting Bucket 1

**Create S3 bucket for hosting:**
```bash
aws s3api create-bucket --bucket YOUR-HOSTING-BUCKET-1
```

**Make bucket publicly accessible:**
```bash
aws s3api put-public-access-block --bucket YOUR-HOSTING-BUCKET-1 --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

**Enable versioning:**
```bash
aws s3api put-bucket-versioning --bucket YOUR-HOSTING-BUCKET-1 --versioning-configuration Status=Enabled
```

**Configure static website hosting:**
```bash
aws s3api put-bucket-website --bucket YOUR-HOSTING-BUCKET-1 --website-configuration '{"IndexDocument": {"Suffix": "index.html"}}'
```

**Attach bucket policy for public access:**
```bash
aws s3api put-bucket-policy --bucket YOUR-HOSTING-BUCKET-1 --policy file://host1-policy.json
```

### Step 2: Create Hosting Bucket 2

**Create second hosting bucket:**
```bash
aws s3api create-bucket --bucket YOUR-HOSTING-BUCKET-2
```

**Make bucket publicly accessible:**
```bash
aws s3api put-public-access-block --bucket YOUR-HOSTING-BUCKET-2 --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

**Enable versioning:**
```bash
aws s3api put-bucket-versioning --bucket YOUR-HOSTING-BUCKET-2 --versioning-configuration Status=Enabled
```

**Configure static website hosting:**
```bash
aws s3api put-bucket-website --bucket YOUR-HOSTING-BUCKET-2 --website-configuration '{"IndexDocument": {"Suffix": "index.html"}}'
```

**Attach bucket policy for public access:**
```bash
aws s3api put-bucket-policy --bucket YOUR-HOSTING-BUCKET-2 --policy file://host2-policy.json
```

### Step 3: Create Private Logging Bucket

**Create private logging bucket:**
```bash
aws s3api create-bucket --bucket YOUR-LOGGING-BUCKET --acl private
```

**Attach logging bucket policy:**
```bash
aws s3api put-bucket-policy --bucket YOUR-LOGGING-BUCKET --policy file://logging-policy.json
```

### Step 4: Enable Server Access Logging

**Enable logging for hosting bucket 1:**
```bash
aws s3api put-bucket-logging --bucket YOUR-HOSTING-BUCKET-1 --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"YOUR-LOGGING-BUCKET","TargetPrefix":"logs/YOUR-HOSTING-BUCKET-1/"}}'
```

**Enable logging for hosting bucket 2:**
```bash
aws s3api put-bucket-logging --bucket YOUR-HOSTING-BUCKET-2 --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"YOUR-LOGGING-BUCKET","TargetPrefix":"logs/YOUR-HOSTING-BUCKET-2/"}}'
```

## Testing the Setup

### Upload Test Files
```bash
echo "<html><body><h1>Store A</h1></body></html>" > index.html
aws s3 cp index.html s3://YOUR-HOSTING-BUCKET-1/

echo "<html><body><h1>Store B</h1></body></html>" > index.html
aws s3 cp index.html s3://YOUR-HOSTING-BUCKET-2/
```

### Access Websites
```bash
# Get website endpoints
aws s3api get-bucket-website --bucket YOUR-HOSTING-BUCKET-1
aws s3api get-bucket-website --bucket YOUR-HOSTING-BUCKET-2

# Access via browser or curl to generate logs
curl http://YOUR-HOSTING-BUCKET-1.s3-website-us-east-1.amazonaws.com
curl http://YOUR-HOSTING-BUCKET-2.s3-website-us-east-1.amazonaws.com
```

### Verify Logging
```bash
# Check logging configuration
aws s3api get-bucket-logging --bucket YOUR-HOSTING-BUCKET-1
aws s3api get-bucket-logging --bucket YOUR-HOSTING-BUCKET-2

# Check for log files (may take 2-24 hours)
aws s3 ls s3://YOUR-LOGGING-BUCKET/logs/ --recursive
```

## Cleanup Steps

### Step 1: Disable Server Access Logging
```bash
aws s3api put-bucket-logging --bucket YOUR-HOSTING-BUCKET-1 --bucket-logging-status '{}'
aws s3api put-bucket-logging --bucket YOUR-HOSTING-BUCKET-2 --bucket-logging-status '{}'
```

### Step 2: Remove All Objects from Buckets
```bash
# Empty hosting buckets
aws s3 rm s3://YOUR-HOSTING-BUCKET-1 --recursive
aws s3 rm s3://YOUR-HOSTING-BUCKET-2 --recursive

# Empty logging bucket
aws s3 rm s3://YOUR-LOGGING-BUCKET --recursive
```

### Step 3: Delete Bucket Policies
```bash
aws s3api delete-bucket-policy --bucket YOUR-HOSTING-BUCKET-1
aws s3api delete-bucket-policy --bucket YOUR-HOSTING-BUCKET-2
aws s3api delete-bucket-policy --bucket YOUR-LOGGING-BUCKET
```

### Step 4: Delete Buckets
```bash
aws s3api delete-bucket --bucket YOUR-HOSTING-BUCKET-1
aws s3api delete-bucket --bucket YOUR-HOSTING-BUCKET-2
aws s3api delete-bucket --bucket YOUR-LOGGING-BUCKET
```

## Troubleshooting

### Common Issues
- **Bucket Already Exists**: S3 bucket names must be globally unique
- **Access Denied**: Ensure your AWS user has S3 permissions
- **Logs Not Appearing**: Server access logs can take 2-24 hours to appear

### Verification Commands
```bash
# Check bucket status
aws s3api head-bucket --bucket YOUR-HOSTING-BUCKET-1

# Check public access configuration
aws s3api get-public-access-block --bucket YOUR-HOSTING-BUCKET-1

# Check website configuration
aws s3api get-bucket-website --bucket YOUR-HOSTING-BUCKET-1

# Check logging configuration
aws s3api get-bucket-logging --bucket YOUR-HOSTING-BUCKET-1
```

## Policy Files Required

Make sure you have the following JSON policy files in the same directory:

- **host1-policy.json**: Public read policy for hosting bucket 1
- **host2-policy.json**: Public read policy for hosting bucket 2  
- **logging-policy.json**: S3 logging service permissions for logging bucket

Replace all placeholder values (YOUR-HOSTING-BUCKET-1, YOUR-HOSTING-BUCKET-2, YOUR-LOGGING-BUCKET) with your actual unique bucket names before running the commands.
