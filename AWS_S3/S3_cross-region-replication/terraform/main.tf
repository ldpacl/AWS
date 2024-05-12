provider "aws" {
    region = var.region-1
}

# creating an alias because we have to create the destination bucket in a different region
provider "aws" {
  alias = "region-2"
  region = var.region-2
}

# creating a role for replication which will be assumed by the source bucket
resource "aws_iam_role" "replication-role" {
    name = "replication-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                    Service = "s3.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })
}

# This policy will read the source bucket and write to the destination bucket
resource "aws_iam_policy" "replication-policy" {
  name = "replication-policy"
  description = "replication-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging",
        ]
        Resource = [
          "${aws_s3_bucket.source-bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetReplicationConfiguration"
        ]
        Resource = aws_s3_bucket.source-bucket.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ]
        Resource = [
          "${aws_s3_bucket.destination-bucket.arn}/*"
        ]
      }
    ]
  })
}

# Attaching the policy to the role
resource "aws_iam_role_policy_attachment" "replication-policy-attachment" {
  policy_arn = aws_iam_policy.replication-policy.arn
  role = aws_iam_role.replication-role.name
}

resource "aws_s3_bucket" "destination-bucket" {
  bucket = var.destination-bucket
}

# enabling versioning in both the buckets is mandatory for replication
resource "aws_s3_bucket_versioning" "destination" {
  bucket = aws_s3_bucket.destination-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# creating the source bucket in another region
resource "aws_s3_bucket" "source-bucket" {
  bucket = var.source-bucket
  provider = aws.region-2
}

# use alias whenever you want to create a resource in a different region
resource "aws_s3_bucket_versioning" "source" {
  bucket = aws_s3_bucket.source-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
  provider = aws.region-2
}

# creating replication configuration
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.region-2
  depends_on = [ aws_s3_bucket_versioning.source, aws_s3_bucket_versioning.destination ]

  role = aws_iam_role.replication-role.arn
  bucket = aws_s3_bucket.source-bucket.id

  rule {
    id = "rule-1"
    status = "Enabled"
    destination {
        bucket = aws_s3_bucket.destination-bucket.arn
        storage_class = "STANDARD"
    }
  }
}