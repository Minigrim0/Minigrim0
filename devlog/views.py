from django.shortcuts import render
from devlog import models


def projects(request):
    return render(request, "minigrim0/projects.html", {
        "page_name": "Projects",
        "repos": models.Repository.objects.all()
    })
