import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from devlog.models import Repository
from minigrim0.models import (
    Competition,
    Education,
    Experience,
    Interest,
    InterestCategory,
    Language,
    Skill,
)

fake = Faker()


class Command(BaseCommand):
    help = "Generates fake data for the database"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")

        # Generate Education
        for _ in range(5):
            Education.objects.create(
                name=fake.company(),
                place=fake.city(),
                start_date=str(fake.year()),
                end_date=str(fake.year()),
            )

        # Generate Experience
        for _ in range(5):
            Experience.objects.create(
                name=fake.job(),
                place=fake.company(),
                start_date=str(fake.year()),
                end_date=str(fake.year()),
                link=fake.url(),
            )

        # Generate Competition
        for _ in range(3):
            Competition.objects.create(
                name=fake.catch_phrase(),
                description=fake.text(),
                date=str(fake.year()),
            )

        # Generate Language
        for _ in range(3):
            Language.objects.create(
                name=fake.language_name(),
                level=random.choice(["beg", "int", "adv", "flu", "nat"]),
            )

        # Generate Skill
        for _ in range(10):
            Skill.objects.create(name=fake.job(), level=random.randint(1, 5), details=fake.paragraph())

        # Generate InterestCategory and Interest
        for _ in range(3):
            category = InterestCategory.objects.create(name=fake.word())
            for _ in range(random.randint(2, 5)):
                Interest.objects.create(name=fake.word(), category=category)

        # Generate Repository
        for _ in range(10):
            Repository.objects.create(
                name=fake.word(),
                description=fake.sentence(),
                readme=fake.text(),
                homepage=fake.url() if random.choice([True, False]) else None,
                url=fake.url(),
                stars=random.randint(0, 1000),
            )

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
