import boto3
import json

account_id = boto3.client('sts').get_caller_identity().get('Account')
host_bucket_1 = input("Enter the name of the hosting bucket 1: ")
host_bucket_2 = input("Enter the name of the hosting bucket 2: ")
log_bucket = input("Enter the name of the logging bucket: ")
account_id = input("Enter your account id")
region= input("Enter the region")

s3 = boto3.client('s3')

try:
    s3.create_bucket(
        Bucket= host_bucket_1
    )
    print("Hosting bucket 1 created successfully")

    s3.put_public_access_block(
        Bucket= host_bucket_1,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )

    s3.put_bucket_versioning(
        Bucket= host_bucket_1,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )

    s3.put_bucket_policy(
        Bucket= host_bucket_1,
        Policy = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": [f"arn:aws:s3:::{host_bucket_1}/*"]
                }
            ]
        })
    )
    print("Host Bucket 1 policy added successfully")

    s3.put_bucket_website(
        Bucket= host_bucket_1,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'}
        }
    )

    s3.create_bucket(
        Bucket= host_bucket_2
    )
    print("Hosting bucket 2 created successfully")

    s3.put_public_access_block(
        Bucket= host_bucket_2,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )

    s3.put_bucket_versioning(
        Bucket=host_bucket_2,
        VersioningConfiguration={
            'Status' : 'Enabled'
        }
    )
    
    s3.put_bucket_policy(
        Bucket= host_bucket_2,
        Policy= json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": [f"arn:aws:s3:::{host_bucket_2}/*"]
                }
            ]
        })
    )
    print("Host Bucket 2 policy added successfully")

    s3.put_bucket_website(
        Bucket= host_bucket_2,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'}
        }
    )

    s3.create_bucket(
        Bucket= log_bucket
    )
    print("Logging bucket created successfully")

    s3.put_public_access_block(
        Bucket= log_bucket,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )

    s3.put_bucket_policy(
        Bucket= log_bucket,
        Policy = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "logging.s3.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{log_bucket}/logs/{host_bucket_1}/*",
                    "Condition": {
                        "StringEquals": {
                            "aws:SourceAccount": account_id
                        },
                        "ArnLike": {
                        "aws:SourceArn": f"arn:aws:s3:::{host_bucket_1}"
                        }
                    }
                },
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "logging.s3.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{log_bucket}/logs/{host_bucket_2}/*",
                    "Condition": {
                        "StringEquals": {
                            "aws:SourceAccount": account_id
                        },
                        "ArnLike": {
                            "aws:SourceArn": f"arn:aws:s3:::{host_bucket_2}"
                        }
                    }
                }
            ]
        })
    )
    print("Log Bucket policy added successfully")

    s3.put_bucket_logging(
        Bucket= host_bucket_1,
        BucketLoggingStatus={
            'LoggingEnabled': {
                'TargetBucket': log_bucket,
                'TargetPrefix': f"logs/{host_bucket_1}/"
            }
        }
    )

    s3.put_bucket_logging(
        Bucket= host_bucket_2,
        BucketLoggingStatus={
            'LoggingEnabled': {
                'TargetBucket': log_bucket,
                'TargetPrefix': f"logs/{host_bucket_2}/"
            }
        }
    )

except Exception as e:
    print("An error occurred: ", e)