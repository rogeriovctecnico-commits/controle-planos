@echo off
TITLE Sistema Controle de Clientes

:: 1. Navega para a pasta do projeto
@REM cd /d "D:\Clone-planos-de-saude\controle-planos"

:: 2. Cria o ambiente virtual (.venv) se não existir
if not exist .venv\Scripts\activate.bat (
    echo Criando ambiente virtual...
    python -m venv .venv
)

:: 3. Ativa o ambiente virtual
.\.venv\Scripts\activate.bat

:: 4. Instala dependências se necessário
if exist requirements.txt (
    pip install -r requirements.txt
)

:: 5. Configura o Flask
set FLASK_APP=app
set FLASK_DEBUG=1

:: 6. Inicia o servidor Flask em segundo plano
start "" cmd /c "flask run"

:: 7. Aguarda alguns segundos para o servidor subir
timeout /t 5 >nul

:: 8. Abre o navegador
start http://127.0.0.1:5000

:: Mantém a janela aberta
pause