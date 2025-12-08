import os
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from importlib import import_module
from sqlalchemy import event

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

    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_request_time(response):
        if hasattr(g, 'start_time'):
            elapsed = (time.time() - g.start_time) * 1000  # ms
            app.logger.info(
                f"{request.method} {request.path} took {elapsed:.2f}ms, status={response.status_code}"
            )
        return response
    

def attach_sql_listeners(app):

    @event.listens_for(db.engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        context._query_start_time = time.time()

    @event.listens_for(db.engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = (time.time() - context._query_start_time) * 1000
        app.logger.info(f"[SQL] {total:.2f}ms | {statement}")
        

def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    configure_database(app)

    with app.app_context():
        attach_sql_listeners(app)

    @app.route('/')
    def index():
        return render_template("base.html")

    @app.route('/health')
    def health_check():
        return "OK", 200
    
    return app