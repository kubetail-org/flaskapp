from flask import Blueprint, render_template


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
