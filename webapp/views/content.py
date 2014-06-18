from flask import Blueprint, render_template


bp = Blueprint('content', __name__)


@bp.route('/', methods=['GET'])
def home():
    """GET /: render homepage
    """
    return render_template('/content/home.html')


@bp.route('/about', methods=['GET'])
def about():
    """GET /about: return about page
    """
    return render_template('/content/about.html')


@bp.route('/features', methods=['GET'])
def features():
    """GET /features: render features page
    """
    return render_template('/content/features.html')


@bp.route('/pricing', methods=['GET'])
def pricing():
    """GET /pricing: return pricing page
    """
    return render_template('/content/pricing.html')


@bp.route('/support', methods=['GET'])
def support():
    """GET /support: return support page
    """
    return render_template('/content/support.html')


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """GET|POST /feedback: feedback form handler
    """
    form = FeedbackForm()
    if form.validate_on_submit():
        # TODO: send feedback to contact@example.com
        return 'ok'

    return render_template('/content/feedback.html', form=form)
