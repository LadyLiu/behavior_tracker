"""
Main app logic and routing.  Verifies authorization where necessary for access.
"""

from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_login import login_user, login_required, logout_user
from datetime import datetime
from form.person_form import PersonForm
from model import db, login, UserModel, PersonModel, BehaviorModel
from form.user_form import LoginForm, RegisterForm


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
    Finds a user's people they track.  Allows added more people.
    :return:
    """
    name = None
    if 'name' in session:
        name = session['name']
    people = PersonModel.query.filter_by(observer_id=session['_user_id'])
    return render_template("dashboard.html", myData=people, owner=name)


@app.route('/person/<int:person_id>/', methods=['GET', 'POST'])
@login_required
def person(person_id: int):
    """
    Displays a single person.  Renders template to allow updates and deletes as long as user authorized.
    """
    record = PersonModel.query.filter_by(id=person_id).first()
    if record.observer_id != int(session['_user_id']):  # Session stored as str.
        flash("Unauthorized access.  This person is not registered to you.  Please check login credentials.")
        return redirect('/dashboard')
    
    # for behavior page use
    session['person_id'] = person_id 
    session['person_name'] = record.pseudonym

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
    behaviors = BehaviorModel.query.filter_by(person_id=person_id).order_by(BehaviorModel.registered.desc()) 
    return render_template("/person/person.html", data=behaviors, form=form)
    

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


@app.route("/behavior")
def behavior():
    behavior_names = ['Asking for help', 'Bed Wetting', 'Biting', 'Crying', 
        'Distracted', 'Elopement', 'Hitting', 'Kickig', 'Raising hand', 
        'Restroom break', 'Self harm', 'Tantrum', 'Throwing objects', 'Time on task']
    return render_template('/person/behavior.html', 
        person_name=session['person_name'], 
        person_id=session['person_id'],
        behavior_names=behavior_names)


@app.route("/behavior_timer", methods=['GET', 'POST'])
def duration_timer():
    if request.method == "POST":
        data = request.get_json()
        time_stamp = str(datetime.now())[:19]
        add_behavior_to_db(behavior_name=data[0]['behavior_name'],
                           frequency=data[0]['frequency'],
                           timer=data[0]['timer'],
                           date_time=time_stamp) 
        # display to template
        results = {'frequency': data[0]['frequency'], 'time': data[0]['timer']}
        return jsonify(results)


def add_behavior_to_db(timer, date_time, behavior_name=None, frequency=None):
    """
    Adds a behavior to the database.
    """
    behavior = BehaviorModel(behavior_name, frequency, timer, date_time)
    behavior.person_id = session['person_id']
    db.session.add(behavior)
    db.session.commit()


def add_user(email: str, first_name: str, last_name: str, password: str):
    """
    Adds user to db or flashes that user already exists.  Verified by flask-wtf
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
            session['name'] = user.first_name
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
