# expense-sheet-combiner

Instructions to run this:\
Ensure there is a\
    - sheets/Summary.xls (AMEX xlx file)\
    - sheets/accountactivity1.csv (TD credit csv file)\
    - sheets/accountactivity.csv (TD debit csv file)\
Create a virtual env\
    - python -m venv .venv\
    - . .venv/bin/activate\
Install dependencies\
    - pip install -r requirements.txt\
Run python script\
    - python ./src/main.py true

Use this to get the sum of purchases, excluding large purchases greater than 300 or large gains less than -300\
=SUMIFS(INDIRECT("H2:H" & ROW()-1), INDIRECT("H2:H" & ROW()-1), "<=300", INDIRECT("H2:H" & ROW()-1), ">=-300")
