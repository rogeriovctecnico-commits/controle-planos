#!/bin/bash
# iniciar_sistema.sh – Script definitivo Linux para React + Flask

# -----------------------
# 0. Diretório do projeto
# -----------------------
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Diretório do projeto: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Não foi possível acessar o diretório do projeto."; exit 1; }

# -----------------------
# 1. Verifica Python3 e venv
# -----------------------
PYTHON_CMD=$(which python3)
if [[ -z "$PYTHON_CMD" ]]; then
    echo "Python3 não encontrado. Instale o Python3 primeiro."
    exit 1
fi

VENV_DIR="$HOME/.controle-planos-venv"
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Criando ambiente virtual Python..."
    sudo apt update
    sudo apt install -y python3-venv python3-pip
    "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

# Ativa venv
source "$VENV_DIR/bin/activate"

# -----------------------
# 2. Instala dependências Python (Flask)
# -----------------------
if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then
    echo "Instalando dependências Python..."
    python -m pip install --upgrade pip
    python -m pip install -r "$PROJECT_DIR/requirements.txt"
else
    echo "Nenhum requirements.txt encontrado."
fi

# -----------------------
# 3. Verifica Node.js e npm
# -----------------------
if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
    echo "Node.js/NPM não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y curl
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
fi

echo "Node.js versão: $(node -v)"
echo "npm versão: $(npm -v)"

# -----------------------
# 4. Instala dependências Node/React
# -----------------------
if [[ -f "$PROJECT_DIR/package.json" ]]; then
    echo "Instalando dependências Node/React..."
    npm install
else
    echo "Nenhum package.json encontrado."
fi

# -----------------------
# 5. Inicia React Dev Server
# -----------------------
echo "Iniciando sistema (npm start)..."
npm start &

# -----------------------
# 6. Abre navegador
# -----------------------
sleep 5
xdg-open "http://localhost:3000"

echo "Sistema iniciado. Pressione Ctrl+C para encerrar."
$SHELL
