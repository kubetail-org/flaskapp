import os
import pkgutil
import importlib

import jinja2
from flask import Flask, Blueprint

from webapp.meta import mail


def create_app(package_name, package_path, extra_config=None):
    """Create app
    """
    app = Flask(package_name)

    app.config.from_object('config')
    app.config.update(**(extra_config or {}))

    # configure jinja2
    pkgdir = os.path.abspath(os.path.dirname(__file__))
    app.jinja_loader = jinja2.ChoiceLoader([
            jinja2.FileSystemLoader([pkgdir + '/templates']),
            app.jinja_loader
            ])

    # init Flask-Mail
    mail.init_app(app)

    # register blueprints
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)

    return app
