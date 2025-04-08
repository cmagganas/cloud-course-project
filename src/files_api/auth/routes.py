"""
Authentication routes for the FastAPI application.
"""
import os
from urllib.parse import urlencode

import httpx
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
)

from files_api.auth.jwt_auth import cognito_auth

# Create router with auth tag
auth_router = APIRouter(tags=["auth"])

# Get Cognito config from environment variables
REGION = os.environ.get("AWS_REGION")
CLIENT_ID = os.environ.get("REACT_APP_COGNITO_CLIENT_ID") 
CLIENT_SECRET = os.environ.get("REACT_APP_COGNITO_CLIENT_SECRET")
DOMAIN = os.environ.get("REACT_APP_COGNITO_DOMAIN")
SCOPES = os.environ.get("REACT_APP_COGNITO_SCOPES", "")
REDIRECT_URI = os.environ.get("REACT_APP_REDIRECT_URI")


@auth_router.get("/auth/login")
async def login():
    """
    Redirect user to Cognito login page.
    
    Returns:
        dict: URL to redirect to for Cognito login
    """
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
    }
    url = f"https://{DOMAIN}/oauth2/authorize?{urlencode(params)}"
    return {"url": url}


@auth_router.get("/auth/callback")
async def callback(code: str, response: Response):
    """
    Handle the callback from Cognito with authorization code.
    
    Args:
        code: Authorization code from Cognito
        response: FastAPI response object for setting cookies
        
    Returns:
        dict: Success message if authentication is successful
        
    Raises:
        HTTPException: If token exchange fails
    """
    token_url = f"https://{DOMAIN}/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail=f"Token exchange failed: {token_response.text}"
            )
        
        tokens = token_response.json()
        
        # Set the ID token in HttpOnly cookie
        response.set_cookie(
            key="id_token",
            value=tokens["id_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,  # 1 hour expiry
        )
        
        return {"message": "Authentication successful"}


@auth_router.get("/auth/logout")
async def logout(response: Response):
    """
    Log the user out by clearing the auth cookie.
    
    Args:
        response: FastAPI response object for clearing cookies
        
    Returns:
        dict: Success message
    """
    response.delete_cookie(key="id_token")
    return {"message": "Logged out successfully"}


@auth_router.get("/auth/user")
async def get_user_info(request: Request):
    """
    Get the current user's information from the JWT token.
    
    Args:
        request: FastAPI request object containing the JWT token
        
    Returns:
        dict: User claims from the JWT token
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = request.cookies.get("id_token")
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated"
        )
    
    try:
        user_info = await cognito_auth.get_user_info(token)
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Invalid token: {str(e)}"
        ) 