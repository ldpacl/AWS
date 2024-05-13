Step 1: Create Source Bucket
Create a private S3  bucket in the current region to be used as the source bucket. Use a unique name for the bucket in the given command
aws s3api create-bucket --bucket source-bucket --acl private

Step 2: Enable Versioning for Source Bucket
Enable versioning for the source bucket to ensure proper replication.
aws s3api put-bucket-versioning --bucket source-bucket --versioning-configuration Status=Enabled

Step 3: Create Destination Bucket
Create a private S3 bucket in a different location as the destination bucket. Use a unique name
aws s3api create-bucket --bucket destination-bucket --acl private --create-bucket-configuration LocationConstraint=ap-south-1

Step 4: Enable Versioning for Destination Bucket
Enable versioning for the destination bucket.
aws s3api put-bucket-versioning --bucket destination-bucket --versioning-configuration Status=Enabled

Step 5: Create Replication Policy
Create a replication policy by updating the replication_policy.json file with the source and destination bucket ARNs, and then execute the following command.
aws iam create-policy --policy-name replication-policy --policy-document file://replication_policy.json

Step 6: Create Replication Role
Create a replication role by updating the assume-role-policy.json file with the necessary role policy and then execute the following command.
aws iam create-role --role-name replication-role --assume-role-policy-document file://assume-role-policy.json

Step 7: Attach Replication Policy to Replication Role
Attach the previously created replication policy to the replication role by executing the following command. Make sure to replace the policy-arn argument with the appropriate ARN.
aws iam attach-role-policy --role-name replication-role --policy-arn arn:aws:iam::12345:policy/replication-policy

Step 8: Create Replication Configuration
Create the replication configuration for the source bucket by updating the replicatoin_configuration.json file with the destination bucket ARN and then execute the following command.
aws s3api put-bucket-replication --bucket source-bucket --replication-configuration file://replication_configuration.json

Note: Don't forget to replace the placeholder values with the actual desired names and ARNs.