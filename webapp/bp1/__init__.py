from webapp import factory

def create_app(settings_override=None):
    """Return blueprint1 app instance
    """
    app = factory.create_app(__name__, __path__, settings_override)
    return app
