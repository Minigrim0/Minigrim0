# Generated by Django 5.1.1 on 2024-12-03 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='short_description',
            field=models.TextField(default=''),
        ),
    ]
