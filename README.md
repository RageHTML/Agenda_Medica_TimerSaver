# 🩺 Agenda Médica Web

Uma aplicação web moderna para gestão e visualização de agendamentos médicos, desenvolvida em Python (Flask) e PostgreSQL, totalmente conteinerizada com Docker.

---

## 🚀 1. Funcionalidades Principais

* **Autenticação Segura:** Login e registro de usuários com hash de senha via Werkzeug e proteção contra vulnerabilidades CSRF.
* **Painel Dinâmico:** Visualização interativa dos agendamentos através de tabelas reativas com filtragem instantânea sem reload.
* **Integração via API RESTful:** Endpoints expostos para busca e integração com sistemas externos.
* **Povoamento Automático (*Seeding*):** Inicialização do banco de dados com massa de testes pronta para validação imediata.

---

## 🎬 2. Demonstração da Aplicação

Confira abaixo o funcionamento da interface, navegação e busca reativa da aplicação 

![Demonstração da Agenda Médica](./static/demo.gif)

---

## 🛠️ 3. Tecnologias Utilizadas

| Camada | Tecnologias / Bibliotecas |
| --- | --- |
| **Backend** | Python 3.11, Flask, Flask-SQLAlchemy (ORM), Flask-WTF / WTForms, Werkzeug |
| **Banco de Dados** | PostgreSQL 15, Driver `psycopg2-binary` |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla ES6+), **Tabulator.js** |
| **Infraestrutura** | Docker, Docker Compose |

---

## ⚙️ 4. Pré-requisitos e Configuração do Ambiente (.env)

Antes de executar a aplicação, é necessário configurar as variáveis de ambiente renomeando o arquivo de exemplo.

1. Localize o arquivo `env-example` na raiz do projeto.
2. Renomeie-o para `.env`:
* **Linux / macOS:**
```bash
mv env-example .env

```


* **Windows (PowerShell):**
```powershell
Rename-Item env-example .env

```





### 🔑 Como Gerar uma `SECRET_KEY` Segura

Para gerar uma chave criptográfica forte para a variável `SECRET_KEY` no arquivo `.env`, utilize os comandos abaixo com um ambiente virtual temporário:

* **Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -c "import secrets; print(secrets.token_hex(32))"
deactivate

```


* **Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import secrets; print(secrets.token_hex(32))"
deactivate

```


*(Nota para PowerShell: Caso ocorra erro de execução de scripts, execute antes: `Set-ExecutionPolicy Unrestricted -Scope Process`)*

---

## 🐳 5. Como Executar via Docker

Para rodar a aplicação completa conteinerizada utilizando o Docker e o Docker Compose, siga os passos abaixo:

1. **Pré-requisitos:** Certifique-se de ter o [Docker Engine](https://docs.docker.com/get-docker/) e o [Docker Compose](https://docs.docker.com/compose/install/) instalados.
2. **Suba os containers da aplicação e do banco de dados:**
```bash
docker compose up --build

```


*(Este comando criará e iniciará os serviços do PostgreSQL e da aplicação Flask, aplicando as migrações e o seeding de forma automática).*
3. **Comandos Úteis do Docker:**
* **Modo em segundo plano (detached):** `docker compose up -d --build`
* **Visualizar logs:** `docker compose logs -f`
* **Parar containers:** `docker compose down`



---

## 🌐 6. Rotas e Acesso à Aplicação

Assim que a aplicação estiver rodando, você poderá acessar as principais rotas e endpoints através da tabela abaixo:

| Rota / Endpoint | Método HTTP | Descrição / O que é exibido |
| --- | --- | --- |
| **`/`** ou **`/agenda`** | `GET` | Painel principal contendo a tabela dinâmica de agendamentos médicos. |
| **`/login`** | `GET` / `POST` | Tela de autenticação de usuários e processamento do login. |
| **`/register`** | `GET` / `POST` | Página de cadastro de novos usuários no sistema. |
| **`/api/agendamentos`** | `GET` | Endpoint RESTful que retorna a lista completa de agendamentos em formato JSON. |
| **`/api/agendamentos?q=`** | `GET` | Endpoint RESTful com suporte a filtro/busca de agendamentos por termo. |

---

## 🌱 7. Como Popular o Banco de Dados (Flask Seed)

O sistema conta com um comando dedicado para popular o banco de dados com massa de testes.

Para executá-lo manualmente, certifique-se de estar com o ambiente virtual ativado e utilize o comando:

```bash
flask seed

```

---

## 🧪 8. Como Executar os Testes Automatizados (Pytest)

O projeto possui uma suíte de testes automatizados utilizando **Pytest** e o cliente de testes integrado do Flask (`app.test_client()`), operando sobre um banco de dados em memória (`SQLite`).

### Como Executar:

1. Ative o ambiente virtual do projeto no seu terminal.
2. Execute o comando do pytest com a flag `-s` para visualizar os logs detalhados:

```bash
pytest -s

```

### O que cada teste valida:

| Nome do Teste | Comportamento Validado |
| --- | --- |
| **`test_login_valido`** | Simula uma requisição POST na rota de login utilizando credenciais corretas e valida o código de sucesso HTTP `200`. |
| **`test_login_invalido`** | Simula uma tentativa de autenticação com senha incorreta, validando que o sistema bloqueia o acesso indevido. |
| **`test_api_agendamentos_com_dados`** | Popula o banco em memória com dados de teste e consome o endpoint RESTful (`GET /api/agendamentos`), conferindo a integridade e o mapeamento do JSON retornado. |

---

## 📌 9. Considerações Finais / Autor

Projeto desenvolvido com foco em boas práticas de desenvolvimento web backend em Python, testes automatizados e arquitetura conteinerizada.


[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deyvid-martins/)

* Desenvolvido por **Rage** / Repositório Oficial do Projeto.