from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape

from db import Task, create_tables, database

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    username = session.get('username', None)
    return render_template("index.html", username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index')) # TEACH ABOUT REDIRECT AND URL FOR!
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index')) # TEACH ABOUT REDIRECT AND URL FOR!

@app.route("/task", methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        Task.create(name=request.form["name"])
        return redirect(url_for('task'))
    tasks = Task.select().order_by(Task.created)
    return render_template("task.html", tasks=tasks)

@app.route("/task/<task_id>/completed/", methods=["POST"])
def mark_task_completed(task_id):
    query = Task.update(is_completed=True).where(Task.id == task_id)
    query.execute()
    return redirect(url_for('task'))

@app.route("/task/<task_id>/incompleted/", methods=["POST"])
def mark_task_incompleted(task_id):
    query = Task.update(is_completed=False).where(Task.id == task_id)
    query.execute()
    return redirect(url_for('task'))

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)