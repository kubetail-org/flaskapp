import pkgutil
import importlib

from flask import Flask, Blueprint


def create_app(package_name, package_path, settings_override=None):
    """Create app
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_object(settings_override)

    # register blueprints
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)

    return app
