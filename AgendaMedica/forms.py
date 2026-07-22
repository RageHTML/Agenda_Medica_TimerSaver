from flask_wtf import FlaskForm
from models import Paciente, User
from wtforms import StringField, PasswordField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(message='O nome é obrigatório.'), Length(min=2, max=100, message='Insira um nome entre 2 - 100 caracteres')])
    data_nascimento = DateField("Data de Nascimento", validators=[DataRequired(message='A data de nascimento é obrigatória.')], format="%Y-%m-%d")

    email = EmailField("Email", validators=[DataRequired(message='O email é obrigatório.'), Email(message='Insira um email válido.'), Length(min=6, max=254)])
    cpf = StringField("CPF", validators=[DataRequired(message='O CPF é obrigatório.'), Length(min=11, max=11)])
    senha = PasswordField("Senha", validators=[DataRequired(message='A senha é obrigatória.'), Length(min=6, max=128, message='A senha deve ter entre 6 e 128 caracteres.')])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(message='A senha é obrigatória.'), EqualTo("senha", message="As senhas devem coincidir.")])

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError(
                "Este e-mail já está cadastrado. Tente outro ou faça login."
            )

    def validate_cpf(self, field):
        cpf_limpo = field.data.replace(".", "").replace("-", "").strip()
        paciente = Paciente.query.filter_by(cpf=cpf_limpo).first()
        if paciente:
            raise ValidationError("Este CPF já possui cadastro no sistema.")
        
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message='O email é obrigatório.'), Email(message='Insira um email válido.')])
    senha = PasswordField("Senha", validators=[DataRequired(message='A senha é obrigatória.')])