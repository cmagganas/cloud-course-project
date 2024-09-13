"""Pytest fixture to mock AWS services."""

import os
from typing import Generator

import boto3
import pytest
from moto import mock_aws

from tests.consts import TEST_BUCKET_NAME


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

        # 1. Create an s3 client and a bucket
        # ...

        yield

        # 4. Clean up/Teardown by deleting the bucket
        # ...
