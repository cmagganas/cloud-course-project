"""Hello world example of using boto3 to write a file to S3."""

import boto3

try:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import PutObjectOutputTypeDef
except ImportError:
    print("boto3-stubs[s3] is not installed")

BUCKET_NAME = "cloud-course-bucket-eric"

session = boto3.Session()
s3_client: "S3Client" = session.client("s3")

# write a file to the S3 bucket with the contents "Hello, World!"
response: "PutObjectOutputTypeDef" = s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key="folder/hello.txt",
    Body="Hello, World!",
    ContentType="text/plain",
)
