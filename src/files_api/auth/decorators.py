"""
Authentication decorators for FastAPI routes.
"""
from functools import wraps
from typing import (
    Any,
    Callable,
    List,
    Optional,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from files_api.auth.dependencies import get_current_user


def protect_endpoint(
    func: Callable = None, 
    required_scopes: Optional[List[str]] = None
) -> Callable:
    """
    Decorator to protect an endpoint with Cognito authentication.
    
    Args:
        func: The route function to protect
        required_scopes: Optional list of required scopes (not implemented yet)
        
    Returns:
        A wrapped function that requires authentication
        
    Example:
        @router.get("/protected")
        @protect_endpoint
        async def protected_route():
            return {"message": "This route is protected"}
            
        # Or with scopes (future implementation)
        @router.get("/admin")
        @protect_endpoint(required_scopes=["admin"])
        async def admin_route():
            return {"message": "This route requires admin scope"}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # The get_current_user dependency ensures authentication
            # This will raise HTTPException if not authenticated
            user = await get_current_user(kwargs.get("request"))
            
            # In the future, we could check scopes here
            if required_scopes:
                # This is placeholder for future scope validation
                # You would need to extract scopes from the token and validate
                pass
                
            # Add the user to kwargs so the route can access it
            kwargs["user"] = user
            return await func(*args, **kwargs)
        
        # Add the dependency to the route
        wrapper.__dependencies__ = getattr(func, "__dependencies__", []) + [Depends(get_current_user)]
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func) 