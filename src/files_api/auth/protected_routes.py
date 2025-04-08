"""
Example protected routes to demonstrate authentication.
"""
from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from files_api.auth.dependencies import get_current_user

protected_router = APIRouter(tags=["protected"])


@protected_router.get("/protected/test")
async def protected_test_route(user=Depends(get_current_user)):
    """
    A simple protected test route that requires authentication.
    
    Args:
        user: The authenticated user info (injected by the dependency)
        
    Returns:
        dict: A message indicating the route is protected and user info
    """
    return {
        "message": "This is a protected route - you are authenticated!",
        "user": user
    }


@protected_router.get("/protected/user-info")
async def protected_user_info(request: Request, user=Depends(get_current_user)):
    """
    Get information about the authenticated user.
    
    Args:
        request: The incoming request 
        user: The authenticated user info (injected by the dependency)
        
    Returns:
        dict: User information from the JWT token
    """
    return {
        "username": user.get("username", "Unknown"),
        "email": user.get("email", "Not provided"),
        "name": user.get("name", "Not provided"),
        "sub": user.get("sub"),
        "groups": user.get("groups", []),
        "expires": user.get("expires"),
    } 