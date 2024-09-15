import boto3
import json

host_bucket = input("Enter the name of the hosting bucket: ")
region= input("Enter the region: ")

s3 = boto3.client('s3')

try:
    s3.create_bucket(
        Bucket= host_bucket
    )
    print("Hosting bucket created successfully")

    s3.put_bucket_ownership_controls(
        Bucket= host_bucket,
        OwnershipControls={
            'Rules': [
                {
                    'ObjectOwnership': 'BucketOwnerPreferred'
                },
            ]
        }
    )
    print("Bucket Ownership Controls set successfully")

    s3.put_public_access_block(
        Bucket= host_bucket,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
    )
    print("Public Access Block Configuration set to bucket successfully")

    with open('./index.html', 'rb') as file_data:
        s3.put_object(
            Body=file_data,
            Bucket= host_bucket,
            Key='index.html',
            ContentType= 'text/html'
        )
    print("Index file uploaded to bucket successfully")

    s3.put_bucket_website(
        Bucket= host_bucket,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'}
        }
    )
    print("Bucket configured to host static website successfully")

    s3.put_bucket_policy(
        Bucket= host_bucket,
        Policy = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": [f"arn:aws:s3:::{host_bucket}/*"]
                }
            ]
        })
    )
    print("Host Bucket policy added successfully")

except Exception as e:
    print("An error occurred: ", e)