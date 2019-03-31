#!/usr/bin/env bash

project_path=$(dirname $0)/..

cd ${project_path}
export PYTHONPATH=${project_path}

echo "$header: Creating virtual environment."
python3 -m venv ${project_path}/.venv
source ${project_path}/.venv/bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python
pip install -r requirements-dev.txt