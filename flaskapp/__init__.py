import os

from flask import Flask, g
from flask.ext.wtf import CsrfProtect
from flask.ext.login import current_user
from flask.ext.principal import Principal, UserNeed, identity_loaded

from flaskapp.lib import template_helpers
from flaskapp.meta import mail, db, lm
from flaskapp.models import User
from flaskapp.views import content, auth, dashboard


# ================================
# App creator method
# ================================
def create_app(extra_config=None):
    """Create Flask app for Webapp
    """
    app = Flask('flaskapp',
                template_folder='templates',
                static_folder='static')

    app.config.from_object('config')
    app.config.update(**(extra_config or {}))
    app.before_request(before_request)

    # configure jinja2 globals
    app.jinja_env.globals.update({'h': template_helpers})

    # add Flask-WTForms CSRF Protection
    CsrfProtect(app)

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
    app.register_blueprint(dashboard.bp, url_prefix='/dashboard')

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

    if current_user.is_authenticated():
        # add UserNeed to identity
        identity.provides.add(UserNeed(current_user.id))
