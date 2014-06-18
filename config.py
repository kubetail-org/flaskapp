import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

# Global
DEBUG = True
SECRET_KEY = 'replaceme'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Flask-Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'barack@gmail.com'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'Webapp <testreply@webapp.com>'
