from django.shortcuts import render
from minigrim0 import models


def index(request):
    return render(request, "minigrim0/index.html", {
        "page_name": "Home"
    })


def cv(request):
    cv_data = {
        "edu": models.Education.objects.all(),
        "exp": models.Experience.objects.all(),
        "com": models.Competition.objects.all(),
        "lan": models.Language.objects.all(),
        "ski": models.Skill.objects.all(),
        "int": models.Interest.objects.all(),
    }

    return render(request, "minigrim0/cv.html", {
        "page_name": "CV",
        "cv": cv_data
    })


def projects(request):
    return render(request, "minigrim0/projects.html", {
        "page_name": "Projects",
        "repos": models.Repository.objects.all()
    })
