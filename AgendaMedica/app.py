import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegistrationForm
from models import Consulta, Medico, Paciente, User, db

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-padrao-seguranca")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///meubanco.db")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        nasc = form.data_nascimento.data
        idade = date.today().year - nasc.year
        cpf_limpo = form.cpf.data.replace(".", "").replace("-", "").strip()

        try:
            novo_usuario = User(
                email=form.email.data,
                senha=generate_password_hash(form.senha.data),
            )
            db.session.add(novo_usuario)
            db.session.flush()

            novo_paciente = Paciente(
                user_id=novo_usuario.id,
                nome=form.nome.data,
                cpf=cpf_limpo,
                idade=idade,
                data_nascimento=nasc,
                convenio=form.convenio.data
            )
            db.session.add(novo_paciente)
            db.session.commit()

            flash("Registro bem-sucedido!", "success")
            return redirect(url_for("login"))

        except IntegrityError:
            db.session.rollback()
            flash("Erro: Este e-mail ou CPF já está cadastrado no sistema.", "danger")

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

        flash(f"Bem-vindo(a) de volta!", "success")
        return redirect(url_for("agenda"))

    return render_template("login.html", form=form)


@app.route("/agenda")
def agenda():
    return "<p>ja ja sai uma agenda</p>"


if __name__ == "__main__":
    app.run(debug=True)