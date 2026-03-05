@echo off
TITLE Sistema Controle de Clientes

:: 1. Navega para a pasta do projeto
cd /d "D:\Clone-planos-de-saude\controle-planos"

:: 2. Cria o ambiente virtual (.venv) se não existir
 if not exist ./venv\Scripts\activate (
    echo Criando ambiente virtual...
    python -m venv .venv
 )

:: 3. Ativa o ambiente virtual
call ./venv\Scripts\activate

:: 4. Instala dependências se necessário
if exist requirements.txt (
    pip install -r requirements.txt
)

:: 5. Configura o Flask
set FLASK_APP=app
set FLASK_DEBUG=1

:: 6. Abre o navegador e inicia o servidor
start http://127.0.0.1:5000
flask run
pause