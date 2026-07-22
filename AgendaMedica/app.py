from flask import Flask, request

app = Flask(__name__)

@app.route("/register")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        return <p>Data saved successfully!</p>
@app.route("/login")
def login():
    return "<p>Login Page</p>"