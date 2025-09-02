provider "aws" {
  region = var.region
}

# Service users for programmatic access only (no console access)
resource "aws_iam_user" "user1" {
  name = var.user-1
  tags = {
    Purpose = "Service Account"
  }
}

resource "aws_iam_user" "user2" {
  name = var.user-2
  tags = {
    Purpose = "Service Account"
  }
}

resource "aws_iam_access_key" "user1_access_key" {
  user = aws_iam_user.user1.name
}

resource "aws_iam_access_key" "user2_access_key" {
  user = aws_iam_user.user2.name
}

# Groups for better access management
resource "aws_iam_group" "rds_group" {
  name = "RDSAccess"
}

resource "aws_iam_group" "ec2_group" {
  name = "EC2FullAccess"
}

resource "aws_iam_group" "s3_group" {
  name = "S3FullAccess"
}

# Attach policies to groups (not directly to users)
resource "aws_iam_group_policy_attachment" "rds_group_policy" {
  group      = aws_iam_group.rds_group.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}

resource "aws_iam_group_policy_attachment" "ec2_group_policy" {
  group      = aws_iam_group.ec2_group.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_group_policy_attachment" "s3_group_policy" {
  group      = aws_iam_group.s3_group.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Add users to groups
resource "aws_iam_user_group_membership" "user1_groups" {
  user = aws_iam_user.user1.name
  groups = [
    aws_iam_group.rds_group.name,
    aws_iam_group.ec2_group.name
  ]
}

resource "aws_iam_user_group_membership" "user2_groups" {
  user = aws_iam_user.user2.name
  groups = [
    aws_iam_group.s3_group.name
  ]
}

# IAM Role for EC2 instances
resource "aws_iam_role" "ec2_role" {
  name = "EC2S3ReadOnlyRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  
  tags = {
    Purpose = "EC2 Service Role"
  }
}

resource "aws_iam_role_policy_attachment" "ec2_role_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2S3ReadOnlyProfile"
  role = aws_iam_role.ec2_role.name
}
