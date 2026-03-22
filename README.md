<div align="center">

<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge" />
<img src="https://img.shields.io/badge/Versão-1.0.0-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Licença-MIT-purple?style=for-the-badge" />
<img src="https://img.shields.io/badge/Python-3.11+-yellow?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Flask-3.1.2-black?style=for-the-badge&logo=flask&logoColor=white" />
<img src="https://img.shields.io/badge/PostgreSQL-14+-316192?style=for-the-badge&logo=postgresql&logoColor=white" />

# 🏥 Controle de Planos

### Sistema de Controle de Vendas e Finanças de Planos de Saúde

*Para vendedores e corretoras que precisam de controle real sobre suas operações.*

---

</div>

## 📋 Sobre o Projeto

O **Controle de Planos** é uma aplicação web desenvolvida em **Python com Flask** para centralizar e simplificar a gestão de vendas e finanças de planos de saúde. Voltado para **vendedores autônomos e corretoras**, o sistema oferece módulos completos de cadastro, controle comercial, análise financeira e relatórios — tudo em um único lugar.

> *De corretores independentes a pequenas corretoras: tenha o controle que você merece.*

---

## 🧩 Módulos do Sistema

| Módulo | Status | Descrição |
|--------|--------|-----------|
| 🏠 **Início** | ✅ Disponível | Dashboard com gráficos demonstrativos de vendas |
| 👤 **Clientes** | ✅ Disponível | Cadastro e gestão de beneficiários |
| 💰 **Vendas** | ✅ Disponível | Registro e acompanhamento de vendas |
| 📋 **Planos** | ✅ Disponível | Cadastro de planos disponíveis |
| 🏢 **Administradoras** | ✅ Disponível | Gestão de administradoras |
| 🏥 **Operadoras** | ✅ Disponível | Cadastro de operadoras de saúde |
| 💲 **Preços** | ✅ Disponível | Tabela de preços por plano |
| 📊 **Relatórios** | ✅ Disponível | Relatórios financeiros e de vendas |
| 📝 **Cotações** | 🚧 Em construção | Módulo de geração de cotações |
| 🔐 **Login** | 🚧 Em construção | Tela de autenticação de usuários |

---

## 🛠️ Tecnologias Utilizadas

<div align="center">

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Linguagem** | Python | 3.11+ |
| **Framework Web** | Flask | 3.1.2 |
| **ORM** | Flask-SQLAlchemy | 3.1.1 |
| **Banco de Dados** | PostgreSQL | 14+ |
| **Migrações** | Flask-Migrate + Alembic | 4.1.0 / 1.17.2 |
| **Formulários** | Flask-WTF + WTForms | 1.2.2 / 3.2.1 |
| **Templates** | Jinja2 | 3.1.6 |
| **Gráficos** | Plotly | 5.17.0 |
| **Análise de Dados** | Pandas + NumPy | 2.2.3 / 2.1.3 |
| **Variáveis de Ambiente** | python-dotenv | 1.2.1 |
| **Servidor (Linux)** | Gunicorn | 21.2.0 |
| **Servidor (Windows)** | Waitress | 2.1.2 |
| **Empacotamento** | PyInstaller | 6.11.0 |

</div>

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- [Python](https://www.python.org/) `>= 3.11`
- [PostgreSQL](https://www.postgresql.org/) `>= 14`
- [Git](https://git-scm.com/)

---

### 1. Clonar o Repositório

```bash
git clone https://github.com/rogeriovctecnico-commits/controle-planos.git
cd controle-planos
```

---

### 2. Criar e Ativar o Ambiente Virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar as Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui

# PostgreSQL
DATABASE_URL=postgresql://usuario:senha@localhost:5432/controle_planos
```

---

### 5. Criar o Banco de Dados e Aplicar as Migrações

```bash
# Criar o banco no PostgreSQL
createdb controle_planos

# Aplicar as migrações
flask db upgrade
```

---

### 6. Iniciar o Sistema

```bash
flask run
```

Acesse em: **http://localhost:5000**

---

> ⚡ **Da segunda vez em diante**, basta ativar o ambiente virtual e rodar `flask run`:
> ```powershell
> .\.venv\Scripts\Activate.ps1
> flask run
> ```

---

## 📁 Estrutura do Projeto

```
controle-planos/
├── 📂 app/
│   ├── 📂 models/           # Modelos SQLAlchemy (ORM)
│   ├── 📂 routes/           # Blueprints e rotas Flask
│   ├── 📂 templates/        # Templates Jinja2 (HTML)
│   ├── 📂 static/           # CSS, JS e imagens
│   └── 📂 forms/            # Formulários WTForms
│
├── 📂 migrations/           # Migrações Alembic
├── app.py                   # Entrypoint da aplicação
├── iniciar_sistema.sh       # Script de inicialização (Linux)
├── requirements.txt         # Dependências do projeto
├── .env.example             # Exemplo de variáveis de ambiente
└── README.md
```

---

## 🌐 Deploy em Produção

**Linux (com Gunicorn):**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**Windows (com Waitress):**
```bash
waitress-serve --port=8000 app:app
```

**Gerar executável standalone (PyInstaller):**
```bash
pyinstaller --onefile app.py
```

---

## 🧭 Roadmap

- [x] Estrutura inicial do projeto com Flask
- [x] Configuração do ORM com SQLAlchemy + PostgreSQL
- [x] Sistema de migrações com Alembic
- [x] Dashboard com gráficos (Plotly)
- [x] Módulo de Clientes
- [x] Módulo de Vendas
- [x] Módulo de Planos
- [x] Módulo de Administradoras
- [x] Módulo de Operadoras
- [x] Módulo de Preços
- [x] Módulo de Relatórios
- [ ] Módulo de Cotações
- [ ] Tela de Login e autenticação
- [ ] Deploy em produção

---

## 🤝 Contribuindo

1. Faça um **fork** do projeto
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m 'feat: minha nova feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um **Pull Request**

---

## 👨‍💻 Autor

<div align="center">

**Rogério VC Técnico**

[![GitHub](https://img.shields.io/badge/GitHub-rogeriovctecnico--commits-181717?style=for-the-badge&logo=github)](https://github.com/rogeriovctecnico-commits)

</div>

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

Feito com ❤️ e muito ☕ por **Rogério VC Técnico**

*"Saúde é o maior patrimônio. Gerencie com excelência."*

</div>
