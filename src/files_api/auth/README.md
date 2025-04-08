# AWS Cognito Authentication for FastAPI

This module provides AWS Cognito authentication integration for FastAPI applications. It handles the OAuth2 authorization code flow with Cognito and provides dependencies for protecting routes.

## Features

- OAuth2 authorization code flow with AWS Cognito
- JWT token validation
- Protected routes with user information
- Login, callback, and logout endpoints
- Simple and secure authentication with HttpOnly cookies

## Usage

### Authentication Flow

1. User accesses `/auth/login`
2. User is redirected to Cognito login page
3. After successful login, Cognito redirects to `/auth/callback` with an authorization code
4. Backend exchanges the code for tokens and sets the ID token in an HttpOnly cookie
5. User is now authenticated

### Protecting Routes

There are two ways to protect routes:

#### 1. Using the dependency directly

```python
from fastapi import Depends
from files_api.auth.dependencies import get_current_user

@router.get("/protected-endpoint")
async def protected_endpoint(user=Depends(get_current_user)):
    return {"message": "This is protected", "user": user}
```

#### 2. Using the protected router

Add routes to the protected router to automatically require authentication:

```python
from files_api.auth.protected_routes import protected_router

@protected_router.get("/my-protected-endpoint")
async def my_protected_endpoint(user):
    return {"message": "This is protected", "user": user}
```

### Configuration

Authentication settings are loaded from environment variables:

```
AWS_REGION=us-west-1
REACT_APP_COGNITO_USER_POOL_ID=us-west-1_IbylLTjCJ
REACT_APP_COGNITO_CLIENT_ID=50m5rakpde2qse9mf8pb9c12bb
REACT_APP_COGNITO_CLIENT_SECRET=<your-secret>
REACT_APP_COGNITO_DOMAIN=us-west-1ibylltjcj.auth.us-west-1.amazoncognito.com
REACT_APP_COGNITO_SCOPES=openid email profile
COGNITO_REDIRECT_URI=http://localhost:8000/auth/callback
```

## Testing

To test the authentication:

1. Start the FastAPI application: `uvicorn files_api.main:app --reload`
2. Access http://localhost:8000/auth/login
3. After login, try accessing http://localhost:8000/protected/test
4. You should see user information if authentication is successful 