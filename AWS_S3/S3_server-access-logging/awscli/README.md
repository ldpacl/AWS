# Step 1: Create Hosting Bucket 1

### Create an S3  bucket in the current region to be used as the hosting bucket. Use a unique name for the bucket in the given command
```aws s3api create-bucket --bucket hostingbucket1```

### Make the bucket publicly accessible
```aws s3api put-public-access-block --bucket hostingbucket1 --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false" ```

### Enable versioning for the bucket
```aws s3api put-bucket-versioning --bucket hostingbucket1 --versioning-configuration Status=Enabled ```

### Confiure the bucket to enable static website hosting
```aws s3api put-bucket-website --bucket hostingbucket1 --website-configuration '{"IndexDocument": {"Suffix": "index.html"}}' ```

### Attach bucket policy so that the website is publicly accessible
```aws s3api put-bucket-policy --bucket hostingbucket1 --policy file://host1-policy.json ```

# Step 2: Create Hosting Bucket 2

### Follow the same steps as above using the following commands

```aws s3api create-bucket --bucket hostingbucket2dpac```

```aws s3api put-public-access-block --bucket hostingbucket2 --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"```

```aws s3api put-bucket-versioning --bucket hostingbucket2 --versioning-configuration Status=Enabled```

```aws s3api put-bucket-website --bucket hostingbucket2 --website-configuration '{"IndexDocument": {"Suffix": "index.html"}}'```

```aws s3api put-bucket-policy --bucket hostingbucket2 --policy file://host2-policy.json```

# Step 3: Create a private S3 bucket in the current region to be used as the logging bucket. Use a unique name for the bucket in the given command
```aws s3api create-bucket --bucket loggingbucket --acl private```

### Attach a bucket policy to the logging bucket so that it logs the data of the 2 buckets in 2 different folders
```aws s3api put-bucket-policy --bucket loggingbucket --policy file://logging-policy.json```

# Step 4: Enable logging

### Enable logging for hosting bucket 1 to the destination folder in logging bucket
```aws s3api put-bucket-logging --bucket hostingbucket1 --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"loggingbucket","TargetPrefix":"logs/hostingbucket1/"}}'```

### Enable logging for hosting bucket 2 to the destination folder in logging bucket
```aws s3api put-bucket-logging --bucket hostingbucket2 --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"loggingbucket","TargetPrefix":"logs/hostingbucket2/"}}'```