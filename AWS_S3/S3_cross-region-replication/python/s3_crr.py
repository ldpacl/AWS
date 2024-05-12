import boto3
import json

source_bucket = input("Enter the source bucket name: ")
destination_bucket = input("Enter the destination bucket name: ")
region_2 = input("Enter the destination bucket region: ")


s3 = boto3.client('s3')
iam = boto3.client('iam')

try:
    s3.create_bucket(
        Bucket=source_bucket,   
    )
    print("Source bucket created successfully")

    s3.put_bucket_versioning(
        Bucket=source_bucket,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )

    s3.create_bucket(
        Bucket=destination_bucket,
        CreateBucketConfiguration={
            'LocationConstraint': region_2
        }
    )
    print("Destination bucket created successfully")

    s3.put_bucket_versioning(
        Bucket=destination_bucket,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )

    replication_policy_response=iam.create_policy(
        PolicyName='replication-policy',
        PolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObjectVersionForReplication",
                        "s3:GetObjectVersionAcl",
                        "s3:GetObjectVersionTagging",
                    ],
                    "Resource": [f"arn:aws:s3:::{source_bucket}/*"]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetReplicationConfiguration",
                    ],
                    "Resource": [f"arn:aws:s3:::{source_bucket}"]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:ReplicateObject",
                        "s3:ReplicateDelete",
                        "s3:ReplicateTags",
                    ],
                    "Resource": [f"arn:aws:s3:::{destination_bucket}/*"]
                }
            ]
        })
    )
    print("Replication policy created successfully")

    replication_policy_arn = replication_policy_response['Policy']['Arn']

    replication_role_response=iam.create_role(
        AssumeRolePolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "s3.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }),
        Path='/',
        RoleName='replication-role'
    )
    print("Replication role created successfully")

    replication_role_arn = replication_role_response['Role']['Arn']

    iam.attach_role_policy(
        RoleName='replication-role',
        PolicyArn=replication_policy_arn
    )

    s3.put_bucket_replication(
        Bucket=source_bucket,
        ReplicationConfiguration={
            'Role': replication_role_arn,
            'Rules': [{
                'ID': 'rule-1',
                'Status': 'Enabled',
                'Filter': { 'Prefix': '' },
                'Priority': 1,
                'DeleteMarkerReplication': { 'Status': 'Disabled' },
                'Destination': {
                    'Bucket': f"arn:aws:s3:::{destination_bucket}",
                    'StorageClass': 'STANDARD'
                }
            }]
        }
    )
    print("Replication configuration set successfully")

except Exception as e:
    print("An error occurred:", e)