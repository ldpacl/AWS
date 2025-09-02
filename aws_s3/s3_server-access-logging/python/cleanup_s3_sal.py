import boto3

# Get user input
host_bucket_1 = input("Enter hosting bucket 1 name to delete: ")
host_bucket_2 = input("Enter hosting bucket 2 name to delete: ")
log_bucket = input("Enter logging bucket name to delete: ")

s3 = boto3.client('s3')

try:
    # Disable logging first
    print("Disabling server access logging...")
    s3.put_bucket_logging(Bucket=host_bucket_1, BucketLoggingStatus={})
    s3.put_bucket_logging(Bucket=host_bucket_2, BucketLoggingStatus={})
    print("Logging disabled successfully")
    
    # Empty and delete buckets
    for bucket in [host_bucket_1, host_bucket_2, log_bucket]:
        print(f"Emptying bucket: {bucket}")
        
        # Empty bucket (handle both regular objects and versions)
        try:
            # List and delete all objects
            response = s3.list_objects_v2(Bucket=bucket)
            if 'Contents' in response:
                objects = [{'Key': obj['Key']} for obj in response['Contents']]
                s3.delete_objects(Bucket=bucket, Delete={'Objects': objects})
            
            # List and delete all object versions
            response = s3.list_object_versions(Bucket=bucket)
            if 'Versions' in response:
                versions = [{'Key': obj['Key'], 'VersionId': obj['VersionId']} for obj in response['Versions']]
                s3.delete_objects(Bucket=bucket, Delete={'Objects': versions})
            
            # List and delete all delete markers
            if 'DeleteMarkers' in response:
                markers = [{'Key': obj['Key'], 'VersionId': obj['VersionId']} for obj in response['DeleteMarkers']]
                s3.delete_objects(Bucket=bucket, Delete={'Objects': markers})
                
        except Exception as e:
            print(f"Error emptying bucket {bucket}: {e}")
        
        # Delete bucket
        s3.delete_bucket(Bucket=bucket)
        print(f"Bucket {bucket} deleted successfully")
        
    print("Cleanup completed successfully!")
    
except Exception as e:
    print(f"An error occurred: {e}")
