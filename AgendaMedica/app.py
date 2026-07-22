from flask import Flask, request, render_template, flash, url_for, redirect
from datetime import date
from forms import RegistrationForm, LoginForm
from models import db, User, Paciente, Medico, Consulta
from werkzeug.security import check_password_hash
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
        return redirect(url_for('login'))
    
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("E-mail não encontrado.", "danger")
            return render_template("login.html", form=form)

        if not check_password_hash(user.senha, form.senha.data):
            flash("Senha incorreta. Tente novamente.", "danger")
            return render_template("login.html", form=form)

        flash(f"Bem-vindo(a) de volta, {user.nome}!", "success")
        return redirect(url_for("agenda"))

    return render_template("login.html", form=form)

@app.route("/agenda")
def agenda():
    return "<p>ja ja sai uma agenda</p>"