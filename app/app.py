"""
Main app logic and routing.  Verifies authorization where necessary for access.
"""

from flask import Flask, render_template, request, redirect, flash, session
from flask_login import login_user, login_required, logout_user
from app.person.person_form import PersonForm
# from app.person.person_model import PersonModel -- Problem with loading tables from other locations
from app.user.user_model import db, login, UserModel, PersonModel
from app.user.user_form import LoginForm, RegisterForm



app = Flask(__name__)
app.secret_key = "a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
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
    people = PersonModel.query.filter_by(observer_id=session['_user_id'])
    return render_template("dashboard.html", myData=people)


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
    person = PersonModel.query.filter_by(pseudonym="trendsetter").first()
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
    return render_template("/user/login.html", form=form)


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
    return render_template("/user/register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/add-person', methods=['GET', 'POST'])
@login_required
def add_person():
    form = PersonForm()
    if form.validate_on_submit():
        if request.method == "POST":
            pseudonym = request.form["pseudonym"]
            notes = request.form["notes"]
            add_person(session['_user_id'], pseudonym, notes)
            flash("New person added.")
            return redirect('/dashboard')
    return render_template("/person/add-person.html", form=form)


def add_person(observer, pseudonym, notes):
    person = PersonModel()
    person.observer_id = observer
    person.pseudonym = pseudonym
    person.notes = notes
    db.session.add(person)
    db.session.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
