from webapp import factory

def create_app(extra_config=None):
    """Return blueprint1 app instance
    """
    app = factory.create_app(__name__, __path__, extra_config)
    return app
