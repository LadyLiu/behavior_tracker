"""
Form for adding a behavior to a person.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class BehaviorForm(FlaskForm):
    name = StringField(label="Enter name of behavior", validators=[DataRequired(), Length(min=1, max=20)])
    description = TextAreaField(label="Enter description of behavior", validators=[Length(min=0, max=500)])
    submit = SubmitField(label="Add")