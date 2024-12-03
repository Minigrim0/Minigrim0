from django.urls import path

from devlog import views

urlpatterns = [
    path("projects/", views.projects, name="projects"),
]
