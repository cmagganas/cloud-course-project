import os
from textwrap import dedent
from typing import Optional

import pydantic
from fastapi import (
    FastAPI,
    Request,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from files_api.auth.protected_routes import protected_router
from files_api.auth.routes import auth_router
from files_api.errors import (
    handle_broad_exceptions,
    handle_pydantic_validation_errors,
)
from files_api.monitoring.logger import inject_lambda_context__middleware
from files_api.route_handler import RouteHandler
from files_api.routes import (
    FILES_ROUTER,
    GENERATED_FILES_ROUTER,
)
from files_api.settings import Settings


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """Create a FastAPI application."""
    settings = settings or Settings()

    app = FastAPI(
        title="Files API",
        summary="Store and retrieve files.",
        version="v1",  # a fancier version would read the semver from pkg metadata
        description=dedent(
            """\
        ![Maintained by](https://img.shields.io/badge/Maintained%20by-MLOps%20Club-05998B?style=for-the-badge)

        | Helpful Links | Notes |
        | --- | --- |
        | [Course Homepage](https://mlops-club.org) | |
        | [Course Student Portal](https://courses.mlops-club.org) | |
        | [Course Materials Repo](https://github.com/mlops-club/python-on-aws-course.git) | `mlops-club/python-on-aws-course` |
        | [Course Reference Project Repo](https://github.com/mlops-club/cloud-course-project.git) | `mlops-club/cloud-course-project` |
        | [FastAPI Documentation](https://fastapi.tiangolo.com/) | |
        | [Learn to make "badges"](https://shields.io/) | Example: <img alt="Awesome Badge" src="https://img.shields.io/badge/Awesome-😎-blueviolet?style=for-the-badge"> |
        """
        ),
        docs_url="/docs",  # Standard Swagger docs URL
        redoc_url="/redoc",  # Standard ReDoc URL
        generate_unique_id_function=custom_generate_unique_id,
        root_path=settings.root_path,
    )
    app.state.settings = settings

    app.router.route_class = RouteHandler
    app.include_router(FILES_ROUTER)
    app.include_router(GENERATED_FILES_ROUTER)
    app.include_router(auth_router)
    app.include_router(protected_router)

    # Root path redirects to auth page
    @app.get("/", response_class=HTMLResponse, tags=["ui"])
    async def root(request: Request):
        return RedirectResponse(url="/auth")

    # Serve static files for authentication UI
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Auth page route
    @app.get("/auth", response_class=HTMLResponse, tags=["ui"])
    async def auth_page(request: Request):
        html_path = os.path.join(static_dir, "index.html")
        with open(html_path, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)

    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=handle_pydantic_validation_errors,
    )
    app.add_exception_handler(
        exc_class_or_status_code=pydantic.ValidationError,
        handler=handle_pydantic_validation_errors,
    )
    app.middleware("http")(handle_broad_exceptions)
    app.middleware("http")(inject_lambda_context__middleware)

    # Add global authentication middleware
    @app.middleware("http")
    async def authenticate_all_routes(request: Request, call_next):
        # List of paths that don't require authentication
        public_paths = [
            "/auth",
            "/auth/login",
            "/auth/callback",
            "/auth/logout",
            "/static",
        ]

        # Check if the request path starts with any of the public paths
        is_public = any(request.url.path.startswith(path) for path in public_paths)

        # If it's a public path, proceed without authentication
        if is_public:
            return await call_next(request)

        # Otherwise, check for authentication
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers.get("Authorization")
            if auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "")
        elif "id_token" in request.cookies:
            token = request.cookies.get("id_token")

        # If no token, redirect to login
        if not token:
            response = RedirectResponse(url="/auth?redirect_from_protected=true", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        # Continue with the request if token exists
        response = await call_next(request)
        return response

    return app


def custom_generate_unique_id(route: APIRoute):
    """
    Generate prettier `operationId`s in the OpenAPI schema.

    These become the function names in generated client SDKs.
    """
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    return route.name


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
