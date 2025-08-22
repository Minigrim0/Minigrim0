from django.shortcuts import render
from django_tex.shortcuts import render_to_pdf

from minigrim0 import models


def index(request):
    return render(request, "minigrim0/index.html", {"page_name": "Home"})


def cv(request):
    cv_data = {
        "edu": models.Education.objects.all(),
        "exp": models.Experience.objects.all(),
        "com": models.Competition.objects.all().order_by("-_order"),
        "lan": models.Language.objects.all(),
        "ski": models.Skill.objects.all().order_by("-level"),
        "int": models.Interest.objects.all(),
    }

    return render(request, "minigrim0/cv.html", {"page_name": "CV", "cv": cv_data})


def cv_pdf(request):
    """Generate CV PDF from LaTeX template"""
    cv_data = {
        "edu": models.Education.objects.all(),
        "exp": models.Experience.objects.all(),
        "com": models.Competition.objects.all().order_by("-_order"),
        "lan": models.Language.objects.all(),
        "ski": models.Skill.objects.all().order_by("-level"),
        "int": models.Interest.objects.all(),
    }
    
    # Debug: print the context to see what's available
    print("CV Data keys:", cv_data.keys())
    print("Education count:", cv_data['edu'].count())
    
    return render_to_pdf(request, 'cv.tex', cv_data, filename='cv.pdf')

def error(request, error_type):
    return render(request, "error.html", {"page_name": "Error", "error": error_type})
