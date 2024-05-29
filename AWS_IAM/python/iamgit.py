import boto3
import json

awsconsole = boto3.session.Session(profile_name="default")
iamconsole = awsconsole.client('iam')

name1= input("Enter the name of the user1: ")
password1= input("Enter the password of the user1: ")

name2= input("Enter the name of the user2: ")
password2= input("Enter the password of the user2: ")

#Creating User Groups
iamconsole.create_group(
    GroupName = "ec2fullaccess"
)
iamconsole.create_group(
    GroupName = "s3fullaccess"
)

#Attaching AWS managed policies to the groups
iamconsole.attach_group_policy(
    GroupName="ec2fullaccess",
    PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess"
)
iamconsole.attach_group_policy(
    GroupName="s3fullaccess",
    PolicyArn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
)

#Creating users
iamconsole.create_user(
    UserName=name1
)
iamconsole.create_user(
    UserName=name2
)

#Creating passwords for the users so that they can login from the console
iamconsole.create_login_profile(
    UserName=name1,
    Password=password1,
    PasswordResetRequired=False
)
iamconsole.create_login_profile(
    UserName=name2,
    Password=password2,
    PasswordResetRequired=False
)

#Adding users to groups
iamconsole.add_user_to_group(
    GroupName="ec2fullaccess",
    UserName=name2
)
iamconsole.add_user_to_group(
    GroupName="s3fullaccess",
    UserName=name1
)

#Attaching an extra policy to dpac
iamconsole.attach_user_policy(
    UserName=name1,
    PolicyArn="arn:aws:iam::aws:policy/AmazonRDSFullAccess"
)

#Creating a role and attaching a policy to it
assume_role_policy_document = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
})

iamconsole.create_role(
    RoleName="role1",
    AssumeRolePolicyDocument = assume_role_policy_document 
)

iamconsole.attach_role_policy(
    RoleName="role1",
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
)