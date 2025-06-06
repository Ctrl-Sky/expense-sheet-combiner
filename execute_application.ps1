# Ensure repo is up-to-date
git pull

# Setup Virtual Environment
python3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Run validation
Write-Host "Validating..."
python ./verify_sheets.py
Write-Host "Completed"

# Run python script
python ./src/main.py true
Write-Host "Application successfully executed"

# Exit venv
deactivate