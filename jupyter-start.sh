#!/usr/bin/env bash
# Prepara l'ambiente locale e apre i notebook generati con JupyterLab.
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
venv_dir="$project_dir/ai_lab/.venv-jupyter"
venv_python="$venv_dir/bin/python"
requirements="$project_dir/ai_lab/requirements/jupyter.txt"

if [[ ! -f "$project_dir/ai_lab/build/notebooks/00-python-essenziale.ipynb" ]]; then
    echo 'Notebook non presente. Esegui prima ./build.sh.' >&2
    exit 1
fi

if [[ ! -x "$venv_python" ]]; then
    python_command="${JUPYTER_PYTHON:-python3}"
    if ! command -v "$python_command" >/dev/null 2>&1; then
        echo "Interprete Python non trovato: $python_command." >&2
        echo 'Installa Python oppure indica il suo percorso con JUPYTER_PYTHON.' >&2
        exit 1
    fi
    echo 'Creazione ambiente Jupyter…'
    "$python_command" -m venv "$venv_dir"
fi

echo 'Preparazione dipendenze Jupyter e dei notebook…'
"$venv_python" -m pip install -r "$requirements"


if "$venv_python" -c 'import sys; sys.exit(sys.version_info >= (3, 14))'; then
    echo 'Preparazione TensorFlow per il deep learning…'
    "$venv_python" -m pip install 'tensorflow>=2.16,<2.22'
else
    echo 'TensorFlow stabile non è disponibile per questa versione di Python: i notebook di deep learning richiedono un ambiente compatibile.' >&2
fi

# Ogni avvio usa una nuova copia, così il salvataggio non modifica la build.
session_dir="$(mktemp -d "$project_dir/ai_lab/runtime/jupyter-XXXXXXXX")"
cp -R "$project_dir/ai_lab/build/notebooks/." "$session_dir/"
echo "Copie della sessione: $session_dir"
echo 'Avvio JupyterLab su http://127.0.0.1:8888.'
exec "$venv_python" -m jupyterlab --no-browser --ip=127.0.0.1 --port=8888 --ServerApp.port_retries=0 --IdentityProvider.token='' --PasswordIdentityProvider.hashed_password='' --ServerApp.root_dir="$session_dir"
