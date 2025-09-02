"""
Configuration file for IAM resource management
"""

# IAM Groups configuration
IAM_GROUPS = [
    {
        "name": "RDSAccess",
        "policy_arn": "arn:aws:iam::aws:policy/AmazonRDSFullAccess",
        "description": "Group for RDS database access"
    },
    {
        "name": "EC2FullAccess", 
        "policy_arn": "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
        "description": "Group for EC2 compute access"
    },
    {
        "name": "S3FullAccess",
        "policy_arn": "arn:aws:iam::aws:policy/AmazonS3FullAccess", 
        "description": "Group for S3 storage access"
    }
]

# IAM Role configuration
IAM_ROLE = {
    "name": "EC2S3ReadOnlyRole",
    "policy_arn": "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
    "instance_profile": "EC2S3ReadOnlyProfile",
    "assume_role_policy": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
}

# Default tags for resources
DEFAULT_TAGS = [
    {"Key": "CreatedBy", "Value": "PythonScript"},
    {"Key": "Environment", "Value": "Development"},
    {"Key": "Project", "Value": "IAM-Learning"}
]
