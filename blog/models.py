import logging

from colorfield.fields import ColorField
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

logger = logging.getLogger(__file__)


class Post(models.Model):
    """Represents a blog post"""

    title = models.CharField(max_length=100)
    short_description = models.CharField(default="", max_length=200)
    content = models.TextField()
    date_updated = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField("Tag", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, primary_key=True, default="")

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """
        Save the model and add initial slug/pk value if needed
        """
        logger.info("Saving model")

        expected_slug = slugify(self.title)
        if self.pk != expected_slug:
            logger.info("New post created, setting slug")
            self.slug = expected_slug
        logger.info("Instance pk: %s", self.pk)

        super().save(*args, **kwargs)


class PostImage(models.Model):
    """Represents an image in a blog post"""

    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    alt = models.TextField()
    image = models.ImageField()


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
    color = ColorField(default="#FF0000")

    def __str__(self) -> str:
        return self.name
