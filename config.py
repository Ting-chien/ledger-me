import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables when running by gunicorn
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get("DB_USERNAME"), 
        os.environ.get("DB_PASSWORD"), 
        os.environ.get("DB_HOST"),
        os.environ.get("DB_PORT"), 
        os.environ.get("DB_NAME")
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}