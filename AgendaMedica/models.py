from datetime import date, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meubanco.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    senha: Mapped[str] = mapped_column(nullable=False)


class Paciente(db.Model):
    __tablename__ = "paciente"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    nome: Mapped[str] = mapped_column(nullable=False, index=True)
    cpf: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    idade: Mapped[int] = mapped_column(nullable=False)
    data_nascimento: Mapped[date] = mapped_column(nullable=False)
    convenio: Mapped[str] = mapped_column(nullable=False, index=True, default="Particular")

    user: Mapped["User"] = relationship()


class Medico(db.Model):
    __tablename__ = "medico"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(nullable=False, index=True)
    crm: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    especialidade: Mapped[str] = mapped_column(nullable=False, index=True)


class Consulta(db.Model):
    __tablename__ = "consulta"  _

    id: Mapped[int] = mapped_column(primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("paciente.id"), nullable=False)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medico.id"), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, index=True, default="Agendada")
    data_hora: Mapped[datetime] = mapped_column(nullable=False)

    paciente: Mapped["Paciente"] = relationship()
    medico: Mapped["Medico"] = relationship()



with app.app_context():
    db.create_all()