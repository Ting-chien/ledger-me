from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from importlib import import_module

db = SQLAlchemy()
migrate = Migrate()


def register_blueprints(app):
    for module_name in ["transactions", "reports"]:
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    configure_database(app)

    @app.route('/')
    def index():
        return render_template("base.html")
    
    return app