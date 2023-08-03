import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "vairy-sea-cret-kee")
    REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
