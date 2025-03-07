#!/bin/bash
set -e

test -d venv || python -m venv venv

source venv/bin/activate
pip install -r requirements.txt

python load_ai.py
python run_entity_extract.py
