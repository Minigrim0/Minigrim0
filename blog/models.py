from django.db import models
from colorfield.fields import ColorField


class Post(models.Model):
    """Represents a blog post"""

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_updated = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField('Tag', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Represents a comment to a blog post"""

    pseudo = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.pseudo


class Tag(models.Model):
    """Represents a tag for a blog post"""

    name = models.CharField(max_length=100)
    color = ColorField(default='#FF0000')

    def __str__(self) -> str:
        return self.name
