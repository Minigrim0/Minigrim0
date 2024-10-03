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

    def __str__(self) -> str:
        return self.name
    
    @property
    def related_posts(self) -> int:
        return self.posts.count()


class Tag(models.Model):
    """Represents a tag for a dev log post"""

    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class DevLog(models.Model):
    """Represents a dev log post"""

    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", blank=True)
    image = models.ImageField(upload_to="devlog/", blank=True, null=True)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.title
