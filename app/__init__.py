from flask import Flask, render_template
from importlib import import_module


def register_blueprints(app):
    for module_name in ["transactions"]:
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)

    @app.route('/')
    def index():
        return render_template("base.html")
    
    return app