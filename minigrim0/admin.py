from django.contrib import admin

import minigrim0.models as models

@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    def move_up(self, request, queryset):
        for obj in queryset:
            obj.move(up=True)

    def move_down(self, request, queryset):
        for obj in queryset:
            obj.move(up=False)

    list_display = ("name", "place", "start_date", "end_date", "_order")
    actions = ["move_up", "move_down"]


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    def move_up(self, request, queryset):
        for obj in queryset:
            obj.move(up=True)

    def move_down(self, request, queryset):
        for obj in queryset:
            obj.move(up=False)

    list_display = ("name", "place", "start_date", "end_date", "_order")
    actions = ["move_up", "move_down"]


@admin.register(models.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    def move_up(self, request, queryset):
        for obj in queryset:
            obj.move(up=True)

    def move_down(self, request, queryset):
        for obj in queryset:
            obj.move(up=False)

    list_display = ("name", "date", "_order")
    actions = ["move_up", "move_down"]


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
