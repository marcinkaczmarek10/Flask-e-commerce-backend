import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secret_key'


class ProductionConfig(Config):
    DEBUG = False
