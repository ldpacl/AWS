import boto3
import json

# Get user input
source_bucket = input("Enter the source bucket name to delete: ")
destination_bucket = input("Enter the destination bucket name to delete: ")
region_2 = input("Enter the destination bucket region: ")

s3 = boto3.client('s3')
iam = boto3.client('iam')

try:
    # Empty and delete source bucket
    print("Emptying source bucket...")
    s3_resource = boto3.resource('s3')
    source_bucket_obj = s3_resource.Bucket(source_bucket)
    source_bucket_obj.objects.all().delete()
    source_bucket_obj.object_versions.all().delete()
    
    s3.delete_bucket(Bucket=source_bucket)
    print("Source bucket deleted successfully")
    
    # Empty and delete destination bucket
    print("Emptying destination bucket...")
    dest_bucket_obj = s3_resource.Bucket(destination_bucket)
    dest_bucket_obj.objects.all().delete()
    dest_bucket_obj.object_versions.all().delete()
    
    s3.delete_bucket(Bucket=destination_bucket)
    print("Destination bucket deleted successfully")
    
    # Detach policy from role
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    iam.detach_role_policy(
        RoleName='replication-role',
        PolicyArn=f'arn:aws:iam::{account_id}:policy/replication-policy'
    )
    print("Policy detached from role")
    
    # Delete IAM role
    iam.delete_role(RoleName='replication-role')
    print("Replication role deleted successfully")
    
    # Delete IAM policy
    iam.delete_policy(
        PolicyArn=f'arn:aws:iam::{account_id}:policy/replication-policy'
    )
    print("Replication policy deleted successfully")
    
    print("Cleanup completed successfully!")
    
except Exception as e:
    print("An error occurred during cleanup:", e)
