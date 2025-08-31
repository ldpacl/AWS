# CloudFormation IAM Setup Guide

## Prerequisites

1. **AWS Account**
   - Active AWS account with billing enabled
   - Root user or IAM user with administrative permissions

2. **Required Permissions**
   - IAM full access (to create users, groups, roles, and policies)
   - CloudFormation full access (to create and manage stacks)

3. **Browser Requirements**
   - Modern web browser (Chrome, Firefox, Safari, Edge)


4. **Verify Access**
   - Sign in to AWS Management Console
   - Navigate to CloudFormation service to confirm access
   - Navigate to IAM service to confirm permissions

## Template Overview

The `cft.json` template creates:
- **2 IAM Users**: Database Administrator and DevOps Engineer
- **2 IAM Groups**: S3FullAccess and EC2FullAccess with respective policies
- **1 IAM Role**: EC2 service role with S3 read-only access
- **User Assignments**: Users automatically added to appropriate groups

## Deployment via AWS Console

### Step 1: Access CloudFormation Console
1. Sign in to AWS Management Console
2. Navigate to **CloudFormation** service
3. Click **"Create stack"** → **"With new resources (standard)"**

### Step 2: Upload Template
1. Select **"Upload a template file"**
2. Click **"Choose file"** and select `cft.json`
3. Click **"Next"**

### Step 3: Configure Stack
1. **Stack name**: `ecommerce-iam-stack`
2. **Parameters**:
   - **User1Name**: `sarah-db-admin`
   - **User1Password**: `TempPassword123!`
   - **User2Name**: `mike-devops`
   - **User2Password**: `TempPassword456!`
3. Click **"Next"**

### Step 4: Configure Stack Options
1. **Tags** (optional):
   - Key: `Project`, Value: `E-Commerce-Platform`
   - Key: `Environment`, Value: `Development`
2. **Permissions**: Leave default (use current role)
3. Click **"Next"**

### Step 5: Review and Deploy
1. Review all configurations
2. **Capabilities**: Check **"I acknowledge that AWS CloudFormation might create IAM resources"**
3. Click **"Submit"**

### Step 6: Monitor Deployment
1. Watch the **Events** tab for real-time progress
2. Stack status will change from `CREATE_IN_PROGRESS` to `CREATE_COMPLETE`
3. Check **Resources** tab to see created IAM components

## Stack Verification via Console

1. **Check Stack Status**:
   - In CloudFormation console, verify stack shows `CREATE_COMPLETE`
   - Review **Resources** tab to see all created components

2. **Verify IAM Resources**:
   - Navigate to **IAM** service
   - Check **Users**: `sarah-db-admin` and `mike-devops` should exist
   - Check **Groups**: `s3fullaccess` and `ec2fullaccess` should exist
   - Check **Roles**: Service role should be created

3. **Test User Access**:
   - Sign out and sign in as `sarah-db-admin`
   - Verify access to RDS and EC2 services
   - Repeat for `mike-devops` with S3 access

## Template Structure

### Parameters
- **User1Name**: Database Administrator username
- **User1Password**: Database Administrator password
- **User2Name**: DevOps Engineer username  
- **User2Password**: DevOps Engineer password

### Resources Created
- **UserGroup1**: S3FullAccess group with AmazonS3FullAccess policy
- **UserGroup2**: EC2FullAccess group with AmazonEC2FullAccess policy
- **User1**: Database Administrator with RDS full access + EC2 group membership
- **User2**: DevOps Engineer with S3 group membership
- **Role1**: EC2 service role with S3 read-only access

## Stack Updates via Console

To modify user passwords or stack configuration:

1. Navigate to **CloudFormation** console
2. Select `ecommerce-iam-stack`
3. Click **"Update"** → **"Use current template"**
4. Modify parameters as needed
5. Click **"Next"** through configuration pages
6. Check **"I acknowledge that AWS CloudFormation might create IAM resources"**
7. Click **"Submit"**

## Troubleshooting

### Common Issues

1. **Insufficient Permissions**
   - Error: "User is not authorized to perform iam:CreateUser"
   - Solution: Ensure your AWS user has IAM admin permissions

2. **Stack Already Exists**
   - Error: "Stack already exists"
   - Solution: Delete existing stack first via console

3. **Parameter Validation**
   - Ensure passwords meet AWS requirements (8+ characters, complexity)

4. **IAM Capability Missing**
   - Error: "Requires capabilities: [CAPABILITY_IAM]"
   - Solution: Check the acknowledgment box in Step 5

## Stack Cleanup via Console

1. Navigate to **CloudFormation** console
2. Select `ecommerce-iam-stack`
3. Click **"Delete"**
4. Confirm deletion by clicking **"Delete stack"**
5. Monitor deletion progress in **Events** tab
6. Stack will be removed from list when deletion completes
