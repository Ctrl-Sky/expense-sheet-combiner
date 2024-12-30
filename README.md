# expense-sheet-combiner

Instructions to run this:
Ensure there is a
    - sheets/Summary.xls (AMEX xlx file)
    - sheets/accountactivity1.csv (TD credit csv file)
    - sheets/accountactivity.csv (TD debit csv file)
Create a virtual env 
    - python -m venv .venv
    - . .venv/bin/activate
Install dependencies
    - pip install -r requirements.txt
From python script
    - python ./src/main.py

Use this to get the sum of purchases, excluding large purchases greater or less than 300
=SUMIFS(INDIRECT("F2:F" & ROW()-1), INDIRECT("F2:F" & ROW()-1), "<=300", INDIRECT("F2:F" & ROW()-1), ">=-300")