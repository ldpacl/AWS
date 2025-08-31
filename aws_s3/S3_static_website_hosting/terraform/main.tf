provider "aws" {
  region = var.region
}

# Creating bucket
resource "aws_s3_bucket" "host-bucket" {
  bucket = var.host-bucket
}

# Enforcing object ownership controls
resource "aws_s3_bucket_ownership_controls" "ownership" {
  bucket = aws_s3_bucket.host-bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Allowing public access to bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.host-bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Adding index file to the bucket
resource "aws_s3_object" "index_file" {
  bucket = aws_s3_bucket.host-bucket.id
  key    = "index.html"
  source = "${path.module}/index.html"
  content_type = "text/html"
}

# Setting website configuration for the bucket
resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.host-bucket.id

  index_document {
    suffix = "index.html"
  }
}

# Bucket policy for static website hosting
resource "aws_s3_bucket_policy" "host-bucket-policy" {
  bucket = aws_s3_bucket.host-bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.host-bucket.arn}/*"
      }
    ]
  })
}

# This gives you the URL to access
output "s3-url" {
  value = aws_s3_bucket_website_configuration.website.website_endpoint
}