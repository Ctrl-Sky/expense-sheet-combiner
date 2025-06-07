#!/bin/bash

# Ensure repo is up-to-date
git pull

# Setup Virtual Environment
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# Run validation
echo "Validating..."
python verify_sheets.py
echo "Completed"

# Run python script
python src/main.py true
echo "Application successfully executed"

# Exit venv
deactivate
git add .
git commit -m "(Automated Commit) Expense sheet updated"
git push