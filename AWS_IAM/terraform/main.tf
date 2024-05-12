provider "aws" {
  region = var.region
}

resource "aws_iam_user" "user1" {
  name = var.user-1
}

resource "aws_iam_user" "user2" {
  name = var.user-2
}

resource "aws_iam_access_key" "user1_access_key" {
  user = aws_iam_user.user1.name
}

resource "aws_iam_access_key" "user2_access_key" {
  user = aws_iam_user.user2.name
}   

resource "aws_iam_user_login_profile" "user1_login_profile" {
  user = aws_iam_user.user1.name
  password_reset_required = true
}

resource "aws_iam_user_login_profile" "user2_login_profile" {
  user = aws_iam_user.user2.name
  password_reset_required = true
}

resource "aws_iam_user_policy_attachment" "user1_policy" {
  user = aws_iam_user.user1.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}

resource "aws_iam_group" "group1" {
    name = "EC2FullAccess"
}

resource "aws_iam_group" "group2" {
    name = "S3FullAccess"
}

resource "aws_iam_group_policy_attachment" "group1_policy" {
    group = aws_iam_group.group1.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_group_policy_attachment" "group2_policy" {
    group = aws_iam_group.group2.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_user_group_membership" "user1_group" {
    user = aws_iam_user.user1.name
    groups = [aws_iam_group.group1.name]
}

resource "aws_iam_user_group_membership" "user2_group" {
    user = aws_iam_user.user2.name
    groups = [aws_iam_group.group2.name]
}

resource "aws_iam_role" "role1" {
    name = "role1"
    assume_role_policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Principal = {
            Service = "ec2.amazonaws.com"
          }
          Action = "sts:AssumeRole"
        },
      ]
    })
}

resource "aws_iam_role_policy_attachment" "role1_policy" {
    role = aws_iam_role.role1.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}