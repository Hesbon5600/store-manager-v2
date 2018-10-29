import os


class Config():
    # Parent confuguration fila
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


class Development(Config):
    '''Configuration for development environment'''
    DEBUG = True
    APP_SETTINGS = 'development'


class Testing(Config):
    '''Configuration for testing environment'''
    WTF_CSRF_ENABLED = False
    DEBUG = True
    APP_SETTINGS = 'testing'


class Production(Config):
    '''Configuration for production environment'''
    DEBUG = False


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
