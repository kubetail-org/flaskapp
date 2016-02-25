import os
import ast
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

# Global
DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
SECRET_KEY = os.environ.get('SECRET_KEY', 'replaceme')
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Will be false in Flask-SQLA v3

# Flask-Mail
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'Flaskapp <noreply@flaskapp.com>'
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEBUG = False
