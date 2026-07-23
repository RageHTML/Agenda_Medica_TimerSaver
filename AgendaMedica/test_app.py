import pytest
from app import app, db, User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" 
    app.config["WTF_CSRF_ENABLED"] = False 

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
           
            usuario_teste = User(
                email="teste@email.com",
                senha=generate_password_hash("123456")
            )
            db.session.add(usuario_teste)
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()

def test_login_valido(client):
    """Testa o comportamento de login com credenciais corretas."""
    resposta = client.post("/login", data={
        "email": "teste@email.com",
        "senha": "123456"
    }, follow_redirects=True)
    
    assert resposta.status_code == 200
    assert b"Agenda" in resposta.data or b"Sair" in resposta.data

def test_login_invalido(client):
    """Testa o comportamento de login com senha incorreta."""
    resposta = client.post("/login", data={
        "email": "teste@email.com",
        "senha": "senha_errada"
    }, follow_redirects=True)
    

    assert resposta.status_code == 200
    assert b"E-mail ou senha invalidos" in resposta.data or b"Login" in resposta.data