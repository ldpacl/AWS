# Secure AWS CLI IAM Setup Guide

## Prerequisites

1. **Install AWS CLI v2**
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

2. **Configure AWS CLI**
   ```bash
   aws configure
   ```

3. **Verify Configuration**
   ```bash
   aws sts get-caller-identity
   ```

## Step 1: Create IAM Groups

```bash
# Create groups with descriptive names
aws iam create-group --group-name RDSAccess
aws iam create-group --group-name EC2FullAccess
aws iam create-group --group-name S3FullAccess
```

## Step 2: Attach Policies to Groups

```bash
# Attach policies to groups (not users directly)
aws iam attach-group-policy \
    --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess \
    --group-name RDSAccess

aws iam attach-group-policy \
    --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess \
    --group-name EC2FullAccess

aws iam attach-group-policy \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
    --group-name S3FullAccess
```

## Step 3: Create Service Users (No Console Access)

```bash
# Create service users with tags
aws iam create-user \
    --user-name service-user-1 \
    --tags Key=Purpose,Value=ServiceAccount Key=Environment,Value=Development

aws iam create-user \
    --user-name service-user-2 \
    --tags Key=Purpose,Value=ServiceAccount Key=Environment,Value=Development
```

## Step 4: Create Access Keys for Programmatic Access

```bash
# Create access keys (store securely!)
aws iam create-access-key --user-name service-user-1
aws iam create-access-key --user-name service-user-2
```

## Step 5: Add Users to Groups

```bash
# Add users to appropriate groups
aws iam add-user-to-group --group-name RDSAccess --user-name service-user-1
aws iam add-user-to-group --group-name EC2FullAccess --user-name service-user-1
aws iam add-user-to-group --group-name S3FullAccess --user-name service-user-2
```

## Step 6: Create EC2 Service Role

```bash
# Create trust policy file
cat > trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

# Create role with tags
aws iam create-role \
    --role-name EC2S3ReadOnlyRole \
    --assume-role-policy-document file://trust-policy.json \
    --tags Key=Purpose,Value=EC2ServiceRole Key=Environment,Value=Development

# Attach policy to role
aws iam attach-role-policy \
    --role-name EC2S3ReadOnlyRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile
aws iam create-instance-profile --instance-profile-name EC2S3ReadOnlyProfile
aws iam add-role-to-instance-profile \
    --instance-profile-name EC2S3ReadOnlyProfile \
    --role-name EC2S3ReadOnlyRole

# Clean up
rm trust-policy.json
```

## Verification Commands

```bash
# List service users
aws iam list-users --query 'Users[?contains(Tags[?Key==`Purpose`].Value, `ServiceAccount`)].UserName'

# List groups and their policies
aws iam list-groups
aws iam list-attached-group-policies --group-name RDSAccess

# Check user group memberships
aws iam get-groups-for-user --user-name service-user-1

# List roles
aws iam list-roles --query 'Roles[?RoleName==`EC2S3ReadOnlyRole`].RoleName'
```

## Cleanup Commands

```bash
# Remove users from groups
aws iam remove-user-from-group --group-name RDSAccess --user-name service-user-1
aws iam remove-user-from-group --group-name EC2FullAccess --user-name service-user-1
aws iam remove-user-from-group --group-name S3FullAccess --user-name service-user-2

# Delete access keys (list first to get key IDs)
aws iam list-access-keys --user-name service-user-1
aws iam delete-access-key --user-name service-user-1 --access-key-id <ACCESS_KEY_ID>
aws iam list-access-keys --user-name service-user-2
aws iam delete-access-key --user-name service-user-2 --access-key-id <ACCESS_KEY_ID>

# Delete users
aws iam delete-user --user-name service-user-1
aws iam delete-user --user-name service-user-2

# Detach policies and delete groups
aws iam detach-group-policy --group-name RDSAccess --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess
aws iam detach-group-policy --group-name EC2FullAccess --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
aws iam detach-group-policy --group-name S3FullAccess --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam delete-group --group-name RDSAccess
aws iam delete-group --group-name EC2FullAccess
aws iam delete-group --group-name S3FullAccess

# Clean up role and instance profile
aws iam remove-role-from-instance-profile --instance-profile-name EC2S3ReadOnlyProfile --role-name EC2S3ReadOnlyRole
aws iam delete-instance-profile --instance-profile-name EC2S3ReadOnlyProfile
aws iam detach-role-policy --role-name EC2S3ReadOnlyRole --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam delete-role --role-name EC2S3ReadOnlyRole
```

## Security Best Practices

✅ **What This Guide Does Right:**
- Creates service accounts (no console access)
- Uses group-based permissions
- Applies resource tagging
- Provides proper cleanup procedures

❌ **Avoid These Common Mistakes:**
- Creating login profiles for service accounts
- Attaching policies directly to users
- Using hardcoded passwords
- Skipping resource cleanup
