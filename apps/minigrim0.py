from flask import Blueprint, request, url_for, redirect, render_template, flash
minigrim0 = Blueprint('minigrim0', __name__, template_folder="../templates/")


@minigrim0.route("/")
def home():
    return render_template("minigrim0/index.html")


@minigrim0.route("/cv")
def cv():
    return render_template("minigrim0/cv.html")


@minigrim0.route("/projects")
def projects():
    return render_template("minigrim0/projects.html")


@minigrim0.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
