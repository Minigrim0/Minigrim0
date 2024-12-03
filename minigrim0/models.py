from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction


class Orderable(models.Model):
    _order = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True

    def move(self, up: bool = True):
        """Move the object in the list"""

        if up and self._order > 1:
            other = self.__class__.objects.get(_order=self._order - 1)
        elif not up and Experience.objects.count() > self._order:
            other = self.__class__.objects.get(_order=self._order + 1)
        else:
            return

        with transaction.atomic():
            self._order, other._order = other._order, self._order
            self.save()
            other.save()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self._order = self.__class__.objects.count() + 1
        return super().save(*args, **kwargs)


class Education(Orderable):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255, help_text="Markdown is supported")
    start_date = models.CharField(max_length=4)
    end_date = models.CharField(max_length=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["_order"],
                name="_order_unique_education",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Experience(Orderable):
    name = models.CharField(verbose_name="experience_name", max_length=100)
    description = models.TextField(null=True, blank=True, help_text="Markdown is supported")
    start_date = models.CharField(max_length=4)
    end_date = models.CharField(max_length=4)
    place = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["_order"],
                name="_order_unique_expeerience",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Competition(Orderable):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["_order"],
                name="_order_unique_competition",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    level_choice = (
        ("beg", "Beginner"),
        ("int", "Intermediate"),
        ("flu", "fluent"),
        ("nat", "native"),
    )

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100, choices=level_choice)

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    details = models.TextField(null=True, blank=True, help_text="Markdown is supported")

    def __str__(self) -> str:
        return self.name


class InterestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Interest(models.Model):
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
