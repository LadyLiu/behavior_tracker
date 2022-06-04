"""
Form template classes for use with app.py for verifying data collected from login.html, and register.html.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class EmailPassForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Enter password", validators=[DataRequired(), Length(min=6, max=16)])


class LoginForm(EmailPassForm):
    submit = SubmitField(label="Login")


class RegisterForm(EmailPassForm):
    first_name = StringField(label="Enter first name", validators=[DataRequired(), Length(min=1, max=20)])
    last_name = StringField(label="Enter last name", validators=[DataRequired(), Length(min=1, max=20)])
    confirm_password = PasswordField(label="Confirm password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Register")
