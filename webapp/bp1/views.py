from flask import Blueprint, render_template
from flask.ext.mail import Message

from webapp.meta import mail


bp = Blueprint('bp1', __name__)


@bp.route('/', methods=['GET'])
def path1():
    """GET /: render path1
    """
    return render_template('/path1.html')


@bp.route('/path2', methods=['GET'])
def path2():
    """GET /path2: render path2
    """
    return render_template('/path2.html')


@bp.route('/send-email', methods=['GET'])
def send_email():
    """GET /send-email: send email
    """
    msg = Message('Subject', recipients=['barack@whitehouse.gov'])
    msg.body = 'body'
    msg.html = '<html></html>'
    mail.send(msg)
    return 'ok'
