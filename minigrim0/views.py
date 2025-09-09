from django.shortcuts import render
from django_tex.shortcuts import render_to_pdf
from itertools import groupby
from operator import attrgetter

from minigrim0 import models


def index(request):
    cv_profile = models.CVProfile.objects.first()
    return render(request, "minigrim0/index.html", {"page_name": "Home", "cv_profile": cv_profile})


def cv(request):
    cv_profile = models.CVProfile.objects.first()
    
    # Organize skills by category and subcategory for HTML display
    skill_categories = []
    for skill_cat in models.SkillCategory.objects.all().order_by("_order"):
        category_data = {
            'name': skill_cat.name,
            'subcategories': []
        }
        for skill_subcat in skill_cat.skillsubcategory_set.all().order_by("_order"):
            subcat_data = {
                'name': skill_subcat.name,
                'skills': list(skill_subcat.skill_set.all())
            }
            category_data['subcategories'].append(subcat_data)
        skill_categories.append(category_data)
    
    cv_data = {
        "edu": models.Education.objects.all().order_by("_order"),
        "exp": models.Experience.objects.all().order_by("_order"),
        "com": models.Competition.objects.all().order_by("-_order"),
        "lan": models.Language.objects.all(),
        "skill_categories": skill_categories,
        "int": models.Interest.objects.all(),
        "profile": cv_profile,
    }

    return render(request, "minigrim0/cv.html", {"page_name": "CV", "cv": cv_data})


def cv_pdf(request):
    """Generate CV PDF from LaTeX template"""
    profile = models.CVProfile.objects.first()
    
    # Simple querysets - LaTeX processing handled by model properties
    educations = models.Education.objects.all().order_by("_order")
    experiences = models.Experience.objects.all().order_by("_order")
    competitions = models.Competition.objects.all().order_by("-_order")
    languages = models.Language.objects.all()
    
    # Process skills - group by category and subcategory
    skill_cats = {}
    for skill_cat in models.SkillCategory.objects.all().order_by("_order"):
        skill_cats[skill_cat.name_latex] = {}
        for skill_subcat in skill_cat.skillsubcategory_set.all().order_by("_order"):
            skill_cats[skill_cat.name_latex][skill_subcat.name_latex] = list(skill_subcat.skill_set.all())
    
    # Process interests - group by category using model properties
    interests_query = models.Interest.objects.select_related('category').order_by('category__name')
    interest_categories = []
    for category_name, interests_group in groupby(interests_query, key=attrgetter('category.name')):
        interests_list = list(interests_group)  # Convert to list first
        if interests_list:  # Only if there are interests in this category
            interest_categories.append({
                'name': interests_list[0].category.name_latex,  # Get category from first interest
                'interests': [interest.name_latex for interest in interests_list]
            })
    
    cv_data = {
        "edu": educations,
        "exp": experiences,
        "com": competitions,
        "lan": languages,
        "skill_cats": skill_cats,
        "interest_categories": interest_categories,
        "profile": profile,
    }
    
    return render_to_pdf(request, 'cv.tex', cv_data, filename='cv.pdf')

def error(request, error_type):
    return render(request, "error.html", {"page_name": "Error", "error": error_type})
