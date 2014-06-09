from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from webapp import bp1, bp2


application = DispatcherMiddleware(
    bp1.create_app(),
    {'/bp2': bp2.create_app()}
    )


if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application, use_reloader=True,
               use_debugger=True)
