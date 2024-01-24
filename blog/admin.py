from django.contrib import admin
from blog import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_posted")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
