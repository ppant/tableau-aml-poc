#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  source "$REPO_ROOT/.env"
  set +a
fi

if ! python -c "import flask, streamlit" >/dev/null 2>&1; then
  echo "Missing dependencies in current environment."
  echo "Run: pip install -r $REPO_ROOT/requirements.txt"
  exit 1
fi

cd "$REPO_ROOT/backend"
python api.py &
BACKEND_PID=$!

cleanup() {
  kill "$BACKEND_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

cd "$REPO_ROOT"
python -m streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
