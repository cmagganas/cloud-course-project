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
from fastapi.responses import RedirectResponse

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
        RedirectResponse: Redirects to Cognito login page
    """
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
    }
    url = f"https://{DOMAIN}/oauth2/authorize?{urlencode(params)}"
    return RedirectResponse(url=url)


@auth_router.get("/auth/callback")
async def callback(code: str, response: Response):
    """
    Handle the callback from Cognito with authorization code.
    
    Args:
        code: Authorization code from Cognito
        response: FastAPI response object for setting cookies
        
    Returns:
        RedirectResponse: Redirects to home page after successful authentication
        
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
            secure=False,  # Allow in development
            samesite="lax",
            path="/",
            max_age=3600,  # 1 hour expiry
            domain=None  # Allow cookie to be set on localhost
        )
        
        # Create redirect response
        redirect = RedirectResponse(
            url="/",
            status_code=303  # See Other
        )
        
        # Set the cookie on the redirect response as well
        redirect.set_cookie(
            key="id_token",
            value=tokens["id_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=3600,
            domain=None
        )
        
        return redirect


@auth_router.get("/auth/logout")
async def logout(response: Response):
    """
    Log the user out by clearing the auth cookie and redirecting to home.
    
    Args:
        response: FastAPI response object for clearing cookies
        
    Returns:
        RedirectResponse: Redirects to home page
    """
    # Create redirect response
    redirect = RedirectResponse(
        url="/",
        status_code=303  # See Other
    )
    
    # Clear the ID token cookie with same settings as when it was set
    redirect.delete_cookie(
        key="id_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        domain=None
    )
    
    return redirect


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