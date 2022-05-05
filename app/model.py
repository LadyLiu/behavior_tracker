"""
Database model for users.

Notes: Due to limitations of flask, all models need to be in here for tables to lazy load.
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login = LoginManager()


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    people = db.relationship('PersonModel', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PersonModel(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    pseudonym = db.Column(db.String(80), unique=True, nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    last_observation = db.Column(db.Date, nullable=True)
    observer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def set_last_observation(self, date):
        """
        Sets last observation date.  Verified in the form.
        :param date: Date type, formatted for db
        """
        self.last_observation = date


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
