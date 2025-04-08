"""
JWT authentication for Cognito tokens.
"""
import base64
import json
import os
import time
from typing import (
    Dict,
    Optional,
)

import httpx
import jwt
import requests
from jwt.api_jwk import PyJWK


class CognitoJWTAuth:
    """JWT authentication for Cognito tokens."""

    def __init__(self):
        """Initialize the Cognito JWT Auth."""
        self.region = os.environ.get("AWS_REGION")
        self.userpool_id = os.environ.get("REACT_APP_COGNITO_USER_POOL_ID")
        self.app_client_id = os.environ.get("REACT_APP_COGNITO_CLIENT_ID")
        
        # Don't fetch keys immediately in case environment variables aren't set
        self.keys = None
        self.jwks = {}

    def _get_public_keys(self) -> Dict:
        """
        Get the public keys from Cognito to verify JWT tokens.
        
        Returns:
            Dict: Dictionary of public keys
        """
        if not self.region or not self.userpool_id:
            print("Warning: AWS_REGION or COGNITO_USER_POOL_ID not set")
            return []
            
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.userpool_id}/.well-known/jwks.json"
        try:
            response = requests.get(keys_url)
            response.raise_for_status()
            self.keys = response.json()["keys"]
            
            # Create a mapping of kid to public key
            for key_dict in self.keys:
                kid = key_dict.get('kid')
                if kid:
                    # Convert JWK to PEM using PyJWK
                    public_key = PyJWK.from_dict(key_dict).key
                    self.jwks[kid] = public_key
                    
            return self.keys
        except Exception as e:
            print(f"Error fetching public keys: {e}")
            return []

    async def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify a JWT token from Cognito.
        
        Args:
            token: The JWT token to verify
            
        Returns:
            Dict: The token claims if valid
            
        Raises:
            Exception: If the token is invalid
        """
        # Lazy-load keys when needed
        if not self.keys:
            self._get_public_keys()
            
        if not self.keys:
            raise Exception("No public keys available for token verification")
            
        # Get the token header
        try:
            # Parse header without verification
            header = jwt.get_unverified_header(token)
        except Exception as e:
            raise Exception(f"Invalid token header: {e}")
        
        # Get the key ID
        kid = header.get('kid')
        if not kid:
            raise Exception("No kid found in token header")
            
        # Get the public key
        public_key = self.jwks.get(kid)
        if not public_key:
            # Try refreshing keys if not found
            self._get_public_keys()
            public_key = self.jwks.get(kid)
            
        if not public_key:
            raise Exception(f"Public key not found for kid: {kid}")
            
        try:
            # Verify the token
            payload = jwt.decode(
                token, 
                public_key,
                algorithms=['RS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                    'verify_aud': True
                },
                audience=self.app_client_id
            )
            
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidAudienceError:
            raise Exception("Token was not issued for this client ID")
        except Exception as e:
            raise Exception(f"Token verification failed: {str(e)}")
        
    async def get_user_info(self, token: str) -> Dict:
        """
        Get user information from a token.
        
        Args:
            token: The JWT token
            
        Returns:
            Dict: User information extracted from the token
        """
        claims = await self.verify_token(token)
        
        # Extract relevant user information
        user_info = {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "username": claims.get("cognito:username", claims.get("sub")),
            "name": claims.get("name"),
            "groups": claims.get("cognito:groups", []),
            "expires": claims.get("exp"),
        }
        
        return user_info


# Create a singleton instance
cognito_auth = CognitoJWTAuth() 