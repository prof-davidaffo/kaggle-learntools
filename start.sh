#!/usr/bin/env bash
# Avvia soltanto il server locale per il sito già generato.
set -euo pipefail

usage() {
    echo 'Uso: ./start.sh [--port PORTA]'
    echo 'Porta predefinita: 8000. Ferma il server con Ctrl+C.'
}

port=8000
while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)
            if [[ $# -lt 2 || ! "$2" =~ ^[0-9]{1,5}$ ]]; then
                echo 'Errore: --port richiede un numero tra 1 e 65535.' >&2
                exit 1
            fi
            port=$((10#$2))
            if ((port < 1 || port > 65535)); then
                echo 'Errore: la porta deve essere tra 1 e 65535.' >&2
                exit 1
            fi
            shift 2 ;;
        --help|-h) usage; exit 0 ;;
        *) echo "Opzione sconosciuta: $1" >&2; usage >&2; exit 1 ;;
    esac
done


project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "$project_dir/ai_lab/build/index.html" ]]; then
    echo 'Sito non presente. Esegui prima ./build.sh.' >&2
    exit 1
fi

python_command="${PYTHON:-$project_dir/ai_lab/.venv/bin/python}"
if [[ -z "${PYTHON:-}" && ! -x "$python_command" ]]; then
    python_command=python3
fi
if ! command -v "$python_command" >/dev/null 2>&1; then
    echo "Interprete non trovato: $python_command. Installa Python 3 e riprova." >&2
    exit 1
fi

echo "Avvio server su http://localhost:$port — premi Ctrl+C per fermarlo."
exec "$python_command" -m http.server "$port" --bind 127.0.0.1 --directory "$project_dir/ai_lab/build"
