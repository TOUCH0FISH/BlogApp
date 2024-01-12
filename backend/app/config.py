import os


class Config:
    DEBUG = True
    # Database config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    # Message queue
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # JWT config
    JWT_SECRET = '123456'
    JWT_EXPIRATION = 86400  # in seconds
    JWT_ALGORITHM = 'HS256'
    # File manager
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg',
                          'jpeg', 'gif', 'docx', 'doc', 'xlsx', 'xls'}


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'mysql+mysqlconnector://user:password@localhost/database')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
