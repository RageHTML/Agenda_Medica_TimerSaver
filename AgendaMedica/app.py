import os
import requests
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegistrationForm, LoginForm
import click
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
                convenio=form.convenio.data,
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
    url_api = "http://127.0.0.1:5000/api/agendamentos"
    
    try:
        response = requests.get(url_api)
        if response.status_code == 200:
            agendamentos = response.json()  # Transforma a resposta HTTP em lista/dicionário Python
        else:
            agendamentos = []
    except requests.exceptions.RequestException:
        agendamentos = []

    return render_template("agenda.html", agendamentos=agendamentos)


@app.route("/api/agendamentos", methods=["GET"])
def api_agendamentos():
    try:
        consultas = Consulta.query.all()
        dados = []

        for c in consultas:
            dados.append({
                "paciente": c.paciente.nome if c.paciente else "Não informado",
                "cpf": c.paciente.cpf if c.paciente else "Não informado",
                "medico": c.medico.nome if c.medico else "Não informado",
                "especialidade": c.medico.especialidade if c.medico else "Não informado",
                "data": c.data_hora.strftime("%d/%m/%Y"),
                "horario": c.data_hora.strftime("%H:%M"),
                "convenio": c.paciente.convenio if c.paciente else "Particular",
                "status": c.status
            })

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao buscar agendamentos", "detalhes": str(e)}), 500


@app.cli.command("seed")
def seed():
    db.create_all()

    medico1 = Medico.query.filter_by(crm="12345/PB").first()
    if not medico1:
        medico1 = Medico(
            nome="Dr. Roberto Silva", crm="12345/PB", especialidade="Cardiologia"
        )
        db.session.add(medico1)

    medico2 = Medico.query.filter_by(crm="67890/PB").first()
    if not medico2:
        medico2 = Medico(
            nome="Dra. Juliana Costa", crm="67890/PB", especialidade="Dermatologia"
        )
        db.session.add(medico2)

    db.session.flush()

    email_teste = "paciente@teste.com"
    user_teste = User.query.filter_by(email=email_teste).first()

    if not user_teste:
        user_teste = User(
            email=email_teste, senha=generate_password_hash("123456")
        )
        db.session.add(user_teste)
        db.session.flush()

        paciente_teste = Paciente(
            user_id=user_teste.id,
            nome="Paciente Teste",
            cpf="11122233344",
            idade=30,
            data_nascimento=date(1996, 5, 15),
            convenio="Unimed",
        )
        db.session.add(paciente_teste)
        db.session.flush()
        print("-> Usuário e Paciente de teste criados.")
    else:
        paciente_teste = Paciente.query.filter_by(user_id=user_teste.id).first()
        print("-> Usuário de teste já existe no banco.")

    if paciente_teste and not Consulta.query.filter_by(paciente_id=paciente_teste.id).first():
        consulta1 = Consulta(
            paciente_id=paciente_teste.id,
            medico_id=medico1.id,
            status="Agendada",
            data_hora=datetime.now() + timedelta(days=2, hours=4),
        )
        consulta2 = Consulta(
            paciente_id=paciente_teste.id,
            medico_id=medico2.id,
            status="Agendada",
            data_hora=datetime.now() + timedelta(days=5, hours=2),
        )
        db.session.add_all([consulta1, consulta2])
        print("-> Consultas de teste criadas.")

    db.session.commit()
    print("Base de dados populada com sucesso!")

if __name__ == "__main__":
    app.run(debug=True)