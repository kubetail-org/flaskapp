from flask import g
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, TextAreaField,
                     FileField)
from wtforms.validators import (InputRequired, Email, URL, EqualTo,
                                ValidationError, StopValidation)
from wtforms.widgets import PasswordInput, CheckboxInput

from flaskapp.models import User
from flaskapp.lib.util import verify_password_hash


# ============================
# Auth forms
# ============================
class LoginForm(FlaskForm):
    """Sign in form
    """
    email = StringField(
        'Email address',
        validators=[
            InputRequired('Please enter your email address'),
            Email()
            ])

    password = PasswordField(
        'Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            InputRequired('Please enter your password')
            ])

    remember_me = BooleanField(
        'Remember me',
        widget=CheckboxInput(),
        default=True)

    def validate_password(form, field):
        """Verify password
        """
        if not form.email.data:
            raise StopValidation()
        
        # get user and verify password
        u = User.query.filter(User.email == form.email.data).first()
        if not u or not verify_password_hash(field.data, u.password):
            raise ValidationError('Email and password must match')


class CreateAccountForm(FlaskForm):
    """Create account form
    """
    email = StringField(
        'Email address',
        validators=[
            InputRequired('Please enter an email address'),
            Email()
            ])

    password = PasswordField(
        'Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            InputRequired('Please choose a password'),
            EqualTo('password_confirm', message='Passwords must match')
            ])
    
    password_confirm = PasswordField(
        'Confirm Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            InputRequired('Please confirm your password')
            ])

    newsletter = BooleanField(
        'Please send me product updates',
        widget=CheckboxInput(),
        default=True
        )

    def validate_email(form, field):
        """Check if email already exists
        """
        u = User.query.filter(User.email == field.data).first()
        if u != None:
            raise ValidationError('Did your forget your password?')


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        'Email address',
        validators=[
            InputRequired('Please enter an email address'),
            Email()
            ])

    def validate_email(form, field):
        """Check if email exists
        """
        u = User.query.filter(User.email == field.data).first()
        if u == None:
            raise ValidationError('Sorry, %s is not registered' % field.data)


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            InputRequired('Please choose a password'),
            EqualTo('password_confirm', message='Passwords must match')
            ])

    password_confirm = PasswordField(
        'Confirm Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            InputRequired('Please confirm your password')
            ])


# ====================================
# Miscellaneous forms
# ====================================
class FeedbackForm(FlaskForm):
    """Feedback form
    """
    email = StringField(
        'From',
        validators=[
            InputRequired('Please enter your email address'),
            Email()
            ])

    message = TextAreaField()

    newsletter = BooleanField(
        'Please send me product updates',
        widget=CheckboxInput(),
        default=True
        )
