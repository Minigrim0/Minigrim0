from flask import Flask
from flask_sitemap import Sitemap

# blueprint import
from apps.minigrim0 import minigrim0
from flaskext.markdown import Markdown

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # register blueprint
    app.register_blueprint(minigrim0)
    # app.register_blueprint(app2, url_prefix="/app2")
    Markdown(app)
    ext = Sitemap(app=app)
    app.config["SITEMAP_BLUEPRINT"]

    @ext.register_generator
    def index():
        for route in ["minigrim0.home", "minigrim0.cv", "minigrim0.projects"]:
            yield route, {}

    return app


if __name__ == "__main__":
    create_app().run()
