from django.contrib import admin
from devlog import models


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
