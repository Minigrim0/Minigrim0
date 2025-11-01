import logging
from pathlib import Path

import coloredlogs
import environ

from minigrim0.secrets import get_secret, get_database_url, validate_production_secrets

logger = logging.getLogger("Minigrim0")

env = environ.Env(
    SECRET_KEY=(str, "randomSecretKey"),
    DEBUG=(bool, False),
    CI=(bool, False),
    LOGLEVEL=(str, "INFO"),
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=BASE_DIR / ".env")
coloredlogs.install(level=env("LOGLEVEL", default="INFO"))


DEBUG = env("DEBUG", default=False)

# Validate production secrets early - fail fast if misconfigured
if not DEBUG:
    validate_production_secrets()
    logger.info("Production secrets validated successfully")

# Secret key - no default in production for security
SECRET_KEY = get_secret("SECRET_KEY", default="dev-secret-key-change-in-production" if DEBUG else None, required=not DEBUG)

if DEBUG:
    logger.warning("Application is running in DEBUG mode.")

# Service URLs and configuration
REDIS_URL = get_secret("REDIS_URL", default="redis://localhost:6379")
PLAUSIBLE_URL = get_secret("PLAUSIBLE_URL", default=None)
PLAUSIBLE_DOMAIN = get_secret("PLAUSIBLE_DOMAIN", default=None)

# Allowed hosts - from secret in production, default in dev
ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS", default="localhost,127.0.0.1" if DEBUG else None, required=not DEBUG).split(",")
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "colorfield",
    "minigrim0",
    "blog",
    "devlog",
    "import_export",
    "rest_framework",
    "knox",
    "django_tex",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "minigrim0.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "minigrim0.context_processors.plausible_url",
            ],
        },
    },
    {
        'NAME': 'tex',
        'BACKEND': 'django_tex.engine.TeXEngine',
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = "minigrim0.wsgi.application"

DATABASES = {
    "default": env.db("DATABASE_URL", default=get_database_url(debug=DEBUG)),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = ("minigrim0/assets/",)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# PRODUCTION SECURITY SETTINGS
# ==============================================================================
# These settings are enabled in production (DEBUG=False) to ensure secure
# communication and protect against common web vulnerabilities.
# References:
# - https://docs.djangoproject.com/en/5.2/topics/security/
# - https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SSL/HTTPS Configuration
# Redirect all HTTP traffic to HTTPS in production
SECURE_SSL_REDIRECT = not DEBUG

# Only send cookies over HTTPS in production
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Trust X-Forwarded-Proto header from Traefik proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security Headers
# Prevent browsers from guessing content types
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser XSS filtering
SECURE_BROWSER_XSS_FILTER = True

# Prevent site from being embedded in frames (clickjacking protection)
X_FRAME_OPTIONS = 'DENY'

# HTTP Strict Transport Security (HSTS)
# Tell browsers to only access site via HTTPS for 1 year
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Session Security
# Session cookie expires when browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Regenerate session on login to prevent session fixation attacks
SESSION_SAVE_EVERY_REQUEST = False

# CSRF Protection
# Additional CSRF protection settings
CSRF_COOKIE_HTTPONLY = False  # Must be False for JavaScript access
CSRF_USE_SESSIONS = False  # Store CSRF token in cookie, not session

# Logging Configuration for Production
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }
