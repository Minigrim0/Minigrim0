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
        "com": models.Competition.objects.all().order_by("-_order"),
        "lan": models.Language.objects.all(),
        "ski": models.Skill.objects.all().order_by("-level"),
        "int": models.Interest.objects.all(),
    }

    return render(request, "minigrim0/cv.html", {
        "page_name": "CV",
        "cv": cv_data
    })
