from webapp import create_app
from webapp.meta import db

# create database tables
with create_app().app_context():
    db.create_all()
