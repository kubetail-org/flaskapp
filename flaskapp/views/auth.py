import os
import datetime

from flask import (Blueprint, render_template, url_for, redirect, request,
                   current_app, g)
from flask_login import login_user, logout_user, login_required
from flask_principal import identity_changed, Identity, AnonymousIdentity
from flask_mail import Message
from flask_wtf import FlaskForm
from premailer import transform

from flaskapp.meta import db, mail
from flaskapp.forms import (LoginForm, CreateAccountForm, ForgotPasswordForm,
                            ResetPasswordForm)
from flaskapp.models import (User, EmailVerificationRequest, 
                             PasswordResetRequest)
from flaskapp.lib.util import generate_password_hash


bp = Blueprint('auth', __name__)


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

        return redirect(request.args.get('next') or url_for('content.home'))

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

        # send verification email
        send_verification_email(u)

        # login user
        login_user(u, remember=True)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(u.id))

        return redirect(request.args.get('next') or url_for('content.home'))

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
        db.session.flush()

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
        db.session.flush()
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
        db.session.flush()

        return render_template('/auth/reset-password-followup.html')

    return render_template('/auth/reset-password.html', form=form)


@bp.route('/email-verification-request', methods=['GET', 'POST'])
@login_required
def email_verification_request():
    """GET|POST /email-verification-request: handle email verification requests
    """
    u = g.user

    form = FlaskForm()
    if form.validate_on_submit():
        send_verification_email(u)
        fn = '/auth/email-verification-request-followup.html'
        return render_template(fn, email=u.email)

    return render_template('/auth/email-verification-request.html', form=form)


@bp.route('/verify-email', methods=['GET'])
def verify_email():
    """GET|POST /verify-email: handle email verification request
    """
    # get email-verification-request entry
    f = (EmailVerificationRequest.key == request.args.get('key'),
         User.email == request.args.get('email'))
    r = EmailVerificationRequest.query.filter(*f).first()

    # return error response if link doesn't exist or wrong email
    if r == None or r.user.email != request.args['email']:
        return render_template('/auth/verify-email-error.html'), 400

    # expired if older than 3 days
    delta = datetime.datetime.utcnow() - r.create_ts
    if delta.days > 2:
        db.session.delete(r)
        db.session.flush()
        return render_template('/auth/verify-email-error.html'), 400

    # update status
    u = r.user
    u.is_verified = True
    db.session.add(u)

    # delete verification request
    db.session.delete(r)
    db.session.flush()

    return render_template('/auth/verify-email-followup.html')


def send_verification_email(user):
    """Send verification email to user
    """
    # create email verification request
    r = EmailVerificationRequest(key=os.urandom(32).encode('hex'),
                                 user=user)
    db.session.add(r)
    db.session.flush()

    # send email
    subject = 'Flaskapp Account: Please Confirm Email'
    msg = Message(subject, recipients=[user.email])
    verify_url = url_for('.verify_email', key=r.key, email=user.email, \
                             _external=True)

    f = '/auth/verify-email-email'
    msg.body = render_template(f + '.txt', verify_url=verify_url)

    html = render_template(f + '.html', verify_url=verify_url)
    base_url = url_for('content.home', _external=True)
    msg.html = transform(html, base_url=base_url)
    mail.send(msg)
