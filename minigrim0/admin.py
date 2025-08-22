from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

import minigrim0.models as models


@admin.register(models.Education)
class EducationAdmin(ImportExportModelAdmin):
    def move_up(self, request, queryset):
        for obj in queryset:
            obj.move(up=True)

    def move_down(self, request, queryset):
        for obj in queryset:
            obj.move(up=False)

    list_display = ("name", "place", "start_date", "end_date", "_order")
    actions = ["move_up", "move_down"]


@admin.register(models.Experience)
class ExperienceAdmin(ImportExportModelAdmin):
    def move_up(self, request, queryset):
        for obj in queryset:
            obj.move(up=True)

    def move_down(self, request, queryset):
        for obj in queryset:
            obj.move(up=False)

    list_display = ("name", "place", "start_date", "end_date", "_order")
    actions = ["move_up", "move_down"]


@admin.register(models.Competition)
class CompetitionAdmin(ImportExportModelAdmin):
    def move_up(self, request, queryset):
        for obj in queryset:
            obj.move(up=True)

    def move_down(self, request, queryset):
        for obj in queryset:
            obj.move(up=False)

    list_display = ("name", "date", "_order")
    actions = ["move_up", "move_down"]


@admin.register(models.Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ("name", "level")


@admin.register(models.Skill)
class SkillAdmin(ImportExportModelAdmin):
    list_display = ("name", "level")


@admin.register(models.InterestCategory)
class InterestCategoryAdmin(ImportExportModelAdmin):
    list_display = ("name",)


@admin.register(models.Interest)
class InterestAdmin(ImportExportModelAdmin):
    list_display = ("name", "category")


@admin.register(models.CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow adding if no profile exists
        return not models.CVProfile.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion to maintain single profile
        return False
    
    list_display = ("name", "email", "title")
    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "title", "email", "birth_date")
        }),
        ("Contact & Social", {
            "fields": ("address", "github_username")
        }),
        ("Profile Image", {
            "fields": ("profile_image",),
            "description": "Upload a profile image for your CV (recommended: square format, 200x200px)"
        }),
    )
