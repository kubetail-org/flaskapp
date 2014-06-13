import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Global
SECRET_KEY = 'replaceme'

# Flask-Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'barack@gmail.com'
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'Webapp <testreply@webapp.com>'
