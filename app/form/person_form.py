"""
Form for adding a new person to track behavior for.  Requires pseudonym, notes are optional.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PersonForm(FlaskForm):
    pseudonym = StringField(label="Enter person's pseudonym", validators=[DataRequired(), Length(min=1, max=20)])
    notes = StringField(label="Enter brief notes", validators=[Length(min=0, max=500)])
    submit = SubmitField(label="Add")
