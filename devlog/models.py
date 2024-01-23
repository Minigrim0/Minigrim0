from django.db import models


class Repository(models.Model):
    """Represents a github repository for the projects page"""

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    readme = models.TextField()
    homepage = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, primary_key=True)
    stars = models.IntegerField()
