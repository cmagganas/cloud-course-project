"""Example pytest fixture."""

import os
from typing import Generator

import boto3
import pytest
from mypy_boto3_s3 import S3Client


@pytest.fixture
def aws():
    """
    Yield a mocked S3 client to be used in tests.

    Set up a bucket for testing as well, under the name `TEST_BUCKET_NAME`.
    """
    # ...
    yield
