# AWS CLI IAM Setup Guide

## Prerequisites

1. **Install AWS CLI**
   ```bash
   # For Linux/macOS
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   
   # For Windows
   # Download and run: https://awscli.amazonaws.com/AWSCLIV2.msi
   ```

2. **Configure AWS CLI**
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Enter your default region (e.g., us-east-1)
   # Enter output format (json)
   ```

3. **Verify Configuration**
   ```bash
   aws sts get-caller-identity
   ```

## Step 1: Create IAM Users

Create two users for the e-commerce platform team:

```bash
# Create Database Administrator user
aws iam create-user --user-name sarah-db-admin

# Create DevOps Engineer user
aws iam create-user --user-name mike-devops
```

## Step 2: Set User Passwords

1. **Generate login profile template:**
   ```bash
   aws iam create-login-profile --generate-cli-skeleton > create-login-profile.json
   ```

2. **Edit the JSON file:**
   ```json
   {
       "UserName": "sarah-db-admin",
       "Password": "TempPassword123!",
       "PasswordResetRequired": true
   }
   ```

3. **Create login profiles:**
   ```bash
   # For Database Administrator
   aws iam create-login-profile --cli-input-json file://create-login-profile.json
   
   # Update JSON file for DevOps user and run again
   aws iam create-login-profile --cli-input-json file://create-login-profile.json
   ```

## Step 3: Create IAM Groups

```bash
# Create groups for different access levels
aws iam create-group --group-name EC2FullAccess
aws iam create-group --group-name S3FullAccess
```

## Step 4: Attach Policies to Groups

```bash
# Attach EC2 full access to group
aws iam attach-group-policy \
    --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess \
    --group-name EC2FullAccess

# Attach S3 full access to group
aws iam attach-group-policy \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
    --group-name S3FullAccess
```

## Step 5: Assign Direct User Permissions

```bash
# Give Database Administrator direct RDS access
aws iam attach-user-policy \
    --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess \
    --user-name sarah-db-admin
```

## Step 6: Add Users to Groups

```bash
# Add Database Administrator to EC2 group (for connectivity troubleshooting)
aws iam add-user-to-group --group-name EC2FullAccess --user-name sarah-db-admin

# Add DevOps Engineer to S3 group
aws iam add-user-to-group --group-name S3FullAccess --user-name mike-devops
```

## Step 7: Create EC2 Service Role

1. **Create trust policy file:**
   ```bash
   cat > trust-policy.json << EOF
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": "ec2.amazonaws.com"
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }
   EOF
   ```

2. **Create the role:**
   ```bash
   aws iam create-role \
       --role-name EC2-S3-ReadOnly-Role \
       --assume-role-policy-document file://trust-policy.json
   ```

3. **Attach S3 read-only policy:**
   ```bash
   aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
       --role-name EC2-S3-ReadOnly-Role
   ```

## Verification Commands

```bash
# List all users
aws iam list-users

# List all groups
aws iam list-groups

# List all roles
aws iam list-roles

# Check user's attached policies
aws iam list-attached-user-policies --user-name sarah-db-admin

# Check group memberships
aws iam get-groups-for-user --user-name sarah-db-admin
```

## Cleanup (Optional)

```bash
# Detach policies and delete resources
aws iam detach-user-policy --user-name sarah-db-admin --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess
aws iam remove-user-from-group --group-name EC2FullAccess --user-name sarah-db-admin
aws iam delete-login-profile --user-name sarah-db-admin
aws iam delete-user --user-name sarah-db-admin

# Repeat for other resources...
```
