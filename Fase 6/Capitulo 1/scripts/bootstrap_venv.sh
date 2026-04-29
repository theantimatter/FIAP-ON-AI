#!/usr/bin/env bash
# Ambiente padrão para Jupyter local (Fase 6 / Capítulo 1).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Erro: python3 não encontrado no PATH." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
. .venv/bin/activate

python -m pip install -U pip
python -m pip install -r requirements.txt

KERNEL_NAME="farmtech-fase6-venv"
DISPLAY_NAME="Python (FarmTech Fase6 .venv)"
python -m ipykernel install --user --name="${KERNEL_NAME}" --display-name="${DISPLAY_NAME}"

echo ""
echo "Pronto. No Jupyter/VS Code, selecione o kernel: ${DISPLAY_NAME}"
echo "Interpretador: ${ROOT}/.venv/bin/python"
