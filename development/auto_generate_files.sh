#!/bin/sh

set -e # exit script if there is an error.

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/dev_virtual_environment"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment is not set up. Please run 'sh development/create_python_virtual_environment.sh'"
    exit 1
fi


if [ -f "$VENV_DIR/Scripts/activate" ]; then
    "$VENV_DIR/Scripts/activate"
else
    . "$VENV_DIR/bin/activate"
fi

cd "$SCRIPT_DIR/.."

python -m development.capabilities_json_to_python.capabilities_to_py
python -m development.capabilities_json_to_python.capabilities_to_html_docs
python -m development.examples_json_to_html.examples_to_html