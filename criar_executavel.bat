@echo off
TITLE Criando Executavel do Sistema

:: 1. Ativa o ambiente virtual
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)

echo Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
)

echo Fechando processos travados...
taskkill /F /IM app.exe >nul 2>&1
:: Pausa para liberar o arquivo
timeout /t 2 /nobreak >nul

echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist app.spec del app.spec

echo Criando o pacote...
:: --onefile: cria um unico arquivo .exe | --add-data: inclui pastas do Flask
:: Ajuste: Aponta para app\templates e app\static pois estao dentro do pacote 'app'
:: Adicionando hidden-imports para forcar a inclusao dos blueprints que sao importados dentro de funcoes
pyinstaller --noconfirm --clean --name app --noconsole --onefile --paths . ^
 --hidden-import=app ^
 --hidden-import=app.blueprints.administradoras ^
 --hidden-import=app.blueprints.auth ^
 --hidden-import=app.blueprints.clientes ^
 --hidden-import=app.blueprints.operadoras ^
 --hidden-import=app.blueprints.planos ^
 --hidden-import=app.blueprints.precos_faixa_etaria ^
 --hidden-import=app.blueprints.vendas ^
 --hidden-import=app.blueprints.confiauto ^
 --hidden-import=app.blueprints.clientes_confiauto ^
 --add-data "app\templates;app\templates" --add-data "app\static;app\static" --add-data "app\blueprints;app\blueprints" run.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Ocorreu um erro ao criar o executavel. Verifique as mensagens acima.
    pause
    exit /b
)

echo Copiando banco de dados...
:: Cria a pasta instance no destino
if not exist dist\instance mkdir dist\instance

:: 1. Tenta copiar da pasta instance original
if exist instance\*.db copy instance\*.db dist\instance >nul
if exist instance\*.sqlite copy instance\*.sqlite dist\instance >nul

:: 2. Tenta copiar da raiz do projeto (caso o banco esteja solto na raiz)
if exist *.db copy *.db dist\instance >nul
if exist *.sqlite copy *.sqlite dist\instance >nul

echo Verificando se o banco foi copiado...
dir dist\instance

echo.
echo Processo concluido! O executavel foi criado na pasta 'dist'.
pause
