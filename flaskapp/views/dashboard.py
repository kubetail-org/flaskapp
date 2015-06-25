from flask import Blueprint, render_template
from flask.ext.login import login_required


bp = Blueprint('dashboard', __name__)


# ================================
# Route handlers
# ================================
@bp.route('/', methods=['GET'])
@login_required
def home():
    """GET /dashboard: return dashboard homepage
    """
    return render_template('/dashboard/home.html')
