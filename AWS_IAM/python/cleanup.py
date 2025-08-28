import boto3
import json

awsconsole = boto3.session.Session(profile_name="default")
iamconsole = awsconsole.client('iam')

name1 = input("Enter the name of user1 to delete: ")
name2 = input("Enter the name of user2 to delete: ")

try:
    # Detach user policies and remove from groups
    print("Cleaning up User1...")
    iamconsole.detach_user_policy(
        UserName=name1,
        PolicyArn="arn:aws:iam::aws:policy/AmazonRDSFullAccess"
    )
    iamconsole.remove_user_from_group(
        GroupName="s3fullaccess",
        UserName=name1
    )
    iamconsole.delete_login_profile(UserName=name1)
    iamconsole.delete_user(UserName=name1)
    print("User1 deleted successfully")

    print("Cleaning up User2...")
    iamconsole.remove_user_from_group(
        GroupName="ec2fullaccess",
        UserName=name2
    )
    iamconsole.delete_login_profile(UserName=name2)
    iamconsole.delete_user(UserName=name2)
    print("User2 deleted successfully")

    # Detach policies from groups
    print("Cleaning up Groups...")
    iamconsole.detach_group_policy(
        GroupName="ec2fullaccess",
        PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess"
    )
    iamconsole.detach_group_policy(
        GroupName="s3fullaccess",
        PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
    )

    # Delete groups
    iamconsole.delete_group(GroupName="ec2fullaccess")
    iamconsole.delete_group(GroupName="s3fullaccess")
    print("Groups deleted successfully")

    # Detach policy from role and delete role
    print("Cleaning up Role...")
    iamconsole.detach_role_policy(
        RoleName="role1",
        PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
    )
    iamconsole.delete_role(RoleName="role1")
    print("Role deleted successfully")

    print("All resources cleaned up successfully!")

except Exception as e:
    print("An error occurred during cleanup:", e)
