"""
Main app logic and routing.  Verifies authorization where necessary for access.
"""

from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from app.user.user_model import db, login, UserModel
from app.user.user_form import LoginForm, RegisterForm


app = Flask(__name__)
app.secret_key = "a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def find_people():
    """
    Currently just displays empty dashboard.  Logic for displaying a person's tracked people should be here.
    :return:
    """
    return render_template("dashboard.html")


@app.route("/")
def redirect_to_login():
    return redirect("/login")


def add_user(email, first_name, last_name, password):
    user = UserModel.query.filter_by(email=email).first()  # Verify not already in DB
    if user is None:
        user = UserModel()
        user.set_password(password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        db.session.add(user)
        db.session.commit()
    else:  # There is a check already in registration, but this is a back up safety.
        flash("User already exists.  Please sign in.")


@app.before_first_request
def create_table():
    """
    Creates database if it doesn't already exist including a default user for Prof Hong
    """
    db.create_all()
    user = UserModel.query.filter_by(email="lhhung@uw.edu").first()
    if user is None:
        add_user(email="lhhung@uw.edu", first_name="Professor", last_name="Hong", password="qwerty")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                login_user(user)
                return redirect('/dashboard')
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email=email, first_name=first_name, last_name=last_name, password=password)
                flash("Thank you for registering!")
                return redirect('/login')
            elif user is not None and user.check_password(password):
                flash("Welcome back!")
                login_user(user)
                return redirect('/dashboard')
            else:
                flash("User already exists and you used an incorrect password.")
    return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
