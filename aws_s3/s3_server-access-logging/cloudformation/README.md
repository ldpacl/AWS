# S3 Server Access Logging - CloudFormation Console Implementation

## Prerequisites

### AWS Requirements
- **AWS Account** with administrative access
- **IAM Permissions**: CloudFormation and S3 full access
- **Web Browser**: Modern browser for AWS Console access

### Template Files
- `s3-sal.json` - Creates hosting buckets, logging bucket, and server access logging configuration

## CloudFormation Template Overview

### s3-sal.json
- **Purpose**: Creates complete S3 server access logging infrastructure
- **Resources**: 
  - Two public hosting buckets with static website hosting
  - One private logging bucket
  - Bucket policies for public access and logging permissions
  - Server access logging configuration
- **Parameters**: 
  - HostingBucket1Name
  - HostingBucket2Name  
  - LogBucketName

## Pre-Deployment Template Updates

### Step 1: Review Template Parameters

The template uses parameters for bucket names, but you may want to review the hardcoded account references in the logging policy. Ensure the template matches your requirements.

**Key Template Sections:**
- **Hosting Buckets**: Configured for static website hosting with public access
- **Logging Bucket**: Private bucket with S3 logging service permissions
- **Bucket Policies**: Public read access for hosting, logging permissions for log bucket

## Implementation Steps via AWS Console

### Step 1: Deploy S3 Server Access Logging Stack

1. **Open AWS Console** and navigate to **CloudFormation**
2. **Select your desired region** (e.g., US East 1)
3. Click **Create stack** → **With new resources (standard)**
4. **Upload template file**: Select `s3-sal.json`
5. Click **Next**

**Stack Details:**
- **Stack name**: `s3-server-access-logging`
- **HostingBucket1Name**: Enter unique bucket name (e.g., `my-hosting-store-a-20240902`)
- **HostingBucket2Name**: Enter unique bucket name (e.g., `my-hosting-store-b-20240902`)
- **LogBucketName**: Enter unique bucket name (e.g., `my-logging-bucket-20240902`)
- Click **Next**

**Configure Stack Options:**
- **Tags** (Optional): Add tags like `Environment: Demo`, `Project: S3Logging`
- **Permissions**: Leave default or specify IAM role if required
- **Stack failure options**: Leave default
- Click **Next**

**Review:**
- Review all settings and parameters
- **Important**: Check **"I acknowledge that AWS CloudFormation might create IAM resources"**
- Click **Create stack**

**Wait for Completion:**
- Monitor stack status until it shows **CREATE_COMPLETE**
- This typically takes 2-5 minutes

## Testing the Setup via Console

### Step 1: Upload Test Content to Hosting Buckets

**Upload to Hosting Bucket 1:**
1. Navigate to **S3** service
2. Click on your first hosting bucket
3. Click **Upload**
4. Create a simple `index.html` file:
   ```html
   <html><body><h1>Welcome to Store A</h1></body></html>
   ```
5. Upload the file
6. Click **Upload**

**Upload to Hosting Bucket 2:**
1. Click on your second hosting bucket
2. Click **Upload**
3. Create another `index.html` file:
   ```html
   <html><body><h1>Welcome to Store B</h1></body></html>
   ```
4. Upload the file

### Step 2: Access Websites to Generate Logs

**Get Website Endpoints:**
1. Click on first hosting bucket
2. Go to **Properties** tab
3. Scroll to **Static website hosting**
4. Note the **Bucket website endpoint**
5. Repeat for second hosting bucket

**Access Websites:**
- Open the website endpoints in your browser
- Refresh pages multiple times to generate access logs
- Try accessing non-existent pages to generate 404 logs

### Step 3: Verify Logging Configuration

**Check Logging Settings:**
1. Click on first hosting bucket
2. Go to **Properties** tab
3. Scroll to **Server access logging**
4. Verify target bucket and prefix are configured
5. Repeat for second hosting bucket

**Check for Log Files:**
1. Navigate to your logging bucket
2. Look for folders: `logs/YOUR-HOSTING-BUCKET-1/` and `logs/YOUR-HOSTING-BUCKET-2/`
3. **Note**: Log files may take 2-24 hours to appear

## Monitoring Stack via Console

### Check Stack Status
1. Navigate to **CloudFormation**
2. Click on `s3-server-access-logging` stack
3. **Events** tab: View deployment progress and any issues
4. **Resources** tab: See all created S3 buckets and policies
5. **Parameters** tab: Review input parameters
6. **Outputs** tab: View any exported values (if configured)

### Monitor S3 Resources
1. Navigate to **S3** service
2. Verify all three buckets are created
3. Check bucket properties and policies
4. Monitor log file generation in logging bucket

## Cleanup Steps via Console

### Step 1: Empty All S3 Buckets

**Empty Hosting Buckets:**
1. Navigate to **S3**
2. Select first hosting bucket
3. Click **Empty**
4. Type bucket name to confirm
5. Click **Empty**
6. Repeat for second hosting bucket

**Empty Logging Bucket:**
1. Select logging bucket
2. Click **Empty**
3. Type bucket name to confirm
4. Click **Empty**
5. **Note**: This removes all access logs

### Step 2: Delete CloudFormation Stack

1. Navigate to **CloudFormation**
2. Select `s3-server-access-logging` stack
3. Click **Delete**
4. Click **Delete stack** to confirm
5. Wait for **DELETE_COMPLETE** status
6. **Monitor Events** tab for deletion progress

## Troubleshooting via Console

### Stack Creation Failed

**Check Events Tab:**
1. Navigate to **CloudFormation**
2. Click on failed stack name
3. Check **Events** tab for error details
4. Look for red error messages

**Common Issues:**
- **Bucket name already exists**: S3 bucket names must be globally unique
- **Insufficient permissions**: Ensure your user has S3 and CloudFormation permissions
- **Template syntax errors**: Validate JSON syntax

### Logging Not Working

**Verify Configuration:**
1. **Check Bucket Policies**: Navigate to S3 → Bucket → Permissions → Bucket policy
2. **Check Logging Settings**: S3 → Bucket → Properties → Server access logging
3. **Wait Time**: Server access logs can take 2-24 hours to appear
4. **Generate Traffic**: Access the websites multiple times

**Debug Steps:**
1. **Check CloudTrail**: For API-level logging and troubleshooting
2. **Review IAM Permissions**: Ensure S3 logging service has proper permissions
3. **Validate Bucket Policies**: Check JSON syntax and ARN formats

### Template Validation

**Before Deployment:**
1. In CloudFormation **Create stack** wizard
2. After uploading template, check for validation errors
3. Fix any JSON syntax issues before proceeding
4. Verify parameter names match template requirements

## Best Practices

### Naming Conventions
- **Use Timestamps**: Include date/time in bucket names for uniqueness
- **Descriptive Names**: Use clear, descriptive bucket names
- **Environment Tags**: Tag resources with environment (dev, staging, prod)

### Security Considerations
- **Review Policies**: Ensure bucket policies follow least privilege principle
- **Monitor Access**: Regularly review access logs for suspicious activity
- **Log Retention**: Implement lifecycle policies for log retention

### Cost Optimization
- **Log Lifecycle**: Set up lifecycle rules to transition old logs to cheaper storage classes
- **Monitor Usage**: Track storage costs for logging bucket

## Template Customization

To modify the template for your specific needs:
1. **Download** the template from the CloudFormation console
2. **Edit** JSON file with your preferred text editor
3. **Modify** bucket policies, logging prefixes, or add additional resources
4. **Re-upload** the modified template

Remember to use globally unique bucket names when deploying the stack.
