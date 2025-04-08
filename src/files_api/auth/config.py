"""
Configuration settings for AWS Cognito authentication.
"""
import os
from typing import Optional


class CognitoConfig:
    """Configuration for Cognito settings loaded from environment variables."""
    
    REGION: str = os.environ["AWS_REGION"]
    USER_POOL_ID: str = os.environ["REACT_APP_COGNITO_USER_POOL_ID"]
    CLIENT_ID: str = os.environ["REACT_APP_COGNITO_CLIENT_ID"]
    CLIENT_SECRET: str = os.environ["REACT_APP_COGNITO_CLIENT_SECRET"]
    DOMAIN: str = os.environ["REACT_APP_COGNITO_DOMAIN"]
    SCOPES: str = os.environ["REACT_APP_COGNITO_SCOPES"]
    REDIRECT_URI: str = os.environ["REACT_APP_REDIRECT_URI"]


def get_cognito_settings():
    """
    Get Cognito configuration.
    
    Returns:
        CognitoConfig: Cognito configuration
    """
    return CognitoConfig