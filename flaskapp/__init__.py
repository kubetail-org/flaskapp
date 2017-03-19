import os
import json
import logging
import pkg_resources

import cssutils
from flask import Flask, g
from flask_wtf import CSRFProtect
from flask_login import current_user
from flask_principal import Principal, UserNeed, identity_loaded

from flaskapp.lib import template_helpers
from flaskapp.meta import mail, db, lm
from flaskapp.models import User
from flaskapp.views import content, auth


# suppress cssutils warning messages
cssutils.log.setLevel(logging.CRITICAL)


# ================================
# App creator method
# ================================
def create_app(extra_config=None):
    """Create Flask app for Flaskapp
    """
    app = Flask('flaskapp',
                template_folder='templates',
                static_folder='static')

    app.config.from_object('config')
    app.config.update(**(extra_config or {}))
    app.before_request(before_request)

    # import static file manifest
    js = pkg_resources.resource_string('flaskapp', '/static/rev-manifest.json')
    app.config['static_manifest'] = json.loads(js.decode('utf-8'))

    # configure jinja2
    app.jinja_env.globals.update({'h': template_helpers})

    # add Flask-WTForms CSRF Protection
    CSRFProtect(app)

    # init Flask-SQLAlchemy
    db.init_app(app)

    # init Flask-Principal
    Principal(app)
    identity_loaded.connect(on_identity_loaded, app)

    # init Flask-Login
    lm.init_app(app)
    lm.login_view = 'auth.login'
    lm.user_loader(load_user)

    # init Flask-Mail
    mail.init_app(app)

    # register blueprints
    app.register_blueprint(content.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')

    return app


# ===============================
# Helper methods
# ===============================
def before_request():
    """Add current user to g object
    """
    g.user = current_user


def load_user(id):
    """Method for LoginManager user_loader method
    """
    return User.query.get(int(id))


def on_identity_loaded(sender, identity):
    """Method for Flask Principal identity load listener
    """
    # set the identity user object
    identity.user = current_user

    if current_user.is_authenticated:
        # add UserNeed to identity
        identity.provides.add(UserNeed(current_user.id))
