import os
import datetime

from flask import (Blueprint, render_template, url_for, redirect, request,
                   current_app)
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.mail import Message
from premailer import transform

from webapp.meta import db, mail
from webapp.forms import (LoginForm, CreateAccountForm, ForgotPasswordForm,
                          ResetPasswordForm)
from webapp.models import (User, AccountVerificationRequest,
                           PasswordResetRequest)
from webapp.lib.util import generate_password_hash


bp = Blueprint('auth', __name__)


# ===============================
# Route handlers
# ===============================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """GET|POST /login: login form handler
    """
    form = LoginForm()
    if form.validate_on_submit():
        # login user
        u = User.query.filter(User.email == form.email.data).first()
        login_user(u, remember=form.remember_me.data)

        # tell flask-principal the identity changed
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(u.id))

        return redirect(url_for('dashboard.home'))

    return render_template('/auth/login.html', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    """GET /signout: sign out user
    """
    logout_user()

    # tell flask-principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('content.home'))


@bp.route('/create-account', methods=['GET', 'POST'])
def create_account():
    """GET|POST /create-account: create account form handler
    """
    form = CreateAccountForm()
    if form.validate_on_submit():
        # add user to database
        u = User(email=form.email.data,
                 password=generate_password_hash(form.password.data))
        db.session.add(u)
        db.session.flush()

        # create account verification request
        r = AccountVerificationRequest(key=os.urandom(32).encode('hex'),
                                       user=u)
        db.session.add(r)
        db.session.commit()

        # generate email
        msg = Message('ErrorPage Account: Please Confirm Email',
                      recipients=[u.email])
        verify_url = url_for('auth.verify_account', key=r.key, email=u.email, \
                                 _external=True)

        # txt
        msg.body = render_template('/auth/account-verification-email.txt',
                                   verify_url=verify_url)

        # html
        html = render_template('/auth/account-verification-email.html',
                               verify_url=verify_url)
        msg.html = transform(html,
                             base_url=url_for('content.home', _external=True))

        # TODO: send email
        #mail.send(msg)

        # login user
        login_user(u, remember=True)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(u.id))

        return redirect(url_for('dashboard.home'))

    return render_template('/auth/create-account.html', form=form)


@bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """GET|POST /forgot: forgot password form handler
    """
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        # get user
        u = User.query.filter_by(email=form.email.data).one()

        # create reset password
        # Todo: delete all previous entries
        r = PasswordResetRequest(key=os.urandom(32).encode('hex'),
                                 user=u)

        # save to db
        db.session.add(r)
        db.session.commit()

        # generate email
        msg = Message('Password Reset Request',
                      recipients=[u.email])
        reset_url = url_for('auth.reset_password', key=r.key, email=u.email, \
                                _external=True)

        # txt
        msg.body = render_template('/auth/reset-password-email.txt',
                                   reset_url=reset_url)

        # html
        html = render_template('/auth/reset-password-email.html',
                               reset_url=reset_url)
        msg.html = transform(html,
                             base_url=url_for('content.home', _external=True))

        # send email
        mail.send(msg)

        return render_template('/auth/forgot-followup.html',
                               email=u.email)

    return render_template('/auth/forgot.html', form=form)


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """GET /reset-password: choose new password
    """
    # get password-reset entry
    f = (PasswordResetRequest.key == request.args.get('key'),
         User.email == request.args.get('email'))
    r = PasswordResetRequest.query.filter(*f).first()

    # return error response if link doesn't exist or wrong email
    if r == None or r.user.email != request.args['email']:
        return render_template('/auth/reset-password-error.html'), 400

    # expired if older than 1 day
    delta = datetime.datetime.utcnow() - r.create_ts
    if delta.days > 0:
        db.session.delete(r)
        db.session.commit()
        return render_template('/auth/reset-password-error.html'), 400

    # handle form
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # save new password
        u = r.user
        u.password = generate_password_hash(form.password.data)
        db.session.add(u)

        # login user
        login_user(u, remember=True)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(u.id))

        # delete password reset
        db.session.delete(r)
        db.session.commit()

        return render_template('/auth/reset-password-followup.html')

    return render_template('/auth/reset-password.html', form=form)


@bp.route('/account-verification-request', methods=['GET', 'POST'])
@login_required
def account_verification_request():
    """GET|POST /verify-account-request: handle account verification requests
    """
    pass


@bp.route('/verify-account', methods=['GET'])
def verify_account():
    """GET|POST /verify-account: handle account verification request
    """
    pass
