@echo off
TITLE Sistema Controle de Clientes - RVC Assessoria

:: 1. Navega para a pasta do projeto (descomente se necessário)
cd /d "%~dp0"
:: cd /d "E:\Clone-planos-de-saude\controle-planos"

echo.
echo ===================================================
echo  Iniciando Sistema Controle de Clientes
echo ===================================================
echo.

:: 2. Cria o ambiente virtual (.venv) se não existir
if not exist .venv\Scripts\activate (
    echo [SETUP] Criando ambiente virtual '.venv'...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual.
        echo Certifique-se de que Python está instalado.
        pause
        exit /b 1
    )
    echo [SETUP] Ambiente virtual criado com sucesso.
) else (
    echo [SETUP] Ambiente virtual já existe.
)

:: 3. Ativa o ambiente virtual
echo [SETUP] Ativando ambiente virtual...
call .\.venv\Scripts\activate
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)

:: 4. Atualiza pip e instala dependências
if exist requirements.txt (
    echo [DEPENDENCIAS] Atualizando pip...
    pip install --upgrade pip
    echo [DEPENDENCIAS] Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependências.
        pause
        exit /b 1
    )
) else (
    echo [AVISO] requirements.txt não encontrado.
    echo [DEPENDENCIAS] Instalando dependências essenciais...
    pip install --upgrade MarkupSafe
    pip install --force-reinstall Flask-WTF
)

:: 5. Configura o Flask
echo [FLASK] Configurando variáveis de ambiente...
set FLASK_APP=run.py
set FLASK_DEBUG=1

:: 6. Abre o navegador e inicia o servidor
echo [FLASK] Iniciando servidor...
echo [FLASK] Abrindo navegador em http://127.0.0.1:5000/login
start http://127.0.0.1:5000/login

echo [FLASK] Servidor Flask iniciando... (Pressione Ctrl+C para parar)
python run.py

echo.
echo [FIM] Servidor encerrado.
pause