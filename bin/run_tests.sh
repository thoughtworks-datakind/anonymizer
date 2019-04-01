#!/usr/bin/env bash
set -e
project_path=$(dirname $0)/..

export PYTHONPATH=$project_path

coverage run --source='./src' --omit='*/tests/*' -m unittest discover .
coverage report -m