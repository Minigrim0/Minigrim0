from django.contrib import admin
from blog import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "date_posted")
    readonly_fields = ["slug",]

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
