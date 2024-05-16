provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "host-bucket-1" {
  bucket = var.host-bucket-1
}

resource "aws_s3_bucket_ownership_controls" "example" {
  bucket = aws_s3_bucket.host-bucket-1.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.host-bucket-1.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


resource "aws_s3_bucket_policy" "host1-policy" {
  bucket = aws_s3_bucket.host-bucket-1.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.host-bucket-1.arn}/*"
      },
    ]
  })
}

resource "aws_s3_bucket_website_configuration" "example1" {
  bucket = aws_s3_bucket.host-bucket-1.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket" "host-bucket-2" {
  bucket = var.host-bucket-2
}

resource "aws_s3_bucket_ownership_controls" "example1" {
  bucket = aws_s3_bucket.host-bucket-2.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "example1" {
  bucket = aws_s3_bucket.host-bucket-2.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "host2-policy" {
  bucket = aws_s3_bucket.host-bucket-2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.host-bucket-2.arn}/*"
      },
    ]
  })
}

resource "aws_s3_bucket_website_configuration" "example2" {
  bucket = aws_s3_bucket.host-bucket-2.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "log-policy" {
  bucket = aws_s3_bucket.log-bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "S3ServerAccessLogsPolicyforhostingbucket-1"
        Effect    = "Allow"
        Principal = {
          Service = "logging.s3.amazonaws.com"
        },
        Action    = "s3:PutObject",
        Resource  = "${aws_s3_bucket.log-bucket.arn}/log/${aws_s3_bucket.host-bucket-1.id}/*"
        Condition = {
          ArnLike = {
            "aws:SourceArn" = aws_s3_bucket.host-bucket-1.arn
          },
          StringEquals = {
            "aws:SourceAccount" = var.account-id
          }
        }
      },
      {
        Sid = "S3ServerAccessLogsPolicyforhostingbucket-2"
        Effect = "Allow"
        Principal = {
          Service = "logging.s3.amazonaws.com"
        },
        Action = "s3:PutObject",
        Resource = "${aws_s3_bucket.log-bucket.arn}/log/${aws_s3_bucket.host-bucket-2.id}/*"
        Condition = {
          ArnLike = {
            "aws:SourceArn" = aws_s3_bucket.host-bucket-2.arn
          },
          StringEquals = {
            "aws:SourceAccount" = var.account-id
          }
        }
      }
    ]
  })
}

resource "aws_s3_bucket" "log-bucket" {
  bucket = var.log-bucket
}

resource "aws_s3_bucket_ownership_controls" "example2" {
  bucket = aws_s3_bucket.log-bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "example2" {
  bucket = aws_s3_bucket.log-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "logging1" {
  bucket = aws_s3_bucket.host-bucket-1.id

  target_bucket = aws_s3_bucket.log-bucket.id
  target_prefix = "log/${aws_s3_bucket.host-bucket-1.id}/"
}

resource "aws_s3_bucket_logging" "logging2" {
  bucket = aws_s3_bucket.host-bucket-2.id

  target_bucket = aws_s3_bucket.log-bucket.id
  target_prefix = "log/${aws_s3_bucket.host-bucket-2.id}/"
}