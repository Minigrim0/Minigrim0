# Generated by Django 5.0.1 on 2024-01-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("minigrim0", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="repository",
            name="id",
        ),
        migrations.AlterField(
            model_name="repository",
            name="url",
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
    ]
