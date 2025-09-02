import boto3
import json
import logging
from config import IAM_GROUPS, IAM_ROLE, DEFAULT_TAGS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IAMManager:
    def __init__(self):
        self.iam = boto3.client('iam')
    
    def create_groups(self):
        """Create IAM groups and attach policies"""
        for group in IAM_GROUPS:
            try:
                self.iam.create_group(GroupName=group["name"])
                logger.info(f"Group {group['name']} created")
                
                self.iam.attach_group_policy(
                    GroupName=group["name"],
                    PolicyArn=group["policy_arn"]
                )
                logger.info(f"Policy attached to {group['name']}")
            except self.iam.exceptions.EntityAlreadyExistsException:
                logger.warning(f"Group {group['name']} already exists")
    
    def create_service_user(self, username, group_names):
        """Create service user with access keys (no console access)"""
        try:
            # Create user with tags
            tags = DEFAULT_TAGS + [{"Key": "Purpose", "Value": "ServiceAccount"}]
            self.iam.create_user(UserName=username, Tags=tags)
            logger.info(f"Service user {username} created")
            
            # Create access key
            response = self.iam.create_access_key(UserName=username)
            access_key = response['AccessKey']
            
            logger.info(f"Access Key ID: {access_key['AccessKeyId']}")
            logger.warning(f"Secret Key: {access_key['SecretAccessKey']} (Store securely!)")
            
            # Add to groups
            for group_name in group_names:
                self.iam.add_user_to_group(GroupName=group_name, UserName=username)
                logger.info(f"User {username} added to {group_name}")
                
            return access_key
            
        except self.iam.exceptions.EntityAlreadyExistsException:
            logger.warning(f"User {username} already exists")
    
    def create_role(self):
        """Create IAM role with instance profile"""
        try:
            tags = DEFAULT_TAGS + [{"Key": "Purpose", "Value": "EC2ServiceRole"}]
            
            self.iam.create_role(
                RoleName=IAM_ROLE["name"],
                AssumeRolePolicyDocument=json.dumps(IAM_ROLE["assume_role_policy"]),
                Tags=tags
            )
            logger.info(f"Role {IAM_ROLE['name']} created")
            
            self.iam.attach_role_policy(
                RoleName=IAM_ROLE["name"],
                PolicyArn=IAM_ROLE["policy_arn"]
            )
            logger.info("Policy attached to role")
            
            # Create instance profile
            self.iam.create_instance_profile(InstanceProfileName=IAM_ROLE["instance_profile"])
            self.iam.add_role_to_instance_profile(
                InstanceProfileName=IAM_ROLE["instance_profile"],
                RoleName=IAM_ROLE["name"]
            )
            logger.info("Instance profile created and role attached")
            
        except self.iam.exceptions.EntityAlreadyExistsException:
            logger.warning("Role or instance profile already exists")

def main():
    """Main function to create IAM resources"""
    iam_manager = IAMManager()
    
    # Get user input
    name1 = input("Enter name for service user 1: ")
    name2 = input("Enter name for service user 2: ")
    
    try:
        # Create groups
        iam_manager.create_groups()
        
        # Create service users
        iam_manager.create_service_user(name1, ["RDSAccess", "EC2FullAccess"])
        iam_manager.create_service_user(name2, ["S3FullAccess"])
        
        # Create role
        iam_manager.create_role()
        
        logger.info("All IAM resources created successfully!")
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
