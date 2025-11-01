"""
Secrets management for Django application.

Supports both Docker Swarm secrets (production) and environment variables (development).
Docker Swarm secrets are mounted at /run/secrets/<secret_name> as files.
"""

import os
from pathlib import Path
from typing import Optional


def get_secret(secret_name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Read a secret from Docker Swarm secrets or environment variables.

    Priority order:
    1. Docker Swarm secret at /run/secrets/<secret_name>
    2. Environment variable with same name
    3. Default value (if provided)
    4. Raise error if required=True and not found

    Args:
        secret_name: Name of the secret/environment variable
        default: Default value if secret not found
        required: If True, raise ValueError when secret not found

    Returns:
        Secret value as string, or None if not found and not required

    Raises:
        ValueError: If required=True and secret not found

    Example:
        # In production with Docker secrets:
        SECRET_KEY = get_secret("DJANGO_SECRET_KEY", required=True)

        # In development with .env file:
        SECRET_KEY = get_secret("SECRET_KEY", default="dev-secret-key")
    """
    # Try to read from Docker Swarm secret file
    secret_path = Path(f"/run/secrets/{secret_name}")

    if secret_path.exists() and secret_path.is_file():
        try:
            value = secret_path.read_text().strip()
            if value:
                return value
        except (IOError, PermissionError) as e:
            # Log the error but continue to fallback
            print(f"Warning: Could not read secret from {secret_path}: {e}")

    # Fallback to environment variable
    value = os.getenv(secret_name)
    if value is not None:
        return value

    # Use default if provided
    if default is not None:
        return default

    # Raise error if required
    if required:
        raise ValueError(
            f"Required secret '{secret_name}' not found. "
            f"Expected at /run/secrets/{secret_name} or in environment variables."
        )

    return None


def get_database_url(debug: bool = False) -> str:
    """
    Construct DATABASE_URL from individual secrets or environment variable.

    In production (DEBUG=False), reads individual secrets:
    - DB_USER
    - DB_PASSWORD
    - DB_HOST
    - DB_NAME
    - DB_PORT (optional, defaults to 5432)

    In development (DEBUG=True), reads DATABASE_URL environment variable.

    Args:
        debug: Whether running in debug mode

    Returns:
        PostgreSQL connection URL

    Raises:
        ValueError: If required database secrets not found in production

    Example:
        DATABASES = {
            "default": env.db_url("DATABASE_URL", default=get_database_url(debug=DEBUG))
        }
    """
    # In development, use DATABASE_URL env var if present
    if debug:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
        # Fallback to SQLite for local dev
        return "sqlite:///db.sqlite3"

    # In production, construct URL from individual secrets
    db_user = get_secret("DB_USER", required=True)
    db_password = get_secret("DB_PASSWORD", required=True)
    db_host = get_secret("DB_HOST", required=True)
    db_name = get_secret("DB_NAME", required=True)
    db_port = get_secret("DB_PORT", default="5432")

    return f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def validate_production_secrets() -> None:
    """
    Validate that all required secrets exist for production deployment.

    Call this early in Django startup to fail fast if misconfigured.

    Raises:
        ValueError: If any required production secret is missing

    Example:
        # In settings.py
        if not DEBUG:
            validate_production_secrets()
    """
    required_secrets = [
        "SECRET_KEY",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_NAME",
        "ALLOWED_HOSTS",
    ]

    missing = []
    for secret_name in required_secrets:
        if get_secret(secret_name) is None:
            missing.append(secret_name)

    if missing:
        raise ValueError(
            f"Missing required production secrets: {', '.join(missing)}. "
            f"Secrets must be available at /run/secrets/<name> or as environment variables."
        )
