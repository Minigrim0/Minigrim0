from django.shortcuts import render
from django_tex.shortcuts import render_to_pdf

from minigrim0 import models

from minigrim0.utils import latex_markdown


def index(request):
    cv_profile = models.CVProfile.objects.first()
    return render(request, "minigrim0/index.html", {"page_name": "Home", "cv_profile": cv_profile})


def cv(request):
    cv_profile = models.CVProfile.objects.first()
    cv_data = {
        "edu": models.Education.objects.all(),
        "exp": models.Experience.objects.all(),
        "com": models.Competition.objects.all().order_by("-_order"),
        "lan": models.Language.objects.all(),
        "ski": models.Skill.objects.all().order_by("-level"),
        "int": models.Interest.objects.all(),
        "profile": cv_profile,
    }

    return render(request, "minigrim0/cv.html", {"page_name": "CV", "cv": cv_data})


def cv_pdf(request):
    """Generate CV PDF from LaTeX template"""
    try:
        profile = models.CVProfile.objects.first()
        if profile:
            # Process all profile text fields
            if hasattr(profile, 'professional_summary'):
                profile.professional_summary = latex_markdown(profile.professional_summary)
            profile.name = latex_markdown(profile.name)
            profile.title = latex_markdown(profile.title)
            profile.address = latex_markdown(profile.address)
            profile.github_username = latex_markdown(profile.github_username)
    except models.CVProfile.DoesNotExist:
        profile = None
    
    # Process all experience fields
    experiences = list(models.Experience.objects.all())
    for exp in experiences:
        exp.name = latex_markdown(exp.name)
        exp.place = latex_markdown(exp.place)
        exp.start_date = latex_markdown(exp.start_date)
        exp.end_date = latex_markdown(exp.end_date)
        if exp.description:
            exp.description = latex_markdown(exp.description)
        if exp.link:
            exp.link = latex_markdown(exp.link)
    
    # Process all education fields
    educations = list(models.Education.objects.all())
    for edu in educations:
        edu.name = latex_markdown(edu.name)
        edu.place = latex_markdown(edu.place)
        edu.start_date = latex_markdown(edu.start_date)
        edu.end_date = latex_markdown(edu.end_date)
        if hasattr(edu, 'description') and edu.description:
            edu.description = latex_markdown(edu.description)
    
    # Process all competition fields
    competitions = list(models.Competition.objects.all().order_by("-_order"))
    for comp in competitions:
        comp.name = latex_markdown(comp.name)
        comp.date = latex_markdown(comp.date)
        if comp.description:
            comp.description = latex_markdown(comp.description)
    
    # Process languages
    languages = list(models.Language.objects.all())
    for lang in languages:
        lang.name = latex_markdown(lang.name)
    
    # Process skills
    skills_cat = dict([(latex_markdown(skill_cat.name), {}) for skill_cat in models.SkillCategory.objects.all().order_by("_order")])
    for skill_name, category in zip(skills_cat.keys(), models.SkillCategory.objects.all().order_by("_order")):
        skills_cat[skill_name] = {}
        for skill_subcat in category.skillsubcategory_set.order_by("_order"):
            skills_cat[skill_name][latex_markdown(skill_subcat.name)] = list(skill_subcat.skill_set.all())

    from pprint import pprint
    pprint(skills_cat)

    # Process interests
    interests = list(models.Interest.objects.all())
    for interest in interests:
        interest.name = latex_markdown(interest.name)
        if hasattr(interest, 'category') and interest.category:
            interest.category.name = latex_markdown(interest.category.name)
    
    cv_data = {
        "edu": educations,
        "exp": experiences,
        "com": competitions,
        "lan": languages,
        "skill_cats": skills_cat,
        "int": interests,
        "profile": profile,
    }
    
    return render_to_pdf(request, 'cv.tex', cv_data, filename='cv.pdf')

def error(request, error_type):
    return render(request, "error.html", {"page_name": "Error", "error": error_type})
