"""Pytest fixture to mock AWS services."""

import os
from typing import Generator

import boto3
import pytest
from files_api.main import S3_BUCKET_NAME as TEST_BUCKET_NAME
from moto import mock_aws


# Set the environment variables to point away from AWS
def point_away_from_aws() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


# Our fixture is a function and we have named it as a noun instead
# of verb, because it is a resource that is being provided to the test.


@pytest.fixture(scope="function")
def mocked_aws() -> Generator[None, None, None]:
    """
    Set up a mocked AWS environment for testing and clean up after the test.
    """
    with mock_aws():
        # Set the environment variables to point away from AWS
        point_away_from_aws()

        # 1. Create an S3 bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)

        yield

        # 4. Clean up/Teardown by deleting the bucket
        response = s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
        for obj in response.get("Contents", []):
            s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])

        s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)
