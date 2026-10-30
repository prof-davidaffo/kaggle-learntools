#!/usr/bin/env bash
# Prepara l'ambiente, genera e verifica il sito AI Lab.
set -euo pipefail

if [[ $# -gt 0 ]]; then
    if [[ $# -eq 1 && ( "$1" == --help || "$1" == -h ) ]]; then
        echo 'Uso: ./build.sh'
        echo "Per scegliere l'interprete: PYTHON=python3.12 ./build.sh"
        exit 0
    fi
    echo 'Uso: ./build.sh' >&2
    exit 1
fi

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd -- "$project_dir"
venv_python="$project_dir/ai_lab/.venv/bin/python"

if [[ ! -x "$venv_python" ]]; then
    python_command="${PYTHON:-python3}"
    if ! command -v "$python_command" >/dev/null 2>&1; then
        echo "Interprete non trovato: $python_command. Installa Python 3 e riprova." >&2
        exit 1
    fi
    echo 'Creazione ambiente virtuale…'
    "$python_command" -m venv "$project_dir/ai_lab/.venv"
fi

echo 'Preparazione dipendenze…'
"$venv_python" -m pip install -r ai_lab/requirements/site.txt
echo 'Generazione notebook…'
"$venv_python" ai_lab/tools/school_notebooks.py
echo 'Build del sito…'
"$venv_python" ai_lab/tools/build.py
echo 'Verifica del sito…'
"$venv_python" ai_lab/tools/check.py

echo 'Build completata: ai_lab/build/'
