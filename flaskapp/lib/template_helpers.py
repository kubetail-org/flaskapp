import datetime
import pkg_resources

from flask import current_app, url_for
from jinja2 import Markup


__all__ = ['datetime', 'javascript_tag', 'stylesheet_tag']


def javascript_tag(url):
    """Return html tag for external javascript file
    """
    return Markup('<script type="text/javascript" src="%s"></script>' % url)


def stylesheet_tag(url):
    """Return html tag for external stylesheet
    """
    html = '<link rel="stylesheet" type="text/css" media="screen" href="%s" '\
        '/>' % url
    return Markup(html)


def static(rel_pathname):
    """Returns url for cached file if available
    """
    rel_pathname = rel_pathname.lstrip('/')

    # check if file is in manifest
    filename = current_app.config['static_manifest'].get(rel_pathname)

    if filename and current_app.config['DEBUG'] == False:
        filename = 'cache/' + filename
    else:
        filename = rel_pathname

    return url_for('static', filename=filename)
