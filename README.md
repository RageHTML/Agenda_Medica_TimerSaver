# 🩺 Agenda Médica Web

Uma aplicação web para gestão e visualização de agendamentos médicos, desenvolvida com Python (Flask) e banco de dados relacional PostgreSQL, totalmente conteinerizada com Docker.

---

## 📝 Descrição Breve

A **Agenda Médica** é um sistema projetado para facilitar o controle de consultas e o cadastro de pacientes e médicos. A plataforma conta com:
- Autenticação de usuários (Login e Registro com senhas criptografadas e proteção CSRF).
- Painel de visualização de agenda dinâmica com busca instantânea sem recarregar a página.
- API RESTful integrada para consulta e filtragem de agendamentos.
- Povoamento automático do banco de dados (*Seeding*) ao iniciar a aplicação.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.11, Flask, Flask-SQLAlchemy (ORM), Flask-WTF / WTForms, Werkzeug (Security).
* **Banco de Dados:** PostgreSQL 15, SQLAlchemy, Driver `psycopg2`.
* **Frontend:** HTML5, CSS3, JavaScript (ES6+ Vanilla), Biblioteca **Tabulator.js**.
* **Infraestrutura:** Docker, Docker Compose.

---

## 🔐 Configuração das Variáveis de Ambiente (.env)

Antes de executar o projeto, você deve renomear o arquivo de exemplo para o nome correto que a aplicação utiliza:

1. Localize o arquivo `env-example` (ou `.env.example`) na raiz do projeto ou na pasta `AgendaMedica/`.
2. Renomeie o arquivo para `.env`:
   - **Linux / macOS:**
     ```bash
     mv AgendaMedica/env-example AgendaMedica/.env
     ```
   - **Windows (PowerShell):**
     ```powershell
     Rename-Item AgendaMedica/env-example AgendaMedica/.env
     ```

---

## 🔑 Como Gerar uma SECRET_KEY Segura (Ambiente Virtual)

Caso queira alterar a `SECRET_KEY` no seu arquivo `.env` por uma chave aleatória e segura, siga o passo a passo abaixo para criar/ativar um ambiente virtual (`venv`) e gerar a chave via Python:

### 🐧 No Linux / macOS:

1. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Gere a chave secreta no terminal:**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Copie a chave gerada e cole no seu arquivo `.env`:**
   ```env
   SECRET_KEY=sua_chave_gerada_aqui
   ```

4. **Desative o ambiente virtual:**
   ```bash
   deactivate
   ```

### 🪟 No Windows (PowerShell / Prompt de Comando):

1. **Crie e ative o ambiente virtual:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   *(Nota: Se houver erro de permissão no PowerShell, execute primeiro: `Set-ExecutionPolicy Unrestricted -Scope Process`)*

2. **Gere a chave secreta no terminal:**
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Copie a chave gerada e cole no seu arquivo `.env`:**
   ```env
   SECRET_KEY=sua_chave_gerada_aqui
   ```

4. **Desative o ambiente virtual:**
   ```powershell
   deactivate
   ```

---

## 🐳 Instruções para Executar o Projeto com Docker

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados no seu sistema.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd AgendaMedica
   ```

2. **Configure o arquivo de ambiente (`.env`):**
   Certifique-se de ter renomeado o arquivo `env-example` para `.env` conforme instruído acima.

3. **Suba os containers com Docker Compose:**
   ```bash
   docker compose up --build
   ```
   *(O Docker baixará a imagem do Postgres, construirá a aplicação Flask e executará o script de `seed` automaticamente)*.

4. **Acesse no navegador:**
   - **URL Principal:** `http://localhost:5000/agenda`
   - **Tela de Login:** `http://localhost:5000/login`

5. **Para encerrar a execução:**
   ```bash
   docker compose down
   ```

---

## 🔑 Credenciais do Usuário de Teste

O banco de dados é populado automaticamente (*seeding*) na inicialização da aplicação. Você pode utilizar qualquer uma das credenciais abaixo para testar o login:

| Perfil | E-mail | Senha |
| :--- | :--- | :--- |
| **Paciente 1** | `carlos.eduardo@gmail.com` | `123456` |
| **Paciente 2** | `mariana.santos@hotmail.com` | `123456` |
| **Paciente 3** | `lucas.mendes@yahoo.com.br` | `123456` |

---

## 💡 Exemplos de Uso da Aplicação

1. **Autenticação (`/login` e `/register`):**
   - Formulários com validação de entradas e proteção contra ataques **CSRF**.
   - Senhas armazenadas de forma segura com *hash* Werkzeug.

2. **Tabela de Agendamentos (`/agenda`):**
   - Exibe a lista completa de consultas através da biblioteca **Tabulator.js**.
   - Exibição de badges visuais para diferentes estados (*Agendada*, *Confirmada*, *Realizada*, *Cancelada*).

3. **Busca Reativa e Debounce:**
   - Permite filtrar consultas em tempo real por **Nome do Paciente**, **CPF**, **Médico** ou **Especialidade**.
   - O campo de busca utiliza **Debounce (300ms)** em JavaScript para otimizar as requisições ao backend.

4. **API de Consulta (`GET /api/agendamentos`):**
   - Retorno JSON com todos os agendamentos: `http://localhost:5000/api/agendamentos`
   - Consulta filtrada via parâmetro query: `http://localhost:5000/api/agendamentos?q=Cardiologia`

---

## 📐 Decisões Técnicas e Limitações Conhecidas

### Decisões Técnicas
- **Isolamento de Porta PostgreSQL:** O container do banco foi mapeado externamente para a porta `5433:5432` no `docker-compose.yml`, prevenindo conflitos com serviços locais do Postgres na máquina host (porta `5432`).
- **Comunicação por Nome de Serviço:** A aplicação Flask acessa o banco via hostname da rede interna do Docker (`@db:5432`), eliminando a necessidade de mapear IPs dinâmicos.
- **Cache-Busting para Arquivos Estáticos:** Implementação da função utilitária `static_url` no Flask, injetando uma query string de versão (`?v=TIMESTAMP`) baseada na última modificação do arquivo para evitar que o navegador sirva CSS/JS desatualizado.

### Limitações Conhecidas
- **Gerenciamento de Sessão:** A sessão do usuário é gerenciada via *session cookies* nativos do Flask. Para escalar horizontalmente com múltiplas instâncias em produção, recomenda-se adotar um armazenamento compartilhado como o *Redis*.
- **Comando de Seed na Subida:** O comando `seed` é executado diretamente na inicialização do container web (`command: sh -c ...`). Em ambientes de produção de larga escala, o ideal é rodar o script em um job isolado no pipeline de deploy para evitar *race conditions*.