import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_iam_resources():
    """Clean up IAM resources created by the main script"""
    try:
        iam = boto3.client('iam')
        
        name1 = input("Enter the name of service user1 to delete: ")
        name2 = input("Enter the name of service user2 to delete: ")
        
        users = [
            {"name": name1, "groups": ["RDSAccess", "EC2FullAccess"]},
            {"name": name2, "groups": ["S3FullAccess"]}
        ]
        
        # Clean up users
        for user in users:
            try:
                logger.info(f"Cleaning up user: {user['name']}")
                
                # Delete access keys
                keys = iam.list_access_keys(UserName=user['name'])
                for key in keys['AccessKeyMetadata']:
                    iam.delete_access_key(
                        UserName=user['name'],
                        AccessKeyId=key['AccessKeyId']
                    )
                    logger.info(f"Access key deleted for {user['name']}")
                
                # Remove user from groups
                for group_name in user['groups']:
                    try:
                        iam.remove_user_from_group(
                            GroupName=group_name,
                            UserName=user['name']
                        )
                        logger.info(f"User {user['name']} removed from {group_name}")
                    except iam.exceptions.NoSuchEntityException:
                        logger.warning(f"Group {group_name} or user {user['name']} not found")
                
                # Delete user
                iam.delete_user(UserName=user['name'])
                logger.info(f"User {user['name']} deleted successfully")
                
            except iam.exceptions.NoSuchEntityException:
                logger.warning(f"User {user['name']} not found")
        
        # Clean up groups
        groups = [
            {"name": "RDSAccess", "policy": "arn:aws:iam::aws:policy/AmazonRDSFullAccess"},
            {"name": "EC2FullAccess", "policy": "arn:aws:iam::aws:policy/AmazonEC2FullAccess"},
            {"name": "S3FullAccess", "policy": "arn:aws:iam::aws:policy/AmazonS3FullAccess"}
        ]
        
        for group in groups:
            try:
                logger.info(f"Cleaning up group: {group['name']}")
                
                # Detach policy from group
                iam.detach_group_policy(
                    GroupName=group['name'],
                    PolicyArn=group['policy']
                )
                logger.info(f"Policy detached from {group['name']}")
                
                # Delete group
                iam.delete_group(GroupName=group['name'])
                logger.info(f"Group {group['name']} deleted successfully")
                
            except iam.exceptions.NoSuchEntityException:
                logger.warning(f"Group {group['name']} not found")
        
        # Clean up role and instance profile
        try:
            logger.info("Cleaning up role and instance profile")
            
            # Remove role from instance profile
            iam.remove_role_from_instance_profile(
                InstanceProfileName="EC2S3ReadOnlyProfile",
                RoleName="EC2S3ReadOnlyRole"
            )
            
            # Delete instance profile
            iam.delete_instance_profile(InstanceProfileName="EC2S3ReadOnlyProfile")
            logger.info("Instance profile deleted successfully")
            
            # Detach policy from role
            iam.detach_role_policy(
                RoleName="EC2S3ReadOnlyRole",
                PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
            )
            
            # Delete role
            iam.delete_role(RoleName="EC2S3ReadOnlyRole")
            logger.info("Role deleted successfully")
            
        except iam.exceptions.NoSuchEntityException:
            logger.warning("Role or instance profile not found")
        
        logger.info("All IAM resources cleaned up successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred during cleanup: {e}")

if __name__ == "__main__":
    cleanup_iam_resources()
