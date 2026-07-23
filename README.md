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

## 🐳 3. Como Executar via Docker

Para rodar a aplicação completa conteinerizada utilizando o Docker e o Docker Compose, siga os passos abaixo:

1. **Certifique-se de ter os pré-requisitos instalados:**
* [Docker Engine](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)


2. **Configure o arquivo de ambiente:**
Certifique-se de que o arquivo `.env` está devidamente configurado na raiz do projeto a partir do modelo `env-example`.
3. **Suba os containers da aplicação e do banco de dados:**
```bash
docker compose up --build

```


*(Este comando criará e iniciará os serviços do PostgreSQL e da aplicação Flask, aplicando as migrações e o seeding de forma automática).*
4. **Comandos Úteis do Docker:**
* **Para rodar em segundo plano (modo detached):**
```bash
docker compose up -d --build

```


* **Para visualizar os logs em tempo real:**
```bash
docker compose logs -f

```


* **Para parar e remover os containers:**
```bash
docker compose down

```





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