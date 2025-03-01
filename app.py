from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return render_template("index_logged_in.html", username=session['username'])
    return render_template("index_logged_out.html")

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
