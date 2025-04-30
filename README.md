# cloud-course-project

## Quick start

```bash
pip install cloud-course-project
```

## Developing/Contributing

### System requirements

You will need the following installed on your machine to develop on this codebase

- `make` AKA `cmake`, e.g. `sudo apt-get update -y; sudo apt-get install cmake -y`
- Python 3.7+, ideally using `pyenv` to easily change between Python versions
- `git`

###

```bash
# clone the repo
git clone https://github.com/<your github username>/cloud-course-project.git

# install the dev dependencies
make install

# run the tests
make test
```

## Development

### Environment Setup

1. Copy the example environment file to create your own:
   ```bash
   cp env.example .env
   ```

2. Edit the `.env` file to set your AWS credentials and other configuration:
   ```bash
   # Important settings to update:
   AWS_PROFILE=your-aws-profile
   AWS_REGION=your-aws-region
   S3_BUCKET_NAME=your-s3-bucket-name
   ```

   The application uses your AWS profile for authentication. Make sure this profile exists in your `~/.aws/credentials` file.

3. For Cognito authentication to work, make sure to update the Cognito settings in the `.env` file.

### Running the Application

You can run the application in several ways:

1. Using `uv` (recommended for development):
   ```bash
   make run-uv
   ```
   This will:
   - Automatically load environment variables from `.env`
   - Use `uv` to run the application
   - Provide hot-reloading for development

2. Using `uvicorn` directly:
   ```bash
   make run
   ```

3. Using Docker:
   ```bash
   make run-docker
   ```

4. Using mocked AWS services:
   ```bash
   make run-mock
   ```

### Other Commands

- `make install` - Install dependencies
- `make lint` - Run linting
- `make test` - Run tests
- `make clean` - Clean build artifacts
- `make help` - Show all available commands

```python
from files_api import ...
```

## Frontend Authentication UI

A simple authentication UI is integrated directly into the FastAPI application. 
To access the authentication UI:

1. Start the application:
   ```bash
   make run-uv
   ```

2. Access the authentication UI through your browser:
   ```
   http://localhost:8000/auth
   ```
   
   Or simply open the root URL which redirects to the auth page:
   ```
   http://localhost:8000
   ```

3. Use the login and logout buttons to authenticate with Cognito.

The UI is lightweight and served directly from FastAPI without requiring a separate frontend build process, making it suitable for AWS Lambda deployments.

### Environment Configuration

Authentication settings are configured in your `.env` file. See the provided `env.example` for all required settings.
