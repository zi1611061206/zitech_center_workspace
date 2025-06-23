# Virtual Environment Setup for zi-coder-agent

This guide provides instructions for setting up a virtual environment for the `zi-coder-agent` project using either `uv` (a modern Python package manager designed for speed and simplicity) or `pip` (the standard Python package manager). By following these instructions, you ensure that your development environment is properly isolated and configured with all necessary dependencies.

## Prerequisites

- **Python 3.9+**: Ensure you have Python 3.9 or higher installed on your system.
- **UV (Optional)**: If you choose to use `uv`, install it if you haven't already. You can install it via pip or follow the instructions on the official [UV GitHub page](https://github.com/astral-sh/uv).

  ```bash
  pip install uv
  ```

- **Pip**: `pip` comes bundled with Python, so no additional installation is required if Python is installed.

## Setting Up the Virtual Environment

### Option 1: Using UV

1. **Clone the Repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd zi-coder-agent
   ```

2. **Create a Virtual Environment with UV**:

   Use `uv` to create a virtual environment. This will isolate project dependencies from your global Python environment.

   ```bash
   uv venv
   ```

   This command creates a virtual environment in the `.venv` directory within the project root.

3. **Activate the Virtual Environment**:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

   Once activated, your terminal prompt should change to indicate that the virtual environment is active.

4. **Install Dependencies**:

   Use `uv` to install the project dependencies as defined in `pyproject.toml`.

   ```bash
   uv sync
   ```

   This command installs all dependencies (both regular and dev-dependencies) specified under `[project.dependencies]` and `[project.optional-dependencies.dev]` in `pyproject.toml`.

5. **Verify Installation**:

   You can verify that the dependencies were installed correctly by checking the virtual environment's site-packages or by running:

   ```bash
   uv pip list
   ```

### Option 2: Using Pip

1. **Clone the Repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd zi-coder-agent
   ```

2. **Create a Virtual Environment with Pip**:

   Use Python's built-in `venv` module to create a virtual environment.

   ```bash
   python -m venv .venv
   ```

   This command creates a virtual environment in the `.venv` directory within the project root.

3. **Activate the Virtual Environment**:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

   Once activated, your terminal prompt should change to indicate that the virtual environment is active.

4. **Install Dependencies**:

   Use `pip` to install the project dependencies using the provided requirements files. These files list all necessary dependencies as defined in `pyproject.toml`, making installation straightforward.

   Install the main project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Optionally, install development dependencies (for testing, linting, etc.):

   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Verify Installation**:

   You can verify that the dependencies were installed correctly by running:

   ```bash
   pip list
   ```

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```

This will return you to your global Python environment.

## Dependency Information

Below is a comprehensive list of dependencies for the `zi-coder-agent` project as defined in `pyproject.toml`. This includes both main project dependencies and optional development dependencies.

### Main Dependencies

These are required for the core functionality of the `zi-coder-agent` project:

- **Flask (>=2.0.1)**: A lightweight WSGI web application framework for building web applications.
- **SQLAlchemy (>=1.4.41)**: A SQL toolkit and Object-Relational Mapping (ORM) library for database interactions.
- **Alembic (>=1.8.1)**: A lightweight database migration tool for use with SQLAlchemy.
- **redis (>=4.0.2)**: A client for interacting with Redis, an in-memory data structure store used for caching.
- **celery (>=5.2.7)**: A distributed task queue for handling asynchronous tasks and workers.
- **pymysql (>=1.0.2)**: A pure-Python MySQL client library for database connections.
- **flask-swagger-ui (>=4.11.1)**: A Flask extension for integrating Swagger UI to document API endpoints.

### Development Dependencies

These are optional and used for development, testing, and code quality assurance:

- **pytest (>=7.1.2)**: A testing framework for writing simple and scalable test cases.
- **pytest-cov (>=4.0.0)**: A pytest plugin for measuring code coverage.
- **black (>=22.10.0)**: An uncompromising code formatter for Python.
- **isort (>=5.10.1)**: A utility for sorting imports alphabetically and automatically separating them into sections.
- **pylint (>=2.15.5)**: A static code analysis tool for identifying errors and enforcing coding standards.
- **flake8 (>=5.0.4)**: A tool for style guide enforcement and linting.
- **ruff (>=0.0.292)**: A fast Python linter, written in Rust.
- **djlint (>=1.19.7)**: A linter for Django templates.
- **yamllint (>=1.28.0)**: A linter for YAML files.
- **pre-commit (>=2.20.0)**: A framework for managing and maintaining multi-language pre-commit hooks.

## Additional Notes

- **Updating Dependencies**: 
  - With `uv`, if `pyproject.toml` is updated with new dependencies, run `uv sync` again to ensure your virtual environment is up-to-date.
  - With `pip`, manually install any new dependencies listed in `pyproject.toml` or updates to existing ones using `pip install`.
- **Project Structure**: The virtual environment is located in `.venv` at the root of the project directory, keeping it separate from the source code and other project files.
- **UV Documentation**: For more advanced usage of `uv`, refer to the official documentation at [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv).
- **Pip Documentation**: For more information on using `pip` and virtual environments, refer to the official Python documentation at [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html).

By following these steps, you ensure that your development environment for `zi-coder-agent` is properly isolated and configured with all necessary dependencies, whether using `uv` or `pip`.
