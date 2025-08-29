# AWS S3 Projects 🪣

This folder contains practical S3 implementations covering essential use cases and configurations.

## 📁 Project Folders

### S3_cross-region-replication
Implements S3 Cross-Region Replication (CRR) to automatically replicate objects across different AWS regions for disaster recovery and compliance.

**Implementation approaches:**
- `awscli/` - Command-line setup and configuration
- `python/` - Boto3 automation scripts
- `cloudformation/` - Infrastructure as Code templates
- `terraform/` - Multi-cloud infrastructure provisioning

### S3_server-access-logging
Configures S3 server access logging to track requests made to your S3 buckets for security monitoring and analytics.

**Implementation approaches:**
- `awscli/` - CLI-based logging configuration
- `python/` - Programmatic logging setup
- `cloudformation/` - Template-based deployment
- `terraform/` - Infrastructure automation

### S3_static_website_hosting
Sets up S3 static website hosting to serve web content directly from S3 buckets with custom domain support.

**Implementation approaches:**
- `python/` - Automated website deployment
- `cloudformation/` - Complete hosting infrastructure
- `terraform/` - End-to-end website provisioning

## 🚀 Getting Started

1. Choose a project folder based on your use case
2. Select your preferred implementation approach
3. Follow the README in each subfolder for detailed instructions
4. Ensure you have appropriate AWS permissions for S3 operations

Each project includes working examples, prerequisites, and troubleshooting guides.
