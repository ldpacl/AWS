output "user1_arn" {
  description = "ARN of user1"
  value       = aws_iam_user.user1.arn
}

output "user2_arn" {
  description = "ARN of user2"
  value       = aws_iam_user.user2.arn
}

output "user1_access_key_id" {
  description = "Access key ID for user1"
  value       = aws_iam_access_key.user1_access_key.id
}

output "user2_access_key_id" {
  description = "Access key ID for user2"
  value       = aws_iam_access_key.user2_access_key.id
}

output "user1_secret_access_key" {
  description = "Secret access key for user1"
  value       = aws_iam_access_key.user1_access_key.secret
  sensitive   = true
}

output "user2_secret_access_key" {
  description = "Secret access key for user2"
  value       = aws_iam_access_key.user2_access_key.secret
  sensitive   = true
}

output "ec2_instance_profile_name" {
  description = "Name of the EC2 instance profile"
  value       = aws_iam_instance_profile.ec2_profile.name
}

output "groups_created" {
  description = "List of IAM groups created"
  value = [
    aws_iam_group.rds_group.name,
    aws_iam_group.ec2_group.name,
    aws_iam_group.s3_group.name
  ]
}
