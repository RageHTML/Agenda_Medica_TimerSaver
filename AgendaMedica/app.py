import logging
import os
import time
from datetime import date, datetime, timedelta
from threading import Thread

import requests
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegistrationForm
from models import Consulta, Medico, Paciente, User, db

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-padrao-seguranca")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///meubanco.db")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.context_processor
def utilitarios_template():
    def static_url(filename):
        caminho_absoluto = os.path.join(app.static_folder, filename)
        try:
            versao = int(os.path.getmtime(caminho_absoluto))
        except OSError:
            versao = 0
        return url_for("static", filename=filename) + f"?v={versao}"

    return {"static_url": static_url}


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

        flash("Bem-vindo(a) de volta!", "success")
        return redirect(url_for("agenda"))

    return render_template("login.html", form=form)


@app.route("/agenda")
def agenda():
    url_api = url_for("api_agendamentos", _external=True)

    try:
        response = requests.get(url_api, timeout=5)
        agendamentos = response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        agendamentos = []

    return render_template("agenda.html", agendamentos=agendamentos)


@app.route("/api/agendamentos", methods=["GET"])
def api_agendamentos():
    termo = request.args.get("q", default="", type=str).strip()

    try:
        query = Consulta.query.outerjoin(Paciente).outerjoin(Medico)

        if termo:
            termo_limpo = termo.replace(".", "").replace("-", "").strip()
            termo_like = f"%{termo}%"
            termo_cpf_like = f"%{termo_limpo}%"

            query = query.filter(
                or_(
                    Paciente.nome.like(termo_like),
                    Paciente.cpf.like(termo_cpf_like),
                    Medico.nome.like(termo_like),
                    Medico.especialidade.like(termo_like)
                )
            )

        consultas = query.all()
        dados = []

        for c in consultas:
            dados.append({
                "paciente": c.paciente.nome if c.paciente else "Não informado",
                "cpf": c.paciente.cpf if c.paciente else "Não informado",
                "medico": c.medico.nome if c.medico else "Não informado",
                "especialidade": c.medico.especialidade if c.medico else "Não informado",
                "data": c.data_hora.strftime("%d/%m/%Y") if c.data_hora else "",
                "horario": c.data_hora.strftime("%H:%M") if c.data_hora else "",
                "convenio": c.paciente.convenio if c.paciente else "Particular",
                "status": c.status if c.status else "Agendada",
            })

        return jsonify(dados), 200

    except Exception as e:
        logging.error(f"Erro na API de busca: {e}")
        return jsonify([]), 200


def carregar_dados_terminal():
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = os.getenv("FLASK_RUN_PORT", "5000")
    if host == "0.0.0.0":
        host = "127.0.0.1"

    url = f"http://{host}:{port}/api/agendamentos"
    max_tentativas = 15
    intervalo_segundos = 1

    for tentativa in range(1, max_tentativas + 1):
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                dados = res.json()
                msg = "\n" + "=" * 70 + "\n"
                msg += "         DADOS DOS AGENDAMENTOS (BUSCADOS VIA API HTTP)\n"
                msg += "=" * 70 + "\n"
                if not dados:
                    msg += "Nenhum agendamento cadastrado no momento.\n"
                for item in dados:
                    msg += f"Paciente: {item['paciente']} | CPF: {item['cpf']}\n"
                    msg += f"Médico: {item['medico']} ({item['especialidade']})\n"
                    msg += (
                        f"Data/Hora: {item['data']} às {item['horario']} | "
                        f"Convênio: {item['convenio']} | Status: {item['status']}\n"
                    )
                    msg += "-" * 70 + "\n"
                msg += "=" * 70 + "\n"
                logging.info(msg)
                return
        except requests.exceptions.RequestException:
            pass

        time.sleep(intervalo_segundos)

    logging.error(f"\n[ERRO NA API]: Servidor não respondeu após {max_tentativas} tentativas\n")


def iniciar_thread_terminal_automatico():
    if os.environ.get("WERKZEUG_RUN_MAIN") != "false":
        Thread(target=carregar_dados_terminal, daemon=True).start()


iniciar_thread_terminal_automatico()


@app.cli.command("seed")
def seed():
    db.create_all()

    medicos_dados = [
        {"nome": "Dr. Roberto Silva", "crm": "12345/PB", "especialidade": "Cardiologia"},
        {"nome": "Dra. Juliana Costa", "crm": "67890/PB", "especialidade": "Dermatologia"},
        {"nome": "Dr. Fernando Albuquerque", "crm": "11223/PB", "especialidade": "Ortopedia"},
        {"nome": "Dra. Camila Andrade", "crm": "44556/PB", "especialidade": "Pediatria"},
        {"nome": "Dr. Marcelo Vasconcelos", "crm": "77889/PB", "especialidade": "Neurologia"},
    ]

    medicos_objetos = []
    for m in medicos_dados:
        medico = Medico.query.filter_by(crm=m["crm"]).first()
        if not medico:
            medico = Medico(nome=m["nome"], crm=m["crm"], especialidade=m["especialidade"])
            db.session.add(medico)
        medicos_objetos.append(medico)

    db.session.flush()

    pacientes_dados = [
        {
            "email": "carlos.eduardo@gmail.com",
            "nome": "Carlos Eduardo Oliveira",
            "cpf": "12345678901",
            "nascimento": date(1988, 3, 14),
            "convenio": "Unimed",
        },
        {
            "email": "mariana.santos@hotmail.com",
            "nome": "Mariana Santos Ferreira",
            "cpf": "98765432100",
            "nascimento": date(1995, 8, 22),
            "convenio": "Bradesco Saúde",
        },
        {
            "email": "lucas.mendes@yahoo.com.br",
            "nome": "Lucas Mendes Rocha",
            "cpf": "45678912344",
            "nascimento": date(2001, 11, 5),
            "convenio": "Particular",
        },
        {
            "email": "ana.beatriz@gmail.com",
            "nome": "Ana Beatriz Lima",
            "cpf": "78912345688",
            "nascimento": date(1973, 1, 30),
            "convenio": "Amil",
        },
        {
            "email": "rafael.alves@outlook.com",
            "nome": "Rafael Alves Guimarães",
            "cpf": "32165498711",
            "nascimento": date(1990, 6, 18),
            "convenio": "Hapvida",
        },
    ]

    pacientes_objetos = []
    for p in pacientes_dados:
        user = User.query.filter_by(email=p["email"]).first()
        if not user:
            user = User(email=p["email"], senha=generate_password_hash("123456"))
            db.session.add(user)
            db.session.flush()

            idade_calc = date.today().year - p["nascimento"].year
            paciente = Paciente(
                user_id=user.id,
                nome=p["nome"],
                cpf=p["cpf"],
                idade=idade_calc,
                data_nascimento=p["nascimento"],
                convenio=p["convenio"],
            )
            db.session.add(paciente)
            db.session.flush()
        else:
            paciente = Paciente.query.filter_by(user_id=user.id).first()

        pacientes_objetos.append(paciente)

    consultas_dados = [
        {"p_idx": 0, "m_idx": 0, "data_hora": datetime(2026, 8, 10, 8, 30), "status": "Confirmada"},
        {"p_idx": 1, "m_idx": 1, "data_hora": datetime(2026, 8, 10, 10, 0), "status": "Agendada"},
        {"p_idx": 2, "m_idx": 2, "data_hora": datetime(2026, 8, 11, 14, 15), "status": "Realizada"},
        {"p_idx": 3, "m_idx": 3, "data_hora": datetime(2026, 8, 12, 11, 30), "status": "Agendada"},
        {"p_idx": 4, "m_idx": 4, "data_hora": datetime(2026, 8, 13, 16, 0), "status": "Cancelada"},
        {"p_idx": 0, "m_idx": 1, "data_hora": datetime(2026, 8, 18, 9, 0), "status": "Agendada"},
        {"p_idx": 1, "m_idx": 3, "data_hora": datetime(2026, 8, 20, 15, 45), "status": "Confirmada"},
    ]

    for c in consultas_dados:
        paciente_obj = pacientes_objetos[c["p_idx"]]
        medico_obj = medicos_objetos[c["m_idx"]]

        if paciente_obj and medico_obj:
            existente = Consulta.query.filter_by(
                paciente_id=paciente_obj.id,
                medico_id=medico_obj.id,
                data_hora=c["data_hora"],
            ).first()

            if not existente:
                consulta = Consulta(
                    paciente_id=paciente_obj.id,
                    medico_id=medico_obj.id,
                    status=c["status"],
                    data_hora=c["data_hora"],
                )
                db.session.add(consulta)

    db.session.commit()


if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)