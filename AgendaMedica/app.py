from flask import Flask, request, render_template, flash, url_for, redirect
from datetime import date
from forms import RegistrationForm
from models import db, User, Paciente, Medico, Consulta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-padrao-seguranca")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///meubanco.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        nasc = form.data_nascimento.data
        idade = date.today().year - nasc.year

        flash(f"Registro bem-sucedido para {form.nome.data}, idade: {idade} anos, email: {form.email.data}, CPF: {form.cpf.data}")
        return redirect(url_for('agenda'))
    
    return render_template("register.html", form=form)

@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        return render_template("register.html", person=reg)

@app.route("/agenda")
def login():
    return "<p>ja ja sai uma agenda</p>"