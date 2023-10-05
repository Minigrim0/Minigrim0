import json

from flask import Blueprint, request, render_template, send_from_directory
minigrim0 = Blueprint('minigrim0', __name__, template_folder="../templates/", static_folder="../static")

from apps.utils import get_repos

@minigrim0.route("/")
def home():
    return render_template("minigrim0/index.html", page_name="Home")


@minigrim0.route("/cv")
def cv():
    with open("static/json/cv.json") as file:
        cv_data = json.load(file)

    return render_template("minigrim0/cv.html", page_name="CV", cv=cv_data)


@minigrim0.route('/robots.txt')
def static_from_root():
    print(request.path)
    return send_from_directory(minigrim0.static_folder, request.path[1:])


@minigrim0.route("/projects")
def projects():
    repos = get_repos()
    return render_template("minigrim0/projects.html", page_name="Projects", repos=repos)


@minigrim0.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
