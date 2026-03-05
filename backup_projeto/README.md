Sistema de controle de vendas e finanças de planos de saúde para vendedores e corretoras.
Módulos: Inicio com graficos demonstrativos de vendas.
          Clientes, Vendas, Planos, Administradoras, Operadoras, Preços, Relatórios.
          em construão : Módulo de cotações e tela de login.

# Controle de Planos — Sistema de vendas e finanças
- d030a00 (construindo tela de login)

Sistema de controle de vendas e finanças de planos de saúde para vendedores e corretoras.

## Módulos
- Início (com gráficos demonstrativos de vendas)
- Clientes
- Vendas
- Planos
- Administradoras
- Operadoras
- Preços
- Relatórios

Em construção:
- Módulo de cotações
- Tela de login

## Tecnologias e dependências
Lista (requirements.txt):
- alembic==1.17.2
- blinker==1.9.0
- click==8.3.1
- colorama==0.4.6
- Flask==3.1.2
- Flask-Migrate==4.1.0
- Flask-SQLAlchemy==3.1.1
- Flask-WTF==1.2.2
- greenlet==3.3.0
- itsdangerous==2.2.0
- Jinja2==3.1.6
- Mako==1.3.10
- MarkupSafe==3.0.3
- python-dotenv==1.2.1
- PyInstaller==6.11.0
- plotly==5.17.0
- pandas==2.2.3
- numpy==2.1.3
- SQLAlchemy==2.0.45
- typing_extensions==4.15.0
- Werkzeug==3.1.4
- WTForms==3.2.1
- gunicorn==21.2.0
- waitress==2.1.2

---

## Como começar

### 1) Crie e ative um virtualenv
Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1