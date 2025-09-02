import boto3
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_iam_resources():
    """Create IAM resources following security best practices"""
    try:
        # Initialize IAM client
        iam = boto3.client('iam')
        
        # Get user input
        name1 = input("Enter the name of service user1: ")
        name2 = input("Enter the name of service user2: ")
        
        # Create groups with descriptive names
        groups = [
            {"name": "RDSAccess", "policy": "arn:aws:iam::aws:policy/AmazonRDSFullAccess"},
            {"name": "EC2FullAccess", "policy": "arn:aws:iam::aws:policy/AmazonEC2FullAccess"},
            {"name": "S3FullAccess", "policy": "arn:aws:iam::aws:policy/AmazonS3FullAccess"}
        ]
        
        for group in groups:
            iam.create_group(GroupName=group["name"])
            logger.info(f"Group {group['name']} created successfully")
            
            iam.attach_group_policy(
                GroupName=group["name"],
                PolicyArn=group["policy"]
            )
            logger.info(f"Policy attached to {group['name']} successfully")
        
        # Create service users (no console access)
        users = [
            {"name": name1, "groups": ["RDSAccess", "EC2FullAccess"]},
            {"name": name2, "groups": ["S3FullAccess"]}
        ]
        
        for user in users:
            # Create user with tags
            iam.create_user(
                UserName=user["name"],
                Tags=[
                    {"Key": "Purpose", "Value": "ServiceAccount"},
                    {"Key": "CreatedBy", "Value": "PythonScript"}
                ]
            )
            logger.info(f"Service user {user['name']} created successfully")
            
            # Create access keys for programmatic access
            response = iam.create_access_key(UserName=user["name"])
            access_key = response['AccessKey']
            
            logger.info(f"Access key created for {user['name']}")
            logger.info(f"Access Key ID: {access_key['AccessKeyId']}")
            logger.warning(f"Secret Access Key: {access_key['SecretAccessKey']} (Store securely!)")
            
            # Add user to groups
            for group_name in user["groups"]:
                iam.add_user_to_group(
                    GroupName=group_name,
                    UserName=user["name"]
                )
                logger.info(f"User {user['name']} added to {group_name} successfully")
        
        # Create IAM role for EC2 instances
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        iam.create_role(
            RoleName="EC2S3ReadOnlyRole",
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Tags=[
                {"Key": "Purpose", "Value": "EC2ServiceRole"},
                {"Key": "CreatedBy", "Value": "PythonScript"}
            ]
        )
        logger.info("EC2 service role created successfully")
        
        iam.attach_role_policy(
            RoleName="EC2S3ReadOnlyRole",
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
        )
        logger.info("Policy attached to role successfully")
        
        # Create instance profile
        iam.create_instance_profile(InstanceProfileName="EC2S3ReadOnlyProfile")
        iam.add_role_to_instance_profile(
            InstanceProfileName="EC2S3ReadOnlyProfile",
            RoleName="EC2S3ReadOnlyRole"
        )
        logger.info("Instance profile created and role attached successfully")
        
        logger.info("All IAM resources created successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    create_iam_resources()
