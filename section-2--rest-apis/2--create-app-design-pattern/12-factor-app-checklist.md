# API Design Checklist - 12-factor App

The state of the code at this point includes

- The `create_app()` factory pattern
- Use of `APIRouter` and `request.app.state` to declares the routes in their own file
- Use of `pydantic-settings` for configuration management

## 12-factor app (https://12factor.net/)

- [ ] 1. **Codebase** - use version control. One codebase, many deploys.
- [ ] 2. **Dependenices** - explicitly declare and isolate dependencies
  - [ ] Declare unpinned dependencies. Prefer `pyproject.toml` to `requirements.txt`.
  - [ ] (Optional) lock dependenices in a text format, e.g. `requirements.lock.txt` with `pip-tools`
  - [ ] Isolate dependencies using a virtual environment
- [ ] 3. **Config** - Use environment variables for configuration
- [ ] 4. **Backing services** - Treat backing services as attached resources
  - [ ] Store connection information such as URLs, credentials, etc. in the config
- [ ] 5. **Build, release, run** - Strictly separate build and run stages
  - [ ] Build a deployable artifact, e.g. a Docker image or AWS Lambda package
  - [ ] Release the artifact to a runtime environment, e.g. AWS ECS or AWS Lambda
  - [ ] Run the artifact in a runtime environment
- [ ] 6. **Processes** - Execute the app as one or more stateless processes
  - [ ] Do NOT store state in the application (covered by REST)
  - [ ] DO Store state in a backing service, e.g. a database
- [ ] 7. **Port binding** - Export services via port binding
  - [ ] Use a web server to bind to a port and serve the application
- [ ] 8. **Concurrency** - Scale out via the process model (horizontally)
  - [ ] Use a reverse proxy or API Gateway to handle multiple instances of the application
- [ ] 9. **Disposability** - Maximize robustness with fast startup and graceful shutdown ("treat deployments/hardware as cattle, not pets")
  - [ ] Use a reverse proxy or API Gateway to handle graceful shutdown (if applicable)
- [ ] 10. **(Not talked about in this section)** **Dev/prod parity** - Keep development, staging, and production as similar as possible
- [ ] 11. **(Not talked about in this section)** **Logs** - Treat logs as event streams
  - [ ] Log to stdout/stderr
  - [ ] Use a log aggregator, e.g. AWS CloudWatch, to collect logs
- [ ] 12. **(Not talked about in this section)** **Admin processes** - Run admin/management tasks as one-off processes

## Extra

- [ ] Decide if you will version your API endpoints in code or at the API Gateway level
- [ ] Config (`pydantic.BaseSettings` is excellent for this)
  - [ ] Validate configuration
  - [ ] Support any or all of the following config sources in the following order of precedence: (note that often, only implementing environment variables is sufficient, but for widely adopted, large, or complex applications, supporting other config sources is helpful)
    - 1. CLI arguments (highest precedence)
    - 2. Environment variables
    - 3. Config files, e.g. JSON, YAML, TOML
    - 4. Defaults, constant or derived values in code (lowest precedence)

## Beyond this course

- [ ] Decide if authentication is needed--prefer keeping it out of the application and using a reverse proxy or API Gateway to handle authentication
- [ ] Support authorization within the application, e.g. using OAuth 2.0 JWT scopes
- [ ] Support multitenancy