from django.db import models


class Repository(models.Model):
    """Represents a github repository for the projects page"""

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True, blank=True)
    readme = models.TextField(null=True, blank=True)
    homepage = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, primary_key=True)
    stars = models.IntegerField()
    active = models.BooleanField(default=True)  # Use this to disable a repository from the projects page rather than deleting it