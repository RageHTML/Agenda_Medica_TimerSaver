import pytest
from app import app, db, User, Medico, Paciente, Consulta
from werkzeug.security import generate_password_hash
from datetime import datetime, date

@pytest.fixture
def client():
    print("\n🔧 [SETUP] Configurando o ambiente de testes (Banco em memória)...")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            print("👤 [SETUP] Inserindo massa de dados de teste (Seeding)...")
            usuario_teste = User(
                email="teste@email.com",
                senha=generate_password_hash("123456")
            )
            db.session.add(usuario_teste)
            db.session.flush()

            medico = Medico(nome="Dr. Roberto Silva", crm="12345/PB", especialidade="Cardiologia")
            db.session.add(medico)
            db.session.flush()

            paciente = Paciente(
                user_id=usuario_teste.id,
                nome="Carlos Eduardo Oliveira",
                cpf="12345678901",
                idade=38,
                data_nascimento=date(1988, 3, 14),
                convenio="Unimed"
            )
            db.session.add(paciente)
            db.session.flush()

            consulta = Consulta(
                paciente_id=paciente.id,
                medico_id=medico.id,
                status="Confirmada",
                data_hora=datetime(2026, 8, 10, 8, 30)
            )
            db.session.add(consulta)
            db.session.commit()
            print("🌱 [SETUP] Seeding concluído com sucesso no banco de testes!")

        yield client

        print("🧹 [TEARDOWN] Limpando o banco de dados e encerrando o teste...")
        with app.app_context():
            db.drop_all()

def test_login_valido(client):
    print("\n▶️ [TESTE] Iniciando: test_login_valido")
    
    resposta = client.post("/login", data={
        "email": "teste@email.com",
        "senha": "123456"
    }, follow_redirects=True)
    
    print(f"📊 [LOG] Status Code HTTP recebido: {resposta.status_code}")
    assert resposta.status_code == 200
    print("✅ [SUCESSO] Login válido efetuado e verificado com sucesso!")

def test_login_invalido(client):
    print("\n▶️ [TESTE] Iniciando: test_login_invalido")
    
    resposta = client.post("/login", data={
        "email": "teste@email.com",
        "senha": "senha_errada"
    }, follow_redirects=True)
    
    print(f"📊 [LOG] Status Code HTTP recebido: {resposta.status_code}")
    assert resposta.status_code == 200
    assert b"E-mail ou senha invalidos" in resposta.data or b"Login" in resposta.data
    print("✅ [SUCESSO] Tentativa de login inválido interceptada e validada!")

def test_api_agendamentos_com_dados(client):
    print("\n▶️ [TESTE] Iniciando: test_api_agendamentos_com_dados")
    
    resposta = client.get("/api/agendamentos")
    
    print(f"📊 [LOG] Status Code da API: {resposta.status_code}")
    assert resposta.status_code == 200
    
    dados = resposta.get_json()
    print(f"📦 [LOG] Dados retornados pela API após o seeding: {dados}")
    
    assert isinstance(dados, list)
    assert len(dados) > 0, "A lista de agendamentos não deveria estar vazia após o seeding!"
    
    primeiro_agendamento = dados[0]
    print(f"🔍 [LOG] Detalhes do primeiro agendamento recuperado: {primeiro_agendamento}")
    
    assert primeiro_agendamento["status"] == "Confirmada"
    assert "Carlos Eduardo" in primeiro_agendamento["paciente"]
    assert "Roberto Silva" in primeiro_agendamento["medico"]
    
    print("✅ [SUCESSO] API testada com seeding e dados validados com sucesso!")