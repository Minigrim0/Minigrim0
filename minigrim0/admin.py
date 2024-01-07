from django.contrib import admin 

import minigrim0.models as models

@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "start_date", "end_date")


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "start_date", "end_date")


@admin.register(models.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "date")


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "level")


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level")


@admin.register(models.InterestCategory)
class InterestCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("name", "category")


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
