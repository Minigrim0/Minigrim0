from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from devlog.models import Repository
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Fetches repositories from redis and updates/adds them to the database
    """

    def handle(self, *args, **kwargs):
        if hasattr(settings, "REDIS_URL"):
            redis_url = settings.REDIS_URL
        else:
            logger.warning("No Redis URL found, using default")
            redis_url = "redis://127.0.0.1/"

        client = redis.from_url(redis_url)
        

        for repo in client.keys("miniwebsite:*"):
            print(repo)