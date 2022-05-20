"""
Main app logic and routing.  Verifies authorization where necessary for access.
"""

from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_login import login_user, login_required, logout_user
from app.form.person_form import PersonForm
from app.model import db, login, UserModel, PersonModel, BehaviorModel
from app.form.user_form import LoginForm, RegisterForm


app = Flask(__name__)
app.secret_key = "a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

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


@app.route('/person/<int:person_id>/', methods=['GET', 'POST'])
@login_required
def person(person_id: int):
    """
    Displays a single person.  Renders template to allow updates and deletes as long as user authorized.
    TODO - Once you've added behaviors, please update this code and related templates to display that data as well.
    """
    record = PersonModel.query.filter_by(id=person_id).first()
    if record.observer_id != int(session['_user_id']):  # Session stored as str.
        flash("Unauthorized access.  This person is not registered to you.  Please check login credentials.")
        return redirect('/dashboard')
    form = PersonForm()
    form.pseudonym.data, form.notes.data = record.pseudonym, record.notes
    if form.validate_on_submit() and request.method == "POST":
        if request.form['action'] == 'Delete':  # Workaround for multiple action buttons
            temp_pseudonym = record.pseudonym
            db.session.delete(record)
            db.session.commit()
            flash(f"{temp_pseudonym} has been deleted.")
            return redirect('/dashboard')
        elif request.form['action'] == 'Update':
            record.pseudonym = request.form["pseudonym"]
            record.notes = request.form["notes"]
            db.session.commit()
            flash(f"{record.pseudonym} record has been updated.")
            return redirect('/dashboard')
    return render_template("/person/person.html", data=person, form=form)


@app.route('/add-person', methods=['GET', 'POST'])
@login_required
def add_person():
    """
    Renders form to add person and calls function add_person on post.
    :return: rendered template for add-person.html
    """
    form = PersonForm()
    if form.validate_on_submit() and request.method == "POST":
        pseudonym = request.form["pseudonym"]
        notes = request.form["notes"]
        add_person_to_db(session['_user_id'], pseudonym, notes)
        flash("New person added.")
        return redirect('/dashboard')
    return render_template("/person/add-person.html", form=form)


def add_person_to_db(observer: int, pseudonym: str, notes: str):
    """
    Adds a person to the database.
    :param observer: int representing observer ID.  Can be used to verify who has access rights to this record.
    :param pseudonym: string of pseudonym representing person being observed.
    :param notes: string of notes for this record.
    """
    person = PersonModel()
    person.observer_id = observer
    person.pseudonym = pseudonym
    person.notes = notes
    db.session.add(person)
    db.session.commit()


@app.route("/behavior", methods=['GET', 'POST'])
def behavior():
    """
    TODO will this need a form?
    """
    return render_template('/person/behavior.html')

@app.route("/behavior_timer", methods=['GET', 'POST'])
def behavior_timer():
    if request.method == "POST":
        timer_data = request.get_json()
        db.session.add(BehaviorModel(timer_data[0]['timer']))
        db.session.commit()

        # temporary. currently set to retrive longest time but can modify this later
        time_result = BehaviorModel.query.order_by(BehaviorModel.timer.desc()).first()
        print('retrived from db:', time_result.timer)
        results = {'time': time_result.timer}
        return jsonify(results)

def add_user(email: str, first_name: str, last_name: str, password: str):
    """
    Adds user to db or flashes that user already exists.  Verified by flask-wtf
    :param email: str
    :param first_name: str
    :param last_name: str
    :param password: str
    """
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


@app.route("/")
def redirect_to_login():
    return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
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
    if form.validate_on_submit() and request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        user = UserModel.query.filter_by(email=email).first()
        if user is None:
            add_user(email=email, first_name=first_name, last_name=last_name, password=password)
            flash(f"Thank you for registering, {first_name}!", 'success')
            return redirect('/login')
        elif user is not None and user.check_password(password):
            flash("Welcome back!", 'success')
            login_user(user)
            return redirect('/dashboard')
        else:
            flash("User already exists and you used an incorrect password.", 'error')
    return render_template("/user/register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
