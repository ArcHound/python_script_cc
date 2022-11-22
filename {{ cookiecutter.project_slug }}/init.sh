#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
chmod +x "{{ cookiecutter.project_slug }}.py"
rm init.sh
