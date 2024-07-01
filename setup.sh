# setup.sh

#!/bin/bash

PYTHON_VERSION="3.10.12"

get_python_version() {
    $1 --version 2>&1 | awk '{print $2}'
}

CURRENT_PYTHON_VERSION=$(get_python_version python)

if [ "$CURRENT_PYTHON_VERSION" != "$PYTHON_VERSION" ]; then
    echo "Versão do Python atual ($CURRENT_PYTHON_VERSION) é diferente da versão desejada ($PYTHON_VERSION)."
    echo "Por favor, instale a versão correta do Python ($PYTHON_VERSION) e tente novamente."
    exit 1
else
    echo "Versão do Python atual é $CURRENT_PYTHON_VERSION, que é a versão desejada."
fi

python -m venv venv

activate_virtualenv() {
    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        .\venv\Scripts\activate
    else
        echo "Sistema operacional não suportado para ativação automática do ambiente virtual"
        exit 1
    fi
}

activate_virtualenv

pip install --upgrade pip
pip install -r requirements.txt

echo "Configuração concluída. O ambiente virtual está ativo."
