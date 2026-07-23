# 🩺 Agenda Médica Web

Uma aplicação web moderna para gestão e visualização de agendamentos médicos, desenvolvida em Python (Flask) e PostgreSQL, totalmente conteinerizada com Docker.

---

## 🚀 1. Funcionalidades Principais

* **Autenticação Segura:** Login e registro de usuários com hash de senha via Werkzeug e proteção contra vulnerabilidades CSRF.
* **Painel Dinâmico:** Visualização interativa dos agendamentos através de tabelas reativas com filtragem instantânea sem reload.
* **Integração via API RESTful:** Endpoints expostos para busca e integração com sistemas externos.
* **Povoamento Automático (*Seeding*):** Inicialização do banco de dados com massa de testes pronta para validação imediata.

---

## 🛠️ 2. Tecnologias Utilizadas

| Camada | Tecnologias / Bibliotecas |
| --- | --- |
| **Backend** | Python 3.11, Flask, Flask-SQLAlchemy (ORM), Flask-WTF / WTForms, Werkzeug |
| **Banco de Dados** | PostgreSQL 15, Driver `psycopg2-binary` |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla ES6+), **Tabulator.js** |
| **Infraestrutura** | Docker, Docker Compose |

---

## ⚙️ 3. Pré-requisitos e Instalação

### Pré-requisitos

* [Python 3.11+](https://www.python.org/) instalado localmente.
* [Docker Engine](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) (caso queira executar conteinerizado).

### Passo a Passo para Execução com Docker

1. **Clone o repositório:**
```bash
git clone https://github.com/RageHTML/Agenda_Medica_TimerSaver.git
cd Agenda_Medica_TimerSaver

```


2. **Configure o arquivo de ambiente:**
Renomeie o arquivo de exemplo `env-example` para `.env` na raiz do projeto.
3. **Suba os containers com Docker Compose:**
```bash
docker compose up --build

```


4. **Acesse no navegador:**
* **Painel Principal:** [http://localhost:5000/agenda](http://localhost:5000/agenda)
* **Tela de Login:** [http://localhost:5000/login](http://localhost:5000/login)



---

## 🌐 4. Rotas e Acesso à Aplicação

Assim que a aplicação estiver rodando, você poderá acessar as principais rotas e endpoints da API através da tabela abaixo:

| Rota / Endpoint | Método HTTP | Descrição / O que é exibido |
| --- | --- | --- |
| **`/`** ou **`/agenda`** | `GET` | Painel principal contendo a tabela dinâmica de agendamentos médicos. |
| **`/login`** | `GET` / `POST` | Tela de autenticação de usuários e processamento do login. |
| **`/register`** | `GET` / `POST` | Página de cadastro de novos usuários no sistema. |
| **`/api/agendamentos`** | `GET` | Endpoint RESTful que retorna a lista completa de agendamentos em formato JSON. |
| **`/api/agendamentos?q=`** | `GET` | Endpoint RESTful com suporte a filtro/busca de agendamentos por termo. |

---

## 🌱 5. Como Popular o Banco de Dados (Flask Seed)

O sistema conta com um comando dedicado para popular o banco de dados com massa de testes.

Para executá-lo manualmente, certifique-se de estar posicionado no **diretório da aplicação**, com o ambiente virtual ativado, e utilize o comando:

```bash
flask seed

```

Caso o banco já possua registros, o sistema validará a duplicidade e informará que o banco de dados já está populado.

---

## 🧪 6. Como Executar os Testes Automatizados (Pytest)

O projeto possui uma suíte de testes automatizados utilizando **Pytest** e o cliente de testes integrado do Flask (`app.test_client()`), operando sobre um banco de dados em memória (`SQLite`).

### Como Executar:

1. Certifique-se de que o seu ambiente virtual está ativado no terminal.
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

## 📌 7. Considerações Finais / Autor

Projeto desenvolvido com foco em boas práticas de desenvolvimento web backend em Python, testes automatizados e arquitetura conteinerizada.

* Desenvolvido por **Rage** / Repositório Oficial do Projeto.