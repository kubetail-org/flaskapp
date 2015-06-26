from flask import Blueprint, render_template


bp = Blueprint('content', __name__)


@bp.route('/', methods=['GET'])
def home():
    """GET /: render homepage
    """
    return render_template('/content/home.html')


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """GET|POST /feedback: feedback form handler
    """
    form = FeedbackForm()
    if form.validate_on_submit():
        # TODO: send feedback to contact@example.com
        return 'ok'

    return render_template('/content/feedback.html', form=form)
