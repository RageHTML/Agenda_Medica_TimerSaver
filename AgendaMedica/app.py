from flask import Flask, request, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-padrao-seguranca")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///meubanco.db")


@app.route("/login")
def hello_world():
    return render_template("register.html")

@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        return render_template("register.html", person=reg)

@app.route("/login")
def login():
    return "<p>Login Page</p>"