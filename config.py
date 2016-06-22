import os

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLE = True
SECRET_KEY = 'you-will-never-guess'


REDIS_URL = "redis://:@localhost:6379/0"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

APP_FOLDER = os.path.join(basedir,'app')
STATIC_FOLDER = os.path.join(APP_FOLDER,'static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER,'uploads')
UPLOAD_AVATAR = os.path.join(UPLOAD_FOLDER,'avatar')
