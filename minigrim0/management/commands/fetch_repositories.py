import json
import redis
from django.core.management.base import BaseCommand
from django.conf import settings
from devlog.models import Repository
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Fetches repositories from redis and updates/adds them to the database
    """

    def handle(self, *args, **kwargs):
        redis_url = getattr(settings, 'REDIS_URL', None)
        if not redis_url:
            logger.error("REDIS_URL is not set in the settings.")
            return

        redis_client = redis.from_url(redis_url)
        if not redis_client.ping():
            logger.error(f"Failed to connect to Redis at {redis_url}")
            return

        # Fetch all keys starting with 'miniwebsite:'
        keys = redis_client.keys('miniwebsite:*')

        for key in keys:
            repo_data_str = redis_client.get(key)
            if not repo_data_str:
                logger.error(f"No data found for key: {key}")
                continue

            repo_data = json.loads(repo_data_str)
            if not isinstance(repo_data, dict):
                logger.error(f"Invalid data format for key: {key}")
                continue

            repo_name = repo_data.get('name', '')

            repo = Repository.objects.filter(name=repo_name).first()
            if repo:
                # Update existing repository
                repo.description = repo_data.get('description', repo.description)
                repo.readme = repo_data.get('readme', repo.readme)
                repo.homepage = repo_data.get('homepage', repo.homepage)
                repo.url = repo_data.get('url', repo.url)
                repo.stars = repo_data.get('stars', repo.stars)
                repo.active = True  # The repo is found, it must be active
                repo.save()
                logger.info(f"Updated repository: {repo_name}")
            else:
                # Create new repository
                Repository.objects.create(
                    name=repo_name,
                    description=repo_data.get('description', ''),
                    readme=repo_data.get('readme', ''),
                    homepage=repo_data.get('homepage', ''),
                    url=repo_data.get('url', ''),
                    stars=repo_data.get('stars', 0),
                    active=True
                )
                logger.info(f"Created new repository: {repo_name}")

        # Remove repositories that are no longer in Redis
        db_repos = set(Repository.objects.values_list('name', flat=True))
        redis_repos = set(key.split(b':')[1].decode('utf-8') for key in keys)
        repos_to_remove = db_repos - redis_repos

        if repos_to_remove:
            Repository.objects.filter(name__in=repos_to_remove).update(active=False)
            logger.info(f"Disabled repositories: {', '.join(repos_to_remove)}")

        logger.info("Repository synchronization completed.")
