from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/register")
def hello_world():
    return render_template("register.html")

@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        return render_template("register.html", person=reg)

@app.route("/login")
def login():
    return "<p>Login Page</p>"