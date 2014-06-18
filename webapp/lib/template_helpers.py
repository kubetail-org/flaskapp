import datetime

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
