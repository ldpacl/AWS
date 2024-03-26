AWS IAM project using AWS CLI

Create a new user using the command: aws iam create-user --user-name name1
Use this command to generate a json file for the cli skeleton: aws iam create-login-profile --generate-cli-skeleton > create-login-profile.json
This is what the json file had:
{
	“Username”: “name”,
	“Password”: “password”,
	“PasswordResetRequired”: false
}
Set the password by using the command: aws iam create-login-profile --cli-input-json file://create-login-profile.json
You can also update the password by: aws iam update-login-profile --user-name name1 --password $newpassword
Do the same to another user “name2”

Create 2 user groups called “s3fullaccess” and “ec2fullaccess” by: 
aws iam create-group --group-name s3fullaccess
aws iam create-group --group-name ec2fullaccess

Attach policies to user groups by copying the arn of the policy:
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name s3fullaccess
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2fullaccess --group-name ec2fullaccess

Directly attach rds full access policy to name1 user: aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess --user-name name1

Create a role for an ec2 instance named “role1”: aws iam create-role –role-name role1 –assume-role-policy-document file://trust-policy.json

The trust-policy.json contained:
{
“Version”: “2012-10-17”,
“Statement”: [
{
“Effect”: “Allow”,
“Principal”: {
“Service”: “ec2.amazonaws.com”
},
“Action”: “sts:AssumeRole”
}
]
}

Attach IAM readonlyaccess policy to that role:
aws iam attach-role-policy –policy-arn arn:aws:iam::aws:policy/IAMAccessAnalyzerReadOnlyAccess –role-name role1


