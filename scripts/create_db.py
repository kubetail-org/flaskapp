import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flaskapp import create_app
from flaskapp.meta import db

# create database tables
with create_app().app_context():
    db.create_all()
