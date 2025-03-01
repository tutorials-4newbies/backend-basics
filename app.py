from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "Hello, World!"

@app.route("/")
def index():
    return "Index Page"

@app.route("/name/<username>")
def name(username):
    return f"Hi {escape(username)}"

@app.route("/query")
def query():
    message = "You sent the following query params:"
    for key, value in request.args.items():
        message += f"\n{escape(key)}: {escape(value)}"
    return message

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        return f"You sent the username - {request.form['username']}"
    elif request.method == "GET":
        return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
