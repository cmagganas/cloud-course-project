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

### Running the Application

You can run the application in several ways:

1. Using `uv` (recommended for development):
   ```bash
   make run-uv
   ```
   This will:
   - Load environment variables from `.env`
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
