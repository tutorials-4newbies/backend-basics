from peewee import IntegrityError
from flask import Flask, flash, redirect, render_template, request, session, url_for
from markupsafe import escape
from hashlib import md5

from auth import auth_user, check_user_logged_in, get_current_user
from db import Task, User, create_tables, database

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    user = get_current_user()
    username = None
    if user:
        username = user.username
    return render_template("index.html", username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username']:
        try:
            password = md5((request.form['password']).encode('utf-8')).hexdigest()
            user = User.get(
                (User.username == request.form['username']) &
                (User.password == password))
        except User.DoesNotExist:
            flash('The password entered is incorrect')
        else:
            auth_user(user)
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route("/task", methods=['GET', 'POST'])
def task():
    check_user_logged_in()
    if request.method == 'POST':
        Task.create(name=request.form["name"], user=get_current_user())
        return redirect(url_for('task'))
    tasks = Task.select().where(Task.user == get_current_user()).order_by(Task.created)
    return render_template("task.html", tasks=tasks)

@app.route("/task/<task_id>/completed/", methods=["POST"])
def mark_task_completed(task_id):
    check_user_logged_in()
    query = Task.update(is_completed=True).where(Task.id == task_id)
    query.execute()
    return redirect(url_for('task'))

@app.route("/task/<task_id>/incompleted/", methods=["POST"])
def mark_task_incompleted(task_id):
    check_user_logged_in()
    query = Task.update(is_completed=False).where(Task.id == task_id)
    query.execute()
    return redirect(url_for('task'))

@app.route("/user/", methods=["GET", "POST"])
def user():
    if request.method == 'POST' and request.form['username']:
        try:
            with database.atomic():
                # Attempt to create the user. If the username is taken, due to the
                # unique constraint, the database will raise an IntegrityError.
                user = User.create(
                    username=request.form['username'],
                    password=md5((request.form['password']).encode('utf-8')).hexdigest())

            # mark the user as being 'authenticated' by setting the session vars
            auth_user(user)
            return redirect(url_for('index'))

        except IntegrityError:
            flash('That username is already taken')
    return render_template('user.html')

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response

@app.errorhandler(403)
def forbidden(e):
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)