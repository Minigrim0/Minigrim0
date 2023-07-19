from flask import Flask

# blueprint import
from apps.minigrim0 import minigrim0

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # register blueprint
    app.register_blueprint(minigrim0)
    # app.register_blueprint(app2, url_prefix="/app2")

    return app

if __name__ == "__main__":
    create_app().run()
