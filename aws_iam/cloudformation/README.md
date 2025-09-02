# Secure CloudFormation IAM Setup Guide

## Prerequisites

1. **AWS CLI v2 Installed**
   ```bash
   aws --version
   ```

2. **AWS CLI Configured**
   ```bash
   aws configure
   aws sts get-caller-identity
   ```

3. **Required Permissions**
   - IAM full access
   - CloudFormation full access

## Template Overview

The secure templates create:
- **3 IAM Groups**: RDSAccess, EC2FullAccess, S3FullAccess
- **2 Service Users**: No console access, programmatic only
- **1 IAM Role**: EC2S3ReadOnlyRole with instance profile
- **Access Keys**: For programmatic access

## Deployment via AWS CLI

### Using YAML Template (Recommended)

```bash
# Validate template
aws cloudformation validate-template --template-body file://iam-secure.yaml

# Deploy stack
aws cloudformation deploy \
    --template-file iam-secure.yaml \
    --stack-name iam-secure-stack \
    --parameter-overrides \
        User1Name=service-user-1 \
        User2Name=service-user-2 \
        Environment=Development \
    --capabilities CAPABILITY_NAMED_IAM \
    --tags \
        Purpose=Learning \
        Environment=Development
```

### Using JSON Template

```bash
# Deploy with JSON template
aws cloudformation deploy \
    --template-file iam-secure.json \
    --stack-name iam-secure-stack \
    --parameter-overrides \
        User1Name=service-user-1 \
        User2Name=service-user-2 \
        Environment=Development \
    --capabilities CAPABILITY_NAMED_IAM
```

## Deployment via AWS Console

### Step 1: Access CloudFormation Console
1. Sign in to AWS Management Console
2. Navigate to **CloudFormation** service
3. Click **"Create stack"** → **"With new resources (standard)"**

### Step 2: Upload Template
1. Select **"Upload a template file"**
2. Choose `iam-secure.yaml` or `iam-secure.json`
3. Click **"Next"**

### Step 3: Configure Stack
1. **Stack name**: `iam-secure-stack`
2. **Parameters**:
   - **User1Name**: `service-user-1`
   - **User2Name**: `service-user-2`
   - **Environment**: `Development`
3. Click **"Next"**

### Step 4: Configure Options
1. **Tags**:
   - Key: `Purpose`, Value: `Learning`
   - Key: `Environment`, Value: `Development`
2. Click **"Next"**

### Step 5: Review and Deploy
1. Check **"I acknowledge that AWS CloudFormation might create IAM resources with custom names"**
2. Click **"Submit"**

## Verification Commands

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name iam-secure-stack

# List stack outputs
aws cloudformation describe-stacks \
    --stack-name iam-secure-stack \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

# Verify IAM resources
aws iam list-users --query 'Users[?contains(Tags[?Key==`Purpose`].Value, `ServiceAccount`)].UserName'
aws iam list-groups --query 'Groups[?contains(GroupName, `Access`)].GroupName'
aws iam get-role --role-name EC2S3ReadOnlyRole
```

## Stack Updates

```bash
# Update stack with new parameters
aws cloudformation deploy \
    --template-file iam-secure.yaml \
    --stack-name iam-secure-stack \
    --parameter-overrides \
        User1Name=new-service-user-1 \
        User2Name=new-service-user-2 \
        Environment=Staging \
    --capabilities CAPABILITY_NAMED_IAM
```

## Cleanup Commands

```bash
# Delete stack
aws cloudformation delete-stack --stack-name iam-secure-stack

# Wait for deletion to complete
aws cloudformation wait stack-delete-complete --stack-name iam-secure-stack

# Verify deletion
aws cloudformation describe-stacks --stack-name iam-secure-stack
```

## Template Features

### Security Best Practices
- **No Console Access**: Service users for programmatic access only
- **Group-Based Permissions**: Policies attached to groups, not users
- **Resource Tagging**: Comprehensive tagging strategy
- **Secure Outputs**: Secret keys marked with `NoEcho: true`

### Template Structure
- **Parameters**: User names and environment with validation
- **Resources**: Groups, users, role, and instance profile
- **Outputs**: ARNs, access keys, and resource names

## Troubleshooting

### Common Issues

1. **Template Validation Error**
   ```bash
   aws cloudformation validate-template --template-body file://iam-secure.yaml
   ```

2. **Insufficient Permissions**
   - Ensure IAM and CloudFormation permissions
   - Use `--capabilities CAPABILITY_NAMED_IAM`

3. **Stack Already Exists**
   ```bash
   aws cloudformation delete-stack --stack-name iam-secure-stack
   ```

4. **Parameter Validation**
   - User names must match pattern: `^[a-zA-Z0-9+=,.@_-]+$`
   - Environment must be: Development, Staging, or Production

## Security Benefits

✅ **What This Template Does Right:**
- Creates service accounts (no console access)
- Uses group-based permissions
- Applies comprehensive tagging
- Provides secure outputs
- Includes instance profile for EC2

❌ **Avoids Common Mistakes:**
- No login profiles or passwords
- No direct policy attachments to users
- No hardcoded values
- Proper resource dependencies
