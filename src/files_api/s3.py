import boto3

try:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import (
        PutObjectOutputTypeDef,
        ResponseMetadataTypeDef,
    )
except ImportError:
    print("boto3-stubs[s3] not installed. Please run `pip install boto3-stubs[s3]`")


BUCKET_NAME = "python-cloud-eng-course-bucket-avr"

session = boto3.Session()
s3_client: "S3Client" = session.client("s3")

# Write a file to the S3 bucket with the key 'folder/hello.txt' and the content 'Hello, World!'
response: "PutObjectOutputTypeDef" = s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key="folder/hello.txt",
    Body=b"Hello, World! Namaste Duniya!",
    ContentType="text/plain",
)

metadata: "ResponseMetadataTypeDef" = response["ResponseMetadata"]
