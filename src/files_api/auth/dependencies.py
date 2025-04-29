"""
Authentication dependencies for FastAPI routes using AWS Cognito.
"""
import time

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from files_api.auth.jwt_auth import cognito_auth

# HTTP Bearer scheme for authentication
security = HTTPBearer(auto_error=False)


async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get the current authenticated user from Cognito token.
    
    Args:
        request: The incoming request containing the JWT token
        credentials: Bearer token credentials
        
    Returns:
        User claims if token is valid
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = None
    
    # Try to get token from Authorization header
    if credentials:
        token = credentials.credentials
    # If not in header, try to get from cookies
    elif "id_token" in request.cookies:
        token = request.cookies.get("id_token")
    
    if not token:
        # Create a redirect response to the login page
        response = RedirectResponse(url="/auth?redirect_from_protected=true", status_code=status.HTTP_303_SEE_OTHER)
        
        # Add cache control headers to prevent caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        return response
            
    try:
        # Verify token with Cognito
        user_info = await cognito_auth.get_user_info(token)
        
        # Check if token is expired
        current_time = time.time()
        if "exp" in user_info and user_info["exp"] < current_time:
            # Create a redirect response to the login page
            response = RedirectResponse(url="/auth?redirect_from_protected=true", status_code=status.HTTP_303_SEE_OTHER)
            
            # Clear the expired token
            response.delete_cookie(
                key="id_token",
                httponly=True,
                secure=False,
                samesite="lax",
                path="/",
                domain=None
            )
            
            # Add cache control headers to prevent caching
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            
            return response
        
        return user_info
    except Exception as e:
        # Create a redirect response to the login page
        response = RedirectResponse(url="/auth?redirect_from_protected=true", status_code=status.HTTP_303_SEE_OTHER)
        
        # Clear the invalid token
        response.delete_cookie(
            key="id_token",
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            domain=None
        )
        
        # Add cache control headers to prevent caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        return response 