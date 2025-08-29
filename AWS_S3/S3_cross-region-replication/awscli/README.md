# S3 Cross-Region Replication - AWS CLI Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: S3 and IAM full access
- **Two AWS Regions**: Access to at least two different regions

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

### Step 1: Prepare Configuration Files

Update the JSON files with your specific values:

**replication_policy.json** - Replace bucket names:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObjectVersionForReplication",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectVersionTagging"
            ],
            "Resource": "arn:aws:s3:::YOUR-SOURCE-BUCKET/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetReplicationConfiguration"
            ],
            "Resource": "arn:aws:s3:::YOUR-SOURCE-BUCKET"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ReplicateObject",
                "s3:ReplicateDelete",
                "s3:ReplicateTags"
            ],
            "Resource": "arn:aws:s3:::YOUR-DESTINATION-BUCKET/*"
        }
    ]
}
```

**replication_configuration.json** - Replace ARNs:
```json
{
    "Role": "arn:aws:iam::YOUR-ACCOUNT-ID:role/replication-role",
    "Rules": [
        {
            "ID": "rule1",
            "Status": "Enabled",
            "Priority": 1,
            "Filter": {
                "Prefix": ""
            },
            "Destination": {
                "Bucket": "arn:aws:s3:::YOUR-DESTINATION-BUCKET",
                "StorageClass": "STANDARD"
            },
            "DeleteMarkerReplication": {
                "Status": "Disabled"
            }
        }
    ]
}
```

### Step 2: Create Source Bucket
```bash
aws s3api create-bucket --bucket YOUR-SOURCE-BUCKET --acl private
```

### Step 3: Enable Versioning for Source Bucket
```bash
aws s3api put-bucket-versioning --bucket YOUR-SOURCE-BUCKET --versioning-configuration Status=Enabled
```

### Step 4: Create Destination Bucket
```bash
aws s3api create-bucket --bucket YOUR-DESTINATION-BUCKET --acl private --create-bucket-configuration LocationConstraint=us-west-2
```

### Step 5: Enable Versioning for Destination Bucket
```bash
aws s3api put-bucket-versioning --bucket YOUR-DESTINATION-BUCKET --versioning-configuration Status=Enabled
```

### Step 6: Create Replication Policy
```bash
aws iam create-policy --policy-name replication-policy --policy-document file://replication_policy.json
```

### Step 7: Create Replication Role
```bash
aws iam create-role --role-name replication-role --assume-role-policy-document file://assume-role-policy.json
```

### Step 8: Attach Policy to Role
```bash
# Get your account ID first
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Attach the policy
aws iam attach-role-policy --role-name replication-role --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/replication-policy
```

### Step 9: Configure Replication
```bash
aws s3api put-bucket-replication --bucket YOUR-SOURCE-BUCKET --replication-configuration file://replication_configuration.json
```

## Testing Replication

### Upload Test File
```bash
echo "Test replication content" > test-file.txt
aws s3 cp test-file.txt s3://YOUR-SOURCE-BUCKET/
```

### Verify Replication
```bash
# Check source bucket
aws s3 ls s3://YOUR-SOURCE-BUCKET/

# Check destination bucket (wait 5-15 minutes)
aws s3 ls s3://YOUR-DESTINATION-BUCKET/
```

## Cleanup Steps

### Step 1: Remove Objects from Buckets
```bash
# Empty source bucket
aws s3 rm s3://YOUR-SOURCE-BUCKET --recursive

# Empty destination bucket  
aws s3 rm s3://YOUR-DESTINATION-BUCKET --recursive
```

### Step 2: Delete Bucket Replication Configuration
```bash
aws s3api delete-bucket-replication --bucket YOUR-SOURCE-BUCKET
```

### Step 3: Delete Buckets
```bash
aws s3api delete-bucket --bucket YOUR-SOURCE-BUCKET
aws s3api delete-bucket --bucket YOUR-DESTINATION-BUCKET
```

### Step 4: Detach Policy from Role
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws iam detach-role-policy --role-name replication-role --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/replication-policy
```

### Step 5: Delete IAM Role and Policy
```bash
aws iam delete-role --role-name replication-role
aws iam delete-policy --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/replication-policy
```

## Troubleshooting

### Common Issues
- **Permission Denied**: Ensure your AWS user has S3 and IAM permissions
- **Bucket Already Exists**: S3 bucket names must be globally unique
- **Replication Not Working**: Wait 15 minutes, check IAM role permissions

### Verification Commands
```bash
# Check replication status
aws s3api get-bucket-replication --bucket YOUR-SOURCE-BUCKET

# Check bucket versioning
aws s3api get-bucket-versioning --bucket YOUR-SOURCE-BUCKET

# List IAM roles
aws iam list-roles --query 'Roles[?RoleName==`replication-role`]'
```


Replace all placeholder values (YOUR-SOURCE-BUCKET, YOUR-DESTINATION-BUCKET, YOUR-ACCOUNT-ID) with your actual values before running the commands.