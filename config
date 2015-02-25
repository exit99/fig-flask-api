import os


class BaseConfig(object):
    PROJECT = "myv-api"
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    DEBUG = True


class DevConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
