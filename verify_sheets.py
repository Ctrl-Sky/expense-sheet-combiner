import os
import pandas as pd

SHEET_PATH = "sheets"
AMEX_PATH = f"{SHEET_PATH}/Summary.xls"
DEBIT_PATH = f"{SHEET_PATH}/accountactivity.csv"
CREDIT_PATH = f"{SHEET_PATH}/accountactivity1.csv"

def does_it_exist(path):
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")
    
def does_debit_match_path(path):
    df = pd.read_csv(path)
    description_list = df.iloc[:, 1].tolist()

    # Validate paht is debit and not credit by checking if common debit descriptions are in the csv
    if not "INTEREST CREDIT" in description_list or not "WS Investments   INV" in description_list:
        raise Exception(f"{path} does not match with debit file")

if __name__ == "__main__":
    # Validation before running expense-sheet-combiner
    # Checks that correct sheets exist
    # Checks that the debit file matches the correct name

    does_it_exist(AMEX_PATH)
    does_it_exist(DEBIT_PATH)
    does_it_exist(CREDIT_PATH)
    does_debit_match_path(DEBIT_PATH)

