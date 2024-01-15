from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Education(models.Model):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    start_date = models.CharField(max_length=4)
    end_date = models.CharField(max_length=4)

    def __str__(self):
        return self.name

class Experience(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(max_length=4)
    end_date = models.CharField(max_length=4)
    place = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Language(models.Model):
    level_choice = (
        ('beg', 'Beginner'),
        ('int', 'Intermediate'),
        ('flu', 'fluent'),
        ('nat', 'native')
    )

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100, choices=level_choice)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class InterestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Interest(models.Model):
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Repository(models.Model):
    """Represents a github repository for the projects page"""

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    readme = models.TextField()
    homepage = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, primary_key=True)
    stars = models.IntegerField()
