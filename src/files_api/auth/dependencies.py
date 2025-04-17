"""
Authentication dependencies for FastAPI routes using AWS Cognito.
"""
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
        # If we're already on the login page, don't redirect
        if request.url.path == "/auth/login":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        # Otherwise redirect to login
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': '/auth/login'}
        )
            
    try:
        # Verify token with Cognito
        user_info = await cognito_auth.get_user_info(token)
        return user_info
    except Exception as e:
        # Create redirect response
        redirect = RedirectResponse(url="/auth/login")
        
        # Clear invalid token
        if "id_token" in request.cookies:
            redirect.delete_cookie(
                key="id_token",
                httponly=True,
                secure=False,
                samesite="lax",
                path="/",
                domain=None
            )
        
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={'Location': '/auth/login'}
        ) 