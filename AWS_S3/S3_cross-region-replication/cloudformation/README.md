# S3 Cross-Region Replication - CloudFormation Console Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: CloudFormation, S3, and IAM full access
- **Two AWS Regions**: Access to at least two different regions
- **Web Browser**: Modern browser for AWS Console access

### Template Files
- `s3_crr2.json` - Creates destination bucket
- `s3_crr.json` - Creates source bucket with replication

## CloudFormation Templates Overview

### 1. s3_crr2.json
- **Purpose**: Creates the destination bucket in the secondary region
- **Resources**: S3 bucket with versioning enabled
- **Parameters**: DestinationBucket name

### 2. s3_crr.json  
- **Purpose**: Creates source bucket, IAM role, and replication configuration
- **Resources**: S3 bucket, IAM role with policies, replication rules
- **Parameters**: SourceBucket name

## Pre-Deployment Template Updates

### Step 1: Update s3_crr.json Template

Before deploying, update the hardcoded destination bucket name in `s3_crr.json`:

**Find and replace these lines:**
```json
"Resource": [
    "arn:aws:s3:::destinationbucket/*"
]
```
**Replace with:**
```json
"Resource": [
    "arn:aws:s3:::YOUR-DESTINATION-BUCKET/*"
]
```

**And:**
```json
"Destination": {
    "Bucket": "arn:aws:s3:::destinationbucket",
    "StorageClass": "STANDARD"
}
```
**Replace with:**
```json
"Destination": {
    "Bucket": "arn:aws:s3:::YOUR-DESTINATION-BUCKET",
    "StorageClass": "STANDARD"
}
```

## Implementation Steps via AWS Console

### Step 1: Deploy Destination Bucket Stack (Secondary Region)

1. **Open AWS Console** and navigate to **CloudFormation**
2. **Switch to your destination region** (e.g., US West 2)
3. Click **Create stack** → **With new resources (standard)**
4. **Upload template file**: Select `s3_crr2.json`
5. Click **Next**

**Stack Details:**
- **Stack name**: `s3-crr-destination`
- **DestinationBucket**: Enter unique bucket name (e.g., `my-dest-bucket-20240829`)
- Click **Next**

**Configure Stack Options:**
- Leave defaults or add tags as needed
- Click **Next**

**Review:**
- Review all settings
- Click **Create stack**

**Wait for Completion:**
- Monitor stack status until it shows **CREATE_COMPLETE**
- Note down the destination bucket name for next step

### Step 2: Deploy Source Bucket Stack (Primary Region)

1. **Switch to your source region** (e.g., US East 1)
2. Click **Create stack** → **With new resources (standard)**
3. **Upload template file**: Select the updated `s3_crr.json`
4. Click **Next**

**Stack Details:**
- **Stack name**: `s3-crr-source`
- **SourceBucket**: Enter unique bucket name (e.g., `my-source-bucket-20240829`)
- Click **Next**

**Configure Stack Options:**
- Leave defaults or add tags as needed
- Click **Next**

**Review:**
- **Important**: Check **"I acknowledge that AWS CloudFormation might create IAM resources"**
- Click **Create stack**

**Wait for Completion:**
- Monitor stack status until it shows **CREATE_COMPLETE**
- This may take 5-10 minutes due to IAM resource creation

## Testing Replication via Console

### Step 1: Upload Test File to Source Bucket

1. Navigate to **S3** service in the source region
2. Click on your source bucket
3. Click **Upload**
4. **Add files**: Select or drag a test file
5. Click **Upload**

### Step 2: Verify Replication in Destination Bucket

1. **Switch to destination region** in AWS Console
2. Navigate to **S3** service
3. Click on your destination bucket
4. **Wait 5-15 minutes** for replication to complete
5. **Refresh** the bucket contents
6. Verify the test file appears in the destination bucket

## Monitoring Stacks via Console

### Check Stack Status
1. Navigate to **CloudFormation** in each region
2. Click on stack name to view details
3. Check **Events** tab for deployment progress
4. Check **Resources** tab to see created resources
5. Check **Outputs** tab for any exported values

### Monitor Replication
1. Navigate to **S3** in source region
2. Click on source bucket
3. Go to **Management** tab
4. Click **Replication** to view replication rules
5. Check replication metrics and status

## Cleanup Steps via Console

### Step 1: Empty S3 Buckets

**Source Bucket:**
1. Navigate to **S3** in source region
2. Select your source bucket
3. Click **Empty**
4. Type bucket name to confirm
5. Click **Empty**

**Destination Bucket:**
1. Navigate to **S3** in destination region
2. Select your destination bucket
3. Click **Empty**
4. Type bucket name to confirm
5. Click **Empty**

### Step 2: Delete CloudFormation Stacks

**Delete Source Stack First:**
1. Navigate to **CloudFormation** in source region
2. Select `s3-crr-source` stack
3. Click **Delete**
4. Click **Delete stack** to confirm
5. Wait for **DELETE_COMPLETE** status

**Delete Destination Stack:**
1. Navigate to **CloudFormation** in destination region
2. Select `s3-crr-destination` stack
3. Click **Delete**
4. Click **Delete stack** to confirm
5. Wait for **DELETE_COMPLETE** status

## Troubleshooting via Console

### Stack Creation Failed
1. Navigate to **CloudFormation**
2. Click on failed stack name
3. Check **Events** tab for error details
4. Look for red error messages
5. Common issues:
   - Bucket name already exists (use unique names)
   - Insufficient IAM permissions
   - Template syntax errors

### Replication Not Working
1. **Check IAM Role**: Navigate to **IAM** → **Roles** → Search for replication role
2. **Verify Permissions**: Check attached policies
3. **Check Bucket Versioning**: Both buckets must have versioning enabled
4. **Wait Time**: Replication can take up to 15 minutes
5. **Check Replication Rules**: S3 → Bucket → Management → Replication

### Template Validation
1. In CloudFormation **Create stack** wizard
2. After uploading template, check for validation errors
3. Fix any JSON syntax issues before proceeding


## Best Practices
- **Unique Naming**: Always use unique bucket names with timestamps
- **Region Planning**: Choose regions based on compliance and latency requirements


Remember to replace `YOUR-DESTINATION-BUCKET` in the template with your actual destination bucket name before deployment.
