import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# PEOPLE_FOLDER = os.path.join('static', 'upload')
PEOPLE_FOLDER = os.path.dirname(__file__)


SECRET_KEY = "dev"
