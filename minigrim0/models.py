from django.db import models, transaction

from minigrim0.utils import latex_markdown

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

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)
    
    @property
    def place_latex(self) -> str:
        return latex_markdown(self.place)
    
    @property
    def start_date_latex(self) -> str:
        return latex_markdown(self.start_date)
    
    @property
    def end_date_latex(self) -> str:
        return latex_markdown(self.end_date)

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

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)
    
    @property
    def description_latex(self) -> str:
        return latex_markdown(self.description) if self.description else ""
    
    @property
    def start_date_latex(self) -> str:
        return latex_markdown(self.start_date)
    
    @property
    def end_date_latex(self) -> str:
        return latex_markdown(self.end_date)
    
    @property
    def place_latex(self) -> str:
        return latex_markdown(self.place)
    
    @property
    def link_latex(self) -> str:
        return latex_markdown(self.link) if self.link else ""

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

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)
    
    @property
    def description_latex(self) -> str:
        return latex_markdown(self.description) if self.description else ""
    
    @property
    def date_latex(self) -> str:
        return latex_markdown(self.date)

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

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)

    def __str__(self) -> str:
        return self.name


class SkillCategory(Orderable):
    name = models.CharField(max_length=100)

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)

    def __str__(self) -> str:
        return self.name


class SkillSubCategory(Orderable):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("minigrim0.SkillCategory", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)

    def __str__(self) -> str:
        if self.category is not None:
            return f"{self.name} - {self.category.name}"
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True, help_text="Markdown is supported")
    category = models.ForeignKey('minigrim0.SkillSubCategory', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)

    @property
    def details_latex(self) -> str:
        return latex_markdown(self.details)

    def __str__(self) -> str:
        return self.name


class InterestCategory(models.Model):
    name = models.CharField(max_length=100)

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)

    def __str__(self) -> str:
        return self.name


class Interest(models.Model):
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)

    def __str__(self) -> str:
        return self.name


class CVProfile(models.Model):
    """Profile information for CV generation"""
    profile_image = models.ImageField(
        upload_to='cv_images/', 
        null=True, 
        blank=True,
        help_text="Profile image for CV (recommended: square format, 200x200px)"
    )
    name = models.CharField(max_length=100, default="Florent Grimau")
    title = models.CharField(max_length=200, default="Master Student in Embedded Systems")
    address = models.CharField(max_length=200, default="Stockholm - Sweden")
    email = models.EmailField(default="grimauflorent@gmail.com")
    github_username = models.CharField(max_length=100, default="Minigrim0")
    birth_date = models.CharField(max_length=20, default="22 Sept 2000")
    professional_summary = models.TextField(
        default="Passionate about embedded systems and low-level programming. Experienced in C, C++, Python, and Rust. Skilled in microcontroller programming, real-time operating systems, and hardware interfacing. Strong problem-solving abilities and a collaborative team player.",
        help_text="Markdown is supported"
    )

    class Meta:
        verbose_name = "CV Profile"
        verbose_name_plural = "CV Profile"
    
    @property
    def name_latex(self) -> str:
        return latex_markdown(self.name)
    
    @property
    def title_latex(self) -> str:
        return latex_markdown(self.title)
    
    @property
    def address_latex(self) -> str:
        return latex_markdown(self.address)
    
    @property
    def github_username_latex(self) -> str:
        return latex_markdown(self.github_username)
    
    @property
    def professional_summary_latex(self) -> str:
        return latex_markdown(self.professional_summary)
    
    def __str__(self) -> str:
        return f"CV Profile for {self.name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one profile exists
        if not self.pk and CVProfile.objects.exists():
            raise ValueError("Only one CV profile can exist. Please edit the existing one.")
        return super().save(*args, **kwargs)
