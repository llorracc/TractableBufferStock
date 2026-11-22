#!/bin/bash
# Reproduce the handout's computed results: run TractableBufferStock.ipynb, which solves the model, checks the
# solution (a failed check stops the run) and draws the eleven figures. The executed notebook and the figures
# (PNG) go to reproduce/output/.
#
# It runs the notebook with, in this order: a python3 that already has the notebook's packages (as in
# reproduce/Dockerfile); uv, in a Python 3.12 environment of its own; or a new virtual environment, which needs
# python3 to be 3.12 or later.
set -eu

here="$(cd "$(dirname "$0")/.." && pwd)"
out="$here/reproduce/output"
mkdir -p "$out"
find "$out" -mindepth 1 -delete  # empty it, but keep the folder, which a container may have mounted
if command -v ditto >/dev/null 2>&1; then
    ditto "$here/TractableBufferStock.ipynb" "$out/TractableBufferStock.ipynb"
else
    cp -p "$here/TractableBufferStock.ipynb" "$out/TractableBufferStock.ipynb"
fi
cd "$out"

if python3 -c 'import intertemporal_choice, nbconvert, ipykernel' 2>/dev/null; then
    python3 -m jupyter nbconvert --to notebook --execute --inplace TractableBufferStock.ipynb
elif command -v uv >/dev/null 2>&1; then
    uv run --quiet --no-project --python 3.12 --with-requirements "$here/binder/requirements.txt" \
        --with nbconvert --with ipykernel jupyter nbconvert --to notebook --execute --inplace TractableBufferStock.ipynb
else
    python3 -m venv .venv
    .venv/bin/pip install --quiet -r "$here/binder/requirements.txt" nbconvert ipykernel
    .venv/bin/jupyter nbconvert --to notebook --execute --inplace TractableBufferStock.ipynb
fi

echo "The executed notebook, and its figures in figures/, are in reproduce/output."
