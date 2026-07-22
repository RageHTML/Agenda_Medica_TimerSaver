from flask_wtf import FlaskForm

from wt_froms import StringField, PasswordField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=100)])
    data_nascimento = DateField("Data de Nascimento", validators=[DataRequired()], format="%Y-%m-%d")

    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=6, max=254)])
    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=11)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha", message="As senhas devem coincidir.")])