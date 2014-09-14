import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from webapp import create_app
from webapp.meta import db

# create database tables
with create_app().app_context():
    db.create_all()
