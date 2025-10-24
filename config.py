import os

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


config = {
    'development': DevelopmentConfig
}