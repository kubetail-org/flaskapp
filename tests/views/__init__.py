import os
import unittest

from flask import url_for

from config import basedir
from flaskapp import create_app
from flaskapp.meta import db


users = {
    'userA': {
        'email': 'barack@whitehouse.gov',
        'password': 'imabelieber'
        },
    'userB': {
        'email': 'bieber@bieber.com',
        'password': 'imabelieber'
        }
    }


class WebsiteTestCase(unittest.TestCase):
    # ==============================
    # Test-level setup/teardown
    # ==============================
    def setUp(self):
        db_url = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = create_app(extra_config={
                'TESTING': True,
                'SERVER_NAME': 'example.com',
                'WTF_CSRF_ENABLED': False,
                'SQLALCHEMY_DATABASE_URI': db_url
                })
        self.client = self.app.test_client()

        # setup database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # teardown database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ==============================
    # Utility methods
    # ==============================
    def login(self, email, password):
        """Log in user and return response
        """
        data = dict(email=email, password=password)
        return self.client.post(self.url_for('auth.login'), data=data)

    def logout(self):
        """Log out user and return response
        """
        return self.client.get(self.url_for('auth.logout'))

    def create_account(self, email, password, password_confirm=None):
        """Create user account and return response
        """
        if password_confirm == None:
            password_confirm = password

        data = dict(email=email,
                    password=password,
                    password_confirm=password_confirm)

        return self.client.post(self.url_for('auth.create_account'), data=data)

    def url_for(self, *args, **kwargs):
        """Return url generated within app context
        """
        with self.app.app_context():
            u = url_for(*args, **kwargs)
        return u
